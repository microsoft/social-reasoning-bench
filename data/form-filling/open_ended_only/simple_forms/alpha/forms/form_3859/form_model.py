from pydantic import BaseModel, ConfigDict, Field


class AnnualPreparticipationPhysicalExamAIA(BaseModel):
    """2021-22 ANNUAL PREPARTICIPATION PHYSICAL EXAMINATION

    Purpose: Annual physical examination form to assess and document a student's medical fitness for participation in interscholastic sports activities.
    Recipient: Licensed healthcare professionals conducting the examination, and school athletic administrators or coaches who need to verify medical clearance for student athletes.
    """

    model_config = ConfigDict(extra="forbid")

    body_fat_percent: float | None = Field(..., description='Percent body fat (optional)')
    bp_2_diastolic: float | None = Field(..., description='Blood pressure 2 diastolic')
    notes: str = Field(..., description='Examiner notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')