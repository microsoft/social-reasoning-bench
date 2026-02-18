from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OccurrenceReportingDetails(BaseModel):
    """Date, time, and reporting information for the grievance event"""

    date_of_occurrence: str = Field(
        ..., description="Date when the grievance-related event occurred"
    )  # YYYY-MM-DD format

    time_of_occurrence: str = Field(
        ...,
        description=(
            "Time when the grievance-related event occurred .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_reported: str = Field(
        ..., description="Date when the grievance was reported"
    )  # YYYY-MM-DD format

    location_of_occurrence_home: BooleanLike = Field(
        default="", description="Check if the occurrence took place at the participant's home"
    )

    location_of_occurrence_center: BooleanLike = Field(
        default="", description="Check if the occurrence took place at the center"
    )

    location_of_occurrence_transportation: BooleanLike = Field(
        default="", description="Check if the occurrence took place during transportation"
    )

    location_of_occurrence_other: str = Field(
        default="",
        description=(
            "If the location is not home, center, or transportation, specify the other "
            'location .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class ParticipantGrievancePreferences(BaseModel):
    """Participant identity and preferences regarding the grievance and follow-up"""

    participant_name: str = Field(
        ...,
        description=(
            'Full name of the participant involved .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_relationship_of_person_filing_the_grievance_if_other_than_participant: str = Field(
        default="",
        description=(
            "Name and relationship of the person filing the grievance, if not the "
            'participant .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    wants_to_file_grievance_yes: BooleanLike = Field(
        ..., description="Select Yes if the participant wants to file a grievance"
    )

    wants_to_file_grievance_no: BooleanLike = Field(
        ..., description="Select No if the participant does not want to file a grievance"
    )

    wants_oral_feedback_yes: BooleanLike = Field(
        default="",
        description="Select Yes if the participant wants oral feedback on the resolution",
    )

    wants_oral_feedback_no: BooleanLike = Field(
        default="",
        description="Select No if the participant does not want oral feedback on the resolution",
    )

    wants_official_letter_yes: BooleanLike = Field(
        default="",
        description=(
            "Select Yes if the participant wants an official letter mailed to them "
            "acknowledging receipt of the grievance"
        ),
    )

    wants_official_letter_no: BooleanLike = Field(
        default="",
        description="Select No if the participant does not want an official letter mailed to them",
    )

    sdr_needed_yes: BooleanLike = Field(
        default="",
        description="Select Yes if a Service Delivery Request (SDR) needs to be completed",
    )

    sdr_needed_no: BooleanLike = Field(
        default="",
        description="Select No if a Service Delivery Request (SDR) does not need to be completed",
    )


class GrievanceResolutionDetails(BaseModel):
    """Narrative description of the grievance and its resolution, plus form completer"""

    brief_description_of_grievance: str = Field(
        ...,
        description=(
            "Narrative description of the grievance or concern .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_and_title_of_person_completing_form: str = Field(
        ...,
        description=(
            "Name and job title of the person completing this form .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    brief_description_of_resolution: str = Field(
        default="",
        description=(
            "Summary of how the grievance was addressed or resolved .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class InternalFormSeniorCarePartnersPaceParticipantGrievanceForm(BaseModel):
    """
        INTERNAL FORM

    Senior Care Partners P.A.C.E.

    Participant Grievance Form

        ''
    """

    occurrence__reporting_details: OccurrenceReportingDetails = Field(
        ..., description="Occurrence & Reporting Details"
    )
    participant__grievance_preferences: ParticipantGrievancePreferences = Field(
        ..., description="Participant & Grievance Preferences"
    )
    grievance__resolution_details: GrievanceResolutionDetails = Field(
        ..., description="Grievance & Resolution Details"
    )
