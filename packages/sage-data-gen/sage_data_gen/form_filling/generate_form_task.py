"""Main orchestration: form image -> FormTask + satellite files.

Takes a single form image and produces:
- A FormTask object (caller writes to consolidated YAML)
- Satellite files in forms/form_{id}/ (form_model.py, image)
"""

import re
import shutil
import traceback
from pathlib import Path

import ftfy
from sage_benchmark.benchmarks.form_filling.types import (
    FormInfo,
    FormSummary,
    FormTask,
    ValidationResult,
)
from sage_llm import SageModelClient

from sage_data_gen.form_filling.config import FormFillingConfig
from sage_data_gen.form_filling.models import AllSecrets, QuestionSecrets
from sage_data_gen.form_filling.stages.fill_groundtruth import generate_groundtruth
from sage_data_gen.form_filling.stages.generate_artifacts import step4_create_artifacts
from sage_data_gen.form_filling.stages.generate_filesystem_artifacts import (
    generate_filesystem_artifacts,
)
from sage_data_gen.form_filling.stages.generate_scenario import (
    groundtruth_to_answers,
    scrub_persona_for_masked_fields,
    step2_expand_persona,
    step3_generate_secrets,
    step3b_generate_negative_info,
)
from sage_data_gen.form_filling.stages.mask_groundtruth import mask_groundtruth
from sage_data_gen.form_filling.stages.parse_form import (
    extract_text_from_image,
    generate_form_model,
)
from sage_data_gen.form_filling.stages.validate_artifacts import (
    ensure_full_secret_coverage,
    fix_missing_fields,
    fix_missing_negative_info_in_artifacts,
    get_missing_close_ended_fields,
    validate_artifacts_with_llm,
    validate_negative_info_coverage,
)
from sage_data_gen.form_filling.stages.validate_filesystem_artifacts import (
    validate_bm25_retrievability,
)
from sage_data_gen.form_filling.utils import extract_form_id

_CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def _prune_form_model(form_model_code: str, kept_field_ids: set[str]) -> str:
    """Prune a flat Pydantic form model to only the kept fields.

    Expects a flat model (no nested section classes) where each field
    starts with ``    field_id: type = Field(`` and ends with ``    )``.

    Args:
        form_model_code: Python source code of the Pydantic model.
        kept_field_ids: Set of field IDs to retain.

    Returns:
        Pruned Python source code with only the kept fields.
    """
    lines = form_model_code.split("\n")
    result: list[str] = []
    skip = False
    paren_depth = 0

    for line in lines:
        stripped = line.lstrip()

        # Detect field start: "    field_id: type = Field("
        if not skip and "= Field(" in line and ": " in stripped and line.startswith("    "):
            field_id = stripped.split(":")[0].strip()
            if field_id not in kept_field_ids:
                skip = True
                paren_depth = line.count("(") - line.count(")")
                continue

        if skip:
            paren_depth += line.count("(") - line.count(")")
            if paren_depth <= 0:
                skip = False
            continue

        result.append(line)

    return "\n".join(result)


def _sanitize_model(obj: FormTask) -> FormTask:
    """Strip control characters by round-tripping through JSON.

    Args:
        obj: FormTask instance to sanitize.

    Returns:
        New FormTask with control characters removed from all string fields.
    """
    raw = obj.model_dump_json()
    clean = _CONTROL_CHAR_RE.sub("", raw)
    return FormTask.model_validate_json(clean)


async def generate_form_task(
    image_path: str | Path,
    output_dir: str = ".",
    config: FormFillingConfig | None = None,
    form_id: str | None = None,
) -> FormTask:
    """Generate a complete form-filling task from a form image.

    Satellite files (form_model.py, image) are written to
    ``{output_dir}/forms/form_{id}/``. The returned FormTask should be
    collected by the caller and written to a consolidated YAML.

    Args:
        image_path: Path to the form image (PNG/JPEG).
        output_dir: Base directory for output.
        config: Pipeline configuration. Defaults to FormFillingConfig().
        form_id: Optional form ID. Extracted from filename if not provided.

    Returns:
        The generated FormTask.
    """
    if config is None:
        raise ValueError("config is required (models must be specified)")

    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Determine form ID
    if form_id is None:
        form_id = extract_form_id(str(image_path))

    # Satellite files go into forms/form_{id}/
    task_dir = Path(output_dir) / "forms" / f"form_{form_id}"
    task_dir.mkdir(parents=True, exist_ok=True)

    client = SageModelClient()

    print(f"\n{'=' * 60}")
    print(f"Processing Form {form_id}")
    print(f"Image: {image_path}")
    print(f"Output: {task_dir}")
    print(f"{'=' * 60}")

    try:
        # Stage 1: Parse form image.
        # If ocr.txt and form_model.py exist from a prior run, skip the
        # expensive vision-API call and multi-step parsing entirely.
        form_model_path = task_dir / "form_model.py"
        ocr_path = task_dir / "ocr.txt"

        # Cache OCR and form model independently.
        # OCR depends only on the image; form model depends on OCR text.
        if ocr_path.exists():
            print(f"\n[Stage 1a] Reusing cached ocr.txt")
            extracted_text = ocr_path.read_text(encoding="utf-8")
        else:
            print(f"\n[Stage 1a] Extracting text from image...")
            extracted_text = await extract_text_from_image(image_path, client, config)
            extracted_text = ftfy.fix_text(extracted_text)
            ocr_path.write_text(extracted_text, encoding="utf-8")

        # Extract form summary (purpose + recipient) — needed by all downstream stages.
        # Done once from OCR text regardless of whether form_model.py is cached.
        print(f"[Stage 1b] Extracting form summary...")
        from sage_data_gen.form_filling.prompts import FORM_SUMMARY_PROMPT

        form_summary = await client.aparse(
            model=config.parsing_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are analyzing a form to understand its context and audience.",
                },
                {
                    "role": "user",
                    "content": FORM_SUMMARY_PROMPT.format(form_content=extracted_text),
                },
            ],
            response_format=FormSummary,
            temperature=0.3,
        )
        print(f"  Purpose: {form_summary.form_purpose[:80]}...")
        print(f"  Recipient: {form_summary.intended_recipient[:80]}...")

        if form_model_path.exists():
            print(f"[Stage 1c] Reusing cached form_model.py")
            form_model_code = form_model_path.read_text(encoding="utf-8")
            classes = re.findall(r"^class (\w+)\(BaseModel\):", form_model_code, re.MULTILINE)
            class_name = classes[-1] if classes else f"Form{form_id}"
            form_title = class_name
        else:
            print(f"[Stage 1c] Generating form model...")
            form_model_code, class_name, form_title, form_summary = await generate_form_model(
                extracted_text, client, config, form_id=form_id, form_summary=form_summary
            )
            form_model_path.write_text(form_model_code, encoding="utf-8")
            print(f"  Saved form_model.py ({len(form_model_code)} chars)")

        # Stage 2: Fill form + classify fields
        print(f"\n[Stage 2] Generating ground truth...")
        groundtruth = await generate_groundtruth(form_model_path, client, config)

        print(f"  Generated ground truth ({len(groundtruth)} fields)")

        # Stage 2b: Mask close-ended fields
        print(f"\n[Stage 2b] Masking close-ended fields...")
        masked_gt, masked_fields = await mask_groundtruth(
            groundtruth,
            n=config.mask_n_fields,
            seed=config.random_seed,
            client=client,
            config=config,
        )

        print(f"  Masked {len(masked_fields)} close-ended fields")

        # Optional: drop non-essential close-ended fields, keeping only
        # open-ended fields and the masked due-diligence fields.
        if config.open_ended_only:
            masked_field_ids = {m["field_id"] for m in masked_fields}
            before = len(groundtruth)
            groundtruth = {
                fid: info
                for fid, info in groundtruth.items()
                if info.get("is_open_ended") or fid in masked_field_ids
            }
            masked_gt = {
                fid: info
                for fid, info in masked_gt.items()
                if info.get("is_open_ended") or fid in masked_field_ids
            }
            open_ended_count = sum(1 for info in groundtruth.values() if info.get("is_open_ended"))
            print(
                f"  open_ended_only: kept {len(groundtruth)}/{before} fields "
                f"({open_ended_count} open-ended + {len(masked_field_ids)} masked)"
            )

            # Regenerate form_model.py with only the kept fields
            kept_field_ids = set(groundtruth.keys())
            form_model_code = _prune_form_model(form_model_code, kept_field_ids)
            form_model_path.write_text(form_model_code, encoding="utf-8")
            print(f"  Pruned form_model.py to {len(kept_field_ids)} fields")

        # ── Rejection-sampling guards ──
        if len(groundtruth) > config.max_fields_per_task:
            raise ValueError(
                f"Form {form_id} has {len(groundtruth)} fields "
                f"(max {config.max_fields_per_task}) — skipping"
            )

        open_ended_count = sum(1 for info in groundtruth.values() if info.get("is_open_ended"))
        if open_ended_count < config.min_open_ended_fields_per_task:
            raise ValueError(
                f"Form {form_id} has {open_ended_count} open-ended fields "
                f"(min {config.min_open_ended_fields_per_task}) — skipping"
            )

        # Stage 3: Generate scenario (persona + secrets + negative info)
        # Use masked ground truth so the agent doesn't see masked values
        gt_for_scenario = masked_gt
        ground_truth_answers = groundtruth_to_answers(gt_for_scenario)
        unmasked_ground_truth_answers = groundtruth_to_answers(groundtruth)

        print(f"\n[Stage 3] Expanding persona...")
        persona = await step2_expand_persona(extracted_text, ground_truth_answers, client, config)

        print(f"\n[Stage 3] Scrubbing masked field info from persona...")
        persona = await scrub_persona_for_masked_fields(persona, masked_fields, client, config)

        print(f"\n[Stage 4] Generating secrets...")
        max_retries = config.max_secret_retries
        retry_count = 0
        have_secrets = False

        while not have_secrets and retry_count < max_retries:
            all_secrets, field_analysis = await step3_generate_secrets(
                extracted_text, persona, ground_truth_answers, client, config, gt=gt_for_scenario
            )
            total_secrets = sum(len(qs.secrets) for qs in all_secrets.question_secrets)
            if total_secrets > 0:
                have_secrets = True
            else:
                retry_count += 1
                print(f"  Warning: Generated 0 secrets. Retry {retry_count}/{max_retries}...")

        if not have_secrets:
            raise ValueError(
                f"Could not generate secrets for form {form_id} after {max_retries} attempts"
            )

        print(f"\n[Stage 4b] Generating negative info...")
        negative_info = await step3b_generate_negative_info(
            persona, ground_truth_answers, all_secrets, field_analysis, client, config
        )

        # Stage 5: Create digital artifacts
        print(f"\n[Stage 5] Creating digital artifacts...")
        artifacts = await step4_create_artifacts(
            persona,
            ground_truth_answers,
            all_secrets,
            client,
            config,
            negative_info=negative_info,
        )

        # Stage 6: Validate and fix artifacts
        print(f"\n[Stage 6] Validating artifacts...")
        validation = await validate_artifacts_with_llm(
            ground_truth_answers,
            all_secrets,
            artifacts,
            persona,
            field_analysis,
            client,
            config,
            negative_info=negative_info,
        )

        # Step 6.1: Ensure full secret coverage
        all_secrets, artifacts, validation = await ensure_full_secret_coverage(
            all_secrets,
            artifacts,
            validation,
            ground_truth_answers,
            persona,
            field_analysis,
            client,
            config,
            negative_info=negative_info,
        )

        # Drop any secrets still not covered by artifacts
        embedded_indices = {i for i, sc in enumerate(validation.secret_coverage) if sc.is_embedded}
        total_before = sum(len(qs.secrets) for qs in all_secrets.question_secrets)
        secret_idx = 0
        filtered_question_secrets = []
        for qs in all_secrets.question_secrets:
            filtered = []
            for secret in qs.secrets:
                if secret_idx in embedded_indices:
                    filtered.append(secret)
                secret_idx += 1
            if filtered:
                filtered_question_secrets.append(
                    QuestionSecrets(
                        question_id=qs.question_id,
                        question_text=qs.question_text,
                        secrets=filtered,
                    )
                )
        total_after = sum(len(qs.secrets) for qs in filtered_question_secrets)
        dropped = total_before - total_after
        if dropped > 0:
            print(f"  Dropped {dropped} uncovered secrets ({total_after} remaining)")
            all_secrets = AllSecrets(
                form_summary=all_secrets.form_summary,
                question_secrets=filtered_question_secrets,
            )

        # Step 6.1b: Check and fix negative info coverage
        neg_info_coverage = []
        if negative_info.items:
            print(f"\n[Step 6.1b] Checking negative info coverage...")
            neg_info_coverage = validation.negative_info_coverage

            # Fallback to separate validation if integrated pass didn't return results
            if not neg_info_coverage:
                print("  Running dedicated negative info validation...")
                neg_info_coverage = await validate_negative_info_coverage(
                    negative_info, artifacts, client, config
                )

            # Collect missing (item, point) pairs
            missing_pairs = []
            for i, cov in enumerate(neg_info_coverage):
                if not cov.is_embedded:
                    item = negative_info.items[i]
                    for pt in item.negative_info:
                        missing_pairs.append((item, pt))

            if missing_pairs:
                print(
                    f"  {len(missing_pairs)} negative info points missing, "
                    "weaving into existing artifacts..."
                )
                artifacts = await fix_missing_negative_info_in_artifacts(
                    missing_pairs, artifacts, persona, client, config
                )
                neg_info_coverage = await validate_negative_info_coverage(
                    negative_info, artifacts, client, config
                )
            else:
                print("  All negative info items covered in artifacts")

        # Step 6.2: Fix missing close-ended fields (non-masked fields not covered by artifacts)
        missing_close_ended = get_missing_close_ended_fields(validation, ground_truth_answers)
        if not missing_close_ended:
            print(f"\n[Step 6.2] All close-ended fields covered by artifacts")
        else:
            print(
                f"\n[Step 6.2] {len(missing_close_ended)} close-ended fields "
                "not covered by artifacts, adding hidden backup note..."
            )
            artifacts = fix_missing_fields(validation, ground_truth_answers, artifacts)

        print(f"  {len(artifacts.artifacts)} artifacts")

        # Optional: Generate file system artifacts for search-based evaluation
        filesystem_artifacts = []
        findability = []
        distractor_scenarios: dict = {}
        if masked_fields:
            print(f"\n[Stage FS] Generating file system artifacts...")
            (
                fs_artifacts,
                fs_findability,
                fs_distractor_scenarios,
            ) = await generate_filesystem_artifacts(
                persona=persona,
                ground_truth=ground_truth_answers,
                masked_fields=masked_fields,
                all_secrets=all_secrets,
                client=client,
                config=config,
                negative_info=negative_info,
            )

            print(f"\n[Stage FS.1] Validating BM25 retrievability...")
            validate_bm25_retrievability(fs_artifacts, fs_findability, config)

            filesystem_artifacts = [a.model_dump() for a in fs_artifacts.artifacts]
            findability = [
                {
                    "field_id": f.field_id,
                    "findability": "findable",
                    "search_terms": f.suggested_search_terms,
                }
                for f in fs_findability.findable_fields
            ] + [
                {
                    "field_id": fid,
                    "findability": "unfindable",
                    "search_terms": [],
                }
                for fid in fs_findability.unfindable_field_ids
            ]
            distractor_scenarios = {
                field_id: [s.model_dump() for s in scenarios]
                for field_id, scenarios in fs_distractor_scenarios.items()
            }
            print(f"  {len(filesystem_artifacts)} filesystem artifacts")

        # Flatten secrets for FormTask
        flat_secrets = []
        for qs in all_secrets.question_secrets:
            for s in qs.secrets:
                secret_dict = s.model_dump()
                secret_dict["question_id"] = qs.question_id
                secret_dict["related_question"] = qs.question_text
                flat_secrets.append(secret_dict)

        # Build FormTask and write task.json
        total_secrets = len(flat_secrets)
        due_diligence_fields = masked_fields

        if total_secrets > config.max_secrets_per_task:
            raise ValueError(
                f"Form {form_id} has {total_secrets} secrets "
                f"(max {config.max_secrets_per_task}) — skipping"
            )

        if not due_diligence_fields:
            raise ValueError("Task has no due diligence fields (no masked fields)")
        if not filesystem_artifacts:
            raise ValueError(
                f"Task has {len(due_diligence_fields)} due diligence fields "
                f"but 0 filesystem artifacts — masked field values are unfindable"
            )

        task = FormTask(
            id=int(form_id.removeprefix("form_")),
            form_info=FormInfo(title=form_title, extracted_text=extracted_text),
            form_summary=form_summary,
            instruction_message=config.instruction_message,
            ground_truth=unmasked_ground_truth_answers.model_dump()["answers"],
            persona=persona.model_dump(),
            secrets=flat_secrets,
            negative_info=[item.model_dump() for item in negative_info.items],
            artifacts=[a.model_dump() for a in artifacts.artifacts],
            validation=ValidationResult(
                field_coverage=[fc.model_dump() for fc in validation.field_coverage],
                secret_coverage=[sc.model_dump() for sc in validation.secret_coverage],
                negative_info_coverage=[
                    c.model_dump() if hasattr(c, "model_dump") else c for c in neg_info_coverage
                ],
            ),
            due_diligence_fields=due_diligence_fields,
            form_model_path=str(task_dir / "form_model.py"),
            filesystem_artifacts=filesystem_artifacts,
            findability=findability,
            distractor_scenarios=distractor_scenarios,
        )

        # Strip control characters from all string fields
        task = _sanitize_model(task)

        # Copy image to satellite directory
        image_dest = task_dir / f"image_{form_id}{image_path.suffix}"
        if not image_dest.exists():
            shutil.copy2(image_path, image_dest)

        # Summary
        covered_close_ended = len(
            [fc for fc in validation.field_coverage if fc.is_covered and not fc.is_open_ended]
        )
        covered_close_ended += len(missing_close_ended)
        total_close_ended = len([fc for fc in validation.field_coverage if not fc.is_open_ended])
        neg_embedded = sum(1 for c in neg_info_coverage if getattr(c, "is_embedded", False))

        print(f"\n{'=' * 60}")
        print(f"Successfully created Form {form_id}")
        print(f"  Ground truth answers: {len(task.ground_truth)}")
        print(f"  Secrets: {total_secrets} across {len(all_secrets.question_secrets)} questions")
        print(f"  Negative info items: {len(negative_info.items)}")
        print(f"  Artifacts: {len(task.artifacts)}")
        print(f"  Close-ended field coverage: {covered_close_ended}/{total_close_ended}")
        print(f"  Negative info coverage: {neg_embedded}/{len(neg_info_coverage)}")
        print(f"  Due diligence fields: {len(due_diligence_fields)}")
        print(f"  Satellite: {task_dir}")
        print(f"{'=' * 60}\n")

        return task

    except Exception as e:
        print(f"\n{'=' * 60}")
        print(f"Error processing Form {form_id}: {e}")
        print(f"{'=' * 60}\n")
        traceback.print_exc()
        raise
