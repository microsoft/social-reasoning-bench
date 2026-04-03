from pydantic import BaseModel, ConfigDict, Field


class AnnualPreparticipationPhysicalExamination(BaseModel):
    """2021-22 ANNUAL PREPARTICIPATION PHYSICAL EXAMINATION"""

    model_config = ConfigDict(extra="forbid")

    body_fat_percent: str = Field(..., description='% Body Fat (optional). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    bp_diastolic_1: str = Field(..., description='BP diastolic 1. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    vision_l: str = Field(..., description='Vision left (L20/__). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    notes: str = Field(..., description='Notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')