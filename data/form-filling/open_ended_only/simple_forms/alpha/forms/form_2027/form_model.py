from pydantic import BaseModel, ConfigDict, Field


class InnovativeTeachingGrantApplication(BaseModel):
    """Innovative Teaching Grant Application

    Purpose: Application form for educators to request funding for innovative teaching projects, specifying project details, target population, and required approvals.
    Recipient: School district administrators responsible for processing grant applications, including finance, instructional technology, and facilities directors; not seen by the grant review committee.
    """

    model_config = ConfigDict(extra="forbid")

    cover_page_target_students_group: str = Field(
        ..., description='If students, specify target group. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    cover_page_implementation_start_date_additional: str = Field(
        ..., description='Additional implementation start date info. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    cover_page_project_description: str = Field(
        ..., description='Project description (max 100 words). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )