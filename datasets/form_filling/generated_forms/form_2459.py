from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ClientInformation(BaseModel):
    """Basic contact and background information about you"""

    your_full_name: str = Field(
        ...,
        description=(
            'Your full legal name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    todays_date: str = Field(
        ..., description="Date you are completing this questionnaire"
    )  # YYYY-MM-DD format

    phone_number: str = Field(
        ...,
        description=(
            'Best phone number to reach you .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Your email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street address .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            'City, state, and ZIP/postal code .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    occupation: str = Field(
        default="",
        description=(
            "Your current occupation or primary role .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    how_you_heard_and_why_success_strategy_session: str = Field(
        ...,
        description=(
            "Describe how you heard about the coaching services and your reasons for "
            'wanting a Success Strategy Session .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class SelfRating(BaseModel):
    """Your self-assessment in key life and productivity areas"""

    focus_rating_1_10: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Your self-rating for focus on a scale from 1 (lowest) to 10 (highest)"
    )

    consistency_rating_1_10: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Your self-rating for consistency of mental and physical energy on a scale from "
            "1 (lowest) to 10 (highest)"
        ),
    )

    time_management_rating_1_10: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Your self-rating for time management on a scale from 1 (lowest) to 10 (highest)",
    )

    being_in_control_rating_1_10: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Your self-rating for feeling in control of your environments and ability to "
            "de-clutter and organize on a scale from 1 (lowest) to 10 (highest)"
        ),
    )


class ClutterCoachStrategySessionQuestionnaire(BaseModel):
    """
        CLEAR YOUR CLUTTER Coach

    Questionnaire for your Coaching Strategy Session
    with Sue Crum

        Goal: To help you reach improved levels of focus, consistency, time management and taking back control of your environments.
        Instructions: Please answer the questions below and on the following page to the best of your ability and email to me before our call.
    """

    client_information: ClientInformation = Field(..., description="Client Information")
    self_rating: SelfRating = Field(..., description="Self-Rating")
