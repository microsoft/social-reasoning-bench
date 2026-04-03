from pydantic import BaseModel, ConfigDict, Field


class JamminAtMarketApplication(BaseModel):
    """JAMMIN' AT THE MARKET APPLICATION

    Purpose: Application form for solo and duet musicians to be considered for performance slots in the Jammin' at the Market summer concert series at the Welland Farmers' Market.
    Recipient: Staff members of the City of Welland Recreation & Culture Division who organize and select performers for the concert series; they do not personally know the applicants.
    """

    model_config = ConfigDict(extra="forbid")

    entertainer_contact_number: str = Field(
        ..., description='Contact phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    entertainer_address: str = Field(
        ..., description='Mailing address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    entertainer_music_background: str = Field(
        ..., description='Music background/biography. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    entertainer_date: str = Field(
        ..., description='Date of application (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )