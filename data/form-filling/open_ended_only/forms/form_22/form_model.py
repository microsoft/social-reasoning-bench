from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PersonalInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the borrower and co-signer"""

    borrower: str = Field(
        ...,
        description=(
            "Name of the borrower completing the form .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    co_signer: str = Field(
        ...,
        description=(
            "Name of the co-signer, if applicable .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class Assets(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Assets owned by the borrower and co-signer"""

    home_present_value: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current market value of the home owned"
    )

    home_insurance_present_value: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current value of home insurance policy"
    )

    auto_year_make_and_model_present_value: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current value of the auto (year, make, and model)"
    )

    auto_year_make_and_model_present_value_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current value of the second auto (year, make, and model)"
    )

    auto_insurance_present_value: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current value of auto insurance policy"
    )

    other_real_estate_present_value: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current value of other real estate owned"
    )

    assets_owns_total: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Total value of all assets owned"
    )


class Liabilities(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Liabilities and debts owed by the borrower and co-signer"""

    home_rent_or_mortgage_payments: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly rent or mortgage payment amount for the home"
    )

    home_rent_or_mortgage_present_balance: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on rent or mortgage for the home"
    )

    home_rent_or_mortgage_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly rent or mortgage payment amount for the co-signer's home"
    )

    home_rent_or_mortgage_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on rent or mortgage for the co-signer's home"
    )

    home_to_whom: str = Field(
        ...,
        description=(
            "Name of the lender or landlord for the home .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    home_to_whom_co_signer: str = Field(
        ...,
        description=(
            "Name of the lender or landlord for the co-signer's home .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    home_insurance_payments: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for home insurance"
    )

    home_insurance_present_balance: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on home insurance"
    )

    home_insurance_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for co-signer's home insurance"
    )

    home_insurance_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on co-signer's home insurance"
    )

    auto_year_make_and_model_payments: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for the auto"
    )

    auto_year_make_and_model_present_balance: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on the auto"
    )

    auto_year_make_and_model_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for co-signer's auto"
    )

    auto_year_make_and_model_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on co-signer's auto"
    )

    auto_year_make_and_model_payments_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for the second auto"
    )

    auto_year_make_and_model_present_balance_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on the second auto"
    )

    auto_year_make_and_model_payments_co_signer_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for co-signer's second auto"
    )

    auto_year_make_and_model_present_balance_co_signer_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on co-signer's second auto"
    )

    auto_insurance_payments: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for auto insurance"
    )

    auto_insurance_present_balance: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on auto insurance"
    )

    auto_insurance_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for co-signer's auto insurance"
    )

    auto_insurance_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on co-signer's auto insurance"
    )

    auto_insurance_pick_one: Literal["1 month", "3 months", "6 months", "12 months", "N/A", ""] = Field(
        ...,
        description="Select the auto insurance payment period"
    )

    other_real_estate_payments: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for other real estate"
    )

    other_real_estate_present_balance: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on other real estate"
    )

    other_real_estate_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for co-signer's other real estate"
    )

    other_real_estate_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on co-signer's other real estate"
    )

    spokane_tribal_credit_long_term_loan_payments: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for Spokane Tribal Credit long term loan"
    )

    spokane_tribal_credit_long_term_loan_present_balance: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on Spokane Tribal Credit long term loan"
    )

    spokane_tribal_credit_long_term_loan_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for co-signer's Spokane Tribal Credit long term loan"
    )

    spokane_tribal_credit_long_term_loan_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on co-signer's Spokane Tribal Credit long term loan"
    )

    spokane_tribal_credit_short_term_loan_payments: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for Spokane Tribal Credit short term loan"
    )

    spokane_tribal_credit_short_term_loan_present_balance: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on Spokane Tribal Credit short term loan"
    )

    spokane_tribal_credit_short_term_loan_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for co-signer's Spokane Tribal Credit short term loan"
    )

    spokane_tribal_credit_short_term_loan_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on co-signer's Spokane Tribal Credit short term loan"
    )

    spokane_tribal_credit_auto_repair_loan_payments: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for Spokane Tribal Credit auto repair loan"
    )

    spokane_tribal_credit_auto_repair_loan_present_balance: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on Spokane Tribal Credit auto repair loan"
    )

    spokane_tribal_credit_auto_repair_loan_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for co-signer's Spokane Tribal Credit auto repair loan"
    )

    spokane_tribal_credit_auto_repair_loan_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on co-signer's Spokane Tribal Credit auto repair loan"
    )

    spokane_tribal_credit_education_loan_payments: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for Spokane Tribal Credit education loan"
    )

    spokane_tribal_credit_education_loan_present_balance: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on Spokane Tribal Credit education loan"
    )

    spokane_tribal_credit_education_loan_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for co-signer's Spokane Tribal Credit education loan"
    )

    spokane_tribal_credit_education_loan_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on co-signer's Spokane Tribal Credit education loan"
    )

    credit_cards_other_debt_payments: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for credit cards or other debts"
    )

    credit_cards_other_debt_present_balance: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on credit cards or other debts"
    )

    credit_cards_other_debt_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for co-signer's credit cards or other debts"
    )

    credit_cards_other_debt_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed on co-signer's credit cards or other debts"
    )

    alimony_child_support_payments: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for alimony or child support"
    )

    alimony_child_support_present_balance: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed for alimony or child support"
    )

    alimony_child_support_payments_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Monthly payment amount for co-signer's alimony or child support"
    )

    alimony_child_support_present_balance_co_signer: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Current balance owed for co-signer's alimony or child support"
    )

    liabilities_total: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Total value of all liabilities owed"
    )


class CustomerComments(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Additional comments from the customer"""

    customer_comments: str = Field(
        ...,
        description=(
            "Additional comments from the customer .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class Signatures(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Applicant and co-applicant signatures and dates"""

    applicant_signature: str = Field(
        ...,
        description=(
            "Signature of the applicant .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    applicant_date: str = Field(
        ...,
        description="Date of applicant's signature"
    )  # YYYY-MM-DD format

    co_applicant_signature: str = Field(
        ...,
        description=(
            "Signature of the co-applicant .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    co_applicant_date: str = Field(
        ...,
        description="Date of co-applicant's signature"
    )  # YYYY-MM-DD format


class PersonalFinancialStatement(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    Personal Financial Statement

    IMPORTANT: Please complete this Personal Financial Statement. Please indicate all property owned and debts owed. Please list all assets including collateral used. If using a co-signer he/she needs to complete the following information also. Attach additional sheets if necessary.
    I/We hereby authorize anyone to release income/credit information concerning myself/ourselves to Spokane Tribal Credit. This authorization is given to enable STC to evaluate my/our request for credit. I/We certify that all statements are true and complete and are submitted for the purpose of obtaining credit. Verification will be obtained from any source named in the application and from any credit-reporting agency. I agree that the application shall remain STC property whether it is approved or not approved.
    """

    personal_information: PersonalInformation = Field(
        ...,
        description="Personal Information"
    )
    assets: Assets = Field(
        ...,
        description="Assets"
    )
    liabilities: Liabilities = Field(
        ...,
        description="Liabilities"
    )
    customer_comments: CustomerComments = Field(
        ...,
        description="Customer Comments"
    )
    signatures: Signatures = Field(
        ...,
        description="Signatures"
    )