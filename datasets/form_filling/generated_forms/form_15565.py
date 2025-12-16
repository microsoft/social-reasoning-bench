from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ScotchPlainsRescueSquadIncExtracurricularActivities(BaseModel):
    """
        SCOTCH PLAINS RESCUE SQUAD, INC.
    Extracurricular Activities

        Prospective members applying to the Scotch Plains Rescue Squad should list all their extracurricular activities involved through their school, work, or other organizations. Each activity should have a brief description of level of involvement in terms of time.
    """

    extracurricular_activity_and_description_of_level_of_involvement_line_1: str = Field(
        default="",
        description=(
            "First extracurricular activity and brief description of your level of "
            'involvement and time commitment. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    extracurricular_activity_and_description_of_level_of_involvement_line_2: str = Field(
        default="",
        description=(
            "Second extracurricular activity and brief description of your level of "
            'involvement and time commitment. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    extracurricular_activity_and_description_of_level_of_involvement_line_3: str = Field(
        default="",
        description=(
            "Third extracurricular activity and brief description of your level of "
            'involvement and time commitment. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    extracurricular_activity_and_description_of_level_of_involvement_line_4: str = Field(
        default="",
        description=(
            "Fourth extracurricular activity and brief description of your level of "
            'involvement and time commitment. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    extracurricular_activity_and_description_of_level_of_involvement_line_5: str = Field(
        default="",
        description=(
            "Fifth extracurricular activity and brief description of your level of "
            'involvement and time commitment. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    extracurricular_activity_and_description_of_level_of_involvement_line_6: str = Field(
        default="",
        description=(
            "Sixth extracurricular activity and brief description of your level of "
            'involvement and time commitment. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    extracurricular_activity_and_description_of_level_of_involvement_line_7: str = Field(
        default="",
        description=(
            "Seventh extracurricular activity and brief description of your level of "
            'involvement and time commitment. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    extracurricular_activity_and_description_of_level_of_involvement_line_8: str = Field(
        default="",
        description=(
            "Eighth extracurricular activity and brief description of your level of "
            'involvement and time commitment. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    extracurricular_activity_and_description_of_level_of_involvement_line_9: str = Field(
        default="",
        description=(
            "Ninth extracurricular activity and brief description of your level of "
            'involvement and time commitment. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    extracurricular_activity_and_description_of_level_of_involvement_line_10: str = Field(
        default="",
        description=(
            "Tenth extracurricular activity and brief description of your level of "
            'involvement and time commitment. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )
