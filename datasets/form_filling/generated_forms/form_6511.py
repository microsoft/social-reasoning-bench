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
    """Basic details about the applicant and their organisation"""

    name: str = Field(
        ...,
        description=(
            'Applicant\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    company: str = Field(
        default="",
        description=(
            'Name of your company or organisation .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Your mailing address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    invoice_address_if_different: str = Field(
        default="",
        description=(
            "Billing or invoice address if different from your main address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            'Primary contact telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Primary contact email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class TrainingBackground(BaseModel):
    """Coach/supervision related training qualifications and certifications"""

    coach_supervision_related_training_qualifications_and_certifications_including_the_date_duration_and_level: str = Field(
        ...,
        description=(
            "List your coach/supervision related training, qualifications, and "
            "certifications, including date, duration, and level .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CoachingExperience(BaseModel):
    """Experience duration in different coaching roles"""

    how_long_have_you_been_practicing_as_a_coach_a_coach: str = Field(
        default="",
        description=(
            "Length of time you have been practicing as an individual coach .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    how_long_have_you_been_practicing_as_a_coach_team_coach: str = Field(
        default="",
        description=(
            "Length of time you have been practicing as a team coach .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_long_have_you_been_practicing_as_a_coach_coach_supervisor: str = Field(
        default="",
        description=(
            "Length of time you have been practicing as a coach supervisor .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    how_long_have_you_been_practicing_as_a_coach_other: str = Field(
        default="",
        description=(
            "Length of time you have been practicing in any other related coaching role "
            '(please specify) .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class TeamCoachingSupervisionTrainingProgramme(BaseModel):
    """
        Team Coaching Supervision
    Training Programme

        ''
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    training_background: TrainingBackground = Field(..., description="Training Background")
    coaching_experience: CoachingExperience = Field(..., description="Coaching Experience")
