from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class IncidentInformation(BaseModel):
    """Basic identifying information for the incident and when it was initiated"""

    incident_name: str = Field(
        ...,
        description=(
            'Name or designation of the incident .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    incident_number: str = Field(
        ...,
        description=(
            "Unique tracking or reference number for the incident .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_time_initiated_date: str = Field(
        ..., description="Calendar date when the incident briefing was initiated"
    )  # YYYY-MM-DD format

    date_time_initiated_time: str = Field(
        ...,
        description=(
            "Clock time when the incident briefing was initiated .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Objectives(BaseModel):
    """Current and planned incident objectives"""

    current_and_planned_objectives: str = Field(
        ...,
        description=(
            "Describe the current and planned incident objectives .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ActionsStrategiesandTactics(BaseModel):
    """Current and planned actions, strategies, and tactics with associated times"""

    current_and_planned_actions_strategies_and_tactics: str = Field(
        ...,
        description=(
            "Describe current and planned actions, strategies, and tactics for the incident "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    time: str = Field(
        default="",
        description=(
            "Time associated with the listed actions, strategies, or tactics .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    actions: str = Field(
        default="",
        description=(
            "Details of actions, strategies, or tactics taken or planned .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class PreparedBy(BaseModel):
    """Information about the person who prepared this form and when"""

    prepared_by_name: str = Field(
        ...,
        description=(
            "Name of the person who prepared this form .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    prepared_by_position_title: str = Field(
        ...,
        description=(
            "Position or title of the person who prepared this form .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    prepared_by_signature: str = Field(
        ...,
        description=(
            "Signature of the person who prepared this form .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_time: str = Field(
        ...,
        description=(
            "Date and time when this page of the ICS 201 was completed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IncidentBriefingics201(BaseModel):
    """
    INCIDENT BRIEFING (ICS 201)

    ''
    """

    incident_information: IncidentInformation = Field(..., description="Incident Information")
    objectives: Objectives = Field(..., description="Objectives")
    actions_strategies_and_tactics: ActionsStrategiesandTactics = Field(
        ..., description="Actions, Strategies, and Tactics"
    )
    prepared_by: PreparedBy = Field(..., description="Prepared By")
