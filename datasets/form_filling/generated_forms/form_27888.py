from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class InternationallyAcquiredPrograms(BaseModel):
    """Details and required materials for internationally-acquired programs"""

    supplier_name: str = Field(
        ...,
        description=(
            "Name of the program supplier or company .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    country_of_origin: str = Field(
        ...,
        description=(
            "Country where the program was originally produced .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    years_produced: str = Field(
        ...,
        description=(
            "Year or range of years during which the program was produced .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    copyright_clearance_attached: BooleanLike = Field(
        ...,
        description=(
            "Indicate that copyright clearance documentation for the "
            "internationally-acquired program is attached"
        ),
    )

    one_episode_submitted_or_link_provided_international: BooleanLike = Field(
        ...,
        description=(
            "Confirm that one episode of the internationally-acquired program or an online "
            "link has been provided"
        ),
    )


class LocallyProducedPrograms(BaseModel):
    """Required materials for locally-produced programs"""

    copyright_clearances_creative_materials_attached: BooleanLike = Field(
        ...,
        description=(
            "Confirm that copyright clearances for all creative materials used in the "
            "locally-produced program are attached"
        ),
    )

    rundown_general_episode_format_attached: BooleanLike = Field(
        ...,
        description=(
            "Confirm that a rundown of the general episode format, including segments and "
            "descriptions, is attached for the locally-produced program"
        ),
    )

    content_forecast_13_episodes_attached: BooleanLike = Field(
        ...,
        description=(
            "Confirm that a content forecast for 13 episodes of the locally-produced "
            "program is attached"
        ),
    )

    one_episode_submitted_or_link_provided_local: BooleanLike = Field(
        ...,
        description=(
            "Confirm that one episode of the locally-produced program or an online link has "
            "been provided"
        ),
    )

    brief_content_description_non_english_attached: BooleanLike = Field(
        default="",
        description=(
            "Confirm that a brief content description is attached for any segments in "
            "languages other than English in the locally-produced program"
        ),
    )


class AdditionalInformation(BaseModel):
    """Optional extra information about the proposal"""

    additional_information_about_your_proposal: str = Field(
        default="",
        description=(
            "Any extra details or context you would like to provide about your program "
            'proposal .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class ShawMulticulturalChannelProgramApplication(BaseModel):
    """
    Shaw Multicultural Channel Program Application

    ''
    """

    internationally_acquired_programs: InternationallyAcquiredPrograms = Field(
        ..., description="Internationally-Acquired Programs"
    )
    locally_produced_programs: LocallyProducedPrograms = Field(
        ..., description="Locally-Produced Programs"
    )
    additional_information: AdditionalInformation = Field(..., description="Additional Information")
