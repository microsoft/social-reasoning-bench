from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OrganizationalCapabilityTargetRow(BaseModel):
    """Single row in Organizational Capability Target"""

    organizational_capability_target: str = Field(
        default="", description="Organizational_Capability_Target"
    )
    associated_critical_tasks: str = Field(default="", description="Associated_Critical_Tasks")
    observation_notes_and_explanation_of_rating: str = Field(
        default="", description="Observation_Notes_And_Explanation_Of_Rating"
    )
    target_rating: str = Field(default="", description="Target_Rating")


class AssociatedCriticalTasksRow(BaseModel):
    """Single row in Associated Critical Tasks"""

    organizational_capability_target: str = Field(
        default="", description="Organizational_Capability_Target"
    )
    associated_critical_tasks: str = Field(default="", description="Associated_Critical_Tasks")
    observation_notes_and_explanation_of_rating: str = Field(
        default="", description="Observation_Notes_And_Explanation_Of_Rating"
    )
    target_rating: str = Field(default="", description="Target_Rating")


class ObservationNotesAndExplanationOfRatingRow(BaseModel):
    """Single row in Observation Notes and Explanation of Rating"""

    organizational_capability_target: str = Field(
        default="", description="Organizational_Capability_Target"
    )
    associated_critical_tasks: str = Field(default="", description="Associated_Critical_Tasks")
    observation_notes_and_explanation_of_rating: str = Field(
        default="", description="Observation_Notes_And_Explanation_Of_Rating"
    )
    target_rating: str = Field(default="", description="Target_Rating")


class TargetRatingRow(BaseModel):
    """Single row in Target Rating"""

    organizational_capability_target: str = Field(
        default="", description="Organizational_Capability_Target"
    )
    associated_critical_tasks: str = Field(default="", description="Associated_Critical_Tasks")
    observation_notes_and_explanation_of_rating: str = Field(
        default="", description="Observation_Notes_And_Explanation_Of_Rating"
    )
    target_rating: str = Field(default="", description="Target_Rating")


class CapabilityAssessment(BaseModel):
    """Details of the organizational capability target, related tasks, observations, and rating"""

    organizational_capability_target: List[OrganizationalCapabilityTargetRow] = Field(
        default="",
        description="Table to document each organizational capability target being evaluated.",
    )  # List of table rows

    associated_critical_tasks: List[AssociatedCriticalTasksRow] = Field(
        default="",
        description=(
            "Part of the table: list the critical tasks associated with each capability target."
        ),
    )  # List of table rows

    observation_notes_and_explanation_of_rating: List[ObservationNotesAndExplanationOfRatingRow] = (
        Field(
            default="",
            description="Part of the table: narrative notes and justification for the rating assigned.",
        )
    )  # List of table rows

    target_rating: List[TargetRatingRow] = Field(
        default="",
        description="Part of the table: rating for each capability target using the ratings key.",
    )  # List of table rows

    final_core_capability_rating: Literal[
        "P – Performed without Challenges",
        "S – Performed with Some Challenges",
        "M – Performed with Major Challenges",
        "U – Unable to be Performed",
        "N/A",
        "",
    ] = Field(..., description="Overall rating for the core capability, using the ratings key.")


class EvaluatorInformation(BaseModel):
    """Contact information for the evaluator"""

    evaluator_name: str = Field(
        ...,
        description=(
            "Full name of the evaluator completing this form. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    evaluator_e_mail: str = Field(
        ...,
        description=(
            'Email address of the evaluator. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the evaluator. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class HomelandSecurityExerciseAndEvaluationProgramhseep(BaseModel):
    """
    Homeland Security Exercise and Evaluation Program (HSEEP)

    ''
    """

    capability_assessment: CapabilityAssessment = Field(..., description="Capability Assessment")
    evaluator_information: EvaluatorInformation = Field(..., description="Evaluator Information")
