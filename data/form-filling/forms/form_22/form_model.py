from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Assets(BaseModel):
    """Present value of assets owned by the borrower and co-signer"""

    home_present_value: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present market value of the home you own"
    )

    auto_year_make_and_model_present_value_first_auto: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Present market value of the first automobile listed (year, make, and model shown)"
        ),
    )

    auto_year_make_and_model_present_value_second_auto: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Present market value of the second automobile listed (year, make, and model shown)"
        ),
    )

    assets_owns_total: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total value of all assets owned"
    )


class Liabilities(BaseModel):
    """Liabilities with borrower and co-signer payments and balances"""

    rent_or_mortgage_to_whom: str = Field(
        default="",
        description=(
            "Name of landlord or mortgage company to whom rent or mortgage is paid .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    rent_or_mortgage_borrower_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Borrower's regular rent or mortgage payment amount"
    )

    rent_or_mortgage_borrower_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current outstanding balance on the borrower's rent or mortgage obligation",
    )

    rent_or_mortgage_co_signer_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Co-signer's regular rent or mortgage payment amount"
    )

    rent_or_mortgage_co_signer_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current outstanding balance on the co-signer's rent or mortgage obligation",
    )

    home_insurance_borrower_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Borrower's regular home insurance payment amount"
    )

    home_insurance_borrower_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Current outstanding balance owed by the borrower for home insurance, if applicable"
        ),
    )

    home_insurance_co_signer_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Co-signer's regular home insurance payment amount"
    )

    home_insurance_co_signer_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Current outstanding balance owed by the co-signer for home insurance, if applicable"
        ),
    )

    auto_first_borrower_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Borrower's regular payment amount for the first auto loan"
    )

    auto_first_borrower_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current outstanding balance on the borrower's first auto loan"
    )

    auto_first_co_signer_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Co-signer's regular payment amount for the first auto loan"
    )

    auto_first_co_signer_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current outstanding balance on the co-signer's first auto loan"
    )

    auto_second_borrower_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Borrower's regular payment amount for the second auto loan"
    )

    auto_second_borrower_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current outstanding balance on the borrower's second auto loan"
    )

    auto_second_co_signer_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Co-signer's regular payment amount for the second auto loan"
    )

    auto_second_co_signer_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current outstanding balance on the co-signer's second auto loan"
    )

    auto_insurance_term_pick_one_1_3_6_12_months: Literal[
        "1 month", "3 months", "6 months", "12 months", "N/A", ""
    ] = Field(default="", description="Selected billing term for auto insurance payments")

    auto_insurance_borrower_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Borrower's regular auto insurance payment amount"
    )

    auto_insurance_borrower_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Current outstanding balance owed by the borrower for auto insurance, if applicable"
        ),
    )

    auto_insurance_co_signer_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Co-signer's regular auto insurance payment amount"
    )

    auto_insurance_co_signer_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Current outstanding balance owed by the co-signer for auto insurance, if applicable"
        ),
    )

    other_real_estate_borrower_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Borrower's regular payment amount for other real estate loans"
    )

    other_real_estate_borrower_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current outstanding balance on the borrower's other real estate loans",
    )

    other_real_estate_co_signer_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Co-signer's regular payment amount for other real estate loans"
    )

    other_real_estate_co_signer_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current outstanding balance on the co-signer's other real estate loans",
    )

    spokane_tribal_credit_long_term_loan_borrower_payments: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Borrower's regular payment amount for Spokane Tribal Credit long term loan",
        )
    )

    spokane_tribal_credit_long_term_loan_borrower_present_balance: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Current outstanding balance on the borrower's Spokane Tribal Credit long term loan"
        ),
    )

    spokane_tribal_credit_long_term_loan_co_signer_payments: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Co-signer's regular payment amount for Spokane Tribal Credit long term loan",
        )
    )

    spokane_tribal_credit_long_term_loan_co_signer_present_balance: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Current outstanding balance on the co-signer's Spokane Tribal Credit long term loan"
        ),
    )

    spokane_tribal_credit_short_term_loan_borrower_payments: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Borrower's regular payment amount for Spokane Tribal Credit short term loan",
        )
    )

    spokane_tribal_credit_short_term_loan_borrower_present_balance: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Current outstanding balance on the borrower's Spokane Tribal Credit short term loan"
        ),
    )

    spokane_tribal_credit_short_term_loan_co_signer_payments: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Co-signer's regular payment amount for Spokane Tribal Credit short term loan",
        )
    )

    spokane_tribal_credit_short_term_loan_co_signer_present_balance: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Current outstanding balance on the co-signer's Spokane Tribal Credit short term loan"
        ),
    )

    spokane_tribal_credit_auto_repair_loan_borrower_payments: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Borrower's regular payment amount for Spokane Tribal Credit auto repair loan",
        )
    )

    spokane_tribal_credit_auto_repair_loan_borrower_present_balance: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Current outstanding balance on the borrower's Spokane Tribal Credit auto repair loan"
        ),
    )

    spokane_tribal_credit_auto_repair_loan_co_signer_payments: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Co-signer's regular payment amount for Spokane Tribal Credit auto repair loan",
        )
    )

    spokane_tribal_credit_auto_repair_loan_co_signer_present_balance: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Current outstanding balance on the co-signer's Spokane Tribal Credit auto repair loan"
        ),
    )

    spokane_tribal_credit_education_loan_borrower_payments: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Borrower's regular payment amount for Spokane Tribal Credit education loan",
        )
    )

    spokane_tribal_credit_education_loan_borrower_present_balance: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Current outstanding balance on the borrower's Spokane Tribal Credit education loan"
        ),
    )

    spokane_tribal_credit_education_loan_co_signer_payments: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Co-signer's regular payment amount for Spokane Tribal Credit education loan",
        )
    )

    spokane_tribal_credit_education_loan_co_signer_present_balance: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Current outstanding balance on the co-signer's Spokane Tribal Credit education loan"
        ),
    )

    credit_cards_other_debt_borrower_payments: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Borrower's total regular payment amount for credit cards and other debts",
    )

    credit_cards_other_debt_borrower_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Current total outstanding balance on the borrower's credit cards and other debts"
        ),
    )

    credit_cards_other_debt_co_signer_payments: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Co-signer's total regular payment amount for credit cards and other debts",
    )

    credit_cards_other_debt_co_signer_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Current total outstanding balance on the co-signer's credit cards and other debts"
        ),
    )

    alimony_child_support_borrower_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Borrower's regular alimony and/or child support payment amount"
    )

    alimony_child_support_borrower_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Current outstanding balance or arrears on the borrower's alimony/child support "
            "obligations, if applicable"
        ),
    )

    alimony_child_support_co_signer_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Co-signer's regular alimony and/or child support payment amount"
    )

    alimony_child_support_co_signer_present_balance: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Current outstanding balance or arrears on the co-signer's alimony/child "
            "support obligations, if applicable"
        ),
    )

    liabilities_total: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total of all liabilities and debts listed"
    )


class CustomerComments(BaseModel):
    """Additional information or explanations from the customer"""

    customer_comments: str = Field(
        default="",
        description=(
            "Additional information or explanations the customer wishes to provide .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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

    applicant_date: str = Field(
        ..., description="Date the applicant signed the form"
    )  # YYYY-MM-DD format

    co_applicant_signature: str = Field(
        default="",
        description=(
            'Signature of the co-applicant, if any .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    co_applicant_date: str = Field(
        default="", description="Date the co-applicant signed the form"
    )  # YYYY-MM-DD format


class PersonalFinancialStatement(BaseModel):
    """
    Personal Financial Statement

    IMPORTANT: Please complete this Personal Financial Statement. Please indicate all property owned and debts owed. Please list all assets including collateral used. If using a co-signer he/she needs to complete the following information also. Attach additional sheets if necessary.
    """

    assets: Assets = Field(..., description="Assets")
    liabilities: Liabilities = Field(..., description="Liabilities")
    customer_comments: CustomerComments = Field(..., description="Customer Comments")
    signatures_and_authorization: SignaturesandAuthorization = Field(
        ..., description="Signatures and Authorization"
    )
