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
    """Assets owned and corresponding liabilities for borrower and co-signer"""

    home_present_value: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present market value of the home you own"
    )

    rent_or_mortgage_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Regular rent or mortgage payment amount"
    )

    rent_or_mortgage_present_balance_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current mortgage balance owed by the borrower"
    )

    rent_or_mortgage_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current mortgage balance owed by the co-signer"
    )

    home_insurance_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Regular home insurance payment amount"
    )

    home_insurance_present_balance_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current home insurance balance owed by the borrower, if applicable"
    )

    home_insurance_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current home insurance balance owed by the co-signer, if applicable",
    )

    auto_year_make_model_present_value: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present value of the listed vehicle (year, make, and model)"
    )

    auto_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Regular auto loan payment amount for this vehicle"
    )

    auto_present_balance_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current auto loan balance owed by the borrower for this vehicle"
    )

    auto_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current auto loan balance owed by the co-signer for this vehicle"
    )

    auto_2_year_make_model_present_value: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present value of the second listed vehicle (year, make, and model)"
    )

    auto_2_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Regular auto loan payment amount for the second vehicle"
    )

    auto_2_present_balance_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current auto loan balance owed by the borrower for the second vehicle",
    )

    auto_2_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current auto loan balance owed by the co-signer for the second vehicle",
    )

    auto_insurance_term: Literal["1", "3", "6", "12", "N/A", ""] = Field(
        default="", description="Selected auto insurance payment term in months"
    )

    auto_insurance_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Regular auto insurance payment amount"
    )

    auto_insurance_present_balance_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current auto insurance balance owed by the borrower, if applicable"
    )

    auto_insurance_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current auto insurance balance owed by the co-signer, if applicable",
    )

    other_real_estate_present_value: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present value of other real estate owned"
    )

    other_real_estate_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Regular payment amount on other real estate debt"
    )

    other_real_estate_present_balance_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current balance owed by the borrower on other real estate"
    )

    other_real_estate_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current balance owed by the co-signer on other real estate"
    )

    other_real_estate_description: str = Field(
        default="",
        description=(
            "Description or address of other real estate .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    spokane_tribal_credit_long_term_loan_present_value: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Present value or amount of the Spokane Tribal Credit long term loan",
    )

    spokane_tribal_credit_long_term_loan_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Regular payment amount on the Spokane Tribal Credit long term loan"
    )

    spokane_tribal_credit_long_term_loan_present_balance_borrower: Union[
        float, Literal["N/A", ""]
    ] = Field(default="", description="Current balance owed by the borrower on the long term loan")

    spokane_tribal_credit_long_term_loan_present_balance_co_signer: Union[
        float, Literal["N/A", ""]
    ] = Field(default="", description="Current balance owed by the co-signer on the long term loan")

    spokane_tribal_credit_short_term_loan_present_value: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Present value or amount of the Spokane Tribal Credit short term loan",
    )

    spokane_tribal_credit_short_term_loan_payments: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Regular payment amount on the Spokane Tribal Credit short term loan",
    )

    spokane_tribal_credit_short_term_loan_present_balance_borrower: Union[
        float, Literal["N/A", ""]
    ] = Field(default="", description="Current balance owed by the borrower on the short term loan")

    spokane_tribal_credit_short_term_loan_present_balance_co_signer: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="", description="Current balance owed by the co-signer on the short term loan"
    )

    spokane_tribal_credit_auto_repair_loan_present_value: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Present value or amount of the Spokane Tribal Credit auto repair loan",
    )

    spokane_tribal_credit_auto_repair_loan_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Regular payment amount on the auto repair loan"
    )

    spokane_tribal_credit_auto_repair_loan_present_balance_borrower: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="", description="Current balance owed by the borrower on the auto repair loan"
    )

    spokane_tribal_credit_auto_repair_loan_present_balance_co_signer: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="", description="Current balance owed by the co-signer on the auto repair loan"
    )

    spokane_tribal_credit_education_loan_present_value: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Present value or amount of the Spokane Tribal Credit education loan",
    )

    spokane_tribal_credit_education_loan_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Regular payment amount on the education loan"
    )

    spokane_tribal_credit_education_loan_present_balance_borrower: Union[
        float, Literal["N/A", ""]
    ] = Field(default="", description="Current balance owed by the borrower on the education loan")

    spokane_tribal_credit_education_loan_present_balance_co_signer: Union[
        float, Literal["N/A", ""]
    ] = Field(default="", description="Current balance owed by the co-signer on the education loan")

    education_loan_description: str = Field(
        default="",
        description=(
            "Description or details of the education loan .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    credit_cards_other_debt_present_value: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total present amount or credit limit for credit cards/other debt"
    )

    credit_cards_other_debt_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total regular payment amount for credit cards/other debt"
    )

    credit_cards_other_debt_present_balance_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current balance owed by the borrower on credit cards/other debt"
    )

    credit_cards_other_debt_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current balance owed by the co-signer on credit cards/other debt"
    )

    credit_cards_other_debt_description_line_1: str = Field(
        default="",
        description=(
            "First line of description for credit cards or other debts .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    credit_cards_other_debt_description_line_2: str = Field(
        default="",
        description=(
            "Second line of description for credit cards or other debts .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    credit_cards_other_debt_description_line_3: str = Field(
        default="",
        description=(
            "Third line of description for credit cards or other debts .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    alimony_child_support_present_value: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Present amount or obligation related to alimony/child support"
    )

    alimony_child_support_payments: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Regular payment amount for alimony/child support"
    )

    alimony_child_support_present_balance_borrower: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current balance or arrears owed by the borrower for alimony/child support",
    )

    alimony_child_support_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current balance or arrears owed by the co-signer for alimony/child support",
    )

    alimony_child_support_description: str = Field(
        default="",
        description=(
            "Description or details of alimony/child support obligations .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    total_assets: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total value of all listed assets"
    )

    total_liabilities: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total amount of all listed liabilities"
    )

    additional_total_comments_line: str = Field(
        default="",
        description=(
            "Additional notes or clarification related to totals .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CustomerComments(BaseModel):
    """Additional comments from the customer"""

    customer_comments_line_1: str = Field(
        default="",
        description=(
            'First line for customer comments .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    customer_comments_line_2: str = Field(
        default="",
        description=(
            'Second line for customer comments .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    customer_comments_line_3: str = Field(
        default="",
        description=(
            'Third line for customer comments .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    customer_comments_line_4: str = Field(
        default="",
        description=(
            'Fourth line for customer comments .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    customer_comments_line_5: str = Field(
        default="",
        description=(
            'Fifth line for customer comments .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class AuthorizationandSignatures(BaseModel):
    """Applicant and co-applicant signatures and dates"""

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
        ..., description="Date the applicant signed this statement"
    )  # YYYY-MM-DD format

    co_applicant_date: str = Field(
        default="", description="Date the co-applicant signed this statement"
    )  # YYYY-MM-DD format


class PersonalFinancialStatement(BaseModel):
    """
    Personal Financial Statement

    IMPORTANT: Please complete this Personal Financial Statement. Please indicate all property owned and debts owed. Please list all assets including collateral used. If using a co-signer he/she needs to complete the following information also. Attach additional sheets if necessary.
    """

    assets_and_liabilities: AssetsandLiabilities = Field(..., description="Assets and Liabilities")
    customer_comments: CustomerComments = Field(..., description="Customer Comments")
    authorization_and_signatures: AuthorizationandSignatures = Field(
        ..., description="Authorization and Signatures"
    )
