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
    """Initial health goals and progress toward those goals"""

    your_initial_health_goals_for_care_were_goal_1: str = Field(
        default="",
        description=(
            'First initial health goal for care .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    how_would_you_rate_your_progress_toward_those_goals_so_far_goal_1_rating: Literal[
        "Worse", "No change", "Improved", "N/A", ""
    ] = Field(default="", description="Overall progress rating for goal 1")

    your_initial_health_goals_for_care_were_goal_2: str = Field(
        default="",
        description=(
            'Second initial health goal for care .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    how_would_you_rate_your_progress_toward_those_goals_so_far_goal_2_rating: Union[
        float, Literal["N/A", ""]
    ] = Field(default="", description="Numeric progress rating for goal 2 (1–5)")

    your_initial_health_goals_for_care_were_goal_3: str = Field(
        default="",
        description=(
            'Third initial health goal for care .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    how_would_you_rate_your_progress_toward_those_goals_so_far_goal_3_rating: Union[
        float, Literal["N/A", ""]
    ] = Field(default="", description="Numeric progress rating for goal 3 (1–5)")


class HowAreYouDoing(BaseModel):
    """Areas of improvement and changes noticed since beginning care"""

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

    energy_stress_levels_changes: str = Field(
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
    """Overall progress and impact on health and quality of life"""

    your_improvements_so_far_is_taking_longer_than_expected: BooleanLike = Field(
        default="", description="Select if your improvements are taking longer than expected"
    )

    your_improvements_so_far_is_progressing_as_expected: BooleanLike = Field(
        default="", description="Select if your improvements are progressing as expected"
    )

    your_improvements_so_far_is_occurring_faster_than_expected: BooleanLike = Field(
        default="", description="Select if your improvements are occurring faster than expected"
    )

    impact_of_improvements_on_your_health: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Rate the impact of improvements on your health from 1 (no impact) to 5 (great impact)"
        ),
    )

    impact_of_improvements_on_your_quality_of_life: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Rate the impact of improvements on your quality of life from 1 (no impact) to "
            "5 (great impact)"
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
