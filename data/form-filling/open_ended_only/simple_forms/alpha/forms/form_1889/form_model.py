from pydantic import BaseModel, ConfigDict, Field


class MthsBoostersFundsRequestForm(BaseModel):
    """MTHS Boosters Funds Request Form

    Purpose: This form is used to request funds or reimbursement for expenses related to Mountlake Terrace High School (MTHS) sports teams or groups, requiring documentation such as receipts or invoices.
    Recipient: The MTHS Boosters organization's board members or treasurer, who are responsible for reviewing, approving, and processing financial requests from coaches, group leaders, or authorized representatives.
    """

    model_config = ConfigDict(extra="forbid")

    date_of_request: str = Field(..., description='Date of request (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    general_purpose_of_request: str = Field(..., description='General purpose of request. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    total_amount_requested: float | None = Field(..., description="Total amount requested")
    # Accounting Use Only fields