from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicationType(BaseModel):
    """Selected exemption type and fee category"""

    exemption_type: Literal[
        "Unimproved ($1100)",
        "Improved with Valid County Occupancy Approval ($300)",
        "Improved without Proper County Occupancy Approval ($500)",
        "N/A",
        "",
    ] = Field(..., description="Select the applicable exemption type for the property")


class OwnerContactInformation(BaseModel):
    """Primary owner contact details"""

    owner_s: str = Field(
        ...,
        description=(
            "Full legal name(s) of the property owner(s) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            "Mailing address for the owner or applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City for the mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for the mailing address")

    zip: str = Field(..., description="ZIP code for the mailing address")

    email_address: str = Field(
        default="",
        description=(
            "Email address for the owner or applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    home_phone: str = Field(
        default="",
        description=(
            'Home phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    work_phone: str = Field(
        default="",
        description=(
            'Work phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class ApplicantContactInformation(BaseModel):
    """Applicant contact details (if different from owner)"""

    applicant_s: str = Field(
        default="",
        description=(
            "Full legal name(s) of the applicant(s), if different from owner(s) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PropertyInformation(BaseModel):
    """Location, identification, and lot details for the property"""

    legal_description_of_property_1_4_section_section_township_range_or_subdivision_lot_block: str = Field(
        ...,
        description=(
            "Full legal description of the property, including 1/4 section & "
            "section-township-range or subdivision, lot, and block .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_identification_number_pin: str = Field(
        ...,
        description=(
            "Parcel Identification Number (PIN) for the property .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    current_number_of_lots: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Current total number of lots involved"
    )

    acreage_of_each_current_lots: str = Field(
        ...,
        description=(
            'Acreage of each current lot .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    number_of_lots_proposed_for_legalization: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of lots proposed to be legalized"
    )

    acreage_of_each_proposed_lots: str = Field(
        ...,
        description=(
            'Acreage of each proposed lot .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    describe_reason_for_request: str = Field(
        ...,
        description=(
            "Explanation of why this exemption request is being made .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Signatures(BaseModel):
    """Owner and applicant certifications and dates"""

    owner_s_signature_1: str = Field(
        ...,
        description=(
            'Signature of owner .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date_first_owner_signature: str = Field(
        ..., description="Date of first owner’s signature"
    )  # YYYY-MM-DD format

    owner_s_signature_2: str = Field(
        default="",
        description=(
            "Signature of second owner, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_second_owner_signature: str = Field(
        default="", description="Date of second owner’s signature"
    )  # YYYY-MM-DD format

    applicant_s_signature: str = Field(
        default="",
        description=(
            "Signature of applicant, if different from owner .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_applicant_signature: str = Field(
        default="", description="Date of applicant’s signature"
    )  # YYYY-MM-DD format


class ExemptionForCertainIllegalDivisionsOfLand(BaseModel):
    """
    Exemption for Certain Illegal Divisions of Land

    ''
    """

    application_type: ApplicationType = Field(..., description="Application Type")
    owner_contact_information: OwnerContactInformation = Field(
        ..., description="Owner Contact Information"
    )
    applicant_contact_information: ApplicantContactInformation = Field(
        ..., description="Applicant Contact Information"
    )
    property_information: PropertyInformation = Field(..., description="Property Information")
    signatures: Signatures = Field(..., description="Signatures")
