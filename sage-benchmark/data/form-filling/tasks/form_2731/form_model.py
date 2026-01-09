from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Basic information about the applicant and academic status"""

    name: str = Field(
        ...,
        description=(
            'Applicant\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this application is completed")  # YYYY-MM-DD format

    year_in_school_and_aias_position: str = Field(
        ...,
        description=(
            "Current year in school and any AIAS position or role held .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    expected_date_of_graduation: str = Field(
        ...,
        description=(
            'Expected month and year of graduation .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    program_undergraduate: BooleanLike = Field(
        ..., description="Check if you are enrolled in an undergraduate program"
    )

    program_graduate: BooleanLike = Field(
        ..., description="Check if you are enrolled in a graduate program"
    )

    how_long_have_you_been_involved_in_aias: str = Field(
        ...,
        description=(
            "Length of time you have been involved in AIAS (e.g., number of years or "
            'semesters) .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class InterestsandGoals(BaseModel):
    """Applicant’s aspirations and interest in the conference"""

    future_aspirations_after_graduation_brief_statement: str = Field(
        ...,
        description=(
            "Brief description of your goals and plans after graduation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    specific_interest_in_participating_in_conference: str = Field(
        ...,
        description=(
            "Describe any specific interests or areas you are most looking forward to in "
            'the conference .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class AvailabilityandPreferences(BaseModel):
    """Preferences for in-person meet-up and anticipated school schedule"""

    comfortable_with_small_in_person_meetup_yes: BooleanLike = Field(
        ..., description="Select if you would be comfortable with a small in-person meet-up"
    )

    comfortable_with_small_in_person_meetup_no: BooleanLike = Field(
        ..., description="Select if you would NOT be comfortable with a small in-person meet-up"
    )

    indication_of_fall_school_schedule: str = Field(
        ...,
        description=(
            "Describe your anticipated school schedule for the fall term .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class AiAspireAiaIllinoisAiaIllinois2021StudentLeadershipConference(BaseModel):
    """
        AI Aspire  AIA Illinois
    AIA Illinois 2021 Student Leadership Conference

        AIA Illinois 2021 Student Leadership Conference 2021 Application | September 10–11, 2021. Make plans to participate via Zoom. All applicants must submit a resume (one page maximum) and a brief and specific statement of why they would like to attend this event. Feel free to elaborate on your experiences in AIAS and other leadership roles. AIA Illinois welcomes current architecture students who wish to participate in two half days (Friday afternoon and Saturday morning) filled with unique learning and networking opportunities.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    interests_and_goals: InterestsandGoals = Field(..., description="Interests and Goals")
    availability_and_preferences: AvailabilityandPreferences = Field(
        ..., description="Availability and Preferences"
    )
