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
    """Assessment of the rep's call goal and related feedback"""

    did_the_sales_rep_have_a_specific_goal_for_the_call_before_the_call_began: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether the sales rep had a clearly defined goal before the call started."
        ),
    )

    did_the_sales_rep_have_a_specific_goal_for_the_call_before_the_call_began_yes: BooleanLike = (
        Field(default="", description="Check if the answer to this question is YES.")
    )

    did_the_sales_rep_have_a_specific_goal_for_the_call_before_the_call_began_no: BooleanLike = (
        Field(default="", description="Check if the answer to this question is NO.")
    )

    was_this_goal_achieved: BooleanLike = Field(
        ..., description="Indicate whether the sales rep achieved the stated call goal."
    )

    was_this_goal_achieved_yes: BooleanLike = Field(
        default="", description="Check if the goal was achieved (YES)."
    )

    was_this_goal_achieved_no: BooleanLike = Field(
        default="", description="Check if the goal was not achieved (NO)."
    )

    feedback_on_why_goal_not_achieved_or_other_guidance_action_points_to_work_on: str = Field(
        default="",
        description=(
            "Provide feedback on reasons the goal was not achieved and any guidance or "
            'action points for improvement. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class SalesPitch(BaseModel):
    """Evaluation of how the sales pitch was delivered"""

    did_the_rep_follow_your_sales_pitch: BooleanLike = Field(
        ..., description="Indicate whether the rep followed the prescribed sales pitch."
    )

    did_the_rep_follow_your_sales_pitch_yes: BooleanLike = Field(
        default="", description="Check if the rep followed the sales pitch (YES)."
    )

    did_the_rep_follow_your_sales_pitch_no: BooleanLike = Field(
        default="", description="Check if the rep did not follow the sales pitch (NO)."
    )

    how_well_did_the_rep_deliver_the_pitch: str = Field(
        default="",
        description=(
            "Describe the quality and effectiveness of the rep’s delivery of the pitch. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    did_the_rep_demonstrate_strong_product_knowledge: BooleanLike = Field(
        ..., description="Indicate whether the rep showed strong understanding of the product."
    )

    did_the_rep_demonstrate_strong_product_knowledge_yes: BooleanLike = Field(
        default="", description="Check if the rep demonstrated strong product knowledge (YES)."
    )

    did_the_rep_demonstrate_strong_product_knowledge_no: BooleanLike = Field(
        default="",
        description="Check if the rep did not demonstrate strong product knowledge (NO).",
    )

    was_the_rep_able_to_answer_questions: BooleanLike = Field(
        ..., description="Indicate whether the rep was able to answer buyer questions effectively."
    )

    was_the_rep_able_to_answer_questions_yes: BooleanLike = Field(
        default="", description="Check if the rep was able to answer questions (YES)."
    )

    was_the_rep_able_to_answer_questions_no: BooleanLike = Field(
        default="", description="Check if the rep was not able to answer questions (NO)."
    )

    feedback_action_points_sales_pitch: str = Field(
        default="",
        description=(
            "Provide feedback and specific action points related to the sales pitch "
            'section. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class InformationGatheringandBuyerRapport(BaseModel):
    """Evaluation of questioning, listening, and rapport with the buyer"""

    did_the_rep_ask_questions_that_effectively_elicited_actionable_information_from_the_buyer: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether the rep’s questions drew out useful, actionable information "
            "from the buyer."
        ),
    )

    did_the_rep_ask_questions_that_effectively_elicited_actionable_information_from_the_buyer_yes: BooleanLike = Field(
        default="",
        description="Check if the rep effectively elicited actionable information (YES).",
    )

    did_the_rep_ask_questions_that_effectively_elicited_actionable_information_from_the_buyer_no: BooleanLike = Field(
        default="",
        description="Check if the rep did not effectively elicit actionable information (NO).",
    )

    did_the_rep_demonstrate_understanding_of_the_buyers_needs_and_empathy: BooleanLike = Field(
        ...,
        description="Indicate whether the rep showed understanding of the buyer’s needs and empathy.",
    )

    did_the_rep_demonstrate_understanding_of_the_buyers_needs_and_empathy_yes: BooleanLike = Field(
        default="", description="Check if the rep demonstrated understanding and empathy (YES)."
    )

    did_the_rep_demonstrate_understanding_of_the_buyers_needs_and_empathy_no: BooleanLike = Field(
        default="",
        description="Check if the rep did not demonstrate understanding and empathy (NO).",
    )

    did_the_rep_practice_active_listening: BooleanLike = Field(
        ..., description="Indicate whether the rep practiced active listening techniques."
    )

    did_the_rep_practice_active_listening_yes: BooleanLike = Field(
        default="", description="Check if the rep practiced active listening (YES)."
    )

    did_the_rep_practice_active_listening_no: BooleanLike = Field(
        default="", description="Check if the rep did not practice active listening (NO)."
    )

    did_the_rep_listen_more_than_he_or_she_talked: BooleanLike = Field(
        ..., description="Indicate whether the rep spent more time listening than talking."
    )

    did_the_rep_listen_more_than_he_or_she_talked_yes: BooleanLike = Field(
        default="", description="Check if the rep listened more than they talked (YES)."
    )

    did_the_rep_listen_more_than_he_or_she_talked_no: BooleanLike = Field(
        default="", description="Check if the rep did not listen more than they talked (NO)."
    )

    did_the_rep_interrupt_the_client: BooleanLike = Field(
        ..., description="Indicate whether the rep interrupted the client during the call."
    )

    did_the_rep_interrupt_the_client_yes: BooleanLike = Field(
        default="", description="Check if the rep did interrupt the client (YES)."
    )

    did_the_rep_interrupt_the_client_no: BooleanLike = Field(
        default="", description="Check if the rep did not interrupt the client (NO)."
    )

    feedback_action_points_information_gathering_and_buyer_rapport: str = Field(
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
