from pydantic import BaseModel, ConfigDict, Field


class PersonalFinancialStatement(BaseModel):
    """Personal Financial Statement

    Borrowers applying for credit with Spokane Tribal Credit (and any co-signer, if used) complete this statement to disclose assets owned, debts owed, and related payment obligations. STC loan and underwriting staff review the information and may verify it with listed sources and credit-reporting agencies to decide whether to approve credit/loan requests and on what terms.
    """

    model_config = ConfigDict(extra="forbid")

    assets_auto_1_present_value: float | None = Field(..., description="Auto #1 present value")







    liabilities_stc_long_term_loan_borrower_payments: float | None = Field(..., description="STC long term loan borrower payments")






    customer_comments: str = Field(
        ...,
        description='Customer comments. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
