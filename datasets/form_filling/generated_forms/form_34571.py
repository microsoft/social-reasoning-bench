from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RequestingPartyInformation(BaseModel):
    """Information about the individual or business making the request"""

    request_date: str = Field(
        ..., description="Date the public record request is being submitted"
    )  # YYYY-MM-DD format

    first_name: str = Field(
        ...,
        description=(
            'Requesting party\'s first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Requesting party\'s last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    business_name: str = Field(
        default="",
        description=(
            "Business or organization name, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            "Street or PO Box for mailing correspondence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_mailing_address: str = Field(
        ...,
        description=(
            'City for the mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state_mailing_address: str = Field(..., description="State for the mailing address")

    zip: str = Field(..., description="ZIP code for the mailing address")

    physical_address: str = Field(
        default="",
        description=(
            "Physical (street) address if different from mailing address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    city_physical_address: str = Field(
        default="",
        description=(
            'City for the physical address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state_physical_address: str = Field(default="", description="State for the physical address")

    phone_1: str = Field(
        ...,
        description=(
            'Primary phone number for contact .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone_2: str = Field(
        default="",
        description=(
            'Secondary phone number for contact .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Email address for correspondence .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    preferred_contact_email: BooleanLike = Field(
        default="", description="Check if email is the preferred method of contact for questions"
    )

    preferred_contact_phone: BooleanLike = Field(
        default="", description="Check if phone is the preferred method of contact for questions"
    )

    preferred_contact_standard_mail: BooleanLike = Field(
        default="",
        description="Check if standard mail is the preferred method of contact for questions",
    )

    preferred_receive_email: BooleanLike = Field(
        default="", description="Check if you prefer to receive requested records by email"
    )

    preferred_receive_usb_drive: BooleanLike = Field(
        default="",
        description=(
            "Check if you prefer to receive requested records on a USB drive (may incur "
            "additional charges)"
        ),
    )

    preferred_receive_standard_mail: BooleanLike = Field(
        default="", description="Check if you prefer to receive requested records by standard mail"
    )


class RequestedRecordInformation(BaseModel):
    """Details about the records being requested"""

    date_range_of_requested_records: str = Field(
        ...,
        description=(
            "Specify the start and end dates for the records you are requesting .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    names_on_requested_records: str = Field(
        ...,
        description=(
            "Names that appear on the records being requested .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    types_of_records_requested: str = Field(
        ...,
        description=(
            "Types or categories of records you are requesting .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    description_of_requested_records: str = Field(
        ...,
        description=(
            "Specific description of the records or information you are seeking .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Signature(BaseModel):
    """Signature and date of the requesting party"""

    signature_of_requesting_party: str = Field(
        ...,
        description=(
            "Signature of the person submitting the request .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_signature: str = Field(..., description="Date the form was signed")  # YYYY-MM-DD format


class PublicRecordRequest(BaseModel):
    """
    Public Record Request

    Public Record Request
    """

    requesting_party_information: RequestingPartyInformation = Field(
        ..., description="Requesting Party Information"
    )
    requested_record_information: RequestedRecordInformation = Field(
        ..., description="Requested Record Information"
    )
    signature: Signature = Field(..., description="Signature")
