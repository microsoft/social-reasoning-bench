from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EventOrganiserDetails(BaseModel):
    """Contact and unit details for the event organiser"""

    event_organiser_rank_and_surname: str = Field(
        ...,
        description=(
            "Rank and surname of the event organiser .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    unit_address_include_post_code_bfpo_no: str = Field(
        ...,
        description=(
            "Full unit postal address including postcode or BFPO number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            "Primary email address for correspondence about this application .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    contact_number: str = Field(
        ...,
        description=(
            "Best contact telephone number for the event organiser .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Date the application form is completed"
    )  # YYYY-MM-DD format


class EventandGrantDetails(BaseModel):
    """Core information about the event and the grant requested"""

    title_of_event: str = Field(
        ...,
        description=(
            'Official title or name of the event .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    grant_requested: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total amount of grant funding requested in pounds sterling"
    )

    account_name: str = Field(
        ...,
        description=(
            "Name of the bank account to which the grant should be paid .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    sort_code: str = Field(
        ...,
        description=(
            "Bank sort code for the account receiving the grant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    account_number: str = Field(
        ...,
        description=(
            "Bank account number for the account receiving the grant .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AttendanceandTiming(BaseModel):
    """Details of QARANC personnel attending and event dates"""

    qaranc_personnel_attending_offr: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of QARANC officers (Offr) attending the event"
    )

    qaranc_personnel_attending_snco: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of QARANC senior non-commissioned officers (SNCO) attending the event",
    )

    qaranc_personnel_attending_jnco: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of QARANC junior non-commissioned officers (JNCO) attending the event",
    )

    qaranc_personnel_attending_or: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of QARANC other ranks (OR) attending the event"
    )

    qaranc_personnel_attending_retired: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of retired QARANC personnel attending the event"
    )

    start_date: str = Field(..., description="Event start date")  # YYYY-MM-DD format

    finish_date: str = Field(..., description="Event finish date")  # YYYY-MM-DD format


class EventJustification(BaseModel):
    """Narrative description of the event and how it meets Association objectives"""

    brief_outline_aim_of_event: str = Field(
        ...,
        description=(
            "Short description of the event and its main aims .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_does_this_meet_the_objectives_of_the_qa_association: str = Field(
        ...,
        description=(
            "Explain how the event supports or aligns with the objectives of the QA "
            'Association .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class ApplicationFormForAQarancAssociationGrant(BaseModel):
    """
    APPLICATION FORM FOR A QARANC ASSOCIATION GRANT

    Applications must be fully completed and submitted to this office no later than 8 weeks before the event start date in order to be considered by the Board of Trustees. Failure to do so may jeopardise funding. Applications must be fully supported and signed by a minimum of an OF3. (Your Name with the annotation “Certified Original Signed – Lt Bloggs” is acceptable)
    """

    event_organiser_details: EventOrganiserDetails = Field(
        ..., description="Event Organiser Details"
    )
    event_and_grant_details: EventandGrantDetails = Field(
        ..., description="Event and Grant Details"
    )
    attendance_and_timing: AttendanceandTiming = Field(..., description="Attendance and Timing")
    event_justification: EventJustification = Field(..., description="Event Justification")
