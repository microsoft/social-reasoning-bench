from pydantic import BaseModel, ConfigDict, Field


class NoticeOfExemptionAppendixEForm(BaseModel):
    """Notice of Exemption Appendix E"""

    model_config = ConfigDict(extra="forbid")

    date_received_opr: str = Field(..., description='Date received for filing at OPR. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')