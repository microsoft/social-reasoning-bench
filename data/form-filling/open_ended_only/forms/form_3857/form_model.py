from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class StudentInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Basic student details"""

    student_name: str = Field(
        ...,
        description=(
            "Full legal name of the student .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    date_of_birth: str = Field(
        ...,
        description="Student's date of birth"
    )  # YYYY-MM-DD format


class PatientHistoryQuestions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """General health and exercise-related history questions"""

    has_your_child_fainted_or_passed_out_during_or_after_exercise_emotion_or_startle: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the child has fainted or passed out during or after exercise, "
            "emotion, or startle"
        )
    )

    has_your_child_ever_had_extreme_shortness_of_breath_during_exercise: BooleanLike = Field(
        ...,
        description="Indicate if the child has ever had extreme shortness of breath during exercise"
    )

    has_your_child_had_extreme_fatigue_associated_with_exercise_different_from_other_children: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the child has had extreme fatigue with exercise, different from "
            "other children"
        )
    )

    has_your_child_ever_had_discomfort_pain_or_pressure_in_his_her_chest_during_exercise: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the child has had chest discomfort, pain, or pressure during "
            "exercise"
        )
    )

    has_a_doctor_ever_ordered_a_test_for_your_childs_heart: BooleanLike = Field(
        ...,
        description="Indicate if a doctor has ever ordered a test for the child's heart"
    )

    has_your_child_ever_been_diagnosed_with_an_unexplained_seizure_disorder: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the child has ever been diagnosed with an unexplained seizure "
            "disorder"
        )
    )

    has_your_child_ever_been_diagnosed_with_exercise_induced_asthma_not_well_controlled_with_medication: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the child has exercise-induced asthma not well controlled with "
            "medication"
        )
    )

    explain_yes_answers_here_patient_history_questions: str = Field(
        ...,
        description=(
            "Provide explanations for any 'Yes' answers to the patient history questions "
            ".If you cannot fill this, write \"N/A\". If this field should not be filled by "
            "you (for example, it belongs to another person or office), leave it blank "
            "(empty string \"\")."
        )
    )


class COVID19(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """COVID-19 related history and vaccination information"""

    has_your_child_been_diagnosed_with_covid_19: BooleanLike = Field(
        ...,
        description="Indicate if the child has been diagnosed with COVID-19"
    )

    if_yes_is_your_child_still_having_symptoms_from_their_covid_19_infection: BooleanLike = Field(
        ...,
        description="If diagnosed with COVID-19, indicate if the child is still having symptoms"
    )

    was_your_child_hospitalized_as_a_result_for_complications_of_covid_19: BooleanLike = Field(
        ...,
        description="Indicate if the child was hospitalized due to COVID-19 complications"
    )

    has_your_child_been_diagnosed_with_multi_inflammatory_syndrome_in_children_mis_c: BooleanLike = Field(
        ...,
        description="Indicate if the child has been diagnosed with MIS-C"
    )

    did_your_child_have_any_special_tests_ordered_for_their_heart_or_lungs_or_were_referred_to_a_heart_specialist_cardiologist_to_be_cleared_to_return_to_sports: BooleanLike = Field(
        ...,
        description=(
            "Indicate if special tests were ordered or referral to a cardiologist was made "
            "for return to sports"
        )
    )

    has_your_child_returned_back_to_full_participation_in_sports: BooleanLike = Field(
        ...,
        description="Indicate if the child has returned to full participation in sports"
    )

    has_your_child_had_direct_or_known_exposure_to_someone_diagnosed_with_covid_19_in_the_past_3_months: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the child had direct or known exposure to someone with COVID-19 in "
            "the past 3 months"
        )
    )

    was_your_child_tested_for_covid_19: BooleanLike = Field(
        ...,
        description="Indicate if the child was tested for COVID-19"
    )

    did_your_child_receive_the_covid_19_vaccine: BooleanLike = Field(
        ...,
        description="Indicate if the child received the COVID-19 vaccine"
    )

    what_was_the_manufacturer_of_the_vaccine: str = Field(
        ...,
        description=(
            "Enter the manufacturer of the COVID-19 vaccine received .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    date_of_vaccination_s_first: str = Field(
        ...,
        description="Date of the first COVID-19 vaccination"
    )  # YYYY-MM-DD format

    date_of_vaccination_s_second: str = Field(
        ...,
        description="Date of the second COVID-19 vaccination, if applicable"
    )  # YYYY-MM-DD format

    explain_yes_answers_here_covid_19: str = Field(
        ...,
        description=(
            "Provide explanations for any 'Yes' answers to the COVID-19 questions .If you "
            "cannot fill this, write \"N/A\". If this field should not be filled by you "
            "(for example, it belongs to another person or office), leave it blank (empty "
            "string \"\")."
        )
    )


class AnnualPreparticipationPhysicalExamination202122(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    2021-22 ANNUAL PREPARTICIPATION PHYSICAL EXAMINATION

    2021-22 ANNUAL PREPARTICIPATION PHYSICAL EXAMINATION  
    The physician should fill out this form with assistance from the parent or guardian.
    """

    student_information: StudentInformation = Field(
        ...,
        description="Student Information"
    )
    patient_history_questions: PatientHistoryQuestions = Field(
        ...,
        description="Patient History Questions"
    )
    covid_19: COVID19 = Field(
        ...,
        description="COVID-19"
    )