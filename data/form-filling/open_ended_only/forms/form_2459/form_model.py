from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ContactInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Basic contact and personal details"""

    your_full_name: str = Field(
        ...,
        description=(
            "Your complete legal name .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    todays_date: str = Field(
        ...,
        description="Date you are completing this form"
    )  # YYYY-MM-DD format

    phone_number: str = Field(
        ...,
        description=(
            "Your primary phone number .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    email: str = Field(
        ...,
        description=(
            "Your email address .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    address: str = Field(
        ...,
        description=(
            "Your street address .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "Your city, state, and zip code .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    occupation: str = Field(
        ...,
        description=(
            "Your current occupation .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )


class CoachingSessionBackground(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about how you heard about the coaching services and your motivation for the session"""

    how_you_heard_about_my_coaching_services_and_why_you_would_like_a_success_strategy_session: str = Field(
        ...,
        description=(
            "Describe how you heard about the coaching services and your reasons for "
            "wanting a session .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )


class SelfAssessmentRatings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Self-ratings in key areas related to focus, consistency, time management, and control"""

    focus_rating_1_10: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Rate your ability to focus from 1 (lowest) to 10 (highest)"
    )

    consistency_rating_1_10: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Rate your consistency from 1 (lowest) to 10 (highest)"
    )

    time_management_rating_1_10: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Rate your time management from 1 (lowest) to 10 (highest)"
    )

    being_in_control_rating_1_10: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Rate your sense of being in control from 1 (lowest) to 10 (highest)"
    )


class ClutterCoachStrategySessionQuestionnaireWithSueCrum(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    CLEAR YOUR CLUTTER Coach

Questionnaire for your  
Coaching Strategy Session  
with Sue Crum

    Goal: To help you reach improved levels of focus, consistency, time management and taking back control of your environments.
    Instructions: Please answer the questions below and on the following page to the best of your ability and email to me before our call.
    """

    contact_information: ContactInformation = Field(
        ...,
        description="Contact Information"
    )
    coaching_session_background: CoachingSessionBackground = Field(
        ...,
        description="Coaching Session Background"
    )
    self_assessment_ratings: SelfAssessmentRatings = Field(
        ...,
        description="Self-Assessment Ratings"
    )