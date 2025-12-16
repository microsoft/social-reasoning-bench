from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class StartingSmall(BaseModel):
    """Three small actions to implement starting now"""

    i_will_first_action: str = Field(
        ...,
        description=(
            "First small action you promise to implement in your day-to-day life .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    i_will_second_action: str = Field(
        ...,
        description=(
            "Second small action you promise to implement in your day-to-day life .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    i_will_third_action: str = Field(
        ...,
        description=(
            "Third small action you promise to implement in your day-to-day life .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Reflections(BaseModel):
    """Reflections on a recent team experience"""

    reflections_understanding_of_tasks_scope_timeline: str = Field(
        ...,
        description=(
            "Describe whether you clearly understood your tasks, their scope, and expected "
            'timeline when working in the team .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reflections_results_recognized_and_accomplishment: str = Field(
        ...,
        description=(
            "Reflect on whether the results you achieved were recognized and whether you "
            'felt a sense of accomplishment .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reflections_efforts_recognized_even_without_results: str = Field(
        ...,
        description=(
            "Reflect on whether your efforts were acknowledged, even when results were not "
            "achieved, and any discussion of those efforts .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reflections_incomplete_tasks_and_completion_marked: str = Field(
        ...,
        description=(
            "Explain how incomplete tasks were handled and how you knew when the work was "
            "fully completed, including any specific markers of completion .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    reflection_on_own_role_communication_recognition_completion: str = Field(
        ...,
        description=(
            "Reflect on your own communication, how you recognized others’ accomplishments "
            "and efforts, your role in ensuring completion, and what you could have done "
            'differently .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class WhatCouldHaveBeenDoneDifferently(BaseModel):
    """Identify improvements and helpful conversations"""

    what_could_have_been_done_differently: str = Field(
        ...,
        description=(
            "Summarize what could have been done differently to improve the team experience "
            'or outcome .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    type_of_conversation_that_would_have_made_things_better: str = Field(
        default="",
        description=(
            "Specify the kind of conversation (e.g., feedback, planning, conflict "
            "resolution) that would have improved the situation .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class StartingSmall(BaseModel):
    """
    STARTING SMALL

    Think of three small actions that you can take in your day-to-day life and promise yourself that you will implement them starting from now.
    Think of the last time you worked in a team. It might have been a piece of homework, something you accomplished with your family or a project you did with friends. Fill in the table below as you reflect.
    """

    starting_small: StartingSmall = Field(..., description="Starting Small")
    reflections: Reflections = Field(..., description="Reflections")
    what_could_have_been_done_differently: WhatCouldHaveBeenDoneDifferently = Field(
        ..., description="What Could Have Been Done Differently"
    )
