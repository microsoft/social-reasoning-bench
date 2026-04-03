from pydantic import BaseModel, ConfigDict, Field


class PersonalFinancialStatement(BaseModel):
    """Personal Financial Statement"""

    model_config = ConfigDict(extra="forbid")

    borrower_home_to_whom: str = Field(..., description='Borrower home to whom rent/mortgage is paid. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    borrower_spokane_tribal_credit_education_loan_payments: float | None = Field(..., description="Borrower STC education loan payments")
    cosigner_credit_cards_other_debt_present_balance: float | None = Field(..., description="Co-signer credit cards/other debt present balance")

    customer_comments: str = Field(..., description='Customer comments. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')