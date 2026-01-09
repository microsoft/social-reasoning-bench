from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OfficeUseOnly(BaseModel):
    """For internal processing by the Planning & Development Department"""

    permit_no: str = Field(
        default="",
        description=(
            "Internal permit number assigned by the Village .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    zoning_district: str = Field(
        default="",
        description=(
            "Zoning district designation for the property .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    cup_reason: str = Field(
        default="",
        description=(
            "Brief reason for the conditional use permit .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    code_reference: str = Field(
        default="",
        description=(
            'Applicable municipal code section(s) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    plan_comm_meeting: str = Field(
        default="",
        description=(
            "Date or identifier of the Plan Commission meeting .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    outcome: str = Field(
        default="",
        description=(
            "Result of Plan Commission action on the application .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PropertyInformation(BaseModel):
    """Location of the property for which the conditional use permit is requested"""

    property_address: str = Field(
        ...,
        description=(
            "Street address of the property for which the permit is requested .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PropertyOwner(BaseModel):
    """Contact information for the property owner"""

    owner_name: str = Field(
        ...,
        description=(
            'Full legal name of the property owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    owner_address: str = Field(
        ...,
        description=(
            'Mailing address of the property owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    owner_phone_number: str = Field(
        ...,
        description=(
            "Primary phone number for the property owner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    owner_phone_number_alternate_additional: str = Field(
        default="",
        description=(
            "Alternate or additional phone number for the property owner .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    owner_email: str = Field(
        ...,
        description=(
            "Primary email address for the property owner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    owner_email_alternate_additional: str = Field(
        default="",
        description=(
            "Alternate or additional email address for the property owner .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ApplicantBusiness(BaseModel):
    """Contact information for the applicant or business"""

    applicant_business_name: str = Field(
        ...,
        description=(
            "Name of the applicant or business submitting the application .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    applicant_business_address: str = Field(
        ...,
        description=(
            "Mailing address of the applicant or business .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_phone_number: str = Field(
        ...,
        description=(
            "Primary phone number for the applicant or business .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_phone_number_alternate_additional: str = Field(
        default="",
        description=(
            "Alternate or additional phone number for the applicant or business .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    applicant_email: str = Field(
        ...,
        description=(
            "Primary email address for the applicant or business .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_email_alternate_additional: str = Field(
        default="",
        description=(
            "Alternate or additional email address for the applicant or business .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    agenda_email_owner: BooleanLike = Field(
        default="",
        description="Check if the property owner prefers to receive the meeting agenda by email",
    )

    agenda_email_applicant: BooleanLike = Field(
        default="",
        description="Check if the applicant prefers to receive the meeting agenda by email",
    )


class BusinessInformation(BaseModel):
    """Details about the business and required attachments"""

    name_of_business: str = Field(
        ...,
        description=(
            "Official name of the business operating at the property .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    max_employees_on_site: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Maximum number of employees that will be on-site at one time"
    )

    is_survey_attached_if_required: BooleanLike = Field(
        default="", description="Indicate whether a required property survey is attached"
    )

    is_parking_plan_attached_if_required: BooleanLike = Field(
        default="", description="Indicate whether a required parking plan is attached"
    )


class ConditionalUseRequest(BaseModel):
    """Description of the proposed conditional use and applicant certification"""

    cup_request_description: str = Field(
        ...,
        description=(
            "Describe the proposed use or activity that requires a Conditional Use Permit "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of the applicant or authorized representative .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the application is signed")  # YYYY-MM-DD format


class ApplicationForConditionalUsePermit(BaseModel):
    """
        APPLICATION FOR
    CONDITIONAL USE PERMIT

        ''
    """

    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
    property_information: PropertyInformation = Field(..., description="Property Information")
    property_owner: PropertyOwner = Field(..., description="Property Owner")
    applicant__business: ApplicantBusiness = Field(..., description="Applicant / Business")
    business_information: BusinessInformation = Field(..., description="Business Information")
    conditional_use_request: ConditionalUseRequest = Field(
        ..., description="Conditional Use Request"
    )
