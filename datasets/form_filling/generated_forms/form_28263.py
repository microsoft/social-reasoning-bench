from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class DeaconandSupervisingPastorInformation(BaseModel):
    """Basic identifying information for the deacon and supervising pastor"""

    name_of_deacon: str = Field(
        ...,
        description=(
            "Full name of the deacon being evaluated .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    supervising_pastor: str = Field(
        ...,
        description=(
            "Full name of the supervising pastor completing or overseeing the evaluation "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    congregation_city_deacon: str = Field(
        ...,
        description=(
            "Name of the deacon’s congregation and city .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    congregation_city_supervising_pastor: str = Field(
        ...,
        description=(
            "Name of the supervising pastor’s congregation and city .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_evaluation: str = Field(
        ..., description="Date on which this evaluation is completed"
    )  # YYYY-MM-DD format


class TheDeaconPersonalCharacter(BaseModel):
    """Evaluation of the deacon’s personal character traits"""

    humble: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    gentle: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    giving: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    confident: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    mature: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    hospitable: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    peaceful: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    energetic: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    disciplined: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    reputable: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    loving: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    conscientious: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    dependable: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    wise: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    serving: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    dedicated: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    honest: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    faithful: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    serious: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    discerning: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    sensitive: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    responsible: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    empathetic: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    encouraging: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    sacrificial: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    patient: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    thankful: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    forgiving: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    gracious: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    respectful: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    trustworthy: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    cheerful: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    persistent: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    creative: BooleanLike = Field(
        default="",
        description=(
            "Indicate if this characteristic is one of the qualities that best identifies "
            "the deacon"
        ),
    )

    concerns_about_deficiencies_in_personal_characteristics: str = Field(
        default="",
        description=(
            "Describe any concerns raised by deficiencies in the listed personal "
            "characteristics as observed in the parish setting .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RelationshipBetweenSupervisingPastorandDeacon(BaseModel):
    """Description of the working relationship and interaction between the supervising pastor and the deacon"""

    description_of_relationship_between_supervising_pastor_and_deacon: str = Field(
        default="",
        description=(
            "Describe the relationship between you and the deacon, including openness, "
            "guidability, loyalty, willingness, consideration, frequency of communication, "
            'and evaluation .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class MichiganDistrictDeaconEvaluationForm(BaseModel):
    """
    Michigan District Deacon Evaluation Form

    From the following personal characteristics circle up to ten of the qualities which you believe best identify the deacon. Not selecting a characteristic does not imply a deficiency on the part of the deacon.
    """

    deacon_and_supervising_pastor_information: DeaconandSupervisingPastorInformation = Field(
        ..., description="Deacon and Supervising Pastor Information"
    )
    the_deacon_personal_character: TheDeaconPersonalCharacter = Field(
        ..., description="The Deacon: Personal Character"
    )
    relationship_between_supervising_pastor_and_deacon: RelationshipBetweenSupervisingPastorandDeacon = Field(
        ..., description="Relationship Between Supervising Pastor and Deacon"
    )
