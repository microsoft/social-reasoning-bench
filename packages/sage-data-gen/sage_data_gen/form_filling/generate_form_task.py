"""Main orchestration: form image -> complete task directory.

Takes a single form image and produces a complete task directory containing:
- form_model.py: Pydantic BaseModel class for the form
- ground_truth.json: Full unmasked ground truth
- masked_ground_truth.json: Ground truth with N close-ended fields blanked
- masked_fields.json: List of masked fields with original values
- artifacts.json: Digital artifacts
- task.json: Task metadata with persona, secrets, coverage info
- gui_form.html: Interactive HTML form matching the image
"""

import json
import traceback
from pathlib import Path

from sage_llm import ModelClient

from sage_data_gen.form_filling.config import FormFillingConfig
from sage_data_gen.form_filling.models import AllSecrets, QuestionSecrets
from sage_data_gen.form_filling.stages.fill_groundtruth import generate_groundtruth
from sage_data_gen.form_filling.stages.generate_artifacts import step4_create_artifacts
from sage_data_gen.form_filling.stages.generate_filesystem_artifacts import (
    generate_filesystem_artifacts,
)
from sage_data_gen.form_filling.stages.generate_gui_html import generate_gui_html
from sage_data_gen.form_filling.stages.generate_scenario import (
    groundtruth_to_answers,
    scrub_persona_for_masked_fields,
    step2_expand_persona,
    step3_generate_secrets,
    step3b_generate_negative_info,
)
from sage_data_gen.form_filling.stages.mask_groundtruth import mask_groundtruth
from sage_data_gen.form_filling.stages.parse_form import parse_form_image
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


