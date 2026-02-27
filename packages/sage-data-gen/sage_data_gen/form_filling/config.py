"""Configuration for form filling data generation pipeline."""

from pydantic import BaseModel


class FormFillingConfig(BaseModel):
    """Configuration for the form filling data generation pipeline."""

    # Model configuration
    parsing_model: str = "trapi/msraif/shared/gpt-5.1"
    vision_model: str = "trapi/gpt-5.2"
    generation_model: str = "trapi/msraif/shared/gpt-5.1"
    validation_model: str = "trapi/msraif/shared/gpt-5.1"

    # Masking configuration
    mask_n_fields: int = 5
    random_seed: int = 42

    # Masking LLM judge
    max_mask_retries: int = 3

    # Secret generation
    max_secret_retries: int = 5

    # HTML generation
    skip_html: bool = False
