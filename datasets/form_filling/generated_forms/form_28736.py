from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AgeofProgramParticipants(BaseModel):
    """Whether participants are adults or minors"""

    are_participants_in_the_proposed_program_age_18_or_over_yes: BooleanLike = Field(
        ...,
        description=(
            "Select if all participants in the proposed program will be adults age 18 or older."
        ),
    )

    are_participants_in_the_proposed_program_age_18_or_over_no_mix: BooleanLike = Field(
        ...,
        description=(
            "Select if participants will include both minors under 18 and adults 18 or older."
        ),
    )

    are_participants_in_the_proposed_program_age_18_or_over_no_all_minors: BooleanLike = Field(
        ...,
        description="Select if all participants in the proposed program will be minors under age 18.",
    )


class MinorParticipantDetails(BaseModel):
    """Details required for programs serving minors"""

    age_range_of_the_minors_participating_in_the_program: str = Field(
        ...,
        description=(
            "Specify the age range of minor participants (e.g., 10–17 years). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    lab_school_students: BooleanLike = Field(
        default="", description="Check if minor participants include Lab School students."
    )

    charter_school_students: BooleanLike = Field(
        default="", description="Check if minor participants include Charter School students."
    )

    non_affiliates: BooleanLike = Field(
        default="",
        description=(
            "Check if minor participants include individuals who are not affiliated with "
            "the listed schools."
        ),
    )

    combination_of_these_categories: BooleanLike = Field(
        default="",
        description=(
            "Check if minor participants are drawn from a combination of the listed "
            "affiliation categories."
        ),
    )

    will_minors_be_accompanied_by_parent_or_guardian_yes: BooleanLike = Field(
        ...,
        description=(
            "Select if minors will be accompanied by a parent or guardian during the "
            "program or event."
        ),
    )

    will_minors_be_accompanied_by_parent_or_guardian_no: BooleanLike = Field(
        ...,
        description=(
            "Select if minors will not be accompanied by a parent or guardian during the "
            "program or event."
        ),
    )

    mitigation_measures_details_line_1: str = Field(
        ...,
        description=(
            "First line of description of mitigation measures and planning for minors, "
            "including applicable COVID guidelines. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mitigation_measures_details_line_2: str = Field(
        default="",
        description=(
            "Second line of description of mitigation measures and planning for minors, "
            "including applicable COVID guidelines. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mitigation_measures_details_line_3: str = Field(
        default="",
        description=(
            "Third line of description of mitigation measures and planning for minors, "
            "including applicable COVID guidelines. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mitigation_measures_details_line_4: str = Field(
        default="",
        description=(
            "Fourth line of description of mitigation measures and planning for minors, "
            "including applicable COVID guidelines. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class MinorStatusOfParticipants(BaseModel):
    """
    MINOR STATUS OF PARTICIPANTS

    ''
    """

    age_of_program_participants: AgeofProgramParticipants = Field(
        ..., description="Age of Program Participants"
    )
    minor_participant_details: MinorParticipantDetails = Field(
        ..., description="Minor Participant Details"
    )
