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
    """Selected exemption type for the application"""

    exemption_unimproved: BooleanLike = Field(
        ..., description="Select if the property is unimproved for the exemption request"
    )

    exemption_improved_valid_occupancy: BooleanLike = Field(
        ...,
        description="Select if the property is improved and has valid County occupancy approval",
    )

    exemption_improved_without_proper_occupancy: BooleanLike = Field(
        ...,
        description=(
            "Select if the property is improved but does not have proper County occupancy approval"
        ),
    )


class OwnerInformation(BaseModel):
    """Contact information for the property owner(s)"""

    owners: str = Field(
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


class ApplicantInformation(BaseModel):
    """Contact information for the applicant(s), if different from owner"""

    applicants: str = Field(
        default="",
        description=(
            "Full legal name(s) of the applicant(s), if different from owner(s) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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


class PropertyInformation(BaseModel):
    """Details about the property and lots involved"""

    legal_description_of_property_1_4_section_section_township_range_or_subdivision_lot_block: str = Field(
        ...,
        description=(
            "Full legal description of the property, including 1/4 section, "
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
        ..., description="Current number of lots involved in this request"
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
        ..., description="Number of lots proposed to be legalized by this request"
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
    """Certification and authorization signatures"""

    owners_signature_1: str = Field(
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

    owners_signature_2: str = Field(
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

    applicants_signature: str = Field(
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


class ClearCreekCountyPlanningDeptIllegalLandDivisionExemption(BaseModel):
    """
        CLEAR CREEK COUNTY PLANNING DEPARTMENT
    Exemption for Certain Illegal Divisions of Land

        ''
    """

    application_type: ApplicationType = Field(..., description="Application Type")
    owner_information: OwnerInformation = Field(..., description="Owner Information")
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    property_information: PropertyInformation = Field(..., description="Property Information")
    signatures: Signatures = Field(..., description="Signatures")
