from pydantic import BaseModel, ConfigDict, Field


class DuPontStateRecreationalForestCommercialUsePermitApplication(BaseModel):
    """DuPont State Recreational Forest Commercial Use Permit Application"""

    model_config = ConfigDict(extra="forbid")

    fax: str = Field(
        ..., description='Fax number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    activity_description: str = Field(
        ..., description='Description of activity/event and location. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    requested_dates: str = Field(
        ..., description='Requested date(s). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    starting_time: str = Field(
        ..., description='Starting time. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )