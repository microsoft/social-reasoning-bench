from pydantic import BaseModel, ConfigDict, Field


class SalesCallReviewWorksheet(BaseModel):
    """SALES CALL REVIEW WORKSHEET

    Sales managers, team leads, coaches, or QA/training staff use this worksheet to
    review a recorded or observed sales call and score the rep on goal-setting,
    pitch execution, product knowledge, and rapport-building. The evaluator records
    yes/no assessments and written feedback/action items, which the sales rep and
    leadership use to decide coaching priorities and next steps for improvement.
    """

    model_config = ConfigDict(extra="forbid")

    overall_call_goal_feedback_action_points: str = Field(
        ...,
        description='Goal not achieved feedback/action points. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    sales_pitch_how_well_deliver_pitch: str = Field(
        ...,
        description='Pitch delivery rating/notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    sales_pitch_feedback_action_points: str = Field(
        ...,
        description='Pitch feedback/action points. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    info_gathering_feedback_action_points: str = Field(
        ...,
        description='Info gathering/rapport feedback. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )