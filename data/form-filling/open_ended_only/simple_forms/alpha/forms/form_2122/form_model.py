from pydantic import BaseModel, ConfigDict, Field


class ExpandedCampaignPlanningForm(BaseModel):
    """EXPANDED CAMPAIGN PLANNING FORM

    Purpose: This form is used to plan and document the details of a tabletop roleplaying game (RPG) campaign using the GURPS system, including setting, rules, and world-building elements.
    Recipient: The primary recipient is the Game Master (GM) who is organizing the campaign; it may also be shared with players for campaign overview or with other GMs for collaborative planning.
    """

    model_config = ConfigDict(extra="forbid")

    power_level: str = Field(..., description='Power level. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    realism_level: str = Field(..., description='Realism level (Grittily Realistic / Realistic / Cinematic / Over-the-Top). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    campaign_synopsis_and_recent_events: str = Field(..., description='Campaign synopsis and recent events. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    timeline_of_significant_historical_events: str = Field(..., description='Timeline of significant historical events. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    currency_3: str = Field(..., description='Currency/$ value 3. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')





    house_rules: str = Field(..., description='House rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')