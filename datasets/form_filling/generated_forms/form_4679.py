from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Workshops(BaseModel):
    """Morning workshops interest and preferences"""

    are_you_interested_in_joining_the_workshops: Literal[
        "Yes, daily",
        "No, I'm only interested in joining the afternoon camp",
        "Occasionally",
        "N/A",
        "",
    ] = Field(
        ..., description="Select how often you would like to attend the workshops in the morning."
    )

    yes_daily: BooleanLike = Field(
        default="", description="Check if you want to attend the workshops every day."
    )

    no_im_only_interested_in_joining_the_afternoon_camp: BooleanLike = Field(
        default="",
        description=(
            "Check if you only want to participate in the afternoon songwriting & production camp."
        ),
    )

    occasionally: BooleanLike = Field(
        default="", description="Check if you want to attend the workshops only on some days."
    )

    what_workshops_are_you_interested_in_what_would_you_like_to_learn: Literal[
        "Singing/Songwriting", "Production", "Instrumental Workshops", "Other", "N/A", ""
    ] = Field(..., description="Select the type(s) of workshops you are interested in attending.")

    singing_songwriting: BooleanLike = Field(
        default="",
        description="Check if you are interested in singing and/or songwriting workshops.",
    )

    production: BooleanLike = Field(
        default="", description="Check if you are interested in music production workshops."
    )

    instrumental_workshops_if_yes_which_instrument: str = Field(
        default="",
        description=(
            "Indicate that you want instrumental workshops and specify which instrument you "
            'play. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    other: str = Field(
        default="",
        description=(
            "Describe any other type of workshop or topic you are interested in. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SongwritingProductionCamp(BaseModel):
    """Afternoon camp application details"""

    what_team_position_do_you_apply_for: Literal[
        "Singer/Songwriter", "Producer", "Instrumentalist", "N/A", ""
    ] = Field(..., description="Select the primary role you want to have in the afternoon camp.")

    singer_songwriter: BooleanLike = Field(
        default="", description="Check if you are applying as a singer and/or songwriter."
    )

    producer: BooleanLike = Field(
        default="", description="Check if you are applying as a music producer."
    )

    instrumentalist_and_im_playing: str = Field(
        default="",
        description=(
            "If you apply as an instrumentalist, specify the instrument(s) you play. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    for_instrumentalists_only_how_would_you_like_to_participate_in_the_camp: Literal[
        "Making and recording arrangements with my instrument",
        "Mainly as a singer/songwriter",
        "Mainly as a producer",
        "N/A",
        "",
    ] = Field(
        default="",
        description=(
            "For instrumentalists, choose how you would primarily like to contribute in the camp."
        ),
    )

    making_and_recording_arrangements_with_my_instrument: BooleanLike = Field(
        default="",
        description="Check if you want to focus on arranging and recording with your instrument.",
    )

    mainly_as_a_singer_songwriter: BooleanLike = Field(
        default="",
        description=(
            "Check if, as an instrumentalist, you mainly want to participate as a "
            "singer/songwriter."
        ),
    )

    mainly_as_a_producer: BooleanLike = Field(
        default="",
        description="Check if, as an instrumentalist, you mainly want to participate as a producer.",
    )

    please_briefly_describe_your_music_genres_would_you_like_to_write_music_in_similar_genres_or_are_you_willing_to_work_with_musicians_from_various_musical_backgrounds: str = Field(
        default="",
        description=(
            "Describe the music genres you are involved in and your openness to working "
            'across different musical styles. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class SummerCamp(BaseModel):
    """
    SUMMER CAMP

    Under the guidance of highly qualified instructors and well-known musicians, you can expect a wide array of daily songwriting, music production and instrumental workshops in the mornings. The registration can be done beforehand through our website. It is possible to participate in single workshops or to only join the songwriting & music production camp in the afternoon. It is not necessary to apply for participating in the workshops only.
    During our songwriting & music production camp in the afternoon, you will compose, record and produce your own songs in small teams. The workshops in the morning can be attended independently from the camp in the afternoon, but are an ideal complement.
    !! Please note that the application for the afternoon camp obliges daily and regular attendance !!
    """

    workshops: Workshops = Field(..., description="Workshops")
    songwriting__production_camp: SongwritingProductionCamp = Field(
        ..., description="Songwriting & Production Camp"
    )
