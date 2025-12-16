from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MedicalHistory(BaseModel):
    """History of heart, lung, and other systemic diseases"""

    heart_disease_yes: BooleanLike = Field(
        default="", description="Indicate YES if you have or have ever had heart disease"
    )

    heart_disease_no: BooleanLike = Field(
        default="", description="Indicate NO if you have never had heart disease"
    )

    heart_murmur_or_mvp_yes: BooleanLike = Field(
        default="",
        description="YES if you have or have ever had a heart murmur or mitral valve prolapse (MVP)",
    )

    heart_murmur_or_mvp_no: BooleanLike = Field(
        default="",
        description="NO if you have never had a heart murmur or mitral valve prolapse (MVP)",
    )

    heart_attack_yes: BooleanLike = Field(
        default="", description="YES if you have ever had a heart attack"
    )

    heart_attack_no: BooleanLike = Field(
        default="", description="NO if you have never had a heart attack"
    )

    rheumatic_fever_yes: BooleanLike = Field(
        default="", description="YES if you have ever had rheumatic fever"
    )

    rheumatic_fever_no: BooleanLike = Field(
        default="", description="NO if you have never had rheumatic fever"
    )

    pace_maker_yes: BooleanLike = Field(default="", description="YES if you have a pacemaker")

    pace_maker_no: BooleanLike = Field(default="", description="NO if you do not have a pacemaker")

    chest_pain_yes: BooleanLike = Field(
        default="", description="YES if you currently have or have had chest pain"
    )

    chest_pain_no: BooleanLike = Field(default="", description="NO if you have not had chest pain")

    palpitation_yes: BooleanLike = Field(
        default="", description="YES if you experience heart palpitations"
    )

    palpitation_no: BooleanLike = Field(
        default="", description="NO if you do not experience heart palpitations"
    )

    shortness_of_breath_yes: BooleanLike = Field(
        default="", description="YES if you have or have had shortness of breath"
    )

    shortness_of_breath_no: BooleanLike = Field(
        default="", description="NO if you have not had shortness of breath"
    )

    high_blood_pressure_yes: BooleanLike = Field(
        default="", description="YES if you have or have had high blood pressure"
    )

    high_blood_pressure_no: BooleanLike = Field(
        default="", description="NO if you have not had high blood pressure"
    )

    asthma_yes: BooleanLike = Field(default="", description="YES if you have or have had asthma")

    asthma_no: BooleanLike = Field(default="", description="NO if you have not had asthma")

    emphysema_yes: BooleanLike = Field(
        default="", description="YES if you have or have had emphysema"
    )

    emphysema_no: BooleanLike = Field(default="", description="NO if you have not had emphysema")

    chronic_cough_yes: BooleanLike = Field(
        default="", description="YES if you have or have had a chronic cough"
    )

    chronic_cough_no: BooleanLike = Field(
        default="", description="NO if you have not had a chronic cough"
    )

    sinus_trouble_yes: BooleanLike = Field(
        default="", description="YES if you have or have had sinus trouble"
    )

    sinus_trouble_no: BooleanLike = Field(
        default="", description="NO if you have not had sinus trouble"
    )

    hepatitis_yes: BooleanLike = Field(
        default="", description="YES if you have or have had hepatitis"
    )

    hepatitis_no: BooleanLike = Field(default="", description="NO if you have not had hepatitis")

    hiv_virus_yes: BooleanLike = Field(
        default="", description="YES if you are HIV positive or have HIV virus"
    )

    hiv_virus_no: BooleanLike = Field(default="", description="NO if you do not have HIV virus")

    joint_hip_replacement_yes: BooleanLike = Field(
        default="", description="YES if you have had a joint or hip replacement"
    )

    joint_hip_replacement_no: BooleanLike = Field(
        default="", description="NO if you have not had a joint or hip replacement"
    )

    thyroid_disease_yes: BooleanLike = Field(
        default="", description="YES if you have or have had thyroid disease"
    )

    thyroid_disease_no: BooleanLike = Field(
        default="", description="NO if you have not had thyroid disease"
    )

    liver_disease_yes: BooleanLike = Field(
        default="", description="YES if you have or have had liver disease"
    )

    liver_disease_no: BooleanLike = Field(
        default="", description="NO if you have not had liver disease"
    )

    kidney_disease_yes: BooleanLike = Field(
        default="", description="YES if you have or have had kidney disease"
    )

    kidney_disease_no: BooleanLike = Field(
        default="", description="NO if you have not had kidney disease"
    )

    diabetes_yes: BooleanLike = Field(default="", description="YES if you have diabetes")

    diabetes_no: BooleanLike = Field(default="", description="NO if you do not have diabetes")

    anemia_yes: BooleanLike = Field(default="", description="YES if you have or have had anemia")

    anemia_no: BooleanLike = Field(default="", description="NO if you have not had anemia")

    bleeding_problems_yes: BooleanLike = Field(
        default="", description="YES if you have or have had bleeding problems"
    )

    bleeding_problems_no: BooleanLike = Field(
        default="", description="NO if you have not had bleeding problems"
    )

    ulcers_yes: BooleanLike = Field(default="", description="YES if you have or have had ulcers")

    ulcers_no: BooleanLike = Field(default="", description="NO if you have not had ulcers")

    mental_illness_yes: BooleanLike = Field(
        default="", description="YES if you have or have had a mental illness"
    )

    mental_illness_no: BooleanLike = Field(
        default="", description="NO if you have not had a mental illness"
    )

    epilepsy_seizures_yes: BooleanLike = Field(
        default="", description="YES if you have epilepsy or have had seizures"
    )

    epilepsy_seizures_no: BooleanLike = Field(
        default="", description="NO if you have not had epilepsy or seizures"
    )

    fainting_spells_yes: BooleanLike = Field(
        default="", description="YES if you have or have had fainting spells"
    )

    fainting_spells_no: BooleanLike = Field(
        default="", description="NO if you have not had fainting spells"
    )

    immuno_suppressive_disease_yes: BooleanLike = Field(
        default="", description="YES if you have an immunosuppressive disease"
    )

    immuno_suppressive_disease_no: BooleanLike = Field(
        default="", description="NO if you do not have an immunosuppressive disease"
    )


class Medications(BaseModel):
    """Current medications and related drug use"""

    current_medications_list: str = Field(
        default="",
        description=(
            "List all current medications you are taking .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    steroids_yes: BooleanLike = Field(
        default="", description="YES if you are currently taking steroid medications"
    )

    steroids_no: BooleanLike = Field(
        default="", description="NO if you are not currently taking steroid medications"
    )

    anticoagulants_yes: BooleanLike = Field(
        default="",
        description="YES if you are currently taking anticoagulant (blood thinner) medications",
    )

    anticoagulants_no: BooleanLike = Field(
        default="", description="NO if you are not currently taking anticoagulant medications"
    )

    high_blood_pressure_medications_yes: BooleanLike = Field(
        default="", description="YES if you are taking medications for high blood pressure"
    )

    high_blood_pressure_medications_no: BooleanLike = Field(
        default="", description="NO if you are not taking medications for high blood pressure"
    )

    heart_medications_yes: BooleanLike = Field(
        default="", description="YES if you are currently taking heart medications"
    )

    heart_medications_no: BooleanLike = Field(
        default="", description="NO if you are not currently taking heart medications"
    )

    bone_density_yes: BooleanLike = Field(
        default="",
        description="YES if you are taking medications for bone density (e.g., osteoporosis)",
    )

    bone_density_no: BooleanLike = Field(
        default="", description="NO if you are not taking medications for bone density"
    )

    tranquilizers_yes: BooleanLike = Field(
        default="", description="YES if you are currently taking tranquilizers"
    )

    tranquilizers_no: BooleanLike = Field(
        default="", description="NO if you are not currently taking tranquilizers"
    )

    antidepressants_yes: BooleanLike = Field(
        default="", description="YES if you are currently taking antidepressant medications"
    )

    antidepressants_no: BooleanLike = Field(
        default="", description="NO if you are not currently taking antidepressant medications"
    )

    birth_control_pills_yes: BooleanLike = Field(
        default="", description="YES if you are currently taking birth control pills"
    )

    birth_control_pills_no: BooleanLike = Field(
        default="", description="NO if you are not currently taking birth control pills"
    )

    ibuprofen_today_yes: BooleanLike = Field(
        default="", description="YES if you have taken ibuprofen today"
    )

    ibuprofen_today_no: BooleanLike = Field(
        default="", description="NO if you have not taken ibuprofen today"
    )


class Allergies(BaseModel):
    """Latex, penicillin, and other drug allergies"""

    latex_allergy_yes: BooleanLike = Field(
        default="", description="YES if you have a latex allergy"
    )

    latex_allergy_no: BooleanLike = Field(
        default="", description="NO if you do not have a latex allergy"
    )

    penicillin_allergy_yes: BooleanLike = Field(
        default="", description="YES if you have a penicillin allergy"
    )

    penicillin_allergy_no: BooleanLike = Field(
        default="", description="NO if you do not have a penicillin allergy"
    )

    drug_allergies_list: str = Field(
        default="",
        description=(
            'List all drug allergies you have .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalHealthInformation(BaseModel):
    """Pregnancy, serious illnesses or injuries, and physician care"""

    women_are_you_pregnant_yes: BooleanLike = Field(
        default="", description="For women, indicate YES if you are currently pregnant"
    )

    women_are_you_pregnant_no: BooleanLike = Field(
        default="", description="For women, indicate NO if you are not currently pregnant"
    )

    serious_illnesses_or_injuries_yes: BooleanLike = Field(
        default="", description="YES if you have had any serious illnesses or injuries"
    )

    serious_illnesses_or_injuries_no: BooleanLike = Field(
        default="", description="NO if you have not had any serious illnesses or injuries"
    )

    serious_illnesses_or_injuries_explain_line_1: str = Field(
        default="",
        description=(
            "Explanation of serious illnesses or injuries (line 1) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    serious_illnesses_or_injuries_explain_line_2: str = Field(
        default="",
        description=(
            "Continuation of explanation of serious illnesses or injuries (line 2) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    pre_medicated_before_dental_treatment_yes: BooleanLike = Field(
        default="",
        description=(
            "YES if you require pre-medication before dental treatment due to heart "
            "problems or joint replacement"
        ),
    )

    pre_medicated_before_dental_treatment_no: BooleanLike = Field(
        default="", description="NO if you do not require pre-medication before dental treatment"
    )

    under_care_of_physician_past_five_years_yes: BooleanLike = Field(
        default="",
        description="YES if you have been under the care of a physician in the past five years",
    )

    under_care_of_physician_past_five_years_no: BooleanLike = Field(
        default="",
        description="NO if you have not been under the care of a physician in the past five years",
    )

    care_of_physician_explanation_line_1: str = Field(
        default="",
        description=(
            "Explanation of why you were under a physician's care in the past five years "
            '(line 1) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    care_of_physician_explanation_line_2: str = Field(
        default="",
        description=(
            "Continuation of explanation of physician's care in the past five years (line "
            '2) .If you cannot fill this, write "N/A". If this field should not be filled '
            "by you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class Signatures(BaseModel):
    """Patient and doctor attestation"""

    signature: str = Field(
        ...,
        description=(
            "Patient's signature attesting that the information provided is true and "
            'correct .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the form is signed")  # YYYY-MM-DD format

    doctors_signature: str = Field(
        default="",
        description=(
            "Doctor's signature reviewing this medical history .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class MedicalHistory(BaseModel):
    """
    MEDICAL HISTORY

    ''
    """

    medical_history: MedicalHistory = Field(..., description="Medical History")
    medications: Medications = Field(..., description="Medications")
    allergies: Allergies = Field(..., description="Allergies")
    additional_health_information: AdditionalHealthInformation = Field(
        ..., description="Additional Health Information"
    )
    signatures: Signatures = Field(..., description="Signatures")
