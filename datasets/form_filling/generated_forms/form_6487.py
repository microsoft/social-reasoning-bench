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
    """Assessment of whether the rep had and achieved a clear goal for the call, plus related feedback."""

    did_the_sales_rep_have_a_specific_goal_for_the_call_before_the_call_began_yes: BooleanLike = Field(
        default="",
        description="Check YES if the sales rep had a specific goal for the call before it began.",
    )

    did_the_sales_rep_have_a_specific_goal_for_the_call_before_the_call_began_no: BooleanLike = (
        Field(
            default="",
            description=(
                "Check NO if the sales rep did not have a specific goal for the call before it "
                "began."
            ),
        )
    )

    was_this_goal_achieved_yes: BooleanLike = Field(
        default="",
        description="Check YES if the sales rep's stated goal for the call was achieved.",
    )

    was_this_goal_achieved_no: BooleanLike = Field(
        default="",
        description="Check NO if the sales rep's stated goal for the call was not achieved.",
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
    """Evaluation of how the rep followed and delivered the sales pitch, including product knowledge and Q&A."""

    did_the_rep_follow_your_sales_pitch_yes: BooleanLike = Field(
        default="", description="Check YES if the rep followed the prescribed sales pitch."
    )

    did_the_rep_follow_your_sales_pitch_no: BooleanLike = Field(
        default="", description="Check NO if the rep did not follow the prescribed sales pitch."
    )

    how_well_did_the_rep_deliver_the_pitch_yes: BooleanLike = Field(
        default="", description="Check YES if the rep delivered the pitch effectively."
    )

    how_well_did_the_rep_deliver_the_pitch_no: BooleanLike = Field(
        default="", description="Check NO if the rep did not deliver the pitch effectively."
    )

    did_the_rep_demonstrate_strong_product_knowledge_yes: BooleanLike = Field(
        default="", description="Check YES if the rep showed strong knowledge of the product."
    )

    did_the_rep_demonstrate_strong_product_knowledge_no: BooleanLike = Field(
        default="", description="Check NO if the rep did not show strong knowledge of the product."
    )

    was_the_rep_able_to_answer_questions_yes: BooleanLike = Field(
        default="", description="Check YES if the rep was able to answer the buyer's questions."
    )

    was_the_rep_able_to_answer_questions_no: BooleanLike = Field(
        default="", description="Check NO if the rep was not able to answer the buyer's questions."
    )

    feedback_action_points_sales_pitch: str = Field(
        default="",
        description=(
            "Provide feedback and action points related to the rep's sales pitch "
            'performance. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class InformationGatheringandBuyerRapport(BaseModel):
    """Evaluation of questioning, listening skills, and rapport-building with the buyer."""

    did_the_rep_ask_questions_that_effectively_elicited_actionable_information_from_the_buyer_yes: BooleanLike = Field(
        default="",
        description=(
            "Check YES if the rep's questions effectively elicited actionable information "
            "from the buyer."
        ),
    )

    did_the_rep_ask_questions_that_effectively_elicited_actionable_information_from_the_buyer_no: BooleanLike = Field(
        default="",
        description=(
            "Check NO if the rep's questions did not effectively elicit actionable "
            "information from the buyer."
        ),
    )

    did_the_rep_demonstrate_understanding_of_the_buyers_needs_and_empathy_yes: BooleanLike = Field(
        default="",
        description="Check YES if the rep showed understanding of the buyer's needs and empathy.",
    )

    did_the_rep_demonstrate_understanding_of_the_buyers_needs_and_empathy_no: BooleanLike = Field(
        default="",
        description=(
            "Check NO if the rep did not show understanding of the buyer's needs and empathy."
        ),
    )

    did_the_rep_practice_active_listening_yes: BooleanLike = Field(
        default="", description="Check YES if the rep practiced active listening during the call."
    )

    did_the_rep_practice_active_listening_no: BooleanLike = Field(
        default="",
        description="Check NO if the rep did not practice active listening during the call.",
    )

    did_the_rep_listen_more_than_he_or_she_talked_yes: BooleanLike = Field(
        default="", description="Check YES if the rep listened more than they talked."
    )

    did_the_rep_listen_more_than_he_or_she_talked_no: BooleanLike = Field(
        default="", description="Check NO if the rep did not listen more than they talked."
    )

    did_the_rep_interrupt_the_client_yes: BooleanLike = Field(
        default="", description="Check YES if the rep interrupted the client during the call."
    )

    did_the_rep_interrupt_the_client_no: BooleanLike = Field(
        default="", description="Check NO if the rep did not interrupt the client during the call."
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
    """
    SALES CALL REVIEW WORKSHEET

    ''
    """

    overall_call_goal: OverallCallGoal = Field(..., description="Overall Call Goal")
    sales_pitch: SalesPitch = Field(..., description="Sales Pitch")
    information_gathering_and_buyer_rapport: InformationGatheringandBuyerRapport = Field(
        ..., description="Information Gathering and Buyer Rapport"
    )
