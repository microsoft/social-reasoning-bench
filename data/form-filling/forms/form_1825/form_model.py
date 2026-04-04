from pydantic import BaseModel, ConfigDict, Field


class JamminAtTheMarketApplication(BaseModel):
    """Jammin' at the Market Application

    Solo and duo musicians submit this application to be considered for booking and paid performance slots in the City of Welland’s “Jammin’ at the Market” summer concert series at the Welland Farmers’ Market. City of Welland Recreation & Culture Division staff and/or series organizers review the performer details, demo links/materials, availability fit, and fee category to decide who is selected, schedule performance dates, and issue payment by cheque to the named payee.
    """

    model_config = ConfigDict(extra="forbid")

    entertainer_information_contact_number: str = Field(
        ...,
        description='Contact phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    entertainer_information_address: str = Field(
        ...,
        description='Mailing address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    entertainer_information_website: str = Field(
        ...,
        description='Website URL. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    entertainer_information_music_background: str = Field(
        ...,
        description='Music background/experience. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    entertainer_information_together_since: str = Field(
        ...,
        description='Together since (date/year). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    entertainer_information_genre_style: str = Field(
        ...,
        description='Genre/style. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    payment_date: str = Field(
        ...,
        description='Date (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )