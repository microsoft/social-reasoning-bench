from pydantic import BaseModel, ConfigDict, Field


class ExpandedCampaignPlanningForm(BaseModel):
    """EXPANDED CAMPAIGN PLANNING FORM"""

    model_config = ConfigDict(extra="forbid")

    gurps_campaign_prospectus_gm: str = Field(
        ..., description='Game master name. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    gurps_campaign_prospectus_creation_date: str = Field(
        ..., description='Creation date (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    gurps_campaign_prospectus_genre: str = Field(
        ..., description='Campaign genre. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    gurps_campaign_prospectus_tl_exceptions: str = Field(
        ..., description='Tech level exceptions. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    gurps_campaign_prospectus_power_level: str = Field(
        ..., description='Power level. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    gurps_campaign_prospectus_realism_level: str = Field(
        ..., description='Realism level. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    gurps_campaign_prospectus_campaign_synopsis_and_recent_events: str = Field(
        ..., description='Campaign synopsis and recent events. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    gurps_campaign_prospectus_timeline_of_significant_historical_events: str = Field(
        ..., description='Timeline of significant historical events. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )





    rules_house_rules: str = Field(
        ..., description='House rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )