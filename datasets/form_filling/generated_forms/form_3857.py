from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class StudentInformation(BaseModel):
    """Basic information about the student"""

    student_name: str = Field(
        ...,
        description=(
            "Full legal name of the student being examined .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Student's date of birth")  # YYYY-MM-DD format


class PatientHistoryQuestions(BaseModel):
    """General medical history related to exercise and heart/lung conditions"""

    has_your_child_fainted_or_passed_out_during_or_after_exercise_emotion_or_startle: BooleanLike = Field(
        ...,
        description=(
            "Indicate yes or no if the child has ever fainted or passed out during or after "
            "exercise, emotion, or startle"
        ),
    )

    has_your_child_ever_had_extreme_shortness_of_breath_during_exercise: BooleanLike = Field(
        ...,
        description=(
            "Indicate yes or no if the child has ever had extreme shortness of breath "
            "during exercise"
        ),
    )

    has_your_child_had_extreme_fatigue_associated_with_exercise_different_from_other_children: BooleanLike = Field(
        ...,
        description=(
            "Indicate yes or no if the child has had extreme fatigue with exercise that is "
            "different from peers"
        ),
    )

    has_your_child_ever_had_discomfort_pain_or_pressure_in_his_her_chest_during_exercise: BooleanLike = Field(
        ...,
        description=(
            "Indicate yes or no if the child has ever had chest discomfort, pain, or "
            "pressure during exercise"
        ),
    )

    has_a_doctor_ever_ordered_a_test_for_your_childs_heart: BooleanLike = Field(
        ...,
        description="Indicate yes or no if a doctor has ever ordered any test for the child's heart",
    )

    has_your_child_ever_been_diagnosed_with_an_unexplained_seizure_disorder: BooleanLike = Field(
        ...,
        description=(
            "Indicate yes or no if the child has been diagnosed with an unexplained seizure "
            "disorder"
        ),
    )

    has_your_child_ever_been_diagnosed_with_exercise_induced_asthma_not_well_controlled_with_medication: BooleanLike = Field(
        ...,
        description=(
            "Indicate yes or no if the child has exercise-induced asthma that is not well "
            "controlled with medication"
        ),
    )

    explain_yes_answers_here_patient_history: str = Field(
        default="",
        description=(
            "Provide details for any patient history questions above that were answered "
            "'Yes' .If you cannot fill this, write \"N/A\". If this field should not be "
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class COVID19(BaseModel):
    """COVID-19 history, exposure, and vaccination details"""

    has_your_child_been_diagnosed_with_covid_19: BooleanLike = Field(
        ..., description="Indicate yes or no if the child has ever been diagnosed with COVID-19"
    )

    if_yes_is_your_child_still_having_symptoms_from_their_covid_19_infection: BooleanLike = Field(
        default="",
        description=(
            "If the child had COVID-19, indicate yes or no if they are still experiencing symptoms"
        ),
    )

    was_your_child_hospitalized_as_a_result_for_complications_of_covid_19: BooleanLike = Field(
        ...,
        description="Indicate yes or no if the child was hospitalized due to COVID-19 complications",
    )

    has_your_child_been_diagnosed_with_multi_inflammatory_syndrome_in_children_mis_c: BooleanLike = Field(
        ..., description="Indicate yes or no if the child has been diagnosed with MIS-C"
    )

    did_your_child_have_any_special_tests_ordered_for_their_heart_or_lungs_or_were_referred_to_a_heart_specialist_cardiologist_to_be_cleared_to_return_to_sports: BooleanLike = Field(
        ...,
        description=(
            "Indicate yes or no if special heart or lung tests were ordered or if the child "
            "was referred to a cardiologist to return to sports"
        ),
    )

    has_your_child_returned_back_to_full_participation_in_sports: BooleanLike = Field(
        ..., description="Indicate yes or no if the child has resumed full sports participation"
    )

    has_your_child_had_direct_or_known_exposure_to_someone_diagnosed_with_covid_19_in_the_past_3_months: BooleanLike = Field(
        ...,
        description=(
            "Indicate yes or no if the child has had direct or known exposure to a COVID-19 "
            "case in the last 3 months"
        ),
    )

    was_your_child_tested_for_covid_19: BooleanLike = Field(
        default="", description="Indicate yes or no if the child was tested for COVID-19"
    )

    did_your_child_receive_the_covid_19_vaccine: BooleanLike = Field(
        default="",
        description="Indicate yes or no if the child has received any COVID-19 vaccination",
    )

    what_was_the_manufacturer_of_the_vaccine: str = Field(
        default="",
        description=(
            "Name of the manufacturer of the COVID-19 vaccine received (e.g., Pfizer, "
            'Moderna, Johnson & Johnson) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_vaccinations: str = Field(
        default="", description="Date or dates when the COVID-19 vaccine doses were administered"
    )  # YYYY-MM-DD format

    explain_yes_answers_here_covid_19: str = Field(
        default="",
        description=(
            "Provide details for any COVID-19 questions above that were answered 'Yes' .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AnnualPreparticipationPhysicalExamination202122(BaseModel):
    """
    2021-22 ANNUAL PREPARTICIPATION PHYSICAL EXAMINATION

    The physician should fill out this form with assistance from the parent or guardian.
    """

    student_information: StudentInformation = Field(..., description="Student Information")
    patient_history_questions: PatientHistoryQuestions = Field(
        ..., description="Patient History Questions"
    )
    covid_19: COVID19 = Field(..., description="COVID-19")
