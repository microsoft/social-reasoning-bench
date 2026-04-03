from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class TeamInformation(BaseModel):
    """Basic information about the team and challenge"""

    team_challenge: str = Field(
        ...,
        description=(
            "Name or identifier of the Team Challenge .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    level_el: BooleanLike = Field(
        ..., description="Select if the team is in the Elementary Level (EL)"
    )

    level_ml: BooleanLike = Field(..., description="Select if the team is in the Middle Level (ML)")

    level_sl: BooleanLike = Field(
        ..., description="Select if the team is in the Secondary Level (SL)"
    )

    level_ul: BooleanLike = Field(
        ..., description="Select if the team is in the University Level (UL)"
    )

    team_name: str = Field(
        ...,
        description=(
            'Official name of the team .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    team_number_digit_1: Union[float, Literal["N/A", ""]] = Field(
        ..., description="First digit of the team number"
    )

    team_number_digit_2: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Second digit of the team number"
    )

    team_number_digit_3: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Third digit of the team number"
    )

    team_number_digit_4: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Fourth digit of the team number (first digit after the dash)"
    )

    team_number_digit_5: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Fifth digit of the team number"
    )

    team_number_digit_6: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Sixth digit of the team number"
    )

    team_number_digit_7: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Seventh digit of the team number"
    )

    team_number_digit_8: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Eighth digit of the team number"
    )


class Appraisers(BaseModel):
    """Names of appraisers submitting the nomination"""

    appraisers_line_1: str = Field(
        ...,
        description=(
            'First line listing appraiser names .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    appraisers_line_2: str = Field(
        default="",
        description=(
            "Second line for additional appraiser names, if needed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class NominationDetails(BaseModel):
    """Details about what and who is being nominated"""

    nomination_for_team_challenge: BooleanLike = Field(
        ..., description="Select if the nomination is for the Team Challenge"
    )

    nomination_for_instant_challenge: BooleanLike = Field(
        ..., description="Select if the nomination is for the Instant Challenge"
    )

    nomination_to_team: BooleanLike = Field(
        ..., description="Select if the nomination is for a team"
    )

    nomination_to_individual: BooleanLike = Field(
        ..., description="Select if the nomination is for an individual"
    )

    if_individual_name: str = Field(
        default="",
        description=(
            "Name of the individual if the nomination is for an individual .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ReasonforNomination(BaseModel):
    """Explanation and justification for the nomination"""

    reason_for_nomination: str = Field(
        ...,
        description=(
            "Detailed explanation of why this team or individual is being nominated .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class RenaissanceAwardDesignEngineeringOrPerformanceNominationForm(BaseModel):
    """
        Destination Imagination®
    The Renaissance Award
    For Outstanding Design, Engineering, or Performance
    NOMINATION FORM

        This award is offered for exceptional skill in the areas of engineering, design, or performance. Nominations should give examples of outstanding skills in the areas of engineering, design, or performance demonstrated by the team/individual. This award is offered for skill rather than creativity.
    """

    team_information: TeamInformation = Field(..., description="Team Information")
    appraisers: Appraisers = Field(..., description="Appraisers")
    nomination_details: NominationDetails = Field(..., description="Nomination Details")
    reason_for_nomination: ReasonforNomination = Field(..., description="Reason for Nomination")
