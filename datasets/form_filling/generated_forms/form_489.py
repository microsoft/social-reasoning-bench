from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OrganizationInformation(BaseModel):
    """Basic information and contact details for the organization"""

    name_of_organization: str = Field(
        ...,
        description=(
            "Legal name of the organization applying for coverage .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_incorporation: str = Field(
        ..., description="Date the organization was legally incorporated"
    )  # YYYY-MM-DD format

    mailing_address: str = Field(
        ...,
        description=(
            "Primary mailing street address of the organization .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            "City for the organization's mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for the organization's mailing address")

    zip: str = Field(..., description="ZIP or postal code for the organization's mailing address")

    contact_person: str = Field(
        ...,
        description=(
            'Primary contact person\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            'Primary contact email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    web_site: str = Field(
        default="",
        description=(
            'Organization\'s website URL .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    fax_no: str = Field(
        default="",
        description=(
            'Organization\'s fax number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    complete_description_of_your_operations_and_events: str = Field(
        ...,
        description=(
            "Detailed description of the organization's operations and events .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    number_of_full_time_compensated_employees_over_30_hours_a_week_for_12_months: Union[
        float, Literal["N/A", ""]
    ] = Field(
        ...,
        description=(
            "Total count of full-time compensated employees working over 30 hours per week "
            "for 12 months"
        ),
    )

    number_of_part_time_compensated_employees_under_30_hours_a_week_or_less_than_12_months: Union[
        float, Literal["N/A", ""]
    ] = Field(
        ...,
        description=(
            "Total count of part-time compensated employees working under 30 hours per week "
            "or less than 12 months"
        ),
    )

    number_of_volunteers: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of volunteers"
    )

    is_the_organization_a_not_for_profit_entity_yes: BooleanLike = Field(
        ..., description="Indicate Yes if the organization is a not-for-profit entity"
    )

    is_the_organization_a_not_for_profit_entity_no: BooleanLike = Field(
        ..., description="Indicate No if the organization is not a not-for-profit entity"
    )

    tax_id_no: str = Field(
        ...,
        description=(
            "Organization's tax identification number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class FinancialInformation(BaseModel):
    """Financial details of the organization"""

    total_organizations_annual_gross_revenue: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Total annual gross revenue including all receipts from fees, sponsorships, "
            "fundraisers, membership, and ticket sales"
        ),
    )

    total_organizations_assets_on_the_financial_statement: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total assets as reported on the organization's financial statement"
    )

    total_organizations_liabilities_on_the_financial_statement: Union[float, Literal["N/A", ""]] = (
        Field(
            ...,
            description="Total liabilities as reported on the organization's financial statement",
        )
    )


class CurrentCoverageandEffectiveDate(BaseModel):
    """Existing D&O coverage details and requested effective date"""

    does_the_organization_currently_have_do_coverage_in_force_no: BooleanLike = Field(
        ..., description="Indicate No if there is no current D&O coverage in force"
    )

    does_the_organization_currently_have_do_coverage_in_force_yes: BooleanLike = Field(
        ..., description="Indicate Yes if there is current D&O coverage in force"
    )

    carrier: str = Field(
        default="",
        description=(
            "Name of the current D&O insurance carrier .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    limit: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Coverage limit of the current D&O policy"
    )

    premium: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Annual premium of the current D&O policy"
    )

    retention: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Retention or deductible amount on the current D&O policy"
    )

    exp_date: str = Field(
        default="", description="Expiration date of the current D&O policy"
    )  # YYYY-MM-DD format

    desired_effective_date_start_my_coverage_on_the_date_my_enrollment_form_and_payment_are_received: BooleanLike = Field(
        ...,
        description=(
            "Select this option to have coverage start when the enrollment form and payment "
            "are received"
        ),
    )

    desired_effective_date_start_my_coverage_on_this_date: str = Field(
        default="", description="Specific requested effective date for coverage"
    )  # YYYY-MM-DD format


class PastActivities(BaseModel):
    """Prior claims and known circumstances that may lead to claims"""

    past_activities_explanation_of_claims_include_loss_payment_and_defense_costs: str = Field(
        default="",
        description=(
            "If any past claims exist, provide full details including loss payments and "
            'defense costs .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    if_none_check_here_claims_made_against_any_person_or_entity_proposed_for_this_insurance: BooleanLike = Field(
        default="",
        description=(
            "Check if there have been no past claims that would fall within the scope of "
            "the proposed insurance"
        ),
    )

    explanation_of_any_fact_circumstance_or_situation_which_might_afford_grounds_for_any_claim: str = Field(
        default="",
        description=(
            "Describe any known facts, circumstances, or situations that might give rise to "
            'a claim .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    if_none_check_here_any_fact_circumstance_or_situation_which_might_afford_grounds_for_any_claim: BooleanLike = Field(
        default="",
        description=(
            "Check if there are no known facts, circumstances, or situations that might "
            "give rise to a claim"
        ),
    )


class DAndOInsuranceAppForNonProfitEntitiesForm(BaseModel):
    """
        DIRECTORS' AND OFFICERS'
    including Employment Practices
    Liability Insurance Application
    For Not-For-Profit Entities Enrollment Form

        Notice: The policy for which this enrollment form is made applies, subject to its terms, only to any Claim first made against the Insureds during the certificate coverage period. This form must be completed and returned with your payment. The submission of this enrollment form does not guarantee coverage. Completion of this enrollment form confirms your desire to obtain insurance through the Sports, Leisure and Entertainment Risk Purchasing Group. An RPG provides group purchasing power for similar risks resulting in potential advantageous coverage terms, competitive rates, risk management bulletins, and rewards for favorable group loss experience. An RPG administration fee may be charged. The expiration date is one full year from the effective date. Read the entire brochure and enrollment form carefully before signing. This is a claims-made coverage.
    """

    organization_information: OrganizationInformation = Field(
        ..., description="Organization Information"
    )
    financial_information: FinancialInformation = Field(..., description="Financial Information")
    current_coverage_and_effective_date: CurrentCoverageandEffectiveDate = Field(
        ..., description="Current Coverage and Effective Date"
    )
    past_activities: PastActivities = Field(..., description="Past Activities")
