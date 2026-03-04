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
    """Assets owned and liabilities owed for borrower and co-signer"""

    borrower: str = Field(
        ...,
        description=(
            'Name of the primary borrower .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    co_signer: str = Field(
        default="",
        description=(
            'Name of the co-signer, if any .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    home_present_value: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current market value of the home owned"
    )

    home_payments_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current outstanding loan balance on the home"
    )

    home_payments_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current monthly payment amount for the home loan"
    )

    rent_or_mortgage_payments_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Outstanding balance on rent or mortgage obligations, if applicable"
    )

    rent_or_mortgage_payments_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current monthly rent or mortgage payment amount"
    )

    rent_or_mortgage_to_whom: str = Field(
        default="",
        description=(
            "Name of landlord or mortgage company to whom payments are made .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    home_insurance_payments_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Outstanding balance due on home insurance, if any"
    )

    home_insurance_payments_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current periodic payment amount for home insurance"
    )

    auto_year_make_and_model_present_value: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current market value of the first vehicle listed (year, make, and model)",
    )

    auto_payments_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Outstanding loan balance on the first vehicle"
    )

    auto_payments_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current monthly payment amount for the first vehicle loan"
    )

    auto_second_year_make_and_model_present_value: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current market value of the second vehicle listed (year, make, and model)",
    )

    auto_second_payments_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Outstanding loan balance on the second vehicle"
    )

    auto_second_payments_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current monthly payment amount for the second vehicle loan"
    )

    auto_insurance_payments_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Outstanding balance due on auto insurance, if any"
    )

    auto_insurance_payments_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current periodic payment amount for auto insurance"
    )

    auto_insurance_pick_one_1_month: BooleanLike = Field(
        default="", description="Select if auto insurance is paid every 1 month"
    )

    auto_insurance_pick_one_3_months: BooleanLike = Field(
        default="", description="Select if auto insurance is paid every 3 months"
    )

    auto_insurance_pick_one_6_months: BooleanLike = Field(
        default="", description="Select if auto insurance is paid every 6 months"
    )

    auto_insurance_pick_one_12_months: BooleanLike = Field(
        default="", description="Select if auto insurance is paid every 12 months"
    )

    other_real_estate_present_value: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current market value of other real estate owned"
    )

    other_real_estate_payments_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Outstanding loan balance on other real estate"
    )

    other_real_estate_payments_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current monthly payment amount for other real estate loans"
    )

    spokane_tribal_credit_long_term_loan_payments_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Outstanding balance on Spokane Tribal Credit long term loan"
    )

    spokane_tribal_credit_long_term_loan_payments_present_balance: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Current periodic payment amount for Spokane Tribal Credit long term loan",
    )

    spokane_tribal_credit_short_term_loan_payments_balance: Union[float, Literal["N/A", ""]] = (
        Field(
            default="", description="Outstanding balance on Spokane Tribal Credit short term loan"
        )
    )

    spokane_tribal_credit_short_term_loan_payments_present_balance: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Current periodic payment amount for Spokane Tribal Credit short term loan",
    )

    spokane_tribal_credit_auto_repair_loan_payments_balance: Union[float, Literal["N/A", ""]] = (
        Field(
            default="", description="Outstanding balance on Spokane Tribal Credit auto repair loan"
        )
    )

    spokane_tribal_credit_auto_repair_loan_payments_present_balance: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Current periodic payment amount for Spokane Tribal Credit auto repair loan",
    )

    spokane_tribal_credit_education_loan_payments_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Outstanding balance on Spokane Tribal Credit education loan"
    )

    spokane_tribal_credit_education_loan_payments_present_balance: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Current periodic payment amount for Spokane Tribal Credit education loan",
    )

    credit_cards_other_debt_payments_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total outstanding balance on credit cards and other debts"
    )

    credit_cards_other_debt_payments_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current total monthly payment amount for credit cards and other debts",
    )

    alimony_child_support_payments_balance: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Outstanding balance or obligation amount for alimony/child support, if applicable"
        ),
    )

    alimony_child_support_payments_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current periodic payment amount for alimony/child support"
    )

    total_assets_owns_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total value of all assets owned by the borrower"
    )

    total_liabilities_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total amount of all liabilities owed by the borrower"
    )

    total_assets_owns_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total value of all assets owned by the co-signer"
    )

    total_liabilities_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total amount of all liabilities owed by the co-signer"
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
    """Applicant and co-applicant signatures and dates authorizing credit information release"""

    applicant_signature: str = Field(
        ...,
        description=(
            'Signature of the applicant .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    applicant_date: str = Field(..., description="Date the applicant signed")  # YYYY-MM-DD format

    co_applicant_signature: str = Field(
        default="",
        description=(
            'Signature of the co-applicant, if any .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    co_applicant_date: str = Field(
        default="", description="Date the co-applicant signed"
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
