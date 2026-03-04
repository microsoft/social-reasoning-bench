"""CLI for form filling data generation.

Usage:
    sagegen form-filling --image path/to/form.png --output-dir ./output/
"""

import argparse
import sys

from sage_data_gen.form_filling.config import FormFillingConfig
from sage_data_gen.form_filling.generate_form_task import generate_form_task


def main(argv: list[str] | None = None) -> None:
    """Generate a form-filling evaluation task from a single form image."""
    parser = argparse.ArgumentParser(
        prog="sagegen form-filling",
        description="Generate a form-filling evaluation task from a form image.",
    )
    parser.add_argument(
        "--image",
        required=True,
        help="Path to the form image (PNG/JPEG).",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Base output directory (default: current directory).",
    )
    parser.add_argument(
        "--form-id",
        default=None,
        help="Form ID (extracted from filename if omitted).",
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
        "--parsing-model",
        default=None,
        help="Override the parsing model.",
    )
    parser.add_argument(
        "--generation-model",
        default=None,
        help="Override the generation model.",
    )
    parser.add_argument(
        "--validation-model",
        default=None,
        help="Override the validation model.",
    )
    parser.add_argument(
        "--vision-model",
        default=None,
        help="Override the vision model.",
    )
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="Skip HTML form generation (Stage 6).",
    )
    parser.add_argument(
        "--filesystem",
        action="store_true",
        help="Generate file system artifacts (emails/calendar) for search-based evaluation.",
    )

    args = parser.parse_args(argv)

    config_kwargs = {
        "mask_n_fields": args.mask_fields,
        "random_seed": args.seed,
    }
    if args.parsing_model:
        config_kwargs["parsing_model"] = args.parsing_model
    if args.generation_model:
        config_kwargs["generation_model"] = args.generation_model
    if args.validation_model:
        config_kwargs["validation_model"] = args.validation_model
    if args.vision_model:
        config_kwargs["vision_model"] = args.vision_model
    if args.no_html:
        config_kwargs["skip_html"] = True
    if args.filesystem:
        config_kwargs["filesystem_mode"] = True

    config = FormFillingConfig(**config_kwargs)

    try:
        task_dir = generate_form_task(
            image_path=args.image,
            output_dir=args.output_dir,
            config=config,
            form_id=args.form_id,
        )
        print(f"\nTask created: {task_dir}")
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
