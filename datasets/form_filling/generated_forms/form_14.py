from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicationType(BaseModel):
    """Type of application and SSN"""

    new_application: Literal["New Application", "Renewal", "Update", "Other", "N/A", ""] = Field(
        ..., description="Select the type of application being submitted."
    )

    renewal: Literal["New Application", "Renewal", "Update", "Other", "N/A", ""] = Field(
        ..., description="Select if this is a renewal of an existing RACES certification."
    )

    update: Literal["New Application", "Renewal", "Update", "Other", "N/A", ""] = Field(
        ..., description="Select if this application is to update existing information."
    )

    other: Literal["New Application", "Renewal", "Update", "Other", "N/A", ""] = Field(
        ..., description="Select if the application type is not covered by the other options."
    )

    if_other_please_explain: str = Field(
        default="",
        description=(
            "Explanation of application type if 'Other' is selected. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ssn: str = Field(default="", description="Applicant's Social Security Number.")


class ApplicantPersonalInformation(BaseModel):
    """Basic personal and contact details of the applicant"""

    name: str = Field(
        ...,
        description=(
            'Full legal name of the applicant. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Applicant's date of birth.")  # YYYY-MM-DD format

    dl: str = Field(
        default="",
        description=(
            'Applicant\'s driver license number. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Street address of the applicant's residence. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the applicant\'s residence. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    county: str = Field(
        ...,
        description=(
            'County of the applicant\'s residence. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zip: str = Field(..., description="ZIP code for the applicant's residence.")

    phone_home: str = Field(
        default="",
        description=(
            'Applicant\'s home telephone number. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone_work: str = Field(
        default="",
        description=(
            'Applicant\'s work telephone number. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone_cell: str = Field(
        default="",
        description=(
            'Applicant\'s mobile/cell phone number. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        default="",
        description=(
            'Applicant\'s email address. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class EmploymentInformation(BaseModel):
    """Current employment and related details"""

    retired: BooleanLike = Field(
        default="", description="Indicate whether the applicant is retired."
    )

    employer: str = Field(
        default="",
        description=(
            "Name of the applicant's current employer. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    position: str = Field(
        default="",
        description=(
            'Applicant\'s job title or position. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    employers_address: str = Field(
        default="",
        description=(
            "Street address of the applicant's employer. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    employers_city: str = Field(
        default="",
        description=(
            'City where the employer is located. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    employers_zip: str = Field(default="", description="ZIP code for the employer's address.")


class AmateurRadioInformation(BaseModel):
    """License and amateur radio affiliations"""

    call_sign: str = Field(
        ...,
        description=(
            'Applicant\'s amateur radio call sign. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    license_class: str = Field(
        ...,
        description=(
            "Class of the applicant's amateur radio license. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    license_expires: str = Field(
        ..., description="Expiration date of the applicant's amateur radio license."
    )  # YYYY-MM-DD format

    other_amateur_radio_organizations_presently_active_in: str = Field(
        default="",
        description=(
            "List other amateur radio organizations in which the applicant is currently "
            'active. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    fixed_and_mobile_equipment_list: str = Field(
        default="",
        description=(
            "List fixed and mobile equipment including bands, modes, antennas, and "
            'emergency power capability. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class ApplicantCertification(BaseModel):
    """Applicant signature and date certifying the application"""

    signature_of_applicant: str = Field(
        ...,
        description=(
            "Signature of the applicant certifying the information provided. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_of_applicant_signature: str = Field(
        ..., description="Date the applicant signed the application."
    )  # YYYY-MM-DD format


class RACESDRODCReferral(BaseModel):
    """To be completed by RACES DRO or DC making referral"""

    recommended_to_races_position_full_unit_alt_letter: str = Field(
        default="",
        description=(
            "RACES position being recommended, including full unit number and alternate "
            'letter. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    title_include_county_name_if_co_liaison: str = Field(
        default="",
        description=(
            "Title of the position, including county name if serving as county liaison. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    recommended_by: str = Field(
        default="",
        description=(
            "Name of the RACES DRO or DC making the referral. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    recommender_title: str = Field(
        default="",
        description=(
            "Title of the person making the recommendation. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    full_unit_number: str = Field(
        default="",
        description=(
            "Full unit number for the recommended RACES position. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    referral_date: str = Field(
        default="", description="Date the referral was completed."
    )  # YYYY-MM-DD format


class ForOfficialUseOnly(BaseModel):
    """Internal processing and approval information"""

    received: str = Field(
        default="", description="Date the application was received (for official use)."
    )  # YYYY-MM-DD format

    approved: str = Field(
        default="", description="Date the application was approved (for official use)."
    )  # YYYY-MM-DD format

    card_issued: str = Field(
        default="", description="Date the RACES card was issued (for official use)."
    )  # YYYY-MM-DD format

    entered: str = Field(
        default="",
        description="Date the information was entered into HR or records (for official use).",
    )  # YYYY-MM-DD format

    new_expiration: str = Field(
        default="", description="New expiration date assigned (for official use)."
    )  # YYYY-MM-DD format


class TexasDivisionOfEmergencyManagementStateRacesApplication(BaseModel):
    """
        TEXAS DIVISION OF EMERGENCY MANAGEMENT
    STATE RACES APPLICATION

        Attach a current copy of your amateur radio license and forward the completed application to your RACES District Radio Officer (DRO), or District Coordinator (DC) for the Texas Division of Emergency Management.
    """

    application_type: ApplicationType = Field(..., description="Application Type")
    applicant_personal_information: ApplicantPersonalInformation = Field(
        ..., description="Applicant Personal Information"
    )
    employment_information: EmploymentInformation = Field(..., description="Employment Information")
    amateur_radio_information: AmateurRadioInformation = Field(
        ..., description="Amateur Radio Information"
    )
    applicant_certification: ApplicantCertification = Field(
        ..., description="Applicant Certification"
    )
    races_drodc_referral: RACESDRODCReferral = Field(..., description="RACES DRO/DC Referral")
    for_official_use_only: ForOfficialUseOnly = Field(..., description="For Official Use Only")
