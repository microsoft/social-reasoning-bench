from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PatientInformation(BaseModel):
    """Basic patient details"""

    patient_name: str = Field(
        ...,
        description=(
            'Full name of the patient .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this questionnaire is completed")  # YYYY-MM-DD format


class YourWellnessGoals(BaseModel):
    """Initial health goals and progress toward them"""

    your_initial_health_goal_1: str = Field(
        default="",
        description=(
            "First initial health goal you had for care .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    progress_toward_goal_1_rating: Literal["1", "2", "3", "4", "5", "N/A", ""] = Field(
        default="",
        description="Rating of your progress toward your first health goal (1 = worse, 5 = improved)",
    )

    your_initial_health_goal_2: str = Field(
        default="",
        description=(
            "Second initial health goal you had for care .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    progress_toward_goal_2_rating: Literal["1", "2", "3", "4", "5", "N/A", ""] = Field(
        default="",
        description=(
            "Rating of your progress toward your second health goal (1 = worse, 5 = improved)"
        ),
    )

    your_initial_health_goal_3: str = Field(
        default="",
        description=(
            "Third initial health goal you had for care .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    progress_toward_goal_3_rating: Literal["1", "2", "3", "4", "5", "N/A", ""] = Field(
        default="",
        description="Rating of your progress toward your third health goal (1 = worse, 5 = improved)",
    )


class HowAreYouDoing(BaseModel):
    """Improvements noticed and changes since beginning care"""

    sleeping: BooleanLike = Field(
        default="", description="Check if you have noticed improvements in sleeping"
    )

    walking_running: BooleanLike = Field(
        default="", description="Check if you have noticed improvements in walking and running"
    )

    flexibility_mobility: BooleanLike = Field(
        default="", description="Check if you have noticed improvements in flexibility and mobility"
    )

    sitting: BooleanLike = Field(
        default="", description="Check if you have noticed improvements in sitting"
    )

    energy_levels: BooleanLike = Field(
        default="", description="Check if you have noticed improvements in energy levels"
    )

    emotional_stress: BooleanLike = Field(
        default="", description="Check if you have noticed improvements in emotional stress"
    )

    changing_habits: BooleanLike = Field(
        default="", description="Check if you have noticed improvements in changing habits"
    )

    pain_management: BooleanLike = Field(
        default="", description="Check if you have noticed improvements in pain management"
    )

    family_life: BooleanLike = Field(
        default="", description="Check if you have noticed improvements in family life"
    )

    work_life: BooleanLike = Field(
        default="", description="Check if you have noticed improvements in work life"
    )

    physical_changes: str = Field(
        default="",
        description=(
            "Describe any physical changes (e.g., less pain, more mobility, feeling "
            'stronger) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    health_changes: str = Field(
        default="",
        description=(
            "Describe any health changes (e.g., fewer illnesses, less severe symptoms) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    emotional_changes: str = Field(
        default="",
        description=(
            "Describe any emotional changes (e.g., better mood regulation, less anxious) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    energy_stress_levels: str = Field(
        default="",
        description=(
            "Describe any changes in energy and stress levels (e.g., sleeping better, more "
            'energy, happier) .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    new_health_challenges_or_stressors: str = Field(
        default="",
        description=(
            "Describe any new health challenges or stressors in your life .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class YourHealthProgress(BaseModel):
    """Overall progress and impact ratings"""

    improvement_taking_longer_than_expected: BooleanLike = Field(
        default="", description="Select if your improvement so far is taking longer than expected"
    )

    improvement_progressing_as_expected: BooleanLike = Field(
        default="", description="Select if your improvement so far is progressing as expected"
    )

    improvement_occurring_faster_than_expected: BooleanLike = Field(
        default="",
        description="Select if your improvement so far is occurring faster than expected",
    )

    impact_of_improvements_on_health_rating: Literal["1", "2", "3", "4", "5", "N/A", ""] = Field(
        default="",
        description=(
            "Rate the impact of these improvements on your health (1 = no impact, 5 = great impact)"
        ),
    )

    impact_of_improvements_on_quality_of_life_rating: Literal[
        "1", "2", "3", "4", "5", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Rate the impact of these improvements on your quality of life (1 = no impact, "
            "5 = great impact)"
        ),
    )


class ProgressExamQuestionnaire(BaseModel):
    """
    Progress Exam Questionnaire

    To help ensure that we are on track toward achieving your health goals, please tell us what types of changes you are experiencing as your body begins the natural healing process.
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    your_wellness_goals: YourWellnessGoals = Field(..., description="Your Wellness Goals")
    how_are_you_doing: HowAreYouDoing = Field(..., description="How Are You Doing?")
    your_health_progress: YourHealthProgress = Field(..., description="Your Health Progress")
