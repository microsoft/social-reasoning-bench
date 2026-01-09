from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CurrentSeizureTreatment(BaseModel):
    """Current seizure medicines, seizure types, frequency, and satisfaction"""

    these_are_the_seizure_medicines_that_are_currently_being_taken: str = Field(
        default="",
        description=(
            "List all seizure medications currently being taken, including names and doses "
            'if known .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    these_are_the_types_of_seizures_that_are_occurring_while_on_these_medicines: str = Field(
        default="",
        description=(
            "Describe the types of seizures that are still occurring while on the current "
            'medicines .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    seizures_still_happen_rarely_if_ever: BooleanLike = Field(
        default="",
        description="Check if seizures rarely or almost never occur while on current medicines",
    )

    seizures_still_happen_at_least_once_a_month: BooleanLike = Field(
        default="",
        description="Check if seizures occur at least once per month while on current medicines",
    )

    seizures_still_happen_once_or_twice_a_week: BooleanLike = Field(
        default="",
        description="Check if seizures occur once or twice per week while on current medicines",
    )

    seizures_still_happen_about_once_a_day: BooleanLike = Field(
        default="",
        description="Check if seizures occur about once per day while on current medicines",
    )

    seizures_still_happen_more_than_once_a_day: BooleanLike = Field(
        default="",
        description="Check if seizures occur more than once per day while on current medicines",
    )

    satisfaction_with_current_seizure_medicines_fairly_satisfied: BooleanLike = Field(
        default="",
        description="Check if you feel fairly satisfied with your current seizure medicines",
    )

    satisfaction_with_current_seizure_medicines_okay_needs_improvement: BooleanLike = Field(
        default="",
        description="Check if your current seizure medicines are okay but need improvement",
    )

    satisfaction_with_current_seizure_medicines_its_time_to_try_something_different: BooleanLike = (
        Field(
            default="",
            description="Check if you feel it is time to try a different seizure treatment",
        )
    )


class TreatmentGoalsandNotes(BaseModel):
    """Goals, expectations for EPIDIOLEX, and additional notes or questions"""

    my_goals_for_seizure_treatment_are: str = Field(
        default="",
        description=(
            "Describe your main goals and priorities for seizure treatment .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
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


class BeginTheEpidiolexConversation(BaseModel):
    """
    Begin the EPIDIOLEX conversation

    ''
    """

    current_seizure_treatment: CurrentSeizureTreatment = Field(
        ..., description="Current Seizure Treatment"
    )
    treatment_goals_and_notes: TreatmentGoalsandNotes = Field(
        ..., description="Treatment Goals and Notes"
    )
