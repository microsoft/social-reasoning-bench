from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PatientInformationPreferences(BaseModel):
    """Basic patient details and what matters to them"""

    my_name: str = Field(
        ...,
        description=(
            'Patient\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Date this asthma action plan is completed"
    )  # YYYY-MM-DD format

    what_matters_to_me: str = Field(
        default="",
        description=(
            "What is most important to the patient regarding their health and asthma .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class TriggersUsualSymptoms(BaseModel):
    """Patient’s asthma triggers and usual symptoms"""

    other_trigger: str = Field(
        default="",
        description=(
            "Any additional asthma trigger not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_usual_symptoms: str = Field(
        default="",
        description=(
            "Any additional usual asthma symptom not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AsthmaControlAssessment(BaseModel):
    """Questions to assess how well asthma is controlled"""

    daytime_symptoms: Literal[
        "None", "3 or more times a week", "Continuous & getting worse", "N/A", ""
    ] = Field(..., description="Frequency and severity of daytime asthma symptoms")

    nighttime_symptoms: Literal[
        "None", "1 or more times a week", "Continuous & getting worse", "N/A", ""
    ] = Field(..., description="Frequency and severity of nighttime asthma symptoms")

    reliever_use_other_than_exercise: Literal[
        "None", "3 or more times a week", "Relief for less than 3 to 4 hours", "N/A", ""
    ] = Field(
        ...,
        description="How often the reliever inhaler is used, excluding use prescribed for exercise",
    )

    physical_activity_or_exercise: Literal["Normal", "Limited", "Very limited", "N/A", ""] = Field(
        ..., description="Impact of asthma on physical activity or exercise"
    )

    can_go_to_school_or_work: Literal["Yes", "Maybe", "No", "N/A", ""] = Field(
        ..., description="Ability to attend school or work given current asthma control"
    )


class DailyMedicationsControllerReliever(BaseModel):
    """Regular controller medicines and reliever details"""

    controller_1_name_colour_strength: str = Field(
        default="",
        description=(
            "First daily controller medication name, inhaler colour, and strength .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    controller_2_name_colour_strength: str = Field(
        default="",
        description=(
            "Second daily controller medication name, inhaler colour, and strength .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    controller_3_name_colour_strength: str = Field(
        default="",
        description=(
            "Third daily controller medication name, inhaler colour, and strength .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    controller_4_name_colour_strength: str = Field(
        default="",
        description=(
            "Fourth daily controller medication name, inhaler colour, and strength .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reliever_name_colour_strength: str = Field(
        ...,
        description=(
            "Reliever (rescue) medication name, inhaler colour, and strength .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    take_reliever_before_exercise_yes: BooleanLike = Field(
        default="", description="Indicates if the reliever should be taken before exercise"
    )

    take_reliever_as_needed_number_of_puffs: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of reliever puffs to take as needed before or around exercise",
    )


class StayControlledAvoidMyTriggers(BaseModel):
    """Ongoing daily dosing to stay controlled"""

    stay_controlled_1_take_amount: str = Field(
        default="",
        description=(
            "Dose or number of puffs for the first medication in the STAY CONTROLLED "
            'section .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    stay_controlled_1_am: BooleanLike = Field(
        default="", description="Check if the first STAY CONTROLLED dose is taken in the morning"
    )

    stay_controlled_1_pm: BooleanLike = Field(
        default="", description="Check if the first STAY CONTROLLED dose is taken in the evening"
    )

    stay_controlled_2_take_amount: str = Field(
        default="",
        description=(
            "Dose or number of puffs for the second medication in the STAY CONTROLLED "
            'section .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    stay_controlled_2_am: BooleanLike = Field(
        default="", description="Check if the second STAY CONTROLLED dose is taken in the morning"
    )

    stay_controlled_2_pm: BooleanLike = Field(
        default="", description="Check if the second STAY CONTROLLED dose is taken in the evening"
    )

    stay_controlled_3_take_amount: str = Field(
        default="",
        description=(
            "Dose or number of puffs for the third medication in the STAY CONTROLLED "
            'section .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    stay_controlled_3_am: BooleanLike = Field(
        default="", description="Check if the third STAY CONTROLLED dose is taken in the morning"
    )

    stay_controlled_3_pm: BooleanLike = Field(
        default="", description="Check if the third STAY CONTROLLED dose is taken in the evening"
    )

    stay_controlled_4_take_amount: str = Field(
        default="",
        description=(
            "Dose or number of puffs for the fourth medication in the STAY CONTROLLED "
            'section .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    stay_controlled_4_am: BooleanLike = Field(
        default="", description="Check if the fourth STAY CONTROLLED dose is taken in the morning"
    )

    stay_controlled_4_pm: BooleanLike = Field(
        default="", description="Check if the fourth STAY CONTROLLED dose is taken in the evening"
    )


class TakeAction(BaseModel):
    """Step-up treatment when asthma is getting worse"""

    see_doctor_if_no_improvement_days: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of days to wait before seeing a doctor if there is no improvement",
    )

    continue_this_dose_for_first_section: str = Field(
        default="",
        description=(
            "Duration to continue the first TAKE ACTION dose schedule .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    take_action_1_take_amount_first_section: str = Field(
        default="",
        description=(
            "Dose or number of puffs for the first medication in the first TAKE ACTION "
            'schedule .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    take_action_1_am_first_section: BooleanLike = Field(
        default="",
        description="Check if the first TAKE ACTION (first section) dose is taken in the morning",
    )

    take_action_1_pm_first_section: BooleanLike = Field(
        default="",
        description="Check if the first TAKE ACTION (first section) dose is taken in the evening",
    )

    take_action_2_take_amount_first_section: str = Field(
        default="",
        description=(
            "Dose or number of puffs for the second medication in the first TAKE ACTION "
            'schedule .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    take_action_2_am_first_section: BooleanLike = Field(
        default="",
        description="Check if the second TAKE ACTION (first section) dose is taken in the morning",
    )

    take_action_2_pm_first_section: BooleanLike = Field(
        default="",
        description="Check if the second TAKE ACTION (first section) dose is taken in the evening",
    )

    take_action_3_take_amount_first_section: str = Field(
        default="",
        description=(
            "Dose or number of puffs for the third medication in the first TAKE ACTION "
            'schedule .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    take_action_3_am_first_section: BooleanLike = Field(
        default="",
        description="Check if the third TAKE ACTION (first section) dose is taken in the morning",
    )

    take_action_3_pm_first_section: BooleanLike = Field(
        default="",
        description="Check if the third TAKE ACTION (first section) dose is taken in the evening",
    )

    take_action_4_take_amount_first_section: str = Field(
        default="",
        description=(
            "Dose or number of puffs for the fourth medication in the first TAKE ACTION "
            'schedule .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    take_action_4_am_first_section: BooleanLike = Field(
        default="",
        description="Check if the fourth TAKE ACTION (first section) dose is taken in the morning",
    )

    take_action_4_pm_first_section: BooleanLike = Field(
        default="",
        description="Check if the fourth TAKE ACTION (first section) dose is taken in the evening",
    )

    continue_this_dose_for_second_section: str = Field(
        default="",
        description=(
            "Duration to continue the second TAKE ACTION dose schedule .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    take_number_of_puffs_as_needed_second_section: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of puffs to take as needed in the second TAKE ACTION section",
    )


class NotesCompletion(BaseModel):
    """Additional notes and who completed the plan"""

    notes: str = Field(
        default="",
        description=(
            "Additional notes or instructions related to the asthma action plan .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    completed_with: str = Field(
        default="",
        description=(
            "Name of the person or healthcare provider who completed the plan with the "
            'patient .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class AsthmaActionPlan(BaseModel):
    """
    ASTHMA Action Plan

    ''
    """

    patient_information__preferences: PatientInformationPreferences = Field(
        ..., description="Patient Information & Preferences"
    )
    triggers__usual_symptoms: TriggersUsualSymptoms = Field(
        ..., description="Triggers & Usual Symptoms"
    )
    asthma_control_assessment: AsthmaControlAssessment = Field(
        ..., description="Asthma Control Assessment"
    )
    daily_medications___controller__reliever: DailyMedicationsControllerReliever = Field(
        ..., description="Daily Medications – Controller & Reliever"
    )
    stay_controlled__avoid_my_triggers: StayControlledAvoidMyTriggers = Field(
        ..., description="Stay Controlled & Avoid My Triggers"
    )
    take_action: TakeAction = Field(..., description="Take Action")
    notes__completion: NotesCompletion = Field(..., description="Notes & Completion")
