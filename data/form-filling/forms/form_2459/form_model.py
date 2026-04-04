from pydantic import BaseModel, ConfigDict, Field


class ClearYourClutterCoachingStrategySessionQuestionnaire(BaseModel):
    """CLEAR YOUR CLUTTER Coach Questionnaire for your Coaching Strategy Session with Sue Crum

    Clients complete this pre-session questionnaire and email it to Sue Crum before a coaching
    strategy call. Sue (and possibly her coaching/administrative staff) reviews the client’s
    contact details, background, and self-ratings in key areas (focus, consistency, time
    management, and being in control) to tailor the session agenda and coaching approach.
    """

    model_config = ConfigDict(extra="forbid")

    contact_info_todays_date: str = Field(
        ...,
        description='Today’s date (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    contact_info_phone_number: str = Field(
        ...,
        description='Phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    background_referral_and_reason: str = Field(
        ...,
        description='How heard + why want session. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    self_rating_focus_1_to_10: float | None = Field(
        ...,
        description="Focus rating (1-10)",
    )
    self_rating_consistency_1_to_10: float | None = Field(
        ...,
        description="Consistency rating (1-10)",
    )
    self_rating_being_in_control_1_to_10: float | None = Field(
        ...,
        description="Being in control rating (1-10)",
    )