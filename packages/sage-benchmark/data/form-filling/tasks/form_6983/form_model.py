from typing import List, Literal, Optional, Union

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
            "Name or description of the Team Challenge .If you cannot fill this, write "
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
            'Official team name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    team_number: str = Field(
        ...,
        description=(
            "Official team number, including all digits before and after the dash .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    appraisers: str = Field(
        ...,
        description=(
            "Names of appraisers submitting the nomination .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class NominationDetails(BaseModel):
    """Details about what and whom the nomination is for"""

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
            "Name of the individual being nominated (if not a team) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ReasonforNomination(BaseModel):
    """Explanation and justification for the nomination"""

    reason_for_nomination: str = Field(
        ...,
        description=(
            "Detailed explanation citing reasons and examples for the nomination .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class DITheRenaissanceAwardNominationForm(BaseModel):
    """
        Destination Imagination®

    The Renaissance Award
    For Outstanding Design, Engineering, or Performance
    NOMINATION FORM

        This award is offered for exceptional skill in the areas of engineering, design, or performance. Nominations should give examples of outstanding skills in the areas of engineering, design, or performance demonstrated by the team/individual. This award is offered for skill rather than creativity.
    """

    team_information: TeamInformation = Field(..., description="Team Information")
    nomination_details: NominationDetails = Field(..., description="Nomination Details")
    reason_for_nomination: ReasonforNomination = Field(..., description="Reason for Nomination")
