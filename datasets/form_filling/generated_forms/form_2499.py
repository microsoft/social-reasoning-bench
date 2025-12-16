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
    """Type of Board of Adjustment application and basic project characteristics"""

    is_this_design_build: BooleanLike = Field(
        default="", description="Indicate whether this application is for a design-build project."
    )

    is_this_residential: BooleanLike = Field(
        default="", description="Indicate whether the project is residential."
    )

    residential_variance: BooleanLike = Field(
        ..., description="Check if this application is for a residential variance."
    )

    non_residential_variance: BooleanLike = Field(
        ..., description="Check if this application is for a non-residential variance."
    )

    interpretation: BooleanLike = Field(
        ..., description="Check if this application is for an interpretation request."
    )

    ba_blanket_variance: BooleanLike = Field(
        ..., description="Check if this application is for a Board of Adjustment blanket variance."
    )

    is_this_subject_property_within_an_area_of_15_or_greater_hillside_slopes: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the subject property is within an area of 15% or greater "
            "hillside slopes."
        ),
    )


class Request(BaseModel):
    """Details of the variance or interpretation request"""

    description_of_request: str = Field(
        ...,
        description=(
            "Provide a detailed description of the variance or interpretation being "
            'requested. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    existing_use_of_property: str = Field(
        ...,
        description=(
            "Describe the current use of the property. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    existing_zoning_district: str = Field(
        ...,
        description=(
            "Enter the current zoning district designation for the property. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    related_case_numbers: str = Field(
        default="",
        description=(
            "List any related case numbers associated with this property or request. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PropertyInformation(BaseModel):
    """Location and legal information for the subject property"""

    address_if_known: str = Field(
        default="",
        description=(
            "Street address of the subject property, if known. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    general_location_include_nearest_city_town: str = Field(
        ...,
        description=(
            "Describe the general location of the property, including the nearest city or "
            'town. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    size_in_acres: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total size of the property in acres."
    )

    square_feet: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total size of the property in square feet."
    )

    legal_description: str = Field(
        ...,
        description=(
            "Enter the full legal description of the property. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    section: str = Field(
        ...,
        description=(
            "Section number from the legal description. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    township: str = Field(
        ...,
        description=(
            "Township designation from the legal description. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    range: str = Field(
        ...,
        description=(
            "Range designation from the legal description. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    assessors_parcel_number: str = Field(
        ...,
        description=(
            "Assessor's parcel number (APN) for the property. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    subdivision_name_if_applicable: str = Field(
        default="",
        description=(
            "Name of the subdivision, if the property is within a platted subdivision. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ApplicantInformation(BaseModel):
    """Contact information for the applicant"""

    applicant_name: str = Field(
        ...,
        description=(
            'Full name of the applicant. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    applicant_contact: str = Field(
        default="",
        description=(
            "Primary contact person for the applicant, if different from the applicant "
            'name. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    applicant_address: str = Field(
        ...,
        description=(
            'Mailing address of the applicant. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    applicant_city: str = Field(
        ...,
        description=(
            "City for the applicant's mailing address. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_state: str = Field(..., description="State for the applicant's mailing address.")

    applicant_zip: str = Field(..., description="ZIP code for the applicant's mailing address.")

    applicant_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the applicant. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_fax: str = Field(
        default="",
        description=(
            "Fax number for the applicant, if available. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_e_mail_address: str = Field(
        ...,
        description=(
            'Email address for the applicant. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class PropertyOwnerInformation(BaseModel):
    """Contact information for the property owner"""

    property_owner_name: str = Field(
        ...,
        description=(
            'Full name of the property owner. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_contact: str = Field(
        default="",
        description=(
            "Primary contact person for the property owner, if different from the owner "
            'name. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    property_owner_address: str = Field(
        ...,
        description=(
            "Mailing address of the property owner. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_city: str = Field(
        ...,
        description=(
            "City for the property owner's mailing address. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_state: str = Field(
        ..., description="State for the property owner's mailing address."
    )

    property_owner_zip: str = Field(
        ..., description="ZIP code for the property owner's mailing address."
    )

    property_owner_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the property owner. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_fax: str = Field(
        default="",
        description=(
            "Fax number for the property owner, if available. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_e_mail_address: str = Field(
        default="",
        description=(
            'Email address for the property owner. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class PropertyOwnerandApplicantAuthorization(BaseModel):
    """Authorization for applicant to file on behalf of property owner"""

    property_owner_name_authorization: str = Field(
        ...,
        description=(
            "Printed name of the property owner granting authorization to the applicant. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    applicants_name_authorization: str = Field(
        ...,
        description=(
            "Name of the applicant being authorized by the property owner. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class Proposition207Waiver(BaseModel):
    """Waiver of claims for diminution in value under Proposition 207"""

    property_owner_signature_proposition_207_waiver: str = Field(
        ...,
        description=(
            "Signature of the property owner acknowledging the Proposition 207 waiver. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_proposition_207_waiver: str = Field(
        ..., description="Date the Proposition 207 waiver was signed."
    )  # YYYY-MM-DD format


class VerificationofApplicationInformation(BaseModel):
    """Certification that application information is true and correct"""

    owner_or_authorized_agent_signature_verification_of_application_information: str = Field(
        ...,
        description=(
            "Signature of the owner or authorized agent verifying the accuracy of the "
            'application information. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_verification_of_application_information: str = Field(
        ..., description="Date the verification of application information was signed."
    )  # YYYY-MM-DD format


class ARS1605TimeframeExtension(BaseModel):
    """Authorization for a 50% extension of the application review timeframe"""

    property_owner_signature_ars_1605_timeframe_extension: str = Field(
        default="",
        description=(
            "Signature of the property owner authorizing a 50% timeframe extension under "
            'ARS 1605. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    date_ars_1605_timeframe_extension: str = Field(
        default="", description="Date the ARS 1605 timeframe extension authorization was signed."
    )  # YYYY-MM-DD format


class PlanningDevelopmentDepartmentVarianceInterpretationApplication(BaseModel):
    """
        Planning & Development
    Department
    VARIANCE / INTERPRETATION APPLICATION

        ''
    """

    application_type: ApplicationType = Field(..., description="Application Type")
    request: Request = Field(..., description="Request")
    property_information: PropertyInformation = Field(..., description="Property Information")
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    property_owner_information: PropertyOwnerInformation = Field(
        ..., description="Property Owner Information"
    )
    property_owner_and_applicant_authorization: PropertyOwnerandApplicantAuthorization = Field(
        ..., description="Property Owner and Applicant Authorization"
    )
    proposition_207_waiver: Proposition207Waiver = Field(..., description="Proposition 207 Waiver")
    verification_of_application_information: VerificationofApplicationInformation = Field(
        ..., description="Verification of Application Information"
    )
    ars_1605_timeframe_extension: ARS1605TimeframeExtension = Field(
        ..., description="ARS 1605 Timeframe Extension"
    )
