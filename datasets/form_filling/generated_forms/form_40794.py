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

    name: str = Field(
        ...,
        description=(
            'Patient\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    age: Union[float, Literal["N/A", ""]] = Field(..., description="Patient's age in years")

    height: str = Field(
        ...,
        description=(
            "Patient's height (include units, e.g., ft/in or cm) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    weight: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Patient's weight (include units if requested)"
    )


class CurrentPainandTherapyGoals(BaseModel):
    """Current pain description and physical therapy goals"""

    what_eases_your_pain: str = Field(
        default="",
        description=(
            "Describe anything that reduces or eases your pain .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    what_makes_your_pain_worse: str = Field(
        default="",
        description=(
            "Describe anything that increases or worsens your pain .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    what_are_your_goals_in_physical_therapy: str = Field(
        default="",
        description=(
            "List your main goals or expectations for physical therapy .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PreviousTreatmentandDiagnosticTests(BaseModel):
    """History of treatment for this problem and related tests"""

    have_you_had_previous_treatment_for_this_problem: BooleanLike = Field(
        default="",
        description="Indicate whether you have received prior treatment for this problem",
    )

    pt: BooleanLike = Field(
        default="", description="Check if you previously received physical therapy for this problem"
    )

    chiropractic: BooleanLike = Field(
        default="",
        description="Check if you previously received chiropractic care for this problem",
    )

    other_previous_treatment_type: str = Field(
        default="",
        description=(
            "Specify any other type of previous treatment for this problem .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    have_you_had_any_of_the_following_tests_x_ray: BooleanLike = Field(
        default="", description="Indicate if you have had an X-ray related to this condition"
    )

    have_you_had_any_of_the_following_tests_ct_scan: BooleanLike = Field(
        default="", description="Indicate if you have had a CT scan related to this condition"
    )

    have_you_had_any_of_the_following_tests_mri: BooleanLike = Field(
        default="", description="Indicate if you have had an MRI related to this condition"
    )

    have_you_had_any_of_the_following_tests_emg: BooleanLike = Field(
        default="", description="Indicate if you have had an EMG related to this condition"
    )


class PastandCurrentMedicalConditions(BaseModel):
    """Checklist of medical conditions and related details"""

    allergies_yes: BooleanLike = Field(default="", description="Check YES if you have allergies")

    allergies_no: BooleanLike = Field(
        default="", description="Check NO if you do not have allergies"
    )

    anemia_yes: BooleanLike = Field(default="", description="Check YES if you have anemia")

    anemia_no: BooleanLike = Field(default="", description="Check NO if you do not have anemia")

    anxiety_yes: BooleanLike = Field(default="", description="Check YES if you have anxiety")

    anxiety_no: BooleanLike = Field(default="", description="Check NO if you do not have anxiety")

    arthritis_yes: BooleanLike = Field(default="", description="Check YES if you have arthritis")

    arthritis_no: BooleanLike = Field(
        default="", description="Check NO if you do not have arthritis"
    )

    asthma_yes: BooleanLike = Field(default="", description="Check YES if you have asthma")

    asthma_no: BooleanLike = Field(default="", description="Check NO if you do not have asthma")

    autoimmune_disorder_yes: BooleanLike = Field(
        default="", description="Check YES if you have an autoimmune disorder"
    )

    autoimmune_disorder_no: BooleanLike = Field(
        default="", description="Check NO if you do not have an autoimmune disorder"
    )

    cancer_yes: BooleanLike = Field(
        default="", description="Check YES if you have or have had cancer"
    )

    cancer_no: BooleanLike = Field(default="", description="Check NO if you have not had cancer")

    cardiac_conditions_yes: BooleanLike = Field(
        default="", description="Check YES if you have any cardiac (heart) conditions"
    )

    cardiac_conditions_no: BooleanLike = Field(
        default="", description="Check NO if you do not have cardiac conditions"
    )

    cardiac_pacemaker_yes: BooleanLike = Field(
        default="", description="Check YES if you have a cardiac pacemaker"
    )

    cardiac_pacemaker_no: BooleanLike = Field(
        default="", description="Check NO if you do not have a cardiac pacemaker"
    )

    chemical_dependency_yes: BooleanLike = Field(
        default="", description="Check YES if you have a history of chemical dependency"
    )

    chemical_dependency_no: BooleanLike = Field(
        default="", description="Check NO if you do not have a history of chemical dependency"
    )

    circulation_problems_yes: BooleanLike = Field(
        default="", description="Check YES if you have circulation problems"
    )

    circulation_problems_no: BooleanLike = Field(
        default="", description="Check NO if you do not have circulation problems"
    )

    currently_pregnant_yes: BooleanLike = Field(
        default="", description="Check YES if you are currently pregnant"
    )

    currently_pregnant_no: BooleanLike = Field(
        default="", description="Check NO if you are not currently pregnant"
    )

    depression_yes: BooleanLike = Field(default="", description="Check YES if you have depression")

    depression_no: BooleanLike = Field(
        default="", description="Check NO if you do not have depression"
    )

    diabetes_yes: BooleanLike = Field(default="", description="Check YES if you have diabetes")

    diabetes_no: BooleanLike = Field(default="", description="Check NO if you do not have diabetes")

    dizzy_spells_yes: BooleanLike = Field(
        default="", description="Check YES if you experience dizzy spells"
    )

    dizzy_spells_no: BooleanLike = Field(
        default="", description="Check NO if you do not experience dizzy spells"
    )

    emphysema_bronchitis_yes: BooleanLike = Field(
        default="", description="Check YES if you have emphysema or bronchitis"
    )

    emphysema_bronchitis_no: BooleanLike = Field(
        default="", description="Check NO if you do not have emphysema or bronchitis"
    )

    fibromyalgia_yes: BooleanLike = Field(
        default="", description="Check YES if you have fibromyalgia"
    )

    fibromyalgia_no: BooleanLike = Field(
        default="", description="Check NO if you do not have fibromyalgia"
    )

    fractures_yes: BooleanLike = Field(
        default="", description="Check YES if you have had fractures"
    )

    fractures_no: BooleanLike = Field(
        default="", description="Check NO if you have not had fractures"
    )

    gallbladder_problems_yes: BooleanLike = Field(
        default="", description="Check YES if you have gallbladder problems"
    )

    gallbladder_problems_no: BooleanLike = Field(
        default="", description="Check NO if you do not have gallbladder problems"
    )

    headaches_yes: BooleanLike = Field(
        default="", description="Check YES if you experience headaches"
    )

    headaches_no: BooleanLike = Field(
        default="", description="Check NO if you do not experience headaches"
    )

    hearing_impairment_yes: BooleanLike = Field(
        default="", description="Check YES if you have hearing impairment"
    )

    hearing_impairment_no: BooleanLike = Field(
        default="", description="Check NO if you do not have hearing impairment"
    )

    hepatitis_yes: BooleanLike = Field(default="", description="Check YES if you have hepatitis")

    hepatitis_no: BooleanLike = Field(
        default="", description="Check NO if you do not have hepatitis"
    )

    high_cholesterol_yes: BooleanLike = Field(
        default="", description="Check YES if you have high cholesterol"
    )

    high_cholesterol_no: BooleanLike = Field(
        default="", description="Check NO if you do not have high cholesterol"
    )

    high_low_blood_pressure_yes: BooleanLike = Field(
        default="", description="Check YES if you have high or low blood pressure"
    )

    high_low_blood_pressure_no: BooleanLike = Field(
        default="", description="Check NO if you do not have high or low blood pressure"
    )

    hiv_aids_yes: BooleanLike = Field(default="", description="Check YES if you have HIV or AIDS")

    hiv_aids_no: BooleanLike = Field(
        default="", description="Check NO if you do not have HIV or AIDS"
    )

    incontinence_yes: BooleanLike = Field(
        default="", description="Check YES if you have incontinence"
    )

    incontinence_no: BooleanLike = Field(
        default="", description="Check NO if you do not have incontinence"
    )

    kidney_problems_yes: BooleanLike = Field(
        default="", description="Check YES if you have kidney problems"
    )

    kidney_problems_no: BooleanLike = Field(
        default="", description="Check NO if you do not have kidney problems"
    )

    metal_implants_yes: BooleanLike = Field(
        default="", description="Check YES if you have metal implants"
    )

    metal_implants_no: BooleanLike = Field(
        default="", description="Check NO if you do not have metal implants"
    )

    mrsa_yes: BooleanLike = Field(
        default="", description="Check YES if you have a history of MRSA infection"
    )

    mrsa_no: BooleanLike = Field(
        default="", description="Check NO if you do not have a history of MRSA infection"
    )

    multiple_sclerosis_yes: BooleanLike = Field(
        default="", description="Check YES if you have multiple sclerosis"
    )

    multiple_sclerosis_no: BooleanLike = Field(
        default="", description="Check NO if you do not have multiple sclerosis"
    )

    muscular_disease_yes: BooleanLike = Field(
        default="", description="Check YES if you have a muscular disease"
    )

    muscular_disease_no: BooleanLike = Field(
        default="", description="Check NO if you do not have a muscular disease"
    )

    osteoporosis_yes: BooleanLike = Field(
        default="", description="Check YES if you have osteoporosis"
    )

    osteoporosis_no: BooleanLike = Field(
        default="", description="Check NO if you do not have osteoporosis"
    )

    parkinsons_yes: BooleanLike = Field(
        default="", description="Check YES if you have Parkinson’s disease"
    )

    parkinsons_no: BooleanLike = Field(
        default="", description="Check NO if you do not have Parkinson’s disease"
    )

    rheumatoid_arthritis_yes: BooleanLike = Field(
        default="", description="Check YES if you have rheumatoid arthritis"
    )

    rheumatoid_arthritis_no: BooleanLike = Field(
        default="", description="Check NO if you do not have rheumatoid arthritis"
    )

    seizures_yes: BooleanLike = Field(default="", description="Check YES if you have seizures")

    seizures_no: BooleanLike = Field(default="", description="Check NO if you do not have seizures")

    smoking_yes: BooleanLike = Field(default="", description="Check YES if you currently smoke")

    smoking_no: BooleanLike = Field(
        default="", description="Check NO if you do not currently smoke"
    )

    speech_problems_yes: BooleanLike = Field(
        default="", description="Check YES if you have speech problems"
    )

    speech_problems_no: BooleanLike = Field(
        default="", description="Check NO if you do not have speech problems"
    )

    strokes_yes: BooleanLike = Field(default="", description="Check YES if you have had strokes")

    strokes_no: BooleanLike = Field(default="", description="Check NO if you have not had strokes")

    thyroid_disease_yes: BooleanLike = Field(
        default="", description="Check YES if you have thyroid disease"
    )

    thyroid_disease_no: BooleanLike = Field(
        default="", description="Check NO if you do not have thyroid disease"
    )

    tuberculosis_yes: BooleanLike = Field(
        default="", description="Check YES if you have tuberculosis or a history of it"
    )

    tuberculosis_no: BooleanLike = Field(
        default="", description="Check NO if you do not have tuberculosis and no history of it"
    )

    vision_problems_yes: BooleanLike = Field(
        default="", description="Check YES if you have vision problems"
    )

    vision_problems_no: BooleanLike = Field(
        default="", description="Check NO if you do not have vision problems"
    )

    explain_yes_and_additional_conditions: str = Field(
        default="",
        description=(
            "Provide details for any conditions marked YES and list any additional "
            'conditions or precautions .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class FallHistory(BaseModel):
    """History of recent falls"""

    injury_result_of_fall_past_year_yes: BooleanLike = Field(
        default="", description="Select YES if your injury resulted from a fall in the past year"
    )

    injury_result_of_fall_past_year_no: BooleanLike = Field(
        default="",
        description="Select NO if your injury did not result from a fall in the past year",
    )

    two_or_more_falls_last_year_yes: BooleanLike = Field(
        default="", description="Select YES if you have had two or more falls in the last year"
    )

    two_or_more_falls_last_year_no: BooleanLike = Field(
        default="", description="Select NO if you have not had two or more falls in the last year"
    )


class SurgicalHistory(BaseModel):
    """Past surgeries and hospitalizations"""

    surgery_type: str = Field(
        default="",
        description=(
            "Type or description of surgery performed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_mm_yyyy: str = Field(
        default="", description="Date of surgery in mm/yyyy format"
    )  # YYYY-MM-DD format


class CurrentMedications(BaseModel):
    """List of medications currently being taken"""

    medication_row_1: str = Field(
        default="",
        description=(
            'Name of medication (row 1) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    dosage_row_1: str = Field(
        default="",
        description=(
            'Dosage of medication (row 1) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    frequency_row_1: str = Field(
        default="",
        description=(
            "How often the medication is taken (row 1) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    route_row_1: str = Field(
        default="",
        description=(
            "Route of administration (e.g., oral, injection) (row 1) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reason_taking_row_1: str = Field(
        default="",
        description=(
            "Reason for taking this medication (row 1) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medication_row_2: str = Field(
        default="",
        description=(
            'Name of medication (row 2) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    dosage_row_2: str = Field(
        default="",
        description=(
            'Dosage of medication (row 2) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    frequency_row_2: str = Field(
        default="",
        description=(
            "How often the medication is taken (row 2) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    route_row_2: str = Field(
        default="",
        description=(
            'Route of administration (row 2) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reason_taking_row_2: str = Field(
        default="",
        description=(
            "Reason for taking this medication (row 2) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medication_row_3: str = Field(
        default="",
        description=(
            'Name of medication (row 3) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    dosage_row_3: str = Field(
        default="",
        description=(
            'Dosage of medication (row 3) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    frequency_row_3: str = Field(
        default="",
        description=(
            "How often the medication is taken (row 3) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    route_row_3: str = Field(
        default="",
        description=(
            'Route of administration (row 3) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reason_taking_row_3: str = Field(
        default="",
        description=(
            "Reason for taking this medication (row 3) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medication_row_4: str = Field(
        default="",
        description=(
            'Name of medication (row 4) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    dosage_row_4: str = Field(
        default="",
        description=(
            'Dosage of medication (row 4) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    frequency_row_4: str = Field(
        default="",
        description=(
            "How often the medication is taken (row 4) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    route_row_4: str = Field(
        default="",
        description=(
            'Route of administration (row 4) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reason_taking_row_4: str = Field(
        default="",
        description=(
            "Reason for taking this medication (row 4) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medication_row_5: str = Field(
        default="",
        description=(
            'Name of medication (row 5) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    dosage_row_5: str = Field(
        default="",
        description=(
            'Dosage of medication (row 5) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    frequency_row_5: str = Field(
        default="",
        description=(
            "How often the medication is taken (row 5) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    route_row_5: str = Field(
        default="",
        description=(
            'Route of administration (row 5) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reason_taking_row_5: str = Field(
        default="",
        description=(
            "Reason for taking this medication (row 5) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Authorization(BaseModel):
    """Signature and date of completion"""

    signature: str = Field(
        ...,
        description=(
            "Patient's signature acknowledging the information provided .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_signature: str = Field(..., description="Date the form was signed")  # YYYY-MM-DD format


class MedicalHistory(BaseModel):
    """
    Medical History

    ''
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    current_pain_and_therapy_goals: CurrentPainandTherapyGoals = Field(
        ..., description="Current Pain and Therapy Goals"
    )
    previous_treatment_and_diagnostic_tests: PreviousTreatmentandDiagnosticTests = Field(
        ..., description="Previous Treatment and Diagnostic Tests"
    )
    past_and_current_medical_conditions: PastandCurrentMedicalConditions = Field(
        ..., description="Past and Current Medical Conditions"
    )
    fall_history: FallHistory = Field(..., description="Fall History")
    surgical_history: SurgicalHistory = Field(..., description="Surgical History")
    current_medications: CurrentMedications = Field(..., description="Current Medications")
    authorization: Authorization = Field(..., description="Authorization")
