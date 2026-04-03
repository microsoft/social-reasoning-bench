from pydantic import BaseModel, ConfigDict, Field


class MthsBoostersFundsRequestForm(BaseModel):
    """MTHS Boosters Funds Request Form"""

    model_config = ConfigDict(extra="forbid")

    coach_advised: str = Field(..., description='Coach advised. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    general_purpose_of_request: str = Field(..., description='General purpose of request. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    total_amount_requested: float | None = Field(..., description="Total amount requested")