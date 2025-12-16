from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ExemptionType(BaseModel):
    """Selected exemption category for the division of land"""

    exemption_unimproved_1100: BooleanLike = Field(
        ...,
        description=(
            "Select if the property is unimproved for this exemption type ($1100 fee). "
            "Exactly one exemption option must be selected."
        ),
    )

    exemption_improved_valid_occupancy_300: BooleanLike = Field(
        ...,
        description=(
            "Select if the property is improved and has valid County occupancy approval "
            "($300 fee). Exactly one exemption option must be selected."
        ),
    )

    exemption_improved_without_proper_occupancy_500: BooleanLike = Field(
        ...,
        description=(
            "Select if the property is improved but does not have proper County occupancy "
            "approval ($500 fee). Exactly one exemption option must be selected."
        ),
    )


class OwnerInformation(BaseModel):
    """Contact information for property owner(s)"""

    owners: str = Field(
        ...,
        description=(
            "Full legal name(s) of the property owner(s). .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            "Mailing street address for the owner(s). .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City for the owner\'s mailing address. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for the owner's mailing address.")

    zip: str = Field(..., description="ZIP code for the owner's mailing address.")

    email_address: str = Field(
        default="",
        description=(
            'Email address for the owner(s). .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    home_phone: str = Field(
        default="",
        description=(
            'Home phone number for the owner(s). .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    work_phone: str = Field(
        default="",
        description=(
            'Work phone number for the owner(s). .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ApplicantInformation(BaseModel):
    """Contact information for applicant(s), if different from owner"""

    applicants: str = Field(
        default="",
        description=(
            "Full legal name(s) of the applicant(s), if different from owner(s). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mailing_address_applicant: str = Field(
        default="",
        description=(
            "Mailing street address for the applicant(s). .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_applicant: str = Field(
        default="",
        description=(
            "City for the applicant's mailing address. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_applicant: str = Field(
        default="", description="State for the applicant's mailing address."
    )

    zip_applicant: str = Field(
        default="", description="ZIP code for the applicant's mailing address."
    )

    email_address_applicant: str = Field(
        default="",
        description=(
            'Email address for the applicant(s). .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    home_phone_applicant: str = Field(
        default="",
        description=(
            "Home phone number for the applicant(s). .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_phone_applicant: str = Field(
        default="",
        description=(
            "Work phone number for the applicant(s). .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PropertyandRequestDetails(BaseModel):
    """Property identification and details of the requested legalization"""

    legal_description_of_property: str = Field(
        ...,
        description=(
            "Full legal description of the property, including 1/4 Section & "
            "Section-Township-Range or Subdivision, Lot & Block. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_identification_number_pin: str = Field(
        ...,
        description=(
            "Parcel Identification Number (PIN) for the property. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    current_number_of_lots: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of existing lots before legalization."
    )

    acreage_of_each_current_lots: str = Field(
        ...,
        description=(
            "Acreage of each current lot (list or description). .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    number_of_lots_proposed_for_legalization: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of lots that will exist after the proposed legalization."
    )

    acreage_of_each_proposed_lots: str = Field(
        ...,
        description=(
            "Acreage of each proposed lot after legalization (list or description). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    describe_reason_for_request: str = Field(
        ...,
        description=(
            "Narrative explanation of why this exemption request is being made. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Signatures(BaseModel):
    """Certification and authorization signatures"""

    owners_signature_1: str = Field(
        ...,
        description=(
            "Signature of first owner certifying the accuracy of the application. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_for_owners_signature_1: str = Field(
        ..., description="Date the first owner signed the form."
    )  # YYYY-MM-DD format

    owners_signature_2: str = Field(
        default="",
        description=(
            "Signature of second owner, if applicable. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_for_owners_signature_2: str = Field(
        default="", description="Date the second owner signed the form."
    )  # YYYY-MM-DD format

    applicants_signature: str = Field(
        default="",
        description=(
            "Signature of applicant(s), if different from owner(s). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_for_applicants_signature: str = Field(
        default="", description="Date the applicant(s) signed the form."
    )  # YYYY-MM-DD format


class ClearCreekCountyLandDivisionExemption(BaseModel):
    """
        CLEAR CREEK COUNTY PLANNING DEPARTMENT
    Exemption for Certain Illegal Divisions of Land

        ''
    """

    exemption_type: ExemptionType = Field(..., description="Exemption Type")
    owner_information: OwnerInformation = Field(..., description="Owner Information")
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    property_and_request_details: PropertyandRequestDetails = Field(
        ..., description="Property and Request Details"
    )
    signatures: Signatures = Field(..., description="Signatures")
