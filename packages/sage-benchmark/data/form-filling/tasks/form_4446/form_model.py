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
    """Information about current seizure medicines and seizure types/frequency"""

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

    rarely_if_ever: BooleanLike = Field(
        default="",
        description="Check if seizures rarely, if ever, occur while on current seizure medicines",
    )

    at_least_once_a_month: BooleanLike = Field(
        default="",
        description=(
            "Check if seizures occur at least once a month while on current seizure medicines"
        ),
    )

    once_or_twice_a_week: BooleanLike = Field(
        default="",
        description="Check if seizures occur once or twice a week while on current seizure medicines",
    )

    about_once_a_day: BooleanLike = Field(
        default="",
        description="Check if seizures occur about once a day while on current seizure medicines",
    )

    more_than_once_a_day: BooleanLike = Field(
        default="",
        description="Check if seizures occur more than once a day while on current seizure medicines",
    )


class SatisfactionWithCurrentTreatment(BaseModel):
    """Level of satisfaction with current seizure medicines"""

    fairly_satisfied: BooleanLike = Field(
        default="",
        description="Check if you feel fairly satisfied with your current seizure medicines",
    )

    okay_needs_improvement: BooleanLike = Field(
        default="",
        description="Check if your current seizure medicines are okay but need improvement",
    )

    its_time_to_try_something_different: BooleanLike = Field(
        default="", description="Check if you feel it is time to try a different seizure treatment"
    )


class TreatmentGoalsandEPIDIOLEX(BaseModel):
    """Goals for seizure treatment, expectations for EPIDIOLEX, and additional notes"""

    my_goals_for_seizure_treatment_are: str = Field(
        default="",
        description=(
            "Describe your personal goals for seizure treatment .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    my_hopes_for_epidiolex_are: str = Field(
        default="",
        description=(
            "Describe what you hope EPIDIOLEX will help you or your loved one achieve .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
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

    Begin the EPIDIOLEX conversation
    """

    current_seizure_treatment: CurrentSeizureTreatment = Field(
        ..., description="Current Seizure Treatment"
    )
    satisfaction_with_current_treatment: SatisfactionWithCurrentTreatment = Field(
        ..., description="Satisfaction With Current Treatment"
    )
    treatment_goals_and_epidiolex: TreatmentGoalsandEPIDIOLEX = Field(
        ..., description="Treatment Goals and EPIDIOLEX"
    )
