from typing import Literal, Optional, List, Union
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
            'Student\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Student's date of birth")  # YYYY-MM-DD format


class PatientHistoryQuestions(BaseModel):
    """General medical history related to exercise and conditions"""

    fainted_or_passed_out_during_or_after_exercise_emotion_or_startle: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the child has ever fainted or passed out during or after exercise, "
            "emotion, or startle"
        ),
    )

    fainted_or_passed_out_during_or_after_exercise_emotion_or_startle_no: BooleanLike = Field(
        default="",
        description=(
            "Represents a 'No' response to fainting or passing out during or after "
            "exercise, emotion, or startle"
        ),
    )

    extreme_shortness_of_breath_during_exercise: BooleanLike = Field(
        ...,
        description="Indicate if the child has ever had extreme shortness of breath during exercise",
    )

    extreme_shortness_of_breath_during_exercise_no: BooleanLike = Field(
        default="",
        description="Represents a 'No' response to extreme shortness of breath during exercise",
    )

    extreme_fatigue_associated_with_exercise: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the child has had extreme fatigue with exercise, different from peers"
        ),
    )

    extreme_fatigue_associated_with_exercise_no: BooleanLike = Field(
        default="",
        description="Represents a 'No' response to extreme fatigue associated with exercise",
    )

    chest_discomfort_pain_or_pressure_during_exercise: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the child has had chest discomfort, pain, or pressure during exercise"
        ),
    )

    chest_discomfort_pain_or_pressure_during_exercise_no: BooleanLike = Field(
        default="",
        description=(
            "Represents a 'No' response to chest discomfort, pain, or pressure during exercise"
        ),
    )

    doctor_ordered_test_for_heart: BooleanLike = Field(
        ..., description="Indicate if a doctor has ever ordered a test for the child's heart"
    )

    doctor_ordered_test_for_heart_no: BooleanLike = Field(
        default="",
        description="Represents a 'No' response to a doctor ordering a test for the child's heart",
    )

    diagnosed_unexplained_seizure_disorder: BooleanLike = Field(
        ...,
        description="Indicate if the child has been diagnosed with an unexplained seizure disorder",
    )

    diagnosed_unexplained_seizure_disorder_no: BooleanLike = Field(
        default="",
        description="Represents a 'No' response to diagnosis of an unexplained seizure disorder",
    )

    diagnosed_exercise_induced_asthma_not_well_controlled: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the child has exercise-induced asthma that is not well controlled "
            "with medication"
        ),
    )

    diagnosed_exercise_induced_asthma_not_well_controlled_no: BooleanLike = Field(
        default="",
        description=(
            "Represents a 'No' response to diagnosis of poorly controlled exercise-induced asthma"
        ),
    )

    explain_yes_answers_patient_history_questions: str = Field(
        default="",
        description=(
            "Provide details for any 'Yes' answers to the patient history questions above "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class COVID19(BaseModel):
    """COVID-19 history, exposure, and vaccination details"""

    covid_diagnosed: BooleanLike = Field(
        ..., description="Indicate if the child has been diagnosed with COVID-19"
    )

    covid_diagnosed_no: BooleanLike = Field(
        default="",
        description="Represents a 'No' response to the child being diagnosed with COVID-19",
    )

    still_having_covid_symptoms: BooleanLike = Field(
        default="",
        description="If the child had COVID-19, indicate if they are still having symptoms",
    )

    still_having_covid_symptoms_no: BooleanLike = Field(
        default="",
        description="Represents a 'No' response to still having symptoms from COVID-19 infection",
    )

    hospitalized_for_covid_complications: BooleanLike = Field(
        ..., description="Indicate if the child was hospitalized due to complications of COVID-19"
    )

    hospitalized_for_covid_complications_no: BooleanLike = Field(
        default="",
        description="Represents a 'No' response to hospitalization for COVID-19 complications",
    )

    diagnosed_mis_c: BooleanLike = Field(
        ..., description="Indicate if the child has been diagnosed with MIS-C"
    )

    diagnosed_mis_c_no: BooleanLike = Field(
        default="", description="Represents a 'No' response to diagnosis of MIS-C"
    )

    special_heart_or_lung_tests_or_cardiologist_referral: BooleanLike = Field(
        ...,
        description=(
            "Indicate if special heart or lung tests were ordered or if the child was "
            "referred to a cardiologist to return to sports"
        ),
    )

    special_heart_or_lung_tests_or_cardiologist_referral_no: BooleanLike = Field(
        default="",
        description=(
            "Represents a 'No' response to special heart/lung tests or cardiologist "
            "referral to return to sports"
        ),
    )

    returned_to_full_sports_participation: BooleanLike = Field(
        ..., description="Indicate if the child has returned to full participation in sports"
    )

    returned_to_full_sports_participation_no: BooleanLike = Field(
        default="",
        description="Represents a 'No' response to returning to full participation in sports",
    )

    exposure_to_covid_past_3_months: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the child has had direct or known exposure to someone with "
            "COVID-19 in the past 3 months"
        ),
    )

    exposure_to_covid_past_3_months_no: BooleanLike = Field(
        default="",
        description=(
            "Represents a 'No' response to exposure to someone with COVID-19 in the past 3 months"
        ),
    )

    tested_for_covid: BooleanLike = Field(
        default="",
        description="If the child had exposure, indicate if they were tested for COVID-19",
    )

    tested_for_covid_no: BooleanLike = Field(
        default="", description="Represents a 'No' response to the child being tested for COVID-19"
    )

    received_covid_vaccine: BooleanLike = Field(
        ..., description="Indicate if the child received the COVID-19 vaccine"
    )

    received_covid_vaccine_no: BooleanLike = Field(
        default="",
        description="Represents a 'No' response to the child receiving the COVID-19 vaccine",
    )

    vaccine_manufacturer: str = Field(
        default="",
        description=(
            "Name of the manufacturer of the COVID-19 vaccine received .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_vaccinations: str = Field(
        default="",
        description=(
            "Date or dates when the COVID-19 vaccine doses were administered .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    explain_yes_answers_covid_19: str = Field(
        default="",
        description=(
            "Provide details for any 'Yes' answers to the COVID-19 questions above .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
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
