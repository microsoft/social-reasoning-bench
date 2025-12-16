from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PatientInformation(BaseModel):
    """Basic patient details for the Plan of Care meeting"""

    name: str = Field(
        ...,
        description=(
            'Patient\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this form is completed")  # YYYY-MM-DD format

    field_30_day_initial: BooleanLike = Field(
        default="", description="Check if this is a 30-day initial Plan of Care meeting"
    )

    field_90_day_poc_follow_up: BooleanLike = Field(
        default="", description="Check if this is a 90-day follow-up Plan of Care meeting"
    )


class PlanofCareMeetingFeedback(BaseModel):
    """Patient feedback on the Plan of Care (PoC) meeting"""

    q1_strongly_agree: BooleanLike = Field(
        default="",
        description=(
            "Select if you strongly agree that you understand the purpose of your PoC meeting"
        ),
    )

    q1_agree: BooleanLike = Field(
        default="",
        description="Select if you agree that you understand the purpose of your PoC meeting",
    )

    q1_neutral: BooleanLike = Field(
        default="",
        description="Select if you feel neutral about understanding the purpose of your PoC meeting",
    )

    q1_disagree: BooleanLike = Field(
        default="",
        description="Select if you disagree that you understand the purpose of your PoC meeting",
    )

    q1_strongly_disagree: BooleanLike = Field(
        default="",
        description=(
            "Select if you strongly disagree that you understand the purpose of your PoC meeting"
        ),
    )

    q1_comments: str = Field(
        default="",
        description=(
            "Additional comments about your understanding of the purpose of your PoC "
            'meeting .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    q2_strongly_agree: BooleanLike = Field(
        default="",
        description=(
            "Select if you strongly agree that your PoC and PoC meeting are beneficial to your care"
        ),
    )

    q2_agree: BooleanLike = Field(
        default="",
        description="Select if you agree that your PoC and PoC meeting are beneficial to your care",
    )

    q2_neutral: BooleanLike = Field(
        default="",
        description=(
            "Select if you feel neutral about whether your PoC and PoC meeting are "
            "beneficial to your care"
        ),
    )

    q2_disagree: BooleanLike = Field(
        default="",
        description=(
            "Select if you disagree that your PoC and PoC meeting are beneficial to your care"
        ),
    )

    q2_strongly_disagree: BooleanLike = Field(
        default="",
        description=(
            "Select if you strongly disagree that your PoC and PoC meeting are beneficial "
            "to your care"
        ),
    )

    q2_comments: str = Field(
        default="",
        description=(
            "Additional comments about how beneficial your PoC and PoC meeting are to your "
            'care .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    q3_strongly_agree: BooleanLike = Field(
        default="",
        description=(
            "Select if you strongly agree that you feel included as a valued member of the "
            "decision-making team"
        ),
    )

    q3_agree: BooleanLike = Field(
        default="",
        description=(
            "Select if you agree that you feel included as a valued member of the "
            "decision-making team"
        ),
    )

    q3_neutral: BooleanLike = Field(
        default="",
        description=(
            "Select if you feel neutral about being included as a valued member of the "
            "decision-making team"
        ),
    )

    q3_disagree: BooleanLike = Field(
        default="",
        description=(
            "Select if you disagree that you feel included as a valued member of the "
            "decision-making team"
        ),
    )

    q3_strongly_disagree: BooleanLike = Field(
        default="",
        description=(
            "Select if you strongly disagree that you feel included as a valued member of "
            "the decision-making team"
        ),
    )

    q3_comments: str = Field(
        default="",
        description=(
            "Additional comments about feeling included as a valued member of the "
            'decision-making team .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    q4_strongly_agree: BooleanLike = Field(
        default="",
        description=(
            "Select if you strongly agree that your questions and concerns were addressed "
            "by staff during the PoC process"
        ),
    )

    q4_agree: BooleanLike = Field(
        default="",
        description=(
            "Select if you agree that your questions and concerns were addressed by staff "
            "during the PoC process"
        ),
    )

    q4_neutral: BooleanLike = Field(
        default="",
        description=(
            "Select if you feel neutral about whether your questions and concerns were "
            "addressed by staff during the PoC process"
        ),
    )

    q4_disagree: BooleanLike = Field(
        default="",
        description=(
            "Select if you disagree that your questions and concerns were addressed by "
            "staff during the PoC process"
        ),
    )

    q4_strongly_disagree: BooleanLike = Field(
        default="",
        description=(
            "Select if you strongly disagree that your questions and concerns were "
            "addressed by staff during the PoC process"
        ),
    )

    q4_comments: str = Field(
        default="",
        description=(
            "Additional comments about how your questions and concerns were addressed "
            'during the PoC process .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    q5_strongly_agree: BooleanLike = Field(
        default="",
        description=(
            "Select if you strongly agree that you are comfortable bringing questions and "
            "concerns to any staff member during your PoC meeting"
        ),
    )

    q5_agree: BooleanLike = Field(
        default="",
        description=(
            "Select if you agree that you are comfortable bringing questions and concerns "
            "to any staff member during your PoC meeting"
        ),
    )

    q5_neutral: BooleanLike = Field(
        default="",
        description=(
            "Select if you feel neutral about your comfort bringing questions and concerns "
            "to staff during your PoC meeting"
        ),
    )

    q5_disagree: BooleanLike = Field(
        default="",
        description=(
            "Select if you disagree that you are comfortable bringing questions and "
            "concerns to any staff member during your PoC meeting"
        ),
    )

    q5_strongly_disagree: BooleanLike = Field(
        default="",
        description=(
            "Select if you strongly disagree that you are comfortable bringing questions "
            "and concerns to any staff member during your PoC meeting"
        ),
    )

    q5_comments: str = Field(
        default="",
        description=(
            "Additional comments about your comfort bringing questions and concerns to "
            'staff during your PoC meeting .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class YourPlanOfCareMeeting(BaseModel):
    """
    Your Plan of Care Meeting

    Your Plan of Care (PoC) meeting brings together the people who determine the kind of care you will receive and how it will be delivered to you; it is a vital part of ensuring you receive the best and most appropriate care possible for you. Since you are the most important member of your care team, we want to know if your PoC meeting is “meeting” your needs and expectations. Please respond to the statements below and return responses to a staff member.
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    plan_of_care_meeting_feedback: PlanofCareMeetingFeedback = Field(
        ..., description="Plan of Care Meeting Feedback"
    )
