from pydantic import BaseModel, ConfigDict, Field


class InnovativeTeachingGrantApplicationCoverPage(BaseModel):
    """Innovative Teaching Grant Application Cover Page

    Teachers or other LISD applicants submit this cover page to propose an innovative classroom or school project, request a specific grant amount, and provide a brief project summary. The Education Foundation for LISD processes the application, and administrators/reviewers evaluate it to decide whether to approve funding. The applicant’s principal must sign, and district directors (Instructional Technology and/or Facilities) sign when the request involves technology/media purchases or construction/maintenance.
    """

    model_config = ConfigDict(extra="forbid")

    amount_of_grant_requested: float | None = Field(
        ...,
        description="Grant amount requested (USD)",
    )
    target_population_students_target_group: str = Field(
        ...,
        description='Student target group description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    implementation_start_date: str = Field(
        ...,
        description='Implementation start date (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    project_description: str = Field(
        ...,
        description='Project description (<=100 words). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )