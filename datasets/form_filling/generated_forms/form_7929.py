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
    """Basic patient details and visit date"""

    patient_name: str = Field(
        ...,
        description=(
            'Patient\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this questionnaire is completed")  # YYYY-MM-DD format


class YourWellnessGoals(BaseModel):
    """Initial health goals and progress toward each goal"""

    initial_health_goal_1: str = Field(
        default="",
        description=(
            'First initial health goal for care .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    progress_toward_goal_1: Literal[
        "1 - Worse", "2", "3 - No change", "4", "5 - Improved", "N/A", ""
    ] = Field(default="", description="Rating of progress toward the first health goal (1–5)")

    initial_health_goal_2: str = Field(
        default="",
        description=(
            'Second initial health goal for care .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    progress_toward_goal_2: Literal[
        "1 - Worse", "2", "3 - No change", "4", "5 - Improved", "N/A", ""
    ] = Field(default="", description="Rating of progress toward the second health goal (1–5)")

    initial_health_goal_3: str = Field(
        default="",
        description=(
            'Third initial health goal for care .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    progress_toward_goal_3: Literal[
        "1 - Worse", "2", "3 - No change", "4", "5 - Improved", "N/A", ""
    ] = Field(default="", description="Rating of progress toward the third health goal (1–5)")


class HowAreYouDoing(BaseModel):
    """Improvements noticed in daily activities, health, and life areas"""

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
    """Overall perception of improvement and its impact"""

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

    impact_of_improvements_on_health: Literal[
        "1 - No impact", "2", "3", "4", "5 - Great impact", "N/A", ""
    ] = Field(default="", description="Rate the impact of these improvements on your health (1–5)")

    impact_of_improvements_on_quality_of_life: Literal[
        "1 - No impact", "2", "3", "4", "5 - Great impact", "N/A", ""
    ] = Field(
        default="",
        description="Rate the impact of these improvements on your quality of life (1–5)",
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
