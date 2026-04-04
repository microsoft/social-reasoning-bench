from pydantic import BaseModel, ConfigDict, Field


class MadesNorthNottsFoodDrinkAwardsFoodDrinkHeroForm(BaseModel):
    """Made's North Notts Food & Drink Awards - Food & Drink Hero Nomination Form

    Entrants or nominators submit this form to nominate/apply for the “Food & Drink Hero” category in Made’s North Notts Food & Drink Awards.
    Awards organizers and the judging panel review the nominee’s details, consent, and written justification (plus supporting evidence) to assess
    eligibility and decide shortlisting and winners.
    """

    model_config = ConfigDict(extra="forbid")

    section1_contact_telephone: str = Field(
        ...,
        description='Contact telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    section1_mobile: str = Field(
        ...,
        description='Mobile phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    section1_social_media_links_twitter: str = Field(
        ...,
        description='Twitter/X link/handle. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    section1_social_media_links_trip_advisor: str = Field(
        ...,
        description='Tripadvisor link. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    section1_date: str = Field(
        ...,
        description='Date (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    food_drink_hero_box1_justification_1600_words_max: str = Field(
        ...,
        description='Hero justification (max 1600 words). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    supporting_info_box2_additional_supporting_information: str = Field(
        ...,
        description='Supporting info (quals/awards/press/social). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )