from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class VolunteerAvailability(BaseModel):
    """Days and times you are available to volunteer"""

    morning_monday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer Monday morning (9–noon)."
    )

    morning_tuesday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer Tuesday morning (9–noon)."
    )

    morning_wednesday: BooleanLike = Field(
        default="",
        description="Check if you are available to volunteer Wednesday morning (9–noon).",
    )

    morning_thursday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer Thursday morning (9–noon)."
    )

    morning_friday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer Friday morning (9–noon)."
    )

    morning_saturday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer Saturday morning (9–noon)."
    )

    morning_sunday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer Sunday morning (9–noon)."
    )

    afternoon_monday: BooleanLike = Field(
        default="",
        description="Check if you are available to volunteer Monday afternoon (12–5 pm).",
    )

    afternoon_tuesday: BooleanLike = Field(
        default="",
        description="Check if you are available to volunteer Tuesday afternoon (12–5 pm).",
    )

    afternoon_wednesday: BooleanLike = Field(
        default="",
        description="Check if you are available to volunteer Wednesday afternoon (12–5 pm).",
    )

    afternoon_thursday: BooleanLike = Field(
        default="",
        description="Check if you are available to volunteer Thursday afternoon (12–5 pm).",
    )

    afternoon_friday: BooleanLike = Field(
        default="",
        description="Check if you are available to volunteer Friday afternoon (12–5 pm).",
    )

    afternoon_saturday: BooleanLike = Field(
        default="",
        description="Check if you are available to volunteer Saturday afternoon (12–5 pm).",
    )

    afternoon_sunday: BooleanLike = Field(
        default="",
        description="Check if you are available to volunteer Sunday afternoon (12–5 pm).",
    )

    evening_monday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer Monday evening (5–9 pm)."
    )

    evening_tuesday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer Tuesday evening (5–9 pm)."
    )

    evening_wednesday: BooleanLike = Field(
        default="",
        description="Check if you are available to volunteer Wednesday evening (5–9 pm).",
    )

    evening_thursday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer Thursday evening (5–9 pm)."
    )

    evening_friday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer Friday evening (5–9 pm)."
    )

    evening_saturday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer Saturday evening (5–9 pm)."
    )

    evening_sunday: BooleanLike = Field(
        default="", description="Check if you are available to volunteer Sunday evening (5–9 pm)."
    )


class VolunteerBackground(BaseModel):
    """Questions about your interests, experience, and motivation"""

    how_did_you_hear_about_the_family_effect: str = Field(
        default="",
        description=(
            "Describe how you first learned about The Family Effect. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    why_do_you_want_to_volunteer_with_us: str = Field(
        default="",
        description=(
            "Explain your reasons and motivation for volunteering with The Family Effect. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    what_special_skills_and_or_qualifications_do_you_have_to_contribute: str = Field(
        default="",
        description=(
            "List any relevant skills, experience, or qualifications you can offer. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    what_are_your_hobbies_and_interests: str = Field(
        default="",
        description=(
            "Share your hobbies and personal interests. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    what_was_your_most_memorable_volunteer_experience_why: str = Field(
        default="",
        description=(
            "Describe a memorable volunteer experience and why it was meaningful. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ApplicantAcknowledgment(BaseModel):
    """Signature confirming you have read and understand the application process"""

    name: str = Field(
        ...,
        description=(
            'Volunteer’s full name. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the application is signed.")  # YYYY-MM-DD format

    signature: str = Field(
        ...,
        description=(
            "Applicant’s signature acknowledging understanding of the volunteer application "
            'process. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class VolunteerApplication(BaseModel):
    """
    Volunteer Application

    Please read through the easy application steps on the next page. By signing below, you acknowledge that you have read and understand our volunteer application process. Once you have sent us your completed application, you will be contacted by Sarae Smith for a friendly interview. We’ll make it quick and easy for you to get started.
    """

    volunteer_availability: VolunteerAvailability = Field(..., description="Volunteer Availability")
    volunteer_background: VolunteerBackground = Field(..., description="Volunteer Background")
    applicant_acknowledgment: ApplicantAcknowledgment = Field(
        ..., description="Applicant Acknowledgment"
    )
