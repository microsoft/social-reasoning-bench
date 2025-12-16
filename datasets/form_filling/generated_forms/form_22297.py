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
    """Contact information for property owner(s)"""

    owner_s_1: str = Field(
        ...,
        description=(
            'Name(s) of the property owner(s) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_1: str = Field(
        ...,
        description=(
            'Mailing address of the owner(s) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_1: str = Field(
        ...,
        description=(
            'City for the owner(s) mailing address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state_1: str = Field(..., description="State for the owner(s) mailing address")

    zip_1: str = Field(..., description="ZIP code for the owner(s) mailing address")

    email_address_1: str = Field(
        default="",
        description=(
            'Email address for the owner(s) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    home_phone_1: str = Field(
        default="",
        description=(
            'Home phone number for the owner(s) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    work_phone_1: str = Field(
        default="",
        description=(
            'Work phone number for the owner(s) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    owner_s_2: str = Field(
        default="",
        description=(
            "Name(s) of additional owner(s), if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_2: str = Field(
        default="",
        description=(
            "Mailing address of additional owner(s), if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_2: str = Field(
        default="",
        description=(
            "City for the additional owner(s) mailing address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    state_2: str = Field(
        default="", description="State for the additional owner(s) mailing address"
    )

    zip_2: str = Field(
        default="", description="ZIP code for the additional owner(s) mailing address"
    )

    email_address_2: str = Field(
        default="",
        description=(
            "Email address for the additional owner(s) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    home_phone_2: str = Field(
        default="",
        description=(
            "Home phone number for the additional owner(s) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_phone_2: str = Field(
        default="",
        description=(
            "Work phone number for the additional owner(s) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ApplicantInformation(BaseModel):
    """Contact information for applicant(s), if different from owner"""

    applicant_s: str = Field(
        ...,
        description=(
            "Name(s) of the applicant(s), if different from owner(s) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_3: str = Field(
        ...,
        description=(
            'Mailing address of the applicant(s) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_3: str = Field(
        ...,
        description=(
            "City for the applicant(s) mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_3: str = Field(..., description="State for the applicant(s) mailing address")

    zip_3: str = Field(..., description="ZIP code for the applicant(s) mailing address")

    email_address_3: str = Field(
        default="",
        description=(
            'Email address for the applicant(s) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    home_phone_3: str = Field(
        default="",
        description=(
            "Home phone number for the applicant(s) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_phone_3: str = Field(
        default="",
        description=(
            "Work phone number for the applicant(s) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PropertyInformation(BaseModel):
    """Details about the property and request"""

    parcel_number: str = Field(
        ...,
        description=(
            "Assessor parcel number for the subject property .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    legal_description: str = Field(
        ...,
        description=(
            "Full legal description of the property (e.g., 1/4 Section & "
            "Section-Township-Range or Subdivision-Lot & Block) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    describe_reason_for_request: str = Field(
        ...,
        description=(
            "Narrative explanation of why the exemption by resolution is being requested "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class CertificationandSignatures(BaseModel):
    """Owner and applicant certifications and dates"""

    owner_s_certification_1: str = Field(
        ...,
        description=(
            'Signature of owner for certification .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_owner_1: str = Field(
        ..., description="Date the owner signed the certification"
    )  # YYYY-MM-DD format

    owner_s_certification_2: str = Field(
        default="",
        description=(
            "Signature of additional owner for certification, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_owner_2: str = Field(
        default="", description="Date the additional owner signed the certification"
    )  # YYYY-MM-DD format

    applicant_certification: str = Field(
        default="",
        description=(
            "Signature of applicant for certification, if different from owner .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_applicant: str = Field(
        default="", description="Date the applicant signed the certification"
    )  # YYYY-MM-DD format


class ExemptionByResolutionApplication(BaseModel):
    """EXEMPTION BY RESOLUTION APPLICATION"""

    owner_information: OwnerInformation = Field(..., description="Owner Information")
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    property_information: PropertyInformation = Field(..., description="Property Information")
    certification_and_signatures: CertificationandSignatures = Field(
        ..., description="Certification and Signatures"
    )
