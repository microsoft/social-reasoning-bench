from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OverallCallGoal(BaseModel):
    """Assessment of whether the rep had and achieved a clear goal for the call, plus related feedback."""

    overall_call_goal_specific_goal_before_call: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether the sales rep had a clearly defined goal before the call started."
        ),
    )

    overall_call_goal_was_goal_achieved: BooleanLike = Field(
        ..., description="Indicate whether the rep achieved the stated goal for the call."
    )

    feedback_why_goal_not_achieved_or_other_guidance: str = Field(
        default="",
        description=(
            "Provide feedback on why the goal was not achieved and any guidance or action "
            'points for improvement. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class SalesPitch(BaseModel):
    """Evaluation of how the rep delivered the sales pitch and related feedback."""

    sales_pitch_follow_sales_pitch: BooleanLike = Field(
        ..., description="Indicate whether the rep followed the prescribed sales pitch."
    )

    sales_pitch_how_well_delivered: str = Field(
        default="",
        description=(
            "Briefly rate or describe how effectively the rep delivered the pitch. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    sales_pitch_product_knowledge: BooleanLike = Field(
        ..., description="Indicate whether the rep showed strong understanding of the product."
    )

    sales_pitch_answer_questions: BooleanLike = Field(
        ...,
        description="Indicate whether the rep was able to answer the buyer’s questions effectively.",
    )

    feedback_action_points_sales_pitch: str = Field(
        default="",
        description=(
            "Provide feedback and specific action points related to the sales pitch. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class InformationGatheringandBuyerRapport(BaseModel):
    """Review of the rep’s questioning, listening skills, and rapport with the buyer, plus related feedback."""

    info_gathering_rapport_ask_effective_questions: BooleanLike = Field(
        ...,
        description="Indicate whether the rep’s questions elicited useful, actionable information.",
    )

    info_gathering_rapport_understanding_and_empathy: BooleanLike = Field(
        ...,
        description="Indicate whether the rep showed understanding of the buyer’s needs and empathy.",
    )

    info_gathering_rapport_active_listening: BooleanLike = Field(
        ..., description="Indicate whether the rep practiced active listening during the call."
    )

    info_gathering_rapport_listen_more_than_talk: BooleanLike = Field(
        ..., description="Indicate whether the rep spent more time listening than talking."
    )

    info_gathering_rapport_interrupt_client: BooleanLike = Field(
        ..., description="Indicate whether the rep interrupted the client at any point."
    )

    feedback_action_points_information_gathering_rapport: str = Field(
        default="",
        description=(
            "Provide feedback and specific action points related to information gathering "
            'and buyer rapport. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class SalesCallReviewWorksheet(BaseModel):
    """
    SALES CALL REVIEW WORKSHEET

    ''
    """

    overall_call_goal: OverallCallGoal = Field(..., description="Overall Call Goal")
    sales_pitch: SalesPitch = Field(..., description="Sales Pitch")
    information_gathering_and_buyer_rapport: InformationGatheringandBuyerRapport = Field(
        ..., description="Information Gathering and Buyer Rapport"
    )
