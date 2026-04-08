from pydantic import BaseModel, Field


class PipelineConfig(BaseModel):
    num_companies: int = 4
    employees_per_company: int = 5
    calendar_date: str = "2026-02-20"
    fullness_levels: list[int] = Field(default_factory=lambda: [1, 2, 3, 5, 7, 9, 10])
    medium_size: int = 10
    small_size: int = 3
    task_retry_limit: int = Field(
        default=3,
        description="Max retries when a generated task fails validation "
        "(no secret event at suboptimal preference time).",
    )
    model: str = Field(description="Model for generation (e.g. 'phyagi/gpt-5.2')")
    labeling_models: list[str] = Field(
        min_length=1,
        description="Models for majority-vote privacy labeling. "
        "Each model labels independently; final label is majority vote.",
    )
    output_dir: str = "data/calendar-scheduling/final"
    generate_preferences: bool = Field(
        default=True,
        description="Whether to generate scheduling preferences for tasks",
    )
    requestor_fullness: int = Field(
        default=5,
        description="Fixed number of free working-hour slots in the requestor's calendar",
    )
    seed: int = Field(
        default=42,
        description="Random seed for deterministic preference generation",
    )
