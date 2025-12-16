from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class NomineeInformation(BaseModel):
    """Dispatcher(s) being recognized"""

    name_of_dispatchers_you_would_like_to_recognize: str = Field(
        ...,
        description=(
            "Full name(s) of the dispatcher or dispatchers being nominated for recognition "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class SubmitterInformation(BaseModel):
    """Person completing the nomination and their contact details"""

    form_completed_by: str = Field(
        ...,
        description=(
            "Name of the person completing this nomination form .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Date this nomination form is being completed"
    )  # YYYY-MM-DD format

    e_mail: str = Field(
        ...,
        description=(
            "Email address of the person completing the form .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_phone: str = Field(
        ...,
        description=(
            "Primary phone number of the person completing the form .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    withhold_name_checkbox: BooleanLike = Field(
        default="",
        description=(
            "Select this if you want your name to remain confidential during the nomination process"
        ),
    )


class IncidentDetails(BaseModel):
    """Information about the incident related to the nomination"""

    date_of_incident: str = Field(
        ..., description="Calendar date when the incident occurred"
    )  # YYYY-MM-DD format

    nature_of_incident: str = Field(
        ...,
        description=(
            "Brief description or type of incident involved .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    time_of_incident: str = Field(
        ...,
        description=(
            "Time of day when the incident occurred .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_of_incident: str = Field(
        ...,
        description=(
            "Location where the incident took place .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class RecognitionJustification(BaseModel):
    """Reasons for the nomination and impact of the dispatcher’s actions"""

    why_does_this_employee_deserve_to_be_recognized: str = Field(
        ...,
        description=(
            "Detailed explanation of how the nominee went above the normal call of duty and "
            'demonstrated outstanding performance .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    describe_how_their_actions_assisted_you: str = Field(
        ...,
        description=(
            "Description of how the nominee’s actions directly helped or assisted you .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class StCroixCountyCommunicationsCenterNominationForAward(BaseModel):
    """St Croix County Communications Center Nomination for Award"""

    nominee_information: NomineeInformation = Field(..., description="Nominee Information")
    submitter_information: SubmitterInformation = Field(..., description="Submitter Information")
    incident_details: IncidentDetails = Field(..., description="Incident Details")
    recognition_justification: RecognitionJustification = Field(
        ..., description="Recognition Justification"
    )
