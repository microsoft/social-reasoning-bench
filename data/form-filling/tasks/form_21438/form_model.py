from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class GrievanceDetails(BaseModel):
    """Core information about the grievance event and participant preferences"""

    date_of_occurrence: str = Field(
        ..., description="Date when the grievance-related incident occurred"
    )  # YYYY-MM-DD format

    time_of_occurrence: str = Field(
        ...,
        description=(
            "Time when the grievance-related incident occurred .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_reported: str = Field(
        ..., description="Date when the grievance was reported"
    )  # YYYY-MM-DD format

    participant_name: str = Field(
        ...,
        description=(
            "Full name of the participant involved in the grievance .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_relationship_of_person_filing_the_grievance_if_other_than_participant: str = Field(
        default="",
        description=(
            "Name and relationship to the participant of the person filing the grievance, "
            'if not the participant .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    does_he_she_want_to_file_a_grievance: BooleanLike = Field(
        ..., description="Indicate whether the participant wants to file a grievance"
    )

    does_he_she_want_to_file_a_grievance_no: BooleanLike = Field(
        ..., description="Indicate whether the participant does not want to file a grievance"
    )

    does_he_she_want_oral_feedback_on_the_resolution: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the participant wants oral feedback on the grievance resolution"
        ),
    )

    does_he_she_want_oral_feedback_on_the_resolution_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the participant does not want oral feedback on the grievance "
            "resolution"
        ),
    )

    does_he_she_want_an_official_letter_regarding_the_receipt_of_the_grievance_mailed_to_them: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the participant wants an official letter acknowledging "
            "receipt of the grievance mailed to them"
        ),
    )

    does_he_she_want_an_official_letter_regarding_the_receipt_of_the_grievance_mailed_to_them_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the participant does not want an official letter "
            "acknowledging receipt of the grievance mailed to them"
        ),
    )

    does_a_sdr_service_delivery_request_need_to_be_completed: BooleanLike = Field(
        default="",
        description="Indicate whether a Service Delivery Request (SDR) needs to be completed",
    )

    does_a_sdr_service_delivery_request_need_to_be_completed_no: BooleanLike = Field(
        default="",
        description="Indicate whether a Service Delivery Request (SDR) does not need to be completed",
    )

    location_of_occurrence_home: Literal["Home", "Center", "Transportation", "Other", "N/A", ""] = (
        Field(
            ...,
            description=(
                "Select the location where the incident occurred; choose Home if it occurred at "
                "the participant's home"
            ),
        )
    )

    location_of_occurrence_center: Literal[
        "Home", "Center", "Transportation", "Other", "N/A", ""
    ] = Field(
        ...,
        description=(
            "Select the location where the incident occurred; choose Center if it occurred "
            "at the center"
        ),
    )

    location_of_occurrence_transportation: Literal[
        "Home", "Center", "Transportation", "Other", "N/A", ""
    ] = Field(
        ...,
        description=(
            "Select the location where the incident occurred; choose Transportation if it "
            "occurred during transport"
        ),
    )

    location_of_occurrence_other: str = Field(
        default="",
        description=(
            "If the location is not Home, Center, or Transportation, specify the other "
            'location .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    brief_description_of_grievance: str = Field(
        ...,
        description=(
            "Narrative description of the grievance and relevant details .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ResolutionInformation(BaseModel):
    """Information about who completed the form and how the grievance was resolved"""

    name_and_title_of_person_completing_form: str = Field(
        ...,
        description=(
            "Name and job title of the staff member completing this form .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    brief_description_of_resolution: str = Field(
        default="",
        description=(
            "Summary of how the grievance was addressed and resolved .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class InternalFormSeniorCarePartnersPaceParticipantGrievanceForm(BaseModel):
    """
        INTERNAL FORM

    Senior Care
    Partners P.A.C.E.

    Participant Grievance Form

        ''
    """

    grievance_details: GrievanceDetails = Field(..., description="Grievance Details")
    resolution_information: ResolutionInformation = Field(..., description="Resolution Information")
