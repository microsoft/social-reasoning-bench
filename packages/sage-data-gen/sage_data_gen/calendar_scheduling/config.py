from pydantic import BaseModel, Field, model_validator


class PipelineConfig(BaseModel):
    num_companies: int = 4
    employees_per_company: int = 5
    calendar_date: str = "2026-02-20"
    fullness_levels: list[int] = Field(default_factory=lambda: [2, 3, 4, 5, 7, 9, 10])
    medium_size: int = 10
    small_size: int = 3
    task_retry_limit: int = Field(
        default=3,
        description="Max retries when a generated task fails validation "
        "(no secret event at suboptimal preference time).",
    )
    model: str = Field(description="Model for generation (e.g. 'azure_pool/gpt-5.2')")
    labeling_models: list[str] = Field(
        min_length=1,
        description="Models for majority-vote privacy labeling. "
        "Each model labels independently; final label is majority vote.",
    )
    output_dir: str = "data/calendar-scheduling"
    generate_preferences: bool = Field(
        default=True,
        description="Whether to generate scheduling preferences for tasks",
    )
    requestor_fullness: int = Field(
        default=5,
        description="Fixed number of free working-hour slots in the requestor's calendar",
    )
    min_mutual_free_slots: int = Field(
        default=2,
        description="Minimum number of mutually free slots between assistant and requestor calendars",
    )
    seed: int = Field(
        default=42,
        description="Random seed for deterministic preference generation",
    )

    @model_validator(mode="after")
    def _check_min_mutual_free_slots_compatible(self) -> "PipelineConfig":
        smallest = min(self.fullness_levels)
        if self.min_mutual_free_slots > smallest:
            incompatible = sorted(f for f in self.fullness_levels if f < self.min_mutual_free_slots)
            raise ValueError(
                f"min_mutual_free_slots={self.min_mutual_free_slots} is incompatible with "
                f"fullness_levels containing {incompatible} — these levels cannot satisfy the "
                f"constraint and would be silently dropped at verification. "
                f"Either lower min_mutual_free_slots or remove fullness levels below it."
            )
        return self
