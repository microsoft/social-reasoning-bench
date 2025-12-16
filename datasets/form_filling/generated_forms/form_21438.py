from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OccurrenceDetails(BaseModel):
    """Date, time, and location details of the occurrence"""

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

    location_of_occurrence_other: BooleanLike = Field(
        default="", description="Check if the occurrence took place at another location"
    )

    location_of_occurrence_other_specify: str = Field(
        default="",
        description=(
            "If 'Other' is selected, specify the location of occurrence .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ParticipantandGrievanceRequest(BaseModel):
    """Participant identity and preferences regarding filing the grievance and communication"""

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

    does_he_she_want_to_file_a_grievance_yes: BooleanLike = Field(
        ..., description="Select if the participant (or filer) wants to file a grievance"
    )

    does_he_she_want_to_file_a_grievance_no: BooleanLike = Field(
        ..., description="Select if the participant (or filer) does not want to file a grievance"
    )

    does_he_she_want_oral_feedback_on_the_resolution_yes: BooleanLike = Field(
        default="", description="Select if oral feedback on the grievance resolution is requested"
    )

    does_he_she_want_oral_feedback_on_the_resolution_no: BooleanLike = Field(
        default="",
        description="Select if oral feedback on the grievance resolution is not requested",
    )

    does_he_she_want_an_official_letter_regarding_the_receipt_of_the_grievance_mailed_to_them_yes: BooleanLike = Field(
        default="", description="Select if an official acknowledgment letter should be mailed"
    )

    does_he_she_want_an_official_letter_regarding_the_receipt_of_the_grievance_mailed_to_them_no: BooleanLike = Field(
        default="", description="Select if an official acknowledgment letter should not be mailed"
    )

    does_a_sdr_service_delivery_request_need_to_be_completed_yes: BooleanLike = Field(
        default="", description="Select if a Service Delivery Request (SDR) is required"
    )

    does_a_sdr_service_delivery_request_need_to_be_completed_no: BooleanLike = Field(
        default="", description="Select if a Service Delivery Request (SDR) is not required"
    )


class GrievanceDescription(BaseModel):
    """Narrative description of the grievance"""

    brief_description_of_grievance: str = Field(
        ...,
        description=(
            "Provide a brief description of the grievance or concern .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Resolution(BaseModel):
    """Staff information and description of the resolution"""

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
            "Summarize how the grievance was resolved .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class InternalFormlogoSeniorCarePartnersPaceParticipantGrievanceForm(BaseModel):
    """
        INTERNAL FORM

    [Logo] Senior Care Partners P.A.C.E.

    Participant Grievance Form

        ''
    """

    occurrence_details: OccurrenceDetails = Field(..., description="Occurrence Details")
    participant_and_grievance_request: ParticipantandGrievanceRequest = Field(
        ..., description="Participant and Grievance Request"
    )
    grievance_description: GrievanceDescription = Field(..., description="Grievance Description")
    resolution: Resolution = Field(..., description="Resolution")
