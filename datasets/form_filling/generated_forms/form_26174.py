from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PolicyDetails(BaseModel):
    """Basic policy and professional services information"""

    insured_name: str = Field(
        ...,
        description=(
            "Full legal name of the insured entity or individual .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    policy_number: str = Field(
        ...,
        description=(
            "Current professional indemnity policy number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    expiry_date: str = Field(
        ..., description="Expiry date of the current policy"
    )  # YYYY-MM-DD format

    professional_services_covered: str = Field(
        ...,
        description=(
            "Description of the professional services currently covered by the policy .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    details_of_changes_to_professional_services: str = Field(
        default="",
        description=(
            "If professional services have changed from those currently insured, provide "
            'full details .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class FeeIncome(BaseModel):
    """Fee income amounts and state/territory breakdown for stamp duty"""

    last_years_disclosed_fees: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total fee income disclosed for the last financial year (in dollars)"
    )

    gross_fee_income_earned_in_the_last_12_months: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total gross fee income earned in the last 12 months (in dollars)"
    )

    nsw_percentage_of_gross_income_fees_in_last_12_months: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Percentage of total gross income/fees earned in New South Wales in the last 12 months"
        ),
    )

    vic_percentage_of_gross_income_fees_in_last_12_months: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Percentage of total gross income/fees earned in Victoria in the last 12 months",
    )

    qld_percentage_of_gross_income_fees_in_last_12_months: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Percentage of total gross income/fees earned in Queensland in the last 12 months"
        ),
    )

    sa_percentage_of_gross_income_fees_in_last_12_months: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Percentage of total gross income/fees earned in South Australia in the last 12 months"
        ),
    )

    wa_percentage_of_gross_income_fees_in_last_12_months: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Percentage of total gross income/fees earned in Western Australia in the last "
            "12 months"
        ),
    )

    tas_percentage_of_gross_income_fees_in_last_12_months: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Percentage of total gross income/fees earned in Tasmania in the last 12 months",
    )

    act_percentage_of_gross_income_fees_in_last_12_months: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Percentage of total gross income/fees earned in Australian Capital Territory "
            "in the last 12 months"
        ),
    )

    nt_percentage_of_gross_income_fees_in_last_12_months: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Percentage of total gross income/fees earned in Northern Territory in the last "
            "12 months"
        ),
    )

    overseas_percentage_of_gross_income_fees_in_last_12_months: Union[float, Literal["N/A", ""]] = (
        Field(
            ...,
            description=(
                "Percentage of total gross income/fees earned outside Australia in the last 12 "
                "months"
            ),
        )
    )

    total_percentage_of_gross_income_fees_in_last_12_months: Union[float, Literal["N/A", ""]] = (
        Field(..., description="Total of all stated percentages (should equal 100%)")
    )


class ClaimsandCircumstances(BaseModel):
    """Claims history and disciplinary matters"""

    have_any_claims_been_made_or_have_there_been_any_circumstances_that_might_give_rise_to_a_claim_that_have_not_yet_been_reported: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether there are any unreported claims or circumstances that might "
            "give rise to a claim"
        ),
    )

    has_any_principal_partner_director_or_employee_been_subject_to_any_disciplinary_action_been_fined_or_penalised_or_been_the_subject_of_an_inquiry_investigating_or_alleging_professional_misconduct: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether any principal, partner, director or employee has faced "
            "disciplinary or misconduct proceedings"
        ),
    )


class PolicyLimit(BaseModel):
    """Existing and requested policy limits"""

    existing_policy_limit: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Current limit of indemnity under the existing policy (in dollars)"
    )

    alternative_limit_request: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Alternative limit of indemnity requested (in dollars), if different from existing"
        ),
    )


class PolicyExcess(BaseModel):
    """Existing and requested policy excess"""

    existing_policy_excess: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Current policy excess/deductible amount (in dollars)"
    )

    alternative_excess_request: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Alternative excess/deductible amount requested (in dollars), if different from "
            "existing"
        ),
    )


class Declaration(BaseModel):
    """Signatory details for the declaration"""

    name: str = Field(
        ...,
        description=(
            "Name of the person making the declaration .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    signed: str = Field(
        ...,
        description=(
            "Signature of the authorised person making the declaration .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_day: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day of signing the declaration"
    )

    date_month: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month of signing the declaration"
    )

    date_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year of signing the declaration"
    )


class ProfessionalServicesCovered(BaseModel):
    """
    Professional Services Covered

    ''
    """

    policy_details: PolicyDetails = Field(..., description="Policy Details")
    fee_income: FeeIncome = Field(..., description="Fee Income")
    claims_and_circumstances: ClaimsandCircumstances = Field(
        ..., description="Claims and Circumstances"
    )
    policy_limit: PolicyLimit = Field(..., description="Policy Limit")
    policy_excess: PolicyExcess = Field(..., description="Policy Excess")
    declaration: Declaration = Field(..., description="Declaration")
