from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AssetsandLiabilities(BaseModel):
    """ASSETS (OWNS) and LIABILITIES for Borrower and Co-Signer"""

    home_present_value_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present value of the borrower's home"
    )

    home_present_value_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present value of the co-signer's home"
    )

    rent_or_mortgage_present_value_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Present value or amount associated with the borrower's rent or mortgage",
    )

    rent_or_mortgage_present_value_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Present value or amount associated with the co-signer's rent or mortgage",
    )

    rent_or_mortgage_payments_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Borrower's periodic rent or mortgage payment amount"
    )

    rent_or_mortgage_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Co-signer's periodic rent or mortgage payment amount"
    )

    to_whom_borrower: str = Field(
        default="",
        description=(
            "Name of the landlord or mortgage holder for the borrower .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    to_whom_co_signer: str = Field(
        default="",
        description=(
            "Name of the landlord or mortgage holder for the co-signer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    home_insurance_present_value_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present value or coverage amount of the borrower's home insurance"
    )

    home_insurance_present_value_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present value or coverage amount of the co-signer's home insurance"
    )

    home_insurance_payments_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Borrower's periodic home insurance payment amount"
    )

    home_insurance_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Co-signer's periodic home insurance payment amount"
    )

    auto_year_make_and_model_borrower: str = Field(
        default="",
        description=(
            "Year, make, and model of the borrower's vehicle .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    auto_year_make_and_model_co_signer: str = Field(
        default="",
        description=(
            "Year, make, and model of the co-signer's vehicle .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    auto_present_value_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present value of the borrower's vehicle"
    )

    auto_present_value_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present value of the co-signer's vehicle"
    )

    auto_payments_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Borrower's periodic auto loan payment amount"
    )

    auto_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Co-signer's periodic auto loan payment amount"
    )

    auto_second_year_make_and_model_borrower: str = Field(
        default="",
        description=(
            "Year, make, and model of the borrower's second vehicle .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    auto_second_year_make_and_model_co_signer: str = Field(
        default="",
        description=(
            "Year, make, and model of the co-signer's second vehicle .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    auto_second_present_value_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present value of the borrower's second vehicle"
    )

    auto_second_present_value_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present value of the co-signer's second vehicle"
    )

    auto_second_payments_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Borrower's periodic payment amount for the second auto loan"
    )

    auto_second_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Co-signer's periodic payment amount for the second auto loan"
    )

    auto_insurance_present_value_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present value or coverage amount of the borrower's auto insurance"
    )

    auto_insurance_present_value_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present value or coverage amount of the co-signer's auto insurance"
    )

    auto_insurance_payments_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Borrower's periodic auto insurance payment amount"
    )

    auto_insurance_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Co-signer's periodic auto insurance payment amount"
    )

    auto_insurance_term_1_month: BooleanLike = Field(
        default="", description="Select if the auto insurance term is 1 month"
    )

    auto_insurance_term_3_months: BooleanLike = Field(
        default="", description="Select if the auto insurance term is 3 months"
    )

    auto_insurance_term_6_months: BooleanLike = Field(
        default="", description="Select if the auto insurance term is 6 months"
    )

    auto_insurance_term_12_months: BooleanLike = Field(
        default="", description="Select if the auto insurance term is 12 months"
    )

    other_real_estate_present_value_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present value of other real estate owned by the borrower"
    )

    other_real_estate_present_value_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present value of other real estate owned by the co-signer"
    )

    other_real_estate_payments_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Borrower's periodic payment amount on other real estate debt"
    )

    other_real_estate_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Co-signer's periodic payment amount on other real estate debt"
    )

    spokane_tribal_credit_long_term_loan_present_balance_borrower: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Current balance of the borrower's Spokane Tribal Credit long term loan",
    )

    spokane_tribal_credit_long_term_loan_present_balance_co_signer: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Current balance of the co-signer's Spokane Tribal Credit long term loan",
    )

    spokane_tribal_credit_long_term_loan_payments_borrower: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Borrower's periodic payment amount on Spokane Tribal Credit long term loan",
        )
    )

    spokane_tribal_credit_long_term_loan_payments_co_signer: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Co-signer's periodic payment amount on Spokane Tribal Credit long term loan",
        )
    )

    spokane_tribal_credit_short_term_loan_present_balance_borrower: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Current balance of the borrower's Spokane Tribal Credit short term loan",
    )

    spokane_tribal_credit_short_term_loan_present_balance_co_signer: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Current balance of the co-signer's Spokane Tribal Credit short term loan",
    )

    spokane_tribal_credit_short_term_loan_payments_borrower: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Borrower's periodic payment amount on Spokane Tribal Credit short term loan",
        )
    )

    spokane_tribal_credit_short_term_loan_payments_co_signer: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Co-signer's periodic payment amount on Spokane Tribal Credit short term loan",
        )
    )

    spokane_tribal_credit_auto_repair_loan_present_balance_borrower: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Current balance of the borrower's Spokane Tribal Credit auto repair loan",
    )

    spokane_tribal_credit_auto_repair_loan_present_balance_co_signer: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Current balance of the co-signer's Spokane Tribal Credit auto repair loan",
    )

    spokane_tribal_credit_auto_repair_loan_payments_borrower: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Borrower's periodic payment amount on Spokane Tribal Credit auto repair loan",
        )
    )

    spokane_tribal_credit_auto_repair_loan_payments_co_signer: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Co-signer's periodic payment amount on Spokane Tribal Credit auto repair loan",
        )
    )

    spokane_tribal_credit_education_loan_present_balance_borrower: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Current balance of the borrower's Spokane Tribal Credit education loan",
    )

    spokane_tribal_credit_education_loan_present_balance_co_signer: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Current balance of the co-signer's Spokane Tribal Credit education loan",
    )

    spokane_tribal_credit_education_loan_payments_borrower: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Borrower's periodic payment amount on Spokane Tribal Credit education loan",
        )
    )

    spokane_tribal_credit_education_loan_payments_co_signer: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Co-signer's periodic payment amount on Spokane Tribal Credit education loan",
        )
    )

    credit_cards_other_debt_present_balance_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current balance of the borrower's credit cards and other debts"
    )

    credit_cards_other_debt_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current balance of the co-signer's credit cards and other debts"
    )

    credit_cards_other_debt_payments_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Borrower's periodic payment amount on credit cards and other debts"
    )

    credit_cards_other_debt_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Co-signer's periodic payment amount on credit cards and other debts",
    )

    alimony_child_support_present_balance_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current balance or obligation amount for the borrower's alimony/child support",
    )

    alimony_child_support_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current balance or obligation amount for the co-signer's alimony/child support",
    )

    alimony_child_support_payments_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Borrower's periodic alimony/child support payment amount"
    )

    alimony_child_support_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Co-signer's periodic alimony/child support payment amount"
    )

    total_assets_owns_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total value of all assets owned by the borrower"
    )

    total_assets_owns_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total value of all assets owned by the co-signer"
    )

    total_liabilities_present_balance_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total present balance of all liabilities for the borrower"
    )

    total_liabilities_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total present balance of all liabilities for the co-signer"
    )

    total_liabilities_payments_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total periodic payment amount for all liabilities of the borrower"
    )

    total_liabilities_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total periodic payment amount for all liabilities of the co-signer"
    )


