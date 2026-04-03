from pydantic import BaseModel, ConfigDict, Field


class InnovativeTeachingGrantApplicationCoverPage(BaseModel):
    """Innovative Teaching Grant Application Cover Page"""

    model_config = ConfigDict(extra="forbid")

    project_title: str = Field(..., description='Project title. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    amount_of_grant: float | None = Field(..., description="Amount of grant requested")
    number_of_students_participating: float | None = Field(..., description="Number of students participating")
    project_description: str = Field(..., description='Project description (100 words max). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    principal_date: str = Field(..., description='Date of Principal signature. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')