def generate_form_task(
    image_path: str,
    output_dir: str = ".",
    config: FormFillingConfig | None = None,
    form_id: str | None = None,
) -> Path:
    """Generate a complete form-filling task from a form image.

    This is the main entry point. It runs all pipeline stages:
    1. Parse form image -> Pydantic model code
    2. Fill form with realistic data -> ground truth
    2b. Mask N close-ended fields
    3. Expand persona + generate secrets + negative info
    4. Create digital artifacts
    5. Validate artifacts + fix coverage gaps
    6. Generate GUI HTML form

    Args:
        image_path: Path to the form image (PNG/JPEG).
        output_dir: Base directory for output.
        config: Pipeline configuration. Defaults to FormFillingConfig().
        form_id: Optional form ID. Extracted from filename if not provided.

    Returns:
        Path to the created task directory.
    """
    if config is None:
        config = FormFillingConfig()

    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Determine form ID
    if form_id is None:
        form_id = extract_form_id(str(image_path))

    task_dir = Path(output_dir) / f"form_{form_id}"
    task_dir.mkdir(parents=True, exist_ok=True)

    client = ModelClient()

    print(f"\n{'=' * 60}")
    print(f"Processing Form {form_id}")
    print(f"Image: {image_path}")
    print(f"Output: {task_dir}")
    print(f"{'=' * 60}")

    try:
        # Stage 1: Parse form image
        print(f"\n[Stage 1] Parsing form image...")
        extracted_text, form_model_code, class_name, form_title = parse_form_image(
            image_path, client, config
        )

        # Save form_model.py
        form_model_path = task_dir / "form_model.py"
        form_model_path.write_text(form_model_code, encoding="utf-8")
        print(f"  Saved form_model.py ({len(form_model_code)} chars)")

        # Stage 2: Generate ground truth
        print(f"\n[Stage 2] Generating ground truth...")
        groundtruth = generate_groundtruth(form_model_path, client, config)

        # Save ground_truth.json
        gt_path = task_dir / "ground_truth.json"
        gt_path.write_text(json.dumps(groundtruth, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  Saved ground_truth.json ({len(groundtruth)} fields)")

        # Stage 2b: Mask close-ended fields
        print(f"\n[Stage 2b] Masking close-ended fields...")
        masked_gt, masked_fields = mask_groundtruth(
            groundtruth,
            n=config.mask_n_fields,
            seed=config.random_seed,
            client=client,
            config=config,
        )

        # Save masked files
        masked_gt_path = task_dir / "masked_ground_truth.json"
        masked_gt_path.write_text(
            json.dumps(masked_gt, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        masked_fields_path = task_dir / "masked_fields.json"
        masked_fields_path.write_text(
            json.dumps(masked_fields, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(
            f"  Saved masked_ground_truth.json and masked_fields.json ({len(masked_fields)} masked)"
        )

        # Stage 3: Generate scenario (persona + secrets + negative info)
        # Use masked ground truth so the agent doesn't see masked values
        gt_for_scenario = masked_gt
        ground_truth_answers = groundtruth_to_answers(gt_for_scenario)
        unmasked_ground_truth_answers = groundtruth_to_answers(groundtruth)

        print(f"\n[Stage 3] Expanding persona...")
        persona = step2_expand_persona(extracted_text, ground_truth_answers, client, config)

        print(f"\n[Stage 3] Scrubbing masked field info from persona...")
        persona = scrub_persona_for_masked_fields(persona, masked_fields, client, config)

        print(f"\n[Stage 4] Generating secrets...")
        max_retries = config.max_secret_retries
        retry_count = 0
        have_secrets = False

        while not have_secrets and retry_count < max_retries:
            all_secrets, field_analysis = step3_generate_secrets(
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
        negative_info = step3b_generate_negative_info(
            persona, ground_truth_answers, all_secrets, field_analysis, client, config
        )

        # Stage 5: Create digital artifacts
        print(f"\n[Stage 5] Creating digital artifacts...")
        artifacts = step4_create_artifacts(
            persona,
            ground_truth_answers,
            all_secrets,
            client,
            config,
            negative_info=negative_info,
        )

        # Stage 6: Validate and fix artifacts
        print(f"\n[Stage 6] Validating artifacts...")
        validation = validate_artifacts_with_llm(
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
        all_secrets, artifacts, validation = ensure_full_secret_coverage(
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
                neg_info_coverage = validate_negative_info_coverage(
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
                artifacts = fix_missing_negative_info_in_artifacts(
                    missing_pairs, artifacts, persona, client, config
                )
                neg_info_coverage = validate_negative_info_coverage(
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

        # Save artifacts.json
        all_artifacts = artifacts.artifacts
        artifacts_output = {"artifacts": [a.model_dump() for a in all_artifacts]}
        artifacts_path = task_dir / "artifacts.json"
        artifacts_path.write_text(
            json.dumps(artifacts_output, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"  Saved artifacts.json ({len(all_artifacts)} artifacts)")

        # Optional: Generate file system artifacts for search-based evaluation
        fs_data = {}
        if config.filesystem_mode:
            print(f"\n[Stage FS] Generating file system artifacts...")
            fs_artifacts, fs_findability = generate_filesystem_artifacts(
                persona=persona,
                ground_truth=ground_truth_answers,
                masked_fields=masked_fields,
                all_secrets=all_secrets,
                client=client,
                config=config,
                negative_info=negative_info,
            )

            print(f"\n[Stage FS.1] Validating BM25 retrievability...")
            bm25_validation = validate_bm25_retrievability(fs_artifacts, fs_findability, config)

            # Save filesystem_artifacts.json
            fs_artifacts_path = task_dir / "filesystem_artifacts.json"
            fs_artifacts_path.write_text(
                json.dumps(fs_artifacts.model_dump(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            print(f"  Saved filesystem_artifacts.json ({len(fs_artifacts.artifacts)} artifacts)")

            # Save findability.json
            findability_path = task_dir / "findability.json"
            findability_path.write_text(
                json.dumps(fs_findability.model_dump(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            print(f"  Saved findability.json")

            # Save bm25_validation.json
            bm25_path = task_dir / "bm25_validation.json"
            bm25_path.write_text(
                json.dumps(bm25_validation.model_dump(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            print(
                f"  Saved bm25_validation.json (pass rate: {bm25_validation.overall_pass_rate:.1%})"
            )

            fs_data = {
                "filesystem_artifacts": fs_artifacts.model_dump(),
                "findability": fs_findability.model_dump(),
                "bm25_validation": bm25_validation.model_dump(),
            }

        # Build and save task.json
        total_secrets = sum(len(qs.secrets) for qs in all_secrets.question_secrets)
        due_diligence_fields = masked_fields

        # Calculate close-ended field coverage (matches validation output)
        covered_close_ended = len(
            [fc for fc in validation.field_coverage if fc.is_covered and not fc.is_open_ended]
        )
        covered_close_ended += len(missing_close_ended)
        total_close_ended = len([fc for fc in validation.field_coverage if not fc.is_open_ended])

        task_data = {
            "form_id": form_id,
            "form_info": {
                "title": form_title,
                "extracted_text": extracted_text,
            },
            "ground_truth": unmasked_ground_truth_answers.model_dump(),
            "persona": persona.model_dump(),
            "secrets": all_secrets.model_dump(),
            "negative_info": negative_info.model_dump(),
            "artifacts": {"artifacts": [a.model_dump() for a in artifacts.artifacts]},
            "validation": validation.model_dump(),
            "negative_info_coverage": [
                c.model_dump() if hasattr(c, "model_dump") else c for c in neg_info_coverage
            ],
            "due_diligence_fields": due_diligence_fields,
            **fs_data,
        }

        task_path = task_dir / "task.json"
        task_path.write_text(json.dumps(task_data, indent=2, ensure_ascii=False), encoding="utf-8")

        # Stage 7: Generate GUI HTML
        if config.skip_html:
            print(f"\n[Stage 7] Skipping HTML generation (--no-html)")
        else:
            print(f"\n[Stage 7] Generating GUI HTML...")
            html_content = generate_gui_html(image_path, form_model_code, client, config)
            html_path = task_dir / f"form_{form_id}.html"
            html_path.write_text(html_content, encoding="utf-8")
            print(f"  Saved form_{form_id}.html ({len(html_content)} chars)")

        # Copy image to task directory
        import shutil

        image_dest = task_dir / f"image_{form_id}{image_path.suffix}"
        if not image_dest.exists():
            shutil.copy2(image_path, image_dest)

        # Summary
        neg_embedded = len(
            [
                c
                for c in neg_info_coverage
                if (c.is_embedded if hasattr(c, "is_embedded") else c.get("is_embedded", False))
            ]
        )
        neg_total = len(neg_info_coverage)
        print(f"\n{'=' * 60}")
        print(f"Successfully created Form {form_id}")
        print(f"  Ground truth answers: {len(ground_truth_answers.answers)}")
        print(f"  Secrets: {total_secrets} across {len(all_secrets.question_secrets)} questions")
        print(f"  Negative info items: {len(negative_info.items)}")
        print(f"  Artifacts: {len(artifacts.artifacts)}")
        print(f"  Close-ended field coverage: {covered_close_ended}/{total_close_ended}")
        print(f"  Negative info coverage: {neg_embedded}/{neg_total}")
        print(f"  Due diligence fields: {len(due_diligence_fields)}")
        print(f"  Output: {task_dir}")
        print(f"{'=' * 60}\n")

        return task_dir

    except Exception as e:
        print(f"\n{'=' * 60}")
        print(f"Error processing Form {form_id}: {e}")
        print(f"{'=' * 60}\n")
        traceback.print_exc()
        raise
