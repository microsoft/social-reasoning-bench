"""Batch form-filling data generation from common_forms.jsonl.

Reads a JSONL file of filtered forms, fetches images from the HuggingFace
jbarrow/CommonForms dataset (one at a time via DuckDB), and runs the full
generation pipeline for each.

If the JSONL file does not exist, automatically runs the filtering pipeline
(stage 0) to create it from HuggingFace.

Output: a consolidated tasks.yaml + satellite forms/ directory.
"""

import asyncio
import json
import tempfile
import traceback
from pathlib import Path

import yaml
from sage_benchmark.shared import TaskPoolExecutor

from sage_data_gen.form_filling.config import FormFillingConfig
from sage_data_gen.form_filling.generate_form_task import generate_form_task

DATASET_NAME = "jbarrow/CommonForms"
HF_PARQUET_URL = "hf://datasets/jbarrow/CommonForms/data/{split}-*.parquet"


def _load_jsonl(path: str) -> list[dict]:
    """Read all entries from a JSONL file."""
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def _load_existing_task_ids(output_dir: Path) -> set[str]:
    """Load IDs of tasks already present in any YAML file in output_dir."""
    existing: set[str] = set()
    if not output_dir.is_dir():
        return existing
    for yaml_path in output_dir.glob("*.yaml"):
        try:
            with open(yaml_path) as f:
                data = yaml.safe_load(f)
            if data and "tasks" in data:
                for t in data["tasks"]:
                    if "id" in t:
                        existing.add(str(t["id"]))
        except Exception:
            pass
    return existing


def _fetch_image_bytes_sync(form_id: int, split: str = "train") -> bytes:
    """Fetch a single form image from HuggingFace via DuckDB parquet query.

    This is a **blocking** function — call via :func:`_fetch_image_bytes`
    to run it in a thread and avoid blocking the async event loop.

    Each call creates its own DuckDB connection so concurrent threads
    don't collide (the global ``duckdb.sql()`` is not thread-safe).

    Returns:
        Raw JPEG/PNG bytes.
    """
    import duckdb

    url = HF_PARQUET_URL.format(split=split)
    conn = duckdb.connect()
    try:
        result = conn.sql(
            f"SELECT image FROM read_parquet('{url}') WHERE id = {form_id} LIMIT 1"
        ).fetchone()
    finally:
        conn.close()

    if result is None:
        raise ValueError(f"Form {form_id} not found in {split} split")

    image_data = result[0]
    if isinstance(image_data, dict):
        return image_data["bytes"]
    return image_data


async def _fetch_image_bytes(form_id: int, split: str = "train") -> bytes:
    """Fetch a form image without blocking the event loop.

    Runs the synchronous DuckDB query in a thread so other async tasks
    (LLM calls, other form fetches) can proceed concurrently.
    """
    import asyncio

    return await asyncio.to_thread(_fetch_image_bytes_sync, form_id, split)


def _find_local_image(task_dir: Path, form_id: int | str) -> Path | None:
    """Return the cached image path if it exists in the satellite directory.

    Checks for ``image_{form_id}.*`` (any extension) inside *task_dir*.
    Returns *None* if no image is found or the directory doesn't exist.
    """
    if not task_dir.is_dir():
        return None
    for p in task_dir.iterdir():
        if p.name.startswith(f"image_{form_id}") and p.is_file():
            return p
    return None


async def run_batch(
    input_jsonl: str | None = None,
    output_dir: str = ".",
    limit: int | None = None,
    start: int = 0,
    config: FormFillingConfig | None = None,
) -> dict:
    """Run the generation pipeline for forms listed in a JSONL file.

    Each JSONL entry must have at least 'id' and 'split' fields.
    Images are fetched individually from HuggingFace via DuckDB (no full
    dataset download required).

    If the JSONL file does not exist, runs the filtering pipeline first.

    Args:
        input_jsonl: Path to the common_forms.jsonl file. If None, uses
            config.common_forms_jsonl. If the file doesn't exist, the
            filtering pipeline runs automatically to create it.
        output_dir: Base output directory for generated task directories.
        limit: Maximum number of forms to process (None for all).
        start: Index to start from in the JSONL entries.
        config: Pipeline configuration.

    Returns:
        Summary dict with success/fail counts and lists.
    """
    if config is None:
        raise ValueError("config is required (models must be specified)")

    if input_jsonl is None:
        input_jsonl = config.common_forms_jsonl

    # Auto-filter: if JSONL doesn't exist, run stage 0
    if not Path(input_jsonl).exists():
        from sage_data_gen.form_filling.filter_forms import filter_common_forms

        print(f"JSONL not found at {input_jsonl}, running form filtering pipeline...")
        await filter_common_forms(
            output_jsonl=input_jsonl,
            config=config,
        )

    # Load JSONL entries
    entries = _load_jsonl(input_jsonl)
    print(f"Loaded {len(entries)} entries from {input_jsonl}")

    # Apply start offset
    entries = entries[start:]

    # Skip forms already in output YAML files or previously failed
    out = Path(output_dir)
    existing_ids = _load_existing_task_ids(out)
    failed_ids = {d.parent.name.removeprefix("form_") for d in out.glob("forms/form_*/failed.txt")}
    skip_ids = existing_ids | failed_ids
    if skip_ids:
        before = len(entries)
        entries = [e for e in entries if str(e["id"]) not in skip_ids]
        skipped = before - len(entries)
        print(f"Skipping {skipped} forms ({len(existing_ids)} completed, {len(failed_ids)} failed)")

    target = limit if limit is not None else len(entries)
    print(f"Processing up to {len(entries)} entries to produce {target} successful tasks")

    # Process forms concurrently via TaskPoolExecutor.
    # Tasks are written to tasks.yaml incrementally as each form completes,
    # so progress is preserved if the process crashes mid-run.
    succeeded: list[dict] = []
    failed: list[dict] = []
    tasks_yaml = out / "tasks.yaml"
    # Lock protects concurrent YAML read-modify-write from the callback.
    import threading

    _yaml_lock = threading.Lock()

    def _append_task_to_yaml(task_dict: dict) -> None:
        """Append a single task to tasks.yaml (thread-safe)."""
        with _yaml_lock:
            existing_tasks: list[dict] = []
            if tasks_yaml.exists():
                with open(tasks_yaml) as f:
                    data = yaml.safe_load(f)
                if data and "tasks" in data:
                    existing_tasks = data["tasks"]

            existing_tasks.append(task_dict)
            out.mkdir(parents=True, exist_ok=True)
            with open(tasks_yaml, "w", encoding="utf-8") as f:
                yaml.dump(
                    {"tasks": existing_tasks},
                    f,
                    default_flow_style=False,
                    sort_keys=False,
                    allow_unicode=True,
                    width=120,
                )

    async def _process_form(entry: dict) -> dict:
        form_id = entry["id"]
        split = entry.get("split", "train")
        tmp_path = None
        task_dir = out / "forms" / f"form_{form_id}"
        try:
            # Reuse existing image from the satellite directory if available,
            # avoiding a redundant HuggingFace fetch on resume.
            local_image = _find_local_image(task_dir, form_id)

            if local_image is not None:
                print(f"  Form {form_id}: reusing cached image {local_image.name}")
                image_path = str(local_image)
            else:
                # Fetch image from HuggingFace (single row, not full dataset).
                # Runs in a thread to avoid blocking the event loop.
                image_bytes = await _fetch_image_bytes(form_id, split)

                # Save to temp file (cleaned up in finally block)
                with tempfile.NamedTemporaryFile(
                    suffix=".jpg", prefix=f"form_{form_id}_", delete=False
                ) as tmp:
                    tmp.write(image_bytes)
                    tmp_path = tmp.name
                image_path = tmp_path

            # Run the full pipeline (returns FormTask, writes satellite files)
            task = await generate_form_task(
                image_path=image_path,
                output_dir=output_dir,
                config=config,
                form_id=str(form_id),
            )
            return {"id": form_id, "task": task, "success": True}
        except Exception as e:
            print(f"\nError processing form {form_id}: {e}")
            traceback.print_exc()
            # Write failed.txt so this form is skipped on future runs
            task_dir.mkdir(parents=True, exist_ok=True)
            (task_dir / "failed.txt").write_text(str(e), encoding="utf-8")
            return {"id": form_id, "error": str(e), "success": False}
        finally:
            if tmp_path:
                Path(tmp_path).unlink(missing_ok=True)

    def _on_complete(result: dict) -> None:
        if result["success"]:
            succeeded.append(result)
            # Write task to YAML immediately so progress survives crashes.
            _append_task_to_yaml(result["task"].model_dump(mode="json"))
            print(f"  [{len(succeeded) + len(failed)}/{len(entries)}] Form {result['id']} done")
        else:
            failed.append(result)
            print(f"  [{len(succeeded) + len(failed)}/{len(entries)}] Form {result['id']} FAILED")

    # Use cancel_event to stop the pool once we have enough successes
    cancel_event = asyncio.Event()

    def _on_complete_with_limit(result: dict) -> None:
        _on_complete(result)
        if limit is not None and len(succeeded) >= limit:
            cancel_event.set()

    executor = TaskPoolExecutor(
        batch_size=config.max_concurrency,
        on_task_complete=_on_complete_with_limit,
        cancel_event=cancel_event,
    )

    await executor.run(_process_form(entry) for entry in entries)

    # Print summary
    print(f"\n{'=' * 60}")
    print("BATCH GENERATION SUMMARY")
    print(f"{'=' * 60}")
    print(f"Attempted: {len(succeeded) + len(failed)}")
    print(f"Succeeded: {len(succeeded)}")
    print(f"Failed: {len(failed)}")
    if failed:
        print(
            f"Failed forms: {', '.join(str(f['id']) for f in failed)} (see forms/form_*/failed.txt)"
        )
    print(f"Output: {tasks_yaml}")
    print(f"{'=' * 60}\n")

    return {
        "total": len(entries),
        "succeeded": len(succeeded),
        "failed": len(failed),
        "succeeded_forms": succeeded,
        "failed_forms": failed,
    }
