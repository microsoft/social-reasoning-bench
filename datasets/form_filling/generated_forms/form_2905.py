from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MentalHealthPrograms(BaseModel):
    """Program selection for referral"""

    tsrp_first_responder_group: BooleanLike = Field(
        default="",
        description="Check if referring the client to the 5-week TSRP First Responder Group program",
    )

    tsrp_general_public_group: BooleanLike = Field(
        default="",
        description="Check if referring the client to the 5-week TSRP General Public Group program",
    )

    adrp_11_day_program: BooleanLike = Field(
        default="",
        description=(
            "Check if referring the client to the 11-Day Anxiety and Depression Recovery "
            "Program (A&DRP)"
        ),
    )

    pre_admission_virtual_support: BooleanLike = Field(
        default="",
        description=(
            "Check if the client is to receive the 4-week pre-admission virtual support in "
            "addition to TSRP or A&DRP"
        ),
    )


class ClientInformation(BaseModel):
    """Basic information about the client"""

    last_name: str = Field(
        ...,
        description=(
            'Client\'s legal last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    prov_health_card_number: str = Field(
        ...,
        description=(
            "Client's provincial health card number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Client\'s legal first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Client's date of birth")  # YYYY-MM-DD format

    address: str = Field(
        ...,
        description=(
            'Client\'s street address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    primary_language_english: BooleanLike = Field(
        default="", description="Check if the client's primary language is English"
    )

    primary_language_other: str = Field(
        default="",
        description=(
            "Specify the client's primary language if not English .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'Client\'s city of residence .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    pre_disability_occupation: str = Field(
        default="",
        description=(
            "Client's occupation prior to disability .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    province: str = Field(
        ...,
        description=(
            'Client\'s province of residence .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_disability: str = Field(
        default="", description="Date the client's disability began"
    )  # YYYY-MM-DD format

    postal_code: str = Field(..., description="Client's postal code")

    phone: str = Field(
        ...,
        description=(
            'Client\'s primary phone number .If you cannot fill this, write "N/A". If this '
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

    claim_file_number_if_applies: str = Field(
        default="",
        description=(
            "Claim or file number associated with the referral, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ReferralAgencyType(BaseModel):
    """Type/category of the referring agency"""

    ref_agency_veterans_affair_canada: BooleanLike = Field(
        default="", description="Check if the referral agency type is Veteran's Affair Canada"
    )

    ref_agency_long_term_disability: BooleanLike = Field(
        default="", description="Check if the referral agency type is Long Term Disability"
    )

    ref_agency_rcmp: BooleanLike = Field(
        default="", description="Check if the referral agency type is RCMP"
    )

    ref_agency_wcb: BooleanLike = Field(
        default="",
        description="Check if the referral agency type is Workers' Compensation Board (WCB)",
    )

    ref_agency_police_fire_ambulance_corrections: BooleanLike = Field(
        default="",
        description=(
            "Check if the referral agency type is Police, Fire, Ambulance, or Corrections Services"
        ),
    )

    ref_agency_private: BooleanLike = Field(
        default="", description="Check if the referral agency type is Private"
    )

    ref_agency_provincial_federal_health_services: BooleanLike = Field(
        default="",
        description="Check if the referral agency type is Provincial or Federal Health Services",
    )

    ref_agency_other: str = Field(
        default="",
        description=(
            "Specify the referral agency type if 'Other' .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ReferringAgency(BaseModel):
    """Details of the referring agency"""

    ref_agency_name: str = Field(
        ...,
        description=(
            "Name of the contact person at the referring agency .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ref_agency_job_title_specialty: str = Field(
        default="",
        description=(
            "Job title or specialty of the referring agency contact .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ref_agency_company: str = Field(
        ...,
        description=(
            "Name of the referring agency or organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ref_agency_phone: str = Field(
        ...,
        description=(
            "Phone number for the referring agency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ref_agency_address: str = Field(
        ...,
        description=(
            "Mailing address of the referring agency .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ref_agency_fax: str = Field(
        default="",
        description=(
            'Fax number for the referring agency .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    ref_agency_city: str = Field(
        ...,
        description=(
            "City where the referring agency is located .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ref_agency_email: str = Field(
        default="",
        description=(
            "Email address of the referring agency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ref_agency_province: str = Field(
        ...,
        description=(
            "Province where the referring agency is located .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ref_agency_postal_code: str = Field(
        ..., description="Postal code for the referring agency address"
    )


class ReferringTreatmentProvider(BaseModel):
    """Details of the referring treatment provider"""

    ref_provider_name: str = Field(
        default="",
        description=(
            "Name of the referring treatment provider .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ref_provider_job_title_specialty: str = Field(
        default="",
        description=(
            "Job title or specialty of the referring treatment provider .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ref_provider_company: str = Field(
        default="",
        description=(
            "Clinic or organization name of the referring treatment provider .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    ref_provider_phone: str = Field(
        default="",
        description=(
            "Phone number for the referring treatment provider .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ref_provider_address: str = Field(
        default="",
        description=(
            "Mailing address of the referring treatment provider .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ref_provider_fax: str = Field(
        default="",
        description=(
            "Fax number for the referring treatment provider .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ref_provider_city: str = Field(
        default="",
        description=(
            "City where the referring treatment provider is located .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ref_provider_email: str = Field(
        default="",
        description=(
            "Email address of the referring treatment provider .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ref_provider_province: str = Field(
        default="",
        description=(
            "Province where the referring treatment provider is located .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ref_provider_postal_code: str = Field(
        default="", description="Postal code for the referring treatment provider address"
    )


class DiagnosticCriteria(BaseModel):
    """Clinical diagnostic information for the referral"""

    dx_ptsd: BooleanLike = Field(
        default="", description="Check if the client meets diagnostic criteria for PTSD"
    )

    dx_work_related: BooleanLike = Field(
        default="", description="Check if the condition is work related"
    )

    dx_anxiety: BooleanLike = Field(
        default="",
        description="Check if the client meets diagnostic criteria for an anxiety disorder",
    )

    dx_non_work_related: BooleanLike = Field(
        default="", description="Check if the condition is non-work related"
    )

    dx_depression: BooleanLike = Field(
        default="", description="Check if the client meets diagnostic criteria for depression"
    )

    dx_both_work_and_non_work_related: BooleanLike = Field(
        default="", description="Check if the condition is both work and non-work related"
    )

    dx_other: str = Field(
        default="",
        description=(
            'Specify any other relevant diagnosis .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class MentalHealthProgramsReferralForm(BaseModel):
    """
    Mental Health Programs Referral Form

    ''
    """

    mental_health_programs: MentalHealthPrograms = Field(..., description="Mental Health Programs")
    client_information: ClientInformation = Field(..., description="Client Information")
    referral_agency_type: ReferralAgencyType = Field(..., description="Referral Agency Type")
    referring_agency: ReferringAgency = Field(..., description="Referring Agency")
    referring_treatment_provider: ReferringTreatmentProvider = Field(
        ..., description="Referring Treatment Provider"
    )
    diagnostic_criteria: DiagnosticCriteria = Field(..., description="Diagnostic Criteria")
