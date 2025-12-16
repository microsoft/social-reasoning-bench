from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class TournamentInformation(BaseModel):
    """Basic information about the tournament and host association"""

    host_association: str = Field(
        ...,
        description=(
            "Name of the host association organizing the tournament .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            "City where the tournament will be held .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dates: str = Field(
        ...,
        description=(
            "Dates on which the tournament will take place .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class DisciplinaryCommittee(BaseModel):
    """Contact details for the Tournament Disciplinary Committee Chair"""

    disciplinary_committee_chair_legal_name: str = Field(
        ...,
        description=(
            "Full legal name of the Disciplinary Committee Chair for the tournament .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    disciplinary_committee_chair_date_of_birth: str = Field(
        ..., description="Date of birth of the Disciplinary Committee Chair"
    )  # YYYY-MM-DD format

    disciplinary_committee_chair_rma: str = Field(
        ...,
        description=(
            "RMA (Risk Management Application) number of the Disciplinary Committee Chair "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    disciplinary_committee_chair_street: str = Field(
        ...,
        description=(
            "Street address of the Disciplinary Committee Chair .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    disciplinary_committee_chair_city: str = Field(
        ...,
        description=(
            "City of residence for the Disciplinary Committee Chair .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    disciplinary_committee_chair_state: str = Field(
        ..., description="State of residence for the Disciplinary Committee Chair"
    )

    disciplinary_committee_chair_zip: str = Field(
        ..., description="ZIP code for the Disciplinary Committee Chair's address"
    )

    disciplinary_committee_chair_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the Disciplinary Committee Chair .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    disciplinary_committee_chair_e_mail: str = Field(
        ...,
        description=(
            "Email address for the Disciplinary Committee Chair .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RefereeAssignor(BaseModel):
    """Referee system details and contact information for the tournament referee assignor"""

    age_divisions_using_three_referee_system: str = Field(
        default="",
        description=(
            "List of age divisions for which a three-referee system will be used .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    referee_assignor_legal_name: str = Field(
        ...,
        description=(
            "Full legal name of the referee assignor for the tournament .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    referee_assignor_date_of_birth: str = Field(
        ..., description="Date of birth of the referee assignor"
    )  # YYYY-MM-DD format

    referee_assignor_rma: str = Field(
        ...,
        description=(
            "RMA (Risk Management Application) number of the referee assignor .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    referee_assignor_street: str = Field(
        ...,
        description=(
            "Street address of the referee assignor .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    referee_assignor_city: str = Field(
        ...,
        description=(
            "City of residence for the referee assignor .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    referee_assignor_state: str = Field(
        ..., description="State of residence for the referee assignor"
    )

    referee_assignor_zip: str = Field(
        ..., description="ZIP code for the referee assignor's address"
    )

    referee_assignor_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the referee assignor .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    referee_assignor_e_mail: str = Field(
        ...,
        description=(
            "Email address for the referee assignor .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class pythonWashingtonYouthSoccerTournamentHostingAddendum(BaseModel):
    """
        WASHINGTON YOUTH SOCCER

    TOURNAMENT HOSTING AGREEMENT
    (ADDENDUM TO US YOUTH SOCCER TOURNAMENT/GAMES HOSTING AGREEMENT)

        In consideration of permission being granted to ________________________________________ (Host Association) to hold a tournament at _______________________________________________(city) _______________________________________ on the dates of ________________________________________ , we hereby agree that as the Tournament Host Organization we will, in addition to the US Soccer Hosting Agreement, abide by the following:
    """

    tournament_information: TournamentInformation = Field(..., description="Tournament Information")
    disciplinary_committee: DisciplinaryCommittee = Field(..., description="Disciplinary Committee")
    referee_assignor: RefereeAssignor = Field(..., description="Referee Assignor")
