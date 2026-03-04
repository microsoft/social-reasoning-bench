from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OverallCallGoal(BaseModel):
    """Assessment of whether the rep had and achieved a clear goal for the call"""

    overall_call_goal_yes: BooleanLike = Field(
        default="", description="Mark YES if the overall call goal section is rated positively."
    )

    overall_call_goal_no: BooleanLike = Field(
        default="", description="Mark NO if the overall call goal section is not rated positively."
    )

    field_1_did_the_sales_rep_have_a_specific_goal_for_the_call_before_the_call_began: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the sales rep had a clear, specific goal before the call started."
        ),
    )

    field_2_was_this_goal_achieved: BooleanLike = Field(
        default="",
        description="Indicate whether the sales rep achieved the stated goal for the call.",
    )

    feedback_on_why_goal_not_achieved_or_other_guidance_action_points_to_work_on: str = Field(
        default="",
        description=(
            "Provide feedback on why the goal was not achieved and any guidance or action "
            'points for improvement. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class SalesPitch(BaseModel):
    """Evaluation of how the rep delivered the sales pitch and demonstrated product knowledge"""

    sales_pitch_yes: BooleanLike = Field(
        default="", description="Mark YES if the sales pitch section is rated positively overall."
    )

    sales_pitch_no: BooleanLike = Field(
        default="",
        description="Mark NO if the sales pitch section is not rated positively overall.",
    )

    field_3_did_the_rep_follow_your_sales_pitch: BooleanLike = Field(
        default="", description="Indicate whether the rep followed the prescribed sales pitch."
    )

    field_4_how_well_did_the_rep_deliver_the_pitch: str = Field(
        default="",
        description=(
            "Briefly rate or describe how effectively the rep delivered the pitch. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    field_5_did_the_rep_demonstrate_strong_product_knowledge: BooleanLike = Field(
        default="",
        description="Indicate whether the rep showed strong understanding of the product.",
    )

    field_6_was_the_rep_able_to_answer_questions: BooleanLike = Field(
        default="",
        description="Indicate whether the rep was able to answer the buyer’s questions effectively.",
    )

    feedback_action_points_sales_pitch: str = Field(
        default="",
        description=(
            "Provide feedback and action points related to the sales pitch performance. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class InformationGatheringandBuyerRapport(BaseModel):
    """Evaluation of questioning, listening skills, and rapport with the buyer"""

    information_gathering_and_buyer_rapport_yes: BooleanLike = Field(
        default="",
        description=(
            "Mark YES if the information gathering and buyer rapport section is rated "
            "positively overall."
        ),
    )

    information_gathering_and_buyer_rapport_no: BooleanLike = Field(
        default="",
        description=(
            "Mark NO if the information gathering and buyer rapport section is not rated "
            "positively overall."
        ),
    )

    field_7_did_the_rep_ask_questions_that_effectively_elicited_actionable_information_from_the_buyer: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the rep’s questions elicited useful, actionable information "
            "from the buyer."
        ),
    )

    field_8_did_the_rep_demonstrate_understanding_of_the_buyers_needs_and_empathy: BooleanLike = Field(
        default="",
        description="Indicate whether the rep showed understanding of the buyer’s needs and empathy.",
    )

    field_9_did_the_rep_practice_active_listening: BooleanLike = Field(
        default="",
        description="Indicate whether the rep practiced active listening during the call.",
    )

    field_10_did_the_rep_listen_more_than_he_or_she_talked: BooleanLike = Field(
        default="", description="Indicate whether the rep spent more time listening than talking."
    )

    field_11_did_the_rep_interrupt_the_client: BooleanLike = Field(
        default="", description="Indicate whether the rep interrupted the client during the call."
    )

    feedback_action_points_information_gathering_and_buyer_rapport: str = Field(
        default="",
        description=(
            "Provide feedback and action points related to information gathering and buyer "
            'rapport. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class SalesCallReviewWorksheet(BaseModel):
    """SALES CALL REVIEW WORKSHEET"""

    overall_call_goal: OverallCallGoal = Field(..., description="Overall Call Goal")
    sales_pitch: SalesPitch = Field(..., description="Sales Pitch")
    information_gathering_and_buyer_rapport: InformationGatheringandBuyerRapport = Field(
        ..., description="Information Gathering and Buyer Rapport"
    )
