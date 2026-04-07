"""CLI for form filling data generation.

Usage:
    sagegen form-filling --image path/to/form.png --output-dir ./output/
    sagegen form-filling --batch common_forms.jsonl --output-dir ./output/ --concurrency 4
"""

import argparse
import asyncio
import sys

from sage_data_gen.form_filling.config import FormFillingConfig
from sage_data_gen.form_filling.generate_form_task import generate_form_task


def main(argv: list[str] | None = None) -> None:
    """Generate form-filling evaluation tasks.

    Args:
        argv: Command-line arguments to parse. Uses ``sys.argv`` when *None*.
    """
    parser = argparse.ArgumentParser(
        prog="sagegen form-filling",
        description="Generate form-filling evaluation tasks from form images.",
    )

    # Mode selection: --image for single form, --batch for batch (default: bundled JSONL)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--image",
        help="Path to a single form image (PNG/JPEG).",
    )
    mode.add_argument(
        "--batch",
        nargs="?",
        const=None,
        default="__default_batch__",
        help=(
            "Path to a common_forms.jsonl file for batch generation. "
            "If omitted or the file does not exist, uses the bundled JSONL "
            "or filters from HuggingFace."
        ),
    )

    parser.add_argument(
        "--output-dir",
        default=".",
        help="Base output directory (default: current directory).",
    )
    parser.add_argument(
        "--form-id",
        default=None,
        help="Form ID (extracted from filename if omitted). Single-image mode only.",
    )
    parser.add_argument(
        "--mask-fields",
        type=int,
        default=5,
        help="Number of close-ended fields to mask (default: 5).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for masking (default: 42).",
    )
    parser.add_argument(
        "-m",
        "--model",
        default=None,
        help="Default model for all roles (parsing, generation, validation, vision). "
        "Individual --*-model flags take precedence.",
    )
    parser.add_argument("--parsing-model", default=None, help="Model for form parsing.")
    parser.add_argument("--generation-model", default=None, help="Model for data generation.")
    parser.add_argument("--validation-model", default=None, help="Model for validation.")
    parser.add_argument("--vision-model", default=None, help="Model for vision/OCR.")
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="Skip HTML form generation (Stage 6).",
    )
    parser.add_argument(
        "--open-ended-only",
        action="store_true",
        help="Keep only open-ended fields and masked due-diligence fields.",
    )
    parser.add_argument(
        "--secrets-per-field",
        default=None,
        help="Min,max secrets per open-ended field (e.g. '1,3'). Default: '2,5'.",
    )
    parser.add_argument(
        "--filesystem-distractor-scenarios",
        type=int,
        default=None,
        help="Number of distinct wrong-value scenarios per masked field (default: 3).",
    )
    parser.add_argument(
        "--filesystem-artifacts-per-scenario",
        type=int,
        default=None,
        help="Number of artifacts per distractor scenario (default: 3).",
    )

    # Batch-mode options
    parser.add_argument(
        "--start",
        type=int,
        default=0,
        help="Start index for batch processing (default: 0).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of forms to process in batch mode.",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=8,
        help="Maximum concurrent forms for batch processing (default: 8).",
    )
    parser.add_argument(
        "--filter-forms-needed",
        type=int,
        default=None,
        help=(
            "Number of valid forms to collect when auto-filtering from HuggingFace. "
            "Only used when --batch points to a non-existent JSONL file."
        ),
    )

    args = parser.parse_args(argv)

    config_kwargs: dict = {
        "mask_n_fields": args.mask_fields,
        "random_seed": args.seed,
    }
    if args.open_ended_only:
        config_kwargs["open_ended_only"] = True
    if args.secrets_per_field is not None:
        # Parse "min,max" string (e.g. "1,3")
        parts = args.secrets_per_field.split(",")
        if len(parts) != 2:
            parser.error("--secrets-per-field must be 'min,max' (e.g. '1,3')")
        try:
            spf_min, spf_max = int(parts[0]), int(parts[1])
        except ValueError:
            parser.error("--secrets-per-field values must be integers")
        if spf_min < 0 or spf_max < spf_min:
            parser.error("--secrets-per-field: need 0 <= min <= max")
        config_kwargs["secrets_per_field_min"] = spf_min
        config_kwargs["secrets_per_field_max"] = spf_max
    # Resolve models: per-role flags override -m/--model.
    base_model: str | None = args.model
    if not base_model and not all(
        [args.parsing_model, args.generation_model, args.validation_model, args.vision_model]
    ):
        parser.error(
            "-m/--model is required unless all of "
            "--parsing-model, --generation-model, --validation-model, --vision-model are set"
        )
    config_kwargs["parsing_model"] = args.parsing_model or base_model
    config_kwargs["generation_model"] = args.generation_model or base_model
    config_kwargs["validation_model"] = args.validation_model or base_model
    config_kwargs["vision_model"] = args.vision_model or base_model
    if args.no_html:
        config_kwargs["skip_html"] = True
    if args.filesystem_distractor_scenarios is not None:
        config_kwargs["filesystem_distractor_scenarios"] = args.filesystem_distractor_scenarios
    if args.filesystem_artifacts_per_scenario is not None:
        config_kwargs["filesystem_artifacts_per_scenario"] = args.filesystem_artifacts_per_scenario
    config_kwargs["max_concurrency"] = args.concurrency
    if args.filter_forms_needed is not None:
        config_kwargs["filter_forms_needed"] = args.filter_forms_needed

    config = FormFillingConfig(**config_kwargs)

    if args.image:
        # Single-image mode
        try:
            import yaml

            task = asyncio.run(
                generate_form_task(
                    image_path=args.image,
                    output_dir=args.output_dir,
                    config=config,
                    form_id=args.form_id,
                )
            )
            out_path = Path(args.output_dir) / "tasks.yaml"  # ty:ignore[unresolved-reference]
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                yaml.dump(
                    {"tasks": [task.model_dump(mode="json")]},
                    f,
                    default_flow_style=False,
                    sort_keys=False,
                    allow_unicode=True,
                    width=120,
                )
            print(f"\nTask written to {out_path}")
        except Exception as e:
            print(f"\nError: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        # Batch mode (default). args.batch is None (bare --batch) or a path,
        # or "__default_batch__" when neither --image nor --batch was given.
        from sage_data_gen.form_filling.common_form_batch_creation import run_batch

        batch_path = args.batch if args.batch != "__default_batch__" else None

        try:
            summary = asyncio.run(
                run_batch(
                    input_jsonl=batch_path,
                    output_dir=args.output_dir,
                    limit=args.limit,
                    start=args.start,
                    config=config,
                )
            )
            if summary["failed"] > 0:
                sys.exit(1)
        except Exception as e:
            print(f"\nError: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
