from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ReferralHeader(BaseModel):
    """Basic referral details"""

    date: str = Field(..., description="Date the referral form is completed")  # YYYY-MM-DD format

    county: str = Field(
        ...,
        description=(
            'County where the client resides .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ClientInformation(BaseModel):
    """Client contact and housing details"""

    client_name: str = Field(
        ...,
        description=(
            'Full name of the client .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street address of the client .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for the client's address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    birth_date: str = Field(..., description="Client's date of birth")  # YYYY-MM-DD format

    contact_person: str = Field(
        default="",
        description=(
            "Primary contact person for this referral, if different from client .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    relationship: str = Field(
        default="",
        description=(
            "Relationship of the contact person to the client .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    home_phone: str = Field(
        default="",
        description=(
            'Client\'s home phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        default="",
        description=(
            'Client\'s cell phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            'Client\'s email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    own: BooleanLike = Field(
        ..., description="Indicates that the client owns the home to be modified"
    )

    landlord: str = Field(
        default="",
        description=(
            "Name of the landlord if the client owns the home but a landlord is involved "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    rent: BooleanLike = Field(
        ..., description="Indicates that the client rents the home to be modified"
    )

    phone_landlord: str = Field(
        default="",
        description=(
            'Landlord\'s phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    email_landlord: str = Field(
        default="",
        description=(
            'Landlord\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    is_this_a_new_construction_project_yes: BooleanLike = Field(
        ..., description="Indicates that this is a new construction project"
    )

    new_address_will_be: str = Field(
        default="",
        description=(
            "New address for the project if it is new construction .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    is_this_a_new_construction_project_no: BooleanLike = Field(
        ..., description="Indicates that this is not a new construction project"
    )


class CaseManagerInformation(BaseModel):
    """Case manager contact details"""

    case_manager_name: str = Field(
        default="",
        description=(
            'Name of the client\'s case manager .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    case_manager_agency: str = Field(
        default="",
        description=(
            'Agency the case manager works for .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    case_manager_phone: str = Field(
        default="",
        description=(
            'Case manager\'s phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    case_manager_email: str = Field(
        default="",
        description=(
            'Case manager\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class WaiverInformation(BaseModel):
    """Waiver, diagnosis, and funding details"""

    client_pmi: str = Field(
        default="",
        description=(
            "Client's PMI (Person Master Index) number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    diagnosis_codes: str = Field(
        default="",
        description=(
            "Relevant diagnosis codes for the client .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    service_plan_dates_from: str = Field(
        default="", description="Start date of the service plan"
    )  # YYYY-MM-DD format

    service_plan_dates_to: str = Field(
        default="", description="End date of the service plan"
    )  # YYYY-MM-DD format

    waiver_type_dd: BooleanLike = Field(default="", description="Indicates the waiver type is DD")

    waiver_type_cadi: BooleanLike = Field(
        default="", description="Indicates the waiver type is CADI"
    )

    waiver_type_cac: BooleanLike = Field(default="", description="Indicates the waiver type is CAC")

    waiver_type_bi: BooleanLike = Field(default="", description="Indicates the waiver type is BI")

    is_a_positive_support_specialist_involved_yes: BooleanLike = Field(
        default="", description="Indicates that a positive support specialist is involved"
    )

    positive_support_specialist_name: str = Field(
        default="",
        description=(
            "Name of the positive support specialist .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    is_a_positive_support_specialist_involved_no: BooleanLike = Field(
        default="", description="Indicates that a positive support specialist is not involved"
    )

    positive_support_specialist_agency: str = Field(
        default="",
        description=(
            "Agency of the positive support specialist .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    positive_support_specialist_phone: str = Field(
        default="",
        description=(
            "Phone number for the positive support specialist or their agency .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    positive_support_specialist_email: str = Field(
        default="",
        description=(
            "Email address for the positive support specialist or their agency .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    short_term_waiver_yes: BooleanLike = Field(
        default="", description="Indicates that the waiver is short-term"
    )

    short_term_waiver_no: BooleanLike = Field(
        default="", description="Indicates that the waiver is not short-term"
    )

    any_funds_allocated_for_home_vehicle_modifications_to_date_yes: BooleanLike = Field(
        default="",
        description=(
            "Indicates that funds have already been allocated for home or vehicle modifications"
        ),
    )

    any_funds_allocated_for_home_vehicle_modifications_to_date_no: BooleanLike = Field(
        default="",
        description="Indicates that no funds have been allocated for home or vehicle modifications",
    )

    if_yes_how_much: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of funds already allocated for modifications"
    )


class BillingInformation(BaseModel):
    """Billing method and billing contact details"""

    billing_mn_its: BooleanLike = Field(
        default="", description="Indicates that billing will be through MN-ITS"
    )

    billing_spenddown: BooleanLike = Field(
        default="", description="Indicates that billing will involve a spenddown"
    )

    spenddown_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of the spenddown"
    )

    billing_cdcs_mn_its: BooleanLike = Field(
        default="", description="Indicates that billing will be through CDCS and MN-ITS"
    )

    billing_contact_name: str = Field(
        default="",
        description=(
            'Name of the billing contact person .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    billing_agency: str = Field(
        default="",
        description=(
            'Agency responsible for billing .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    billing_email: str = Field(
        default="",
        description=(
            'Email address for the billing contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    billing_phone: str = Field(
        default="",
        description=(
            'Phone number for the billing contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ReferralCoordinationAdaptations(BaseModel):
    """Coordination preferences and requested adaptations"""

    contact_case_manager_prior_to_home_visit_yes: BooleanLike = Field(
        default="",
        description="Indicates that the case manager should be contacted before the home visit",
    )

    contact_case_manager_prior_to_home_visit_no: BooleanLike = Field(
        default="",
        description=(
            "Indicates that the case manager does not need to be contacted before the home visit"
        ),
    )

    describe_adaptations_to_explore: str = Field(
        default="",
        description=(
            "Description of the home or environmental adaptations to be explored .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SubmissionNotices(BaseModel):
    """Form submission instructions and notices"""

    email_submission_instructions: BooleanLike = Field(
        default="",
        description="Indicates acknowledgment of email submission and contact instructions",
    )

    ma_provider_and_service_code_notice: BooleanLike = Field(
        default="", description="Indicates acknowledgment of MA provider number and service code"
    )

    services_and_fees_accrual_notice: BooleanLike = Field(
        default="",
        description="Indicates acknowledgment that services and fees begin accruing upon submission",
    )


class AccessibilityDesignReferralForHomeEnvironmentalAdaptations(BaseModel):
    """
        ACCESSIBILITY
    DESIGN
    Referral for Home
    Environmental Adaptations

        ''
    """

    referral_header: ReferralHeader = Field(..., description="Referral Header")
    client_information: ClientInformation = Field(..., description="Client Information")
    case_manager_information: CaseManagerInformation = Field(
        ..., description="Case Manager Information"
    )
    waiver_information: WaiverInformation = Field(..., description="Waiver Information")
    billing_information: BillingInformation = Field(..., description="Billing Information")
    referral_coordination__adaptations: ReferralCoordinationAdaptations = Field(
        ..., description="Referral Coordination & Adaptations"
    )
    submission__notices: SubmissionNotices = Field(..., description="Submission & Notices")
