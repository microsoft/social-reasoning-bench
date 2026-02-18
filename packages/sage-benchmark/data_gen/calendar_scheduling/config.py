from pydantic import BaseModel, Field


class PipelineConfig(BaseModel):
    num_companies: int = 4
    employees_per_company: int = 6
    calendar_date: str = "2025-03-15"
    calendar_fullness_range: tuple[float, float] = (0.3, 0.9)
    tasks_per_employee: int = 4
    satisfiable_ratio: float = 0.5
    internal_requestor_ratio: float = Field(
        default=0.5,
        description="Ratio of tasks with internal (same company) requestors. "
        "Affects privacy: more internal = lower secret rate. Target: 0.5 = ~85% secret",
    )
    meeting_duration_options: list[int] = Field(default_factory=lambda: [30, 60, 90])
    model: str = "trapi/msraif/shared/gpt-5.2"
    artifacts_per_task: int = 5
    output_dir: str = "data/calendar-scheduling"
    tasks_filename: str = "generated-tasks.yaml"
    artifacts_filename: str = "generated-tasks-artifacts.json"
    generate_preferences: bool = Field(
        default=True,
        description="Whether to generate scheduling preferences for tasks",
    )
    random_seed: int = Field(
        default=42,
        description="Random seed for deterministic preference generation",
    )
