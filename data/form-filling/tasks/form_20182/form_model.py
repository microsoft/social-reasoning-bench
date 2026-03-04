from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ResidentInformation(BaseModel):
    """Contact and address information for the resident filing the complaint"""

    complaint_filed_by: str = Field(
        ...,
        description=(
            "Name of the resident filing the complaint .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Street address of the unit where the resident lives .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    unit_number: str = Field(
        ...,
        description=(
            "Unit or apartment number of the resident filing the complaint .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the resident\'s address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of the resident's address")

    zip: str = Field(..., description="Zip code of the resident's address")

    home_cell_number: str = Field(
        ...,
        description=(
            'Resident\'s home or cell phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    business_phone: str = Field(
        default="",
        description=(
            "Resident's business or work phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class IncidentDetails(BaseModel):
    """Details about when the incident occurred and who was involved"""

    date_of_incident: str = Field(
        ..., description="Calendar date when the incident occurred"
    )  # YYYY-MM-DD format

    time_of_incident: str = Field(
        ...,
        description=(
            "Approximate time when the incident occurred .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_party_1: str = Field(
        default="",
        description=(
            "Name of a party involved in the incident (first entry) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    unit_if_known_1: str = Field(
        default="",
        description=(
            "Unit number of this party, if known (first entry) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_party_2: str = Field(
        default="",
        description=(
            "Name of a party involved in the incident (second entry) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    unit_if_known_2: str = Field(
        default="",
        description=(
            "Unit number of this party, if known (second entry) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_party_3: str = Field(
        default="",
        description=(
            "Name of a party involved in the incident (third entry) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    unit_if_known_3: str = Field(
        default="",
        description=(
            "Unit number of this party, if known (third entry) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_other_witnesses: str = Field(
        default="",
        description=(
            "Name of another witness to the incident .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    unit_of_other_witness_if_known: str = Field(
        default="",
        description=(
            'Unit number of the witness, if known .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ComplaintDescription(BaseModel):
    """Narrative description of the complaint"""

    complaint: str = Field(
        ...,
        description=(
            "Detailed description of the complaint and incident .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SignatureandDate(BaseModel):
    """Date and resident signature for the complaint notice"""

    dated_this: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day of the month when this notice is signed"
    )

    day_of: str = Field(
        ...,
        description=(
            'Month when this notice is signed .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    year_20: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year when this notice is signed (last two digits)"
    )

    resident_signature: str = Field(
        ...,
        description=(
            "Signature of the resident filing the complaint .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class RhawaRentalHousingAssociationOfWaResidentComplaintNotice(BaseModel):
    """
        RHAWA
    Rental Housing Association of WA

    RESIDENT COMPLAINT NOTICE

        ''
    """

    resident_information: ResidentInformation = Field(..., description="Resident Information")
    incident_details: IncidentDetails = Field(..., description="Incident Details")
    complaint_description: ComplaintDescription = Field(..., description="Complaint Description")
    signature_and_date: SignatureandDate = Field(..., description="Signature and Date")
