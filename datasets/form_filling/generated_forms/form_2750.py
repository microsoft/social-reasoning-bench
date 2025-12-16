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
    """Basic patient identification details"""

    patient_name_last: str = Field(
        ...,
        description=(
            'Patient\'s legal last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    patient_name_first: str = Field(
        ...,
        description=(
            'Patient\'s legal first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    patient_name_mi: str = Field(
        default="",
        description=(
            'Patient\'s middle initial .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    patient_name_preferred_name: str = Field(
        default="",
        description=(
            'Name the patient prefers to be called .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class MedicalHistory(BaseModel):
    """Reported medical conditions and history"""

    allergies: BooleanLike = Field(default="", description="Check if the patient has allergies")

    pre_med_other: BooleanLike = Field(
        default="", description="Check if patient requires a pre-medication other than those listed"
    )

    anxiety: BooleanLike = Field(default="", description="Check if the patient has anxiety")

    asthma: BooleanLike = Field(default="", description="Check if the patient has asthma")

    cancer: BooleanLike = Field(
        default="", description="Check if the patient has or has had cancer"
    )

    dizziness: BooleanLike = Field(
        default="", description="Check if the patient experiences dizziness"
    )

    fainting: BooleanLike = Field(
        default="", description="Check if the patient has a history of fainting"
    )

    heart_disease: BooleanLike = Field(
        default="", description="Check if the patient has heart disease"
    )

    hepatitis_b: BooleanLike = Field(default="", description="Check if the patient has Hepatitis B")

    hiv: BooleanLike = Field(default="", description="Check if the patient is HIV positive")

    kidney_disease: BooleanLike = Field(
        default="", description="Check if the patient has kidney disease"
    )

    mental_disorders: BooleanLike = Field(
        default="", description="Check if the patient has any diagnosed mental disorders"
    )

    osteoporosis_meds: BooleanLike = Field(
        default="", description="Check if the patient is taking medications for osteoporosis"
    )

    pregnancy: BooleanLike = Field(
        default="", description="Check if the patient is currently pregnant"
    )

    rheumatic_fever: BooleanLike = Field(
        default="", description="Check if the patient has a history of rheumatic fever"
    )

    stomach_problems: BooleanLike = Field(
        default="", description="Check if the patient has stomach or digestive problems"
    )

    tobacco_use: BooleanLike = Field(
        default="", description="Check if the patient currently uses tobacco products"
    )

    ulcers: BooleanLike = Field(default="", description="Check if the patient has ulcers")

    pre_med_amoxicillin: BooleanLike = Field(
        default="", description="Check if patient requires Amoxicillin as pre-medication"
    )

    anemia: BooleanLike = Field(default="", description="Check if the patient has anemia")

    arthritis: BooleanLike = Field(default="", description="Check if the patient has arthritis")

    blood_disease: BooleanLike = Field(
        default="", description="Check if the patient has any blood disorders or diseases"
    )

    depression: BooleanLike = Field(default="", description="Check if the patient has depression")

    epilepsy: BooleanLike = Field(
        default="", description="Check if the patient has epilepsy or seizure disorders"
    )

    glaucoma: BooleanLike = Field(default="", description="Check if the patient has glaucoma")

    heart_murmur: BooleanLike = Field(
        default="", description="Check if the patient has a heart murmur"
    )

    hepatitis_c: BooleanLike = Field(default="", description="Check if the patient has Hepatitis C")

    jaundice: BooleanLike = Field(default="", description="Check if the patient has had jaundice")

    liver_disease: BooleanLike = Field(
        default="", description="Check if the patient has liver disease"
    )

    mitrovalve_prolapse: BooleanLike = Field(
        default="", description="Check if the patient has mitral valve prolapse"
    )

    osteoporosis: BooleanLike = Field(
        default="", description="Check if the patient has osteoporosis"
    )

    radiation_treatment: BooleanLike = Field(
        default="", description="Check if the patient has received radiation treatment"
    )

    rheumatism: BooleanLike = Field(default="", description="Check if the patient has rheumatism")

    stroke: BooleanLike = Field(default="", description="Check if the patient has had a stroke")

    tuberculosis: BooleanLike = Field(
        default="", description="Check if the patient has tuberculosis"
    )

    venereal_disease: BooleanLike = Field(
        default="",
        description="Check if the patient has any venereal (sexually transmitted) diseases",
    )

    pre_med_clindamycin: BooleanLike = Field(
        default="", description="Check if patient requires Clindamycin as pre-medication"
    )

    angina_pectoris: BooleanLike = Field(
        default="", description="Check if the patient has angina pectoris (chest pain)"
    )

    artificial_joints: BooleanLike = Field(
        default="", description="Check if the patient has artificial joints"
    )

    blood_thinner: BooleanLike = Field(
        default="", description="Check if the patient is taking blood thinners"
    )

    diabetes: BooleanLike = Field(default="", description="Check if the patient has diabetes")

    excessive_bleeding: BooleanLike = Field(
        default="", description="Check if the patient has a history of excessive bleeding"
    )

    head_injuries: BooleanLike = Field(
        default="", description="Check if the patient has had significant head injuries"
    )

    hepatitis_a: BooleanLike = Field(default="", description="Check if the patient has Hepatitis A")

    high_blood_pressure: BooleanLike = Field(
        default="", description="Check if the patient has high blood pressure"
    )

    joint_replacement: BooleanLike = Field(
        default="", description="Check if the patient has had joint replacement surgery"
    )

    low_blood_pressure: BooleanLike = Field(
        default="", description="Check if the patient has low blood pressure"
    )

    nervous_disorders: BooleanLike = Field(
        default="", description="Check if the patient has nervous system disorders"
    )

    pacemaker: BooleanLike = Field(default="", description="Check if the patient has a pacemaker")

    respiratory_problems: BooleanLike = Field(
        default="", description="Check if the patient has respiratory or breathing problems"
    )

    sinus_problems: BooleanLike = Field(
        default="", description="Check if the patient has sinus problems"
    )

    thyroid_disease: BooleanLike = Field(
        default="", description="Check if the patient has thyroid disease"
    )

    tumors: BooleanLike = Field(
        default="", description="Check if the patient has or has had tumors"
    )

    other: BooleanLike = Field(
        default="", description="Check if the patient has other medical conditions not listed"
    )


class OtherMedicalConditions(BaseModel):
    """Free-text explanation of other medical conditions"""

    explain_other_medical_conditions_line_1: str = Field(
        default="",
        description=(
            "First line to describe other medical conditions .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    explain_other_medical_conditions_line_2: str = Field(
        default="",
        description=(
            "Second line to describe other medical conditions .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    explain_other_medical_conditions_line_3: str = Field(
        default="",
        description=(
            "Third line to describe other medical conditions .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class MedicalHistory(BaseModel):
    """
    MEDICAL HISTORY

    ''
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    medical_history: MedicalHistory = Field(..., description="Medical History")
    other_medical_conditions: OtherMedicalConditions = Field(
        ..., description="Other Medical Conditions"
    )