class CustomerComments(BaseModel):
    """Additional information or explanations from the customer"""

    customer_comments: str = Field(
        default="",
        description=(
            "Additional comments or explanations from the customer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SignaturesandAuthorization(BaseModel):
    """Applicant and Co-Applicant signatures and dates authorizing credit information release"""

    applicant_signature: str = Field(
        ...,
        description=(
            "Signature of the applicant authorizing release of information .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    co_applicant_signature: str = Field(
        default="",
        description=(
            "Signature of the co-applicant authorizing release of information .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    applicant_date: str = Field(
        ..., description="Date the applicant signed the form"
    )  # YYYY-MM-DD format

    co_applicant_date: str = Field(
        default="", description="Date the co-applicant signed the form"
    )  # YYYY-MM-DD format


class PersonalFinancialStatement(BaseModel):
    """
    Personal Financial Statement

    IMPORTANT: Please complete this Personal Financial Statement. Please indicate all property owned and debts owed. Please list all assets including collateral used. If using a co-signer he/she needs to complete the following information also. Attach additional sheets if necessary.
    """

    assets_and_liabilities: AssetsandLiabilities = Field(..., description="Assets and Liabilities")
    customer_comments: CustomerComments = Field(..., description="Customer Comments")
    signatures_and_authorization: SignaturesandAuthorization = Field(
        ..., description="Signatures and Authorization"
    )
