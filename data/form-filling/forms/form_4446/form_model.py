from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class BeginTheEpidiolexConversation(BaseModel):
    """
    Begin the EPIDIOLEX conversation

    ''
    """

    these_are_the_seizure_medicines_that_are_currently_being_taken: str = Field(
        default="",
        description=(
            "List all seizure medications currently being taken, including names and doses "
            'if desired .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    these_are_the_types_of_seizures_that_are_occurring_while_on_these_medicines: str = Field(
        default="",
        description=(
            "Describe the types of seizures that are still occurring while on current "
            'medicines .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    seizures_still_happen_rarely_if_ever: BooleanLike = Field(
        default="",
        description="Check if seizures rarely, if ever, still occur while on current medicines",
    )

    seizures_still_happen_at_least_once_a_month: BooleanLike = Field(
        default="",
        description="Check if seizures occur at least once a month while on current medicines",
    )

    seizures_still_happen_once_or_twice_a_week: BooleanLike = Field(
        default="",
        description="Check if seizures occur once or twice a week while on current medicines",
    )

    seizures_still_happen_about_once_a_day: BooleanLike = Field(
        default="",
        description="Check if seizures occur about once a day while on current medicines",
    )

    seizures_still_happen_more_than_once_a_day: BooleanLike = Field(
        default="",
        description="Check if seizures occur more than once a day while on current medicines",
    )

    this_is_how_satisfied_i_am_with_my_current_seizure_medicines_fairly_satisfied: BooleanLike = (
        Field(
            default="",
            description="Check if you feel fairly satisfied with your current seizure medicines",
        )
    )

    this_is_how_satisfied_i_am_with_my_current_seizure_medicines_okay_needs_improvement: BooleanLike = Field(
        default="",
        description="Check if your current seizure medicines are okay but need improvement",
    )

    this_is_how_satisfied_i_am_with_my_current_seizure_medicines_its_time_to_try_something_different: BooleanLike = Field(
        default="", description="Check if you feel it is time to try a different seizure treatment"
    )

    my_goals_for_seizure_treatment_are: str = Field(
        default="",
        description=(
            "Describe your goals for seizure treatment (e.g., fewer seizures, better daily "
            'functioning) .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    my_hopes_for_epidiolex_are: str = Field(
        default="",
        description=(
            "Describe what you hope EPIDIOLEX will help you or your child achieve .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    additional_notes_and_questions_i_have: str = Field(
        default="",
        description=(
            "Add any other notes, concerns, or questions you want to discuss .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )
