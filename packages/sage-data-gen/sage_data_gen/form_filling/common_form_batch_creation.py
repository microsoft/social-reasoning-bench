"""Batch form-filling data generation from common_forms.jsonl.

Reads a JSONL file of filtered forms, extracts images from the HuggingFace
jbarrow/CommonForms dataset, and runs the full generation pipeline for each.
"""

import json
import tempfile
import traceback
from pathlib import Path

from sage_data_gen.form_filling.config import FormFillingConfig
from sage_data_gen.form_filling.generate_form_task import generate_form_task

DATASET_NAME = "jbarrow/CommonForms"


def _load_jsonl(path: str) -> list[dict]:
    """Read all entries from a JSONL file."""
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def run_batch(
    input_jsonl: str,
    output_dir: str = ".",
    limit: int | None = None,
    start: int = 0,
    config: FormFillingConfig | None = None,
) -> dict:
    """Run the generation pipeline for forms listed in a JSONL file.

    Each JSONL entry must have at least 'id' and 'split' fields.
    Images are extracted from the HuggingFace jbarrow/CommonForms dataset.

    Args:
        input_jsonl: Path to the common_forms.jsonl file.
        output_dir: Base output directory for generated task directories.
        limit: Maximum number of forms to process (None for all).
        start: Index to start from in the JSONL entries.
        config: Pipeline configuration.

    Returns:
        Summary dict with success/fail counts and lists.
    """
    from datasets import load_dataset
    from tqdm import tqdm

    if config is None:
        config = FormFillingConfig()

    # Load JSONL entries
    entries = _load_jsonl(input_jsonl)
    print(f"Loaded {len(entries)} entries from {input_jsonl}")

    # Apply start/limit
    entries = entries[start:]
    if limit is not None:
        entries = entries[:limit]
    print(f"Processing {len(entries)} entries (start={start}, limit={limit})")

    # Load HuggingFace dataset
    print(f"\nLoading HuggingFace dataset '{DATASET_NAME}'...")
    ds = load_dataset(DATASET_NAME)
    print(f"Dataset loaded. Splits: {list(ds.keys())}")

    # Process each form
    succeeded = []
    failed = []

    for i, entry in enumerate(tqdm(entries, desc="Generating form tasks")):
        form_id = entry["id"]
        split = entry.get("split", "train")

        print(f"\n{'=' * 60}")
        print(f"[{i + 1}/{len(entries)}] Form {form_id} (split={split})")
        print(f"{'=' * 60}")

        try:
            # Extract image from HuggingFace dataset
            pil_image = ds[split][form_id]["image"]

            # Save to temp PNG
            with tempfile.NamedTemporaryFile(
                suffix=".png", prefix=f"form_{form_id}_", delete=False
            ) as tmp:
                pil_image.save(tmp, format="PNG")
                tmp_path = tmp.name

            # Run the full pipeline
            task_dir = generate_form_task(
                image_path=tmp_path,
                output_dir=output_dir,
                config=config,
                form_id=str(form_id),
            )
            succeeded.append({"id": form_id, "task_dir": str(task_dir)})

            # Clean up temp file (image is copied into task_dir by pipeline)
            Path(tmp_path).unlink(missing_ok=True)

        except Exception as e:
            print(f"\nError processing form {form_id}: {e}")
            traceback.print_exc()
            failed.append({"id": form_id, "error": str(e)})
            # Clean up temp file on error too
            try:
                Path(tmp_path).unlink(missing_ok=True)
            except NameError:
                pass

    # Print summary
    print(f"\n{'=' * 60}")
    print("BATCH GENERATION SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total: {len(entries)}")
    print(f"Succeeded: {len(succeeded)}")
    print(f"Failed: {len(failed)}")
    if failed:
        print(f"\nFailed forms:")
        for f in failed:
            print(f"  Form {f['id']}: {f['error']}")
    print(f"Output directory: {output_dir}")
    print(f"{'=' * 60}\n")

    return {
        "total": len(entries),
        "succeeded": len(succeeded),
        "failed": len(failed),
        "succeeded_forms": succeeded,
        "failed_forms": failed,
    }
