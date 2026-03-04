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
    """Basic identifying information for the patient"""

    name: str = Field(
        ...,
        description=(
            'Patient\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this form is completed")  # YYYY-MM-DD format


class PlanofCareMeetingFeedback(BaseModel):
    """Patient feedback about the Plan of Care (PoC) meeting"""

    field_30_day_initial: BooleanLike = Field(
        default="", description="Check if this is the 30-day (initial) Plan of Care meeting"
    )

    field_90_day_poc_follow_up: BooleanLike = Field(
        default="", description="Check if this is the 90-day Plan of Care (follow-up) meeting"
    )

    q1_understand_purpose_level_of_agreement: Literal[
        "Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree", "N/A", ""
    ] = Field(
        ...,
        description=(
            "Select how strongly you agree that you understand the purpose of your PoC meeting"
        ),
    )

    q1_comments_line_1: str = Field(
        default="",
        description=(
            "First line of comments about your understanding of the PoC meeting .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    q1_comments_line_2: str = Field(
        default="",
        description=(
            "Second line of comments about your understanding of the PoC meeting .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    q1_comments_line_3: str = Field(
        default="",
        description=(
            "Third line of comments about your understanding of the PoC meeting .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    q2_beneficial_to_care_level_of_agreement: Literal[
        "Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree", "N/A", ""
    ] = Field(
        ...,
        description=(
            "Select how strongly you agree that your PoC and PoC meeting are beneficial to "
            "your care"
        ),
    )

    q2_comments_line_1: str = Field(
        default="",
        description=(
            "First line of comments about how beneficial the PoC and meeting are to your "
            'care .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    q2_comments_line_2: str = Field(
        default="",
        description=(
            "Second line of comments about how beneficial the PoC and meeting are to your "
            'care .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    q2_comments_line_3: str = Field(
        default="",
        description=(
            "Third line of comments about how beneficial the PoC and meeting are to your "
            'care .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    q3_included_as_valued_member_level_of_agreement: Literal[
        "Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree", "N/A", ""
    ] = Field(
        ...,
        description=(
            "Select how strongly you agree that you feel included as a valued member of the "
            "decision-making team"
        ),
    )

    q3_comments_line_1: str = Field(
        default="",
        description=(
            "First line of comments about feeling included as a valued team member .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    q3_comments_line_2: str = Field(
        default="",
        description=(
            "Second line of comments about feeling included as a valued team member .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    q3_comments_line_3: str = Field(
        default="",
        description=(
            "Third line of comments about feeling included as a valued team member .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    q4_questions_addressed_level_of_agreement: Literal[
        "Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree", "N/A", ""
    ] = Field(
        ...,
        description=(
            "Select how strongly you agree that your questions and concerns were addressed "
            "by staff during the PoC process"
        ),
    )

    q4_comments_line_1: str = Field(
        default="",
        description=(
            "First line of comments about how your questions and concerns were addressed "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    q4_comments_line_2: str = Field(
        default="",
        description=(
            "Second line of comments about how your questions and concerns were addressed "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    q4_comments_line_3: str = Field(
        default="",
        description=(
            "Third line of comments about how your questions and concerns were addressed "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    q5_comfortable_bringing_questions_level_of_agreement: Literal[
        "Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree", "N/A", ""
    ] = Field(
        ...,
        description=(
            "Select how strongly you agree that you are comfortable bringing questions and "
            "concerns to any staff member during your PoC meeting"
        ),
    )

    q5_comments_line_1: str = Field(
        default="",
        description=(
            "First line of comments about your comfort bringing questions and concerns to "
            'staff .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    q5_comments_line_2: str = Field(
        default="",
        description=(
            "Second line of comments about your comfort bringing questions and concerns to "
            'staff .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    q5_comments_line_3: str = Field(
        default="",
        description=(
            "Third line of comments about your comfort bringing questions and concerns to "
            'staff .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class HsagEsrdNetwork15PlanOfCareMeeting(BaseModel):
    """
        HSAG HEALTH SERVICES ADVISORY GROUP
    ESRD Network 15

    Your Plan of Care Meeting

        Your Plan of Care (PoC) meeting brings together the people who determine the kind of care you will receive and how it will be delivered to you; it is a vital part of ensuring you receive the best and most appropriate care possible for you. Since you are the most important member of your care team, we want to know if your PoC meeting is “meeting” your needs and expectations. Please respond to the statements below and return responses to a staff member.
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    plan_of_care_meeting_feedback: PlanofCareMeetingFeedback = Field(
        ..., description="Plan of Care Meeting Feedback"
    )
