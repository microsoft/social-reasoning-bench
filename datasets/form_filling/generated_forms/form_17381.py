from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OwnerInformation(BaseModel):
    """Contact information for the property owner(s)"""

    owners: str = Field(
        ...,
        description=(
            'Name(s) of the property owner(s) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_owner: str = Field(
        ...,
        description=(
            'Mailing address of the owner(s) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_owner: str = Field(
        ...,
        description=(
            'City for the owner(s) mailing address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state_owner: str = Field(..., description="State for the owner(s) mailing address")

    zip_owner: str = Field(..., description="ZIP code for the owner(s) mailing address")

    email_address_owner: str = Field(
        default="",
        description=(
            'Email address of the owner(s) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    home_phone_owner: str = Field(
        default="",
        description=(
            'Home phone number of the owner(s) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    work_phone_owner: str = Field(
        default="",
        description=(
            'Work phone number of the owner(s) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ApplicantInformation(BaseModel):
    """Contact information for the applicant(s), if different from owner"""

    applicants: str = Field(
        default="",
        description=(
            "Name(s) of the applicant(s), if different from owner(s) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_applicant: str = Field(
        default="",
        description=(
            'Mailing address of the applicant(s) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_applicant: str = Field(
        default="",
        description=(
            "City for the applicant(s) mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_applicant: str = Field(
        default="", description="State for the applicant(s) mailing address"
    )

    zip_applicant: str = Field(
        default="", description="ZIP code for the applicant(s) mailing address"
    )

    email_address_applicant: str = Field(
        default="",
        description=(
            'Email address of the applicant(s) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    home_phone_applicant: str = Field(
        default="",
        description=(
            'Home phone number of the applicant(s) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    work_phone_applicant: str = Field(
        default="",
        description=(
            'Work phone number of the applicant(s) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class PropertyInformation(BaseModel):
    """Details about the subject property and zoning"""

    legal_description_of_property: str = Field(
        ...,
        description=(
            "Full legal description of the property (e.g., 1/4 Section & "
            "Section-Township-Range or Subdivision-Lot & Block) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_of_property: str = Field(
        ...,
        description=(
            "Street address of the property being downzoned .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_number: str = Field(
        ...,
        description=(
            "Assessor parcel number for the property .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    total_acreage: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total acreage of the property"
    )

    current_zoning: str = Field(
        ...,
        description=(
            "Current zoning designation of the property .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class RequestDetails(BaseModel):
    """Explanation of the downzoning request"""

    describe_reason_for_request: str = Field(
        ...,
        description=(
            "Explanation of why the downzoning is being requested .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Signatures(BaseModel):
    """Certifications and signatures of owners and applicants"""

    owners_signature_1: str = Field(
        ...,
        description=(
            "Signature of owner(s) certifying the accuracy of the application .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_owner_signature_1: str = Field(
        ..., description="Date the owner(s) signed the application"
    )  # YYYY-MM-DD format

    owners_signature_2: str = Field(
        default="",
        description=(
            "Additional owner(s) signature, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_owner_signature_2: str = Field(
        default="", description="Date the additional owner(s) signed the application"
    )  # YYYY-MM-DD format

    applicants_signature: str = Field(
        default="",
        description=(
            "Signature of applicant(s), if different from owner(s) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_applicant_signature: str = Field(
        default="", description="Date the applicant(s) signed the application"
    )  # YYYY-MM-DD format


class DownzoningApplication(BaseModel):
    """
    DOWNZONING APPLICATION

    ''
    """

    owner_information: OwnerInformation = Field(..., description="Owner Information")
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    property_information: PropertyInformation = Field(..., description="Property Information")
    request_details: RequestDetails = Field(..., description="Request Details")
    signatures: Signatures = Field(..., description="Signatures")
