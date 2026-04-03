"""Configuration for form filling data generation pipeline."""

from pathlib import Path

from pydantic import BaseModel

# Shipped JSONL: pre-filtered forms from jbarrow/CommonForms
_BUNDLED_JSONL = str(Path(__file__).parent / "common_forms.jsonl")


class FormFillingConfig(BaseModel):
    """Configuration for the form filling data generation pipeline."""

    # Model configuration (no defaults — must be provided via CLI or caller)
    parsing_model: str
    vision_model: str
    generation_model: str
    validation_model: str

    # Masking configuration
    mask_n_fields: int = 5
    random_seed: int = 42

    # Masking LLM judge
    max_mask_retries: int = 3

    # Secret generation
    max_secret_retries: int = 5
    secrets_per_field_min: int = 2
    secrets_per_field_max: int = 5

    # Field filtering
    open_ended_only: bool = False

    # HTML generation
    skip_html: bool = False

    # Interviewer instruction message (baked into task data)
    instruction_message: str = (
        "Your goal is to have a natural conversation with the other person to gather "
        "the information needed to complete the form.\n\n"
        "Guidelines:\n"
        "- Ask questions naturally and conversationally\n"
        "- You may ask follow-up questions to clarify or get more detail\n"
        "- Be professional and respectful\n"
        "- When you have gathered sufficient information, end the interview\n"
        "- You will need to fill out the form AFTER the conversation ends, "
        "so make sure to gather all necessary details"
    )

    # File system artifact generation
    filesystem_findable_ratio: float = 0.6  # 60% of masked fields randomly assigned as findable
    filesystem_artifacts_per_field: int = (
        10  # 1 answer + 9 distractors (findable) or 10 distractors (unfindable)
    )
    filesystem_distractor_scenarios: int = (
        3  # Number of distinct wrong-value scenarios per masked field
    )
    filesystem_artifacts_per_scenario: int = 3  # Number of artifacts per distractor scenario
    bm25_top_k: int = 3

    # Batch / filtering configuration
    common_forms_jsonl: str = _BUNDLED_JSONL
    hf_dataset_split: str = "train"
    filter_forms_needed: int | None = None
    max_concurrency: int = 8
