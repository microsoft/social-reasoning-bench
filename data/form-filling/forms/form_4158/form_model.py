from pydantic import BaseModel, ConfigDict, Field


class NoticeOfDetermination(BaseModel):
    """Notice of Determination (Appendix D)

    A public agency submits this notice after approving a project subject to CEQA to document the
    environmental review outcome (e.g., EIR or Negative Declaration), key findings, and adopted
    mitigation/monitoring actions. It is filed with the State Clearinghouse (OPR) and/or the County
    Clerk, who record and publish it for public notice and to start applicable administrative and legal
    timelines based on the agency’s determinations.
    """

    model_config = ConfigDict(extra="forbid")




    project_applicant: str = Field(
        ...,
        description='Project applicant. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    project_description: str = Field(
        ...,
        description='Project description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    project_approval_date: str = Field(
        ...,
        description='Project approval date (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


