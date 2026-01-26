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
    """Information about the resident filing the complaint"""

    complaint_filed_by: str = Field(
        ...,
        description=(
            "Name of the resident submitting the complaint .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Street address of the resident submitting the complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    unit_number: str = Field(
        ...,
        description=(
            "Unit or apartment number of the resident submitting the complaint .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the resident’s address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of the resident’s address")

    zip: str = Field(..., description="ZIP code of the resident’s address")

    home_cell_number: str = Field(
        default="",
        description=(
            "Resident’s home or mobile phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    business_phone: str = Field(
        default="",
        description=(
            "Resident’s business or work phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class IncidentDetails(BaseModel):
    """Details about the incident and involved parties"""

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

    names_of_parties_involved_in_the_incident_1: str = Field(
        default="",
        description=(
            "Name or names of the first party or group involved in the incident .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    unit_if_known_1: str = Field(
        default="",
        description=(
            "Unit number of the first party involved, if known .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    names_of_parties_involved_in_the_incident_2: str = Field(
        default="",
        description=(
            "Name or names of the second party or group involved in the incident .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    unit_if_known_2: str = Field(
        default="",
        description=(
            "Unit number of the second party involved, if known .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    names_of_parties_involved_in_the_incident_3: str = Field(
        default="",
        description=(
            "Name or names of the third party or group involved in the incident .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    unit_if_known_3: str = Field(
        default="",
        description=(
            "Unit number of the third party involved, if known .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    names_of_other_witnesses_to_the_incident: str = Field(
        default="",
        description=(
            "Name or names of any other witnesses to the incident .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    unit_if_known_witness: str = Field(
        default="",
        description=(
            'Unit number of the witness, if known .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class Complaint(BaseModel):
    """Narrative description of the complaint"""

    complaint_line_1: str = Field(
        ...,
        description=(
            "First line of the detailed description of the complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    complaint_line_2: str = Field(
        default="",
        description=(
            "Second line of the detailed description of the complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    complaint_line_3: str = Field(
        default="",
        description=(
            "Third line of the detailed description of the complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    complaint_line_4: str = Field(
        default="",
        description=(
            "Fourth line of the detailed description of the complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    complaint_line_5: str = Field(
        default="",
        description=(
            "Fifth line of the detailed description of the complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    complaint_line_6: str = Field(
        default="",
        description=(
            "Sixth line of the detailed description of the complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    complaint_line_7: str = Field(
        default="",
        description=(
            "Seventh line of the detailed description of the complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    complaint_line_8: str = Field(
        default="",
        description=(
            "Eighth line of the detailed description of the complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    complaint_line_9: str = Field(
        default="",
        description=(
            "Ninth line of the detailed description of the complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    complaint_line_10: str = Field(
        default="",
        description=(
            "Tenth line of the detailed description of the complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    complaint_line_11: str = Field(
        default="",
        description=(
            "Eleventh line of the detailed description of the complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SignatureandDate(BaseModel):
    """Resident signature and date of the complaint"""

    day_of_month: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Numeric day of the month when the complaint is signed"
    )

    month: str = Field(
        ...,
        description=(
            'Month when the complaint is signed .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year when the complaint is signed"
    )

    resident_signature: str = Field(
        ...,
        description=(
            "Signature of the resident submitting the complaint .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ResidentComplaintNotice(BaseModel):
    """
    RESIDENT COMPLAINT NOTICE

    ''
    """

    resident_information: ResidentInformation = Field(..., description="Resident Information")
    incident_details: IncidentDetails = Field(..., description="Incident Details")
    complaint: Complaint = Field(..., description="Complaint")
    signature_and_date: SignatureandDate = Field(..., description="Signature and Date")
