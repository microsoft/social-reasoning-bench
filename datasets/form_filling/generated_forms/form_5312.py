from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Questionnaire(BaseModel):
    """Background and conduct questions"""

    charged_convicted_criminal_offence_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate if you are answering YES to having ever been charged with and/or "
            "convicted of a criminal offence."
        ),
    )

    charged_convicted_criminal_offence_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate if you are answering NO to having ever been charged with and/or "
            "convicted of a criminal offence."
        ),
    )

    history_alcohol_substance_abuse_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate if you are answering YES to having a history of alcohol or substance abuse."
        ),
    )

    history_alcohol_substance_abuse_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate if you are answering NO to having a history of alcohol or substance abuse."
        ),
    )

    allegations_abuse_child_physical_sexual_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate if you are answering YES to there having been any such allegations "
            "against you."
        ),
    )

    allegations_abuse_child_physical_sexual_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate if you are answering NO to there having been any such allegations "
            "against you."
        ),
    )


class ChurchesAttendedinthePast3Years(BaseModel):
    """Details of churches regularly attended in the last three years"""

    church_1_church_name: str = Field(
        ...,
        description=(
            "Name of the first church you attended regularly in the past 3 years. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    church_1_location: str = Field(
        ...,
        description=(
            "City, town, and/or region of the first church. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    church_1_attended_from_month_year: str = Field(
        ...,
        description=(
            "Month and year you started attending the first church. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    church_1_attended_until_month_year: str = Field(
        ...,
        description=(
            "Month and year you stopped attending the first church (or write 'present'). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    church_1_any_positions_held: str = Field(
        default="",
        description=(
            "Any roles, offices, or positions you held at the first church. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    church_2_church_name: str = Field(
        default="",
        description=(
            "Name of the second church you attended regularly in the past 3 years, if "
            'applicable. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    church_2_location: str = Field(
        default="",
        description=(
            "City, town, and/or region of the second church. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    church_2_attended_from_month_year: str = Field(
        default="",
        description=(
            "Month and year you started attending the second church. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    church_2_attended_until_month_year: str = Field(
        default="",
        description=(
            "Month and year you stopped attending the second church (or write 'present'). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    church_2_any_positions_held: str = Field(
        default="",
        description=(
            "Any roles, offices, or positions you held at the second church. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class Questionnaire(BaseModel):
    """
    QUESTIONNAIRE

    Check either “YES” or “NO” for each of the following questions. If you answer “yes” to a question, please give details on a separate page or discuss with the Senior Pastor. A ‘yes’ answer will not automatically rule an applicant out of selection.
    Note that, if you disclose any potentially criminal actions, the Church may need to report this information to the police or other relevant government authorities.
    """

    questionnaire: Questionnaire = Field(..., description="Questionnaire")
    churches_attended_in_the_past_3_years: ChurchesAttendedinthePast3Years = Field(
        ..., description="Churches Attended in the Past 3 Years"
    )
