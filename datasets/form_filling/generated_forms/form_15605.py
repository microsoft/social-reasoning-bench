from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FeedbackForm(BaseModel):
    """
    FEEDBACK FORM

    ''
    """

    did_you_encounter_any_barriers: str = Field(
        default="",
        description=(
            "Describe any barriers or difficulties you encountered. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_likely_are_you_to_adopt_some_of_these_new_behaviours_rating: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Select a rating from 1 (Not at all) to 10 (Extremely) indicating how likely "
            "you are to adopt some of these new behaviours."
        ),
    )

    if_likely_please_state_which: str = Field(
        default="",
        description=(
            "If you are likely to adopt new behaviours, list which behaviours you are "
            'likely to adopt. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    has_this_challenge_raised_your_awareness_of_key_environmental_issues_rating: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Select a rating from 1 (Strongly disagree) to 10 (Strongly agree) indicating "
            "whether the challenge raised your awareness of key environmental issues."
        ),
    )

    please_state_which: str = Field(
        default="",
        description=(
            "List which key environmental issues your awareness has been raised about. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    how_familiar_were_you_with_wales_well_being_goals_before_doing_the_challenge_rating: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Select a rating from 1 (Not at all) to 10 (Extremely) indicating how familiar "
            "you were with Wales’ Well-being goals before the challenge."
        ),
    )
