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
            'Full legal name of the student .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Student's date of birth")  # YYYY-MM-DD format


class PatientHistoryQuestions(BaseModel):
    """General cardiac and exercise-related medical history"""

    fainted_during_after_exercise_yes: BooleanLike = Field(
        ...,
        description=(
            "Check if the child has fainted or passed out during or after exercise, "
            "emotion, or startle"
        ),
    )

    fainted_during_after_exercise_no: BooleanLike = Field(
        ...,
        description=(
            "Check if the child has not fainted or passed out during or after exercise, "
            "emotion, or startle"
        ),
    )

    extreme_shortness_of_breath_yes: BooleanLike = Field(
        ..., description="Check if the child has had extreme shortness of breath during exercise"
    )

    extreme_shortness_of_breath_no: BooleanLike = Field(
        ...,
        description="Check if the child has not had extreme shortness of breath during exercise",
    )

    extreme_fatigue_with_exercise_yes: BooleanLike = Field(
        ...,
        description=(
            "Check if the child has had extreme fatigue with exercise that is different from peers"
        ),
    )

    extreme_fatigue_with_exercise_no: BooleanLike = Field(
        ...,
        description=(
            "Check if the child has not had extreme fatigue with exercise that is different "
            "from peers"
        ),
    )

    chest_discomfort_during_exercise_yes: BooleanLike = Field(
        ...,
        description="Check if the child has had chest discomfort, pain, or pressure during exercise",
    )

    chest_discomfort_during_exercise_no: BooleanLike = Field(
        ...,
        description=(
            "Check if the child has not had chest discomfort, pain, or pressure during exercise"
        ),
    )

    heart_test_ordered_yes: BooleanLike = Field(
        ..., description="Check if a doctor has ever ordered a test for the child's heart"
    )

    heart_test_ordered_no: BooleanLike = Field(
        ..., description="Check if a doctor has not ordered a test for the child's heart"
    )

    unexplained_seizure_disorder_yes: BooleanLike = Field(
        ...,
        description="Check if the child has been diagnosed with an unexplained seizure disorder",
    )

    unexplained_seizure_disorder_no: BooleanLike = Field(
        ...,
        description="Check if the child has not been diagnosed with an unexplained seizure disorder",
    )

    exercise_induced_asthma_not_controlled_yes: BooleanLike = Field(
        ...,
        description=(
            "Check if the child has exercise-induced asthma that is not well controlled "
            "with medication"
        ),
    )

    exercise_induced_asthma_not_controlled_no: BooleanLike = Field(
        ...,
        description=(
            "Check if the child does not have exercise-induced asthma that is poorly controlled"
        ),
    )

    explain_yes_answers_cardiac_history: str = Field(
        default="",
        description=(
            "Provide details for any 'Yes' answers in the cardiac history questions .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class COVID19(BaseModel):
    """COVID-19 history, exposure, and vaccination details"""

    covid_diagnosed_yes: BooleanLike = Field(
        ..., description="Check if the child has been diagnosed with COVID-19"
    )

    covid_diagnosed_no: BooleanLike = Field(
        ..., description="Check if the child has not been diagnosed with COVID-19"
    )

    still_having_covid_symptoms_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if the child is still experiencing symptoms from a prior COVID-19 infection"
        ),
    )

    still_having_covid_symptoms_no: BooleanLike = Field(
        default="",
        description=(
            "Check if the child is no longer experiencing symptoms from a prior COVID-19 infection"
        ),
    )

    hospitalized_for_covid_yes: BooleanLike = Field(
        default="",
        description="Check if the child was hospitalized due to complications of COVID-19",
    )

    hospitalized_for_covid_no: BooleanLike = Field(
        default="",
        description="Check if the child was not hospitalized due to complications of COVID-19",
    )

    mis_c_diagnosis_yes: BooleanLike = Field(
        default="", description="Check if the child has been diagnosed with MIS-C"
    )

    mis_c_diagnosis_no: BooleanLike = Field(
        default="", description="Check if the child has not been diagnosed with MIS-C"
    )

    special_heart_lung_tests_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if special heart or lung tests were ordered or the child was referred to "
            "a cardiologist to return to sports"
        ),
    )

    special_heart_lung_tests_no: BooleanLike = Field(
        default="",
        description=(
            "Check if no special heart or lung tests were ordered and the child was not "
            "referred to a cardiologist to return to sports"
        ),
    )

    returned_to_full_sports_yes: BooleanLike = Field(
        default="", description="Check if the child has returned to full participation in sports"
    )

    returned_to_full_sports_no: BooleanLike = Field(
        default="",
        description="Check if the child has not returned to full participation in sports",
    )

    covid_exposure_past_3_months_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if the child has had direct or known exposure to a COVID-19 case in the "
            "past 3 months"
        ),
    )

    covid_exposure_past_3_months_no: BooleanLike = Field(
        default="",
        description=(
            "Check if the child has not had direct or known exposure to a COVID-19 case in "
            "the past 3 months"
        ),
    )

    covid_tested_yes: BooleanLike = Field(
        default="", description="Check if the child was tested for COVID-19"
    )

    covid_tested_no: BooleanLike = Field(
        default="", description="Check if the child was not tested for COVID-19"
    )

    covid_vaccine_received_yes: BooleanLike = Field(
        default="", description="Check if the child received a COVID-19 vaccine"
    )

    covid_vaccine_received_no: BooleanLike = Field(
        default="", description="Check if the child did not receive a COVID-19 vaccine"
    )

    vaccine_manufacturer: str = Field(
        default="",
        description=(
            "Name of the COVID-19 vaccine manufacturer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_vaccination_first_dose: str = Field(
        default="", description="Date of the first COVID-19 vaccine dose"
    )  # YYYY-MM-DD format

    date_of_vaccination_second_dose: str = Field(
        default="", description="Date of the second COVID-19 vaccine dose, if applicable"
    )  # YYYY-MM-DD format

    explain_yes_answers_covid_section: str = Field(
        default="",
        description=(
            "Provide details for any 'Yes' answers in the COVID-19 questions .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
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
