from pydantic import BaseModel, ConfigDict, Field


class JamminAtTheMarketApplication(BaseModel):
    """JAMMIN' AT THE MARKET APPLICATION"""

    model_config = ConfigDict(extra="forbid")

    entertainer_information_contact_number: str = Field(
        ..., description='Contact phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    entertainer_information_music_background: str = Field(
        ..., description='Music background/experience. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    entertainer_information_date: str = Field(
        ..., description='Date of application (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )