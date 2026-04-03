from pydantic import BaseModel, ConfigDict, Field


class NoticeOfExemptionFormD(BaseModel):
    """Notice of Exemption Form D"""

    model_config = ConfigDict(extra="forbid")

    description_of_project: str = Field(..., description='Project description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    date_signed: str = Field(..., description='Date signed. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')