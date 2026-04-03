from pydantic import BaseModel, ConfigDict, Field


class PersonalFinancialStatementSTC(BaseModel):
    """Personal Financial Statement - Spokane Tribal Credit

    Purpose: Personal financial statement to assess assets, liabilities, and creditworthiness for a loan application, including information from a co-signer if applicable.
    Recipient: Loan officers or credit evaluators at Spokane Tribal Credit who will use the information to determine eligibility for credit or a loan.
    """

    model_config = ConfigDict(extra="forbid")

    borrower_home_rent_or_mortgage_to_whom: str = Field(..., description='Borrower home rent/mortgage to whom. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    borrower_home_insurance_present_value: float | None = Field(..., description="Borrower home insurance present value")
    cosigner_home_rent_or_mortgage_to_whom: str = Field(..., description='Co-signer home rent/mortgage to whom. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    cosigner_home_insurance_present_value: float | None = Field(..., description="Co-signer home insurance present value")
    customer_comments: str = Field(..., description='Customer comments. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
