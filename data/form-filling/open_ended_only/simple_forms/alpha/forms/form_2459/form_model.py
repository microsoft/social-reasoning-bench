from pydantic import BaseModel, ConfigDict, Field


class ClearYourClutterCoachQuestionnaire(BaseModel):
    """CLEAR YOUR CLUTTER Coach Questionnaire for your Coaching Strategy Session

    Purpose: Pre-coaching questionnaire to assess a potential client's needs, goals, and current challenges in focus, consistency, time management, and organization before a coaching strategy session.
    Recipient: Sue Crum, the Clear Your Clutter Coach, who will use the information to prepare for and tailor the upcoming coaching strategy session with the client.
    """

    model_config = ConfigDict(extra="forbid")

    personal_phone_number: str = Field(..., description='Phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    referral_and_reason: str = Field(..., description='How you heard about coaching and why you want a session. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    self_rating_focus: float | None = Field(..., description='Self-rating for Focus (1-10)')
    self_rating_consistency: float | None = Field(..., description='Self-rating for Consistency (1-10)')