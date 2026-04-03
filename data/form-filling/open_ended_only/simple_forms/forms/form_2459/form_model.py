from pydantic import BaseModel, ConfigDict, Field


class ClearYourClutterCoachQuestionnaire(BaseModel):
    """CLEAR YOUR CLUTTER Coach Questionnaire for Coaching Strategy Session"""

    model_config = ConfigDict(extra="forbid")

    personal_info_date: str = Field(
        ..., description='Today\'s date (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    personal_info_phone_number: str = Field(
        ..., description='Phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    coaching_info_how_heard_and_why: str = Field(
        ..., description='How you heard about coaching and why you want a session. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    self_rating_focus: float | None = Field(
        ..., description='Self-rating for focus (1-10)'
    )
    self_rating_consistency: float | None = Field(
        ..., description='Self-rating for consistency (1-10)'
    )
    self_rating_being_in_control: float | None = Field(
        ..., description='Self-rating for being in control (1-10)'
    )