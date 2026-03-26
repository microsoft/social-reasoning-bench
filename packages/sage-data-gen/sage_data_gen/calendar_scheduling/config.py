from pydantic import BaseModel, Field


class PipelineConfig(BaseModel):
    num_companies: int = 4
    employees_per_company: int = 5
    calendar_date: str = "2026-02-20"
    fullness_levels: list[int] = Field(default_factory=lambda: [0, 1, 3, 5, 7, 9, 11])
    medium_size: int = 10
    small_size: int = 3
    task_retry_limit: int = Field(
        default=3,
        description="Max retries when a generated task fails validation "
        "(no secret event at suboptimal preference time).",
    )
    model: str = "phyagi/gpt-5.2"
    labeling_models: list[str] = Field(
        default_factory=lambda: [
            "phyagi/gpt-5.2",
            "phyagi/gpt-5.1",
            "phyagi/gpt-4.1",
        ],
        description="Models used for majority-vote privacy labeling. "
        "Each model labels independently; final label is majority vote.",
    )
    output_dir: str = "data/calendar-scheduling/final"
    generate_preferences: bool = Field(
        default=True,
        description="Whether to generate scheduling preferences for tasks",
    )
    random_seed: int = Field(
        default=42,
        description="Random seed for deterministic preference generation",
    )
