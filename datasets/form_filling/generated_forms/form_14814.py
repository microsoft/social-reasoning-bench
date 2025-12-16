from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PartIHealthConcernssymptomsAndHowTheyInfluenceYourLife(BaseModel):
    """
    Part I: Health Concerns/Symptoms and How They Influence Your Life

    Part I: Health Concerns/Symptoms and How They Influence Your Life
    """

    what_hurts_and_how_long_has_it_hurt: str = Field(
        ...,
        description=(
            "Describe the area(s) that hurt and how long you have had this pain or problem. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    when_do_you_think_these_problems_originally_started: str = Field(
        ...,
        description=(
            "Indicate when you first noticed these problems or when they began. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    have_you_ever_done_anything_about_this_concern_or_sought_treatment_for_it_y_n: BooleanLike = (
        Field(
            ...,
            description=(
                "Indicate whether you have previously done anything or sought treatment for "
                "this concern."
            ),
        )
    )

    if_yes_what_were_you_told: str = Field(
        default="",
        description=(
            "If you sought treatment, describe what you were told about your condition. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    what_was_done: str = Field(
        default="",
        description=(
            "Briefly describe what treatment or actions were taken. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    did_it_seem_to_work_y_n: BooleanLike = Field(
        default="", description="Indicate whether the treatment or actions seemed to help."
    )

    how_does_this_impact_your_life: str = Field(
        ...,
        description=(
            "Explain how this concern affects areas such as family, work, social life, "
            "sleep, exercise, chores, focus, self-image, self-esteem, play, walking, and "
            'health concerns. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    are_you_doing_anything_differently_because_of_this_condition_symptom_concern: str = Field(
        default="",
        description=(
            "Describe any changes you have made in your activities or routines because of "
            'this issue. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    which_best_describes_your_current_feelings_about_yourself_and_your_situation_a: BooleanLike = (
        Field(
            default="",
            description="Select this if you feel helpless, like little or nothing works.",
        )
    )

    which_best_describes_your_current_feelings_about_yourself_and_your_situation_b: BooleanLike = (
        Field(
            default="",
            description=(
                "Select this if you feel this is terrible, really bad, you’re scared and hope "
                "the provider can fix it."
            ),
        )
    )

    which_best_describes_your_current_feelings_about_yourself_and_your_situation_c: BooleanLike = (
        Field(
            default="",
            description="Select this if you feel stuck and unable to help yourself right now.",
        )
    )

    which_best_describes_your_current_feelings_about_yourself_and_your_situation_d: BooleanLike = (
        Field(
            default="",
            description=(
                "Select this if you feel you deserve more than what you have been experiencing "
                "and would like assistance in healing."
            ),
        )
    )

    anything_else: str = Field(
        default="",
        description=(
            "Add any additional thoughts or feelings about your situation. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    if_nothing_hurts_what_are_your_health_concerns: str = Field(
        default="",
        description=(
            "If you do not have pain, describe any other health concerns you have. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )
