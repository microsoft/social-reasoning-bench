from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EmployerInformation(BaseModel):
    """Basic employer identity and contact details"""

    legal_employer_name: str = Field(
        ...,
        description=(
            "Full legal name of the employer entity .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    employer_federal_ein: str = Field(
        ...,
        description=(
            "Employer’s Federal Employer Identification Number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    state_incorporated: str = Field(..., description="State in which the employer is incorporated")

    street_address: str = Field(
        ...,
        description=(
            "Street address of the employer’s main location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the employer’s address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of the employer’s address")

    zip: str = Field(..., description="ZIP code of the employer’s address")

    contact_name: str = Field(
        ...,
        description=(
            "Primary contact person for this application .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Email address for the primary contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        ...,
        description=(
            'Phone number for the primary contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class EmployerType(BaseModel):
    """Business/entity type classification"""

    c_corp: BooleanLike = Field(
        default="", description="Check if the employer is organized as a C Corporation"
    )

    s_corp: BooleanLike = Field(
        default="", description="Check if the employer is organized as an S Corporation"
    )

    partnership_llp: BooleanLike = Field(
        default="", description="Check if the employer is a Partnership or LLP"
    )

    sole_proprietor: BooleanLike = Field(
        default="", description="Check if the employer is a sole proprietorship"
    )

    non_profit: str = Field(
        default="",
        description=(
            "Check if the employer is a non-profit and specify details if needed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    church: BooleanLike = Field(default="", description="Check if the employer is a church")

    government: BooleanLike = Field(
        default="", description="Check if the employer is a government entity"
    )

    school_public: BooleanLike = Field(
        default="", description="Check if the employer is a public school"
    )

    school_private: BooleanLike = Field(
        default="", description="Check if the employer is a private school"
    )

    psc_must_note_if_file_as_a_c_or_s: str = Field(
        default="",
        description=(
            "Check if the employer is a Personal Service Corporation and note whether it "
            'files as a C or S corporation .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    llc_must_note_if_file_as_partnership_c_or_s: str = Field(
        default="",
        description=(
            "Check if the employer is an LLC and note whether it files as a Partnership, C, "
            'or S corporation .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    other: str = Field(
        default="",
        description=(
            "Specify another employer type if not listed above .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class HealthPlanParticipation(BaseModel):
    """Health insurance funding, renewal, and eligibility details"""

    is_your_health_insurance_plan_self_funded_yes: BooleanLike = Field(
        ..., description="Indicate Yes if the employer’s health insurance plan is self-funded"
    )

    is_your_health_insurance_plan_self_funded_no: BooleanLike = Field(
        ..., description="Indicate No if the employer’s health insurance plan is not self-funded"
    )

    health_insurance_renewal_date: str = Field(
        ..., description="Renewal date of the employer’s health insurance plan"
    )  # YYYY-MM-DD format

    number_eligible: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of employees eligible for the health insurance plan"
    )


class PretaxDeductionsPlanHistory(BaseModel):
    """Information about existing pre-tax deductions and prior Section 125 plan"""

    have_you_been_holding_deductions_pre_tax_yes: BooleanLike = Field(
        ..., description="Indicate Yes if employee deductions have been taken on a pre-tax basis"
    )

    have_you_been_holding_deductions_pre_tax_no: BooleanLike = Field(
        ..., description="Indicate No if employee deductions have not been taken on a pre-tax basis"
    )

    original_effective_date_of_your_section_125_document: str = Field(
        default="",
        description=(
            "Original effective date of the employer’s Section 125 plan document, if applicable"
        ),
    )  # YYYY-MM-DD format

    original_plan_number: str = Field(
        default="",
        description=(
            "Original Section 125 plan number (e.g., 501, 502) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_first_pay_date_after_plan_effective_date: str = Field(
        ..., description="First payroll date occurring after the plan effective date"
    )  # YYYY-MM-DD format

    number_pay_periods: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of pay periods in the plan year"
    )


class TaxableWaiverCompensation(BaseModel):
    """Details on taxable wages for employees waiving coverage"""

    do_you_offer_taxable_wages_for_employees_who_waive_your_group_health_plan_or_for_any_other_reason_related_to_health_and_welfare_benefit_offerings_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate Yes if taxable wages are offered to employees who waive group health "
            "coverage or related benefits"
        ),
    )

    do_you_offer_taxable_wages_for_employees_who_waive_your_group_health_plan_or_for_any_other_reason_related_to_health_and_welfare_benefit_offerings_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate No if taxable wages are not offered in connection with waiving group "
            "health coverage or related benefits"
        ),
    )

    if_yes_are_the_benefits_paid_per_pay_or_lump_sum: str = Field(
        default="",
        description=(
            "Describe whether the taxable benefits are paid each pay period or as a lump "
            'sum .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    if_yes_what_are_the_conditions_required_to_receive_the_extra_compensation: str = Field(
        default="",
        description=(
            "Describe the conditions employees must meet to receive the extra taxable "
            'compensation .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class PlanEffectiveDate(BaseModel):
    """Requested effective date for the POP/Section 125 plan"""

    desired_effective_date: str = Field(
        ..., description="Desired effective date for the Section 125 / POP plan"
    )  # YYYY-MM-DD format


class AffiliatedEmployers(BaseModel):
    """Information about any affiliated employers"""

    affiliated_employers: BooleanLike = Field(
        default="",
        description="Indicate if there are any affiliated employers related to this plan",
    )

    affiliated_employers_legal_name: str = Field(
        default="",
        description=(
            'Legal name of any affiliated employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    affiliated_employers_corp_type_federal_ein: str = Field(
        default="",
        description=(
            "Corporation type and Federal EIN for any affiliated employer .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    affiliated_employers_address: str = Field(
        default="",
        description=(
            "Mailing address for any affiliated employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AuthorizationReferral(BaseModel):
    """Signatures, date, and referral source"""

    date: str = Field(..., description="Date the application is signed")  # YYYY-MM-DD format

    signature_1: str = Field(
        ...,
        description=(
            "Signature of an authorized representative .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    signature_2: str = Field(
        default="",
        description=(
            "Signature of a second authorized representative, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    who_referred_you_to_us_please_note_name_email_phone: str = Field(
        default="",
        description=(
            "Provide the name, email, and phone number of the person or organization that "
            'referred you .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class Section125PremiumOnlyPlanDocumentApplication(BaseModel):
    """
    Section 125 / Premium Only Plan Document Application

    Section 125 of the IRS Code gives employers the opportunity to permit employees to pay for group insurance premiums and health savings account contributions on a pre-tax basis through salary deduction. In order to have a valid Section 125 plan, the IRS says you must have a written plan document and summary plan description (SPD).
    """

    employer_information: EmployerInformation = Field(..., description="Employer Information")
    employer_type: EmployerType = Field(..., description="Employer Type")
    health_plan__participation: HealthPlanParticipation = Field(
        ..., description="Health Plan & Participation"
    )
    pre_tax_deductions__plan_history: PretaxDeductionsPlanHistory = Field(
        ..., description="Pre-tax Deductions & Plan History"
    )
    taxable_waiver_compensation: TaxableWaiverCompensation = Field(
        ..., description="Taxable Waiver Compensation"
    )
    plan_effective_date: PlanEffectiveDate = Field(..., description="Plan Effective Date")
    affiliated_employers: AffiliatedEmployers = Field(..., description="Affiliated Employers")
    authorization__referral: AuthorizationReferral = Field(
        ..., description="Authorization & Referral"
    )
