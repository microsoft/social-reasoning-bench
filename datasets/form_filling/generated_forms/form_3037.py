from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ParticipantInformation(BaseModel):
    """Basic information about the adult member/participant"""

    full_name: str = Field(
        ...,
        description=(
            "Adult member or participant's full legal name .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_number: str = Field(
        ...,
        description=(
            "Primary emergency contact phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    troop_number: str = Field(
        ...,
        description=(
            "Troop number of the adult member or participant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class HealthHistory(BaseModel):
    """Current and past medical conditions"""

    asthma_yes: BooleanLike = Field(
        default="", description="Check if you currently have or have ever been treated for asthma"
    )

    asthma_no: BooleanLike = Field(default="", description="Check if you have never had asthma")

    asthma_explain: str = Field(
        default="",
        description=(
            "Provide details about your asthma history and treatment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    asthma_last_attack_mm_yy: str = Field(
        default="",
        description=(
            "Month and year of your last asthma attack (MM/YY) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    diabetes_yes: BooleanLike = Field(
        default="", description="Check if you currently have or have ever been treated for diabetes"
    )

    diabetes_no: BooleanLike = Field(default="", description="Check if you have never had diabetes")

    diabetes_explain: str = Field(
        default="",
        description=(
            "Provide details about your diabetes history and treatment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    diabetes_last_hba1c_percentage: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Most recent HbA1c value as a percentage"
    )

    hypertension_yes: BooleanLike = Field(
        default="",
        description="Check if you have or have been treated for high blood pressure (hypertension)",
    )

    hypertension_no: BooleanLike = Field(
        default="", description="Check if you have never had hypertension"
    )

    hypertension_explain: str = Field(
        default="",
        description=(
            "Provide details about your hypertension history and treatment .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    heart_disease_heart_attack_chest_pain_heart_murmur_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if you have or have been treated for heart disease, heart attack, chest "
            "pain, or heart murmur"
        ),
    )

    heart_disease_heart_attack_chest_pain_heart_murmur_no: BooleanLike = Field(
        default="",
        description=(
            "Check if you have never had heart disease, heart attack, chest pain, or heart murmur"
        ),
    )

    heart_disease_heart_attack_chest_pain_heart_murmur_explain: str = Field(
        default="",
        description=(
            "Provide details about any heart disease, heart attack, chest pain, or heart "
            'murmur .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    stroke_tia_yes: BooleanLike = Field(
        default="", description="Check if you have had a stroke or transient ischemic attack (TIA)"
    )

    stroke_tia_no: BooleanLike = Field(
        default="", description="Check if you have never had a stroke or TIA"
    )

    stroke_tia_explain: str = Field(
        default="",
        description=(
            "Provide details about any stroke or TIA events .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    lung_respiratory_disease_yes: BooleanLike = Field(
        default="",
        description="Check if you have or have been treated for lung or respiratory disease",
    )

    lung_respiratory_disease_no: BooleanLike = Field(
        default="", description="Check if you have never had lung or respiratory disease"
    )

    lung_respiratory_disease_explain: str = Field(
        default="",
        description=(
            "Provide details about any lung or respiratory disease .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ear_sinus_problems_yes: BooleanLike = Field(
        default="", description="Check if you have or have been treated for ear or sinus problems"
    )

    ear_sinus_problems_no: BooleanLike = Field(
        default="", description="Check if you have never had ear or sinus problems"
    )

    ear_sinus_problems_explain: str = Field(
        default="",
        description=(
            "Provide details about any ear or sinus problems .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    muscular_skeletal_condition_yes: BooleanLike = Field(
        default="",
        description="Check if you have or have been treated for muscular or skeletal conditions",
    )

    muscular_skeletal_condition_no: BooleanLike = Field(
        default="", description="Check if you have never had muscular or skeletal conditions"
    )

    muscular_skeletal_condition_explain: str = Field(
        default="",
        description=(
            "Provide details about any muscular or skeletal conditions .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    psychiatric_psychological_and_emotional_difficulties_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if you have or have been treated for psychiatric, psychological, or "
            "emotional difficulties"
        ),
    )

    psychiatric_psychological_and_emotional_difficulties_no: BooleanLike = Field(
        default="",
        description=(
            "Check if you have never had psychiatric, psychological, or emotional difficulties"
        ),
    )

    psychiatric_psychological_and_emotional_difficulties_explain: str = Field(
        default="",
        description=(
            "Provide details about any psychiatric, psychological, or emotional "
            'difficulties .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    behavioral_neurological_disorders_yes: BooleanLike = Field(
        default="",
        description="Check if you have or have been treated for behavioral or neurological disorders",
    )

    behavioral_neurological_disorders_no: BooleanLike = Field(
        default="", description="Check if you have never had behavioral or neurological disorders"
    )

    behavioral_neurological_disorders_explain: str = Field(
        default="",
        description=(
            "Provide details about any behavioral or neurological disorders .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    bleeding_disorders_yes: BooleanLike = Field(
        default="", description="Check if you have or have been treated for bleeding disorders"
    )

    bleeding_disorders_no: BooleanLike = Field(
        default="", description="Check if you have never had bleeding disorders"
    )

    bleeding_disorders_explain: str = Field(
        default="",
        description=(
            "Provide details about any bleeding disorders .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    fainting_spells_yes: BooleanLike = Field(
        default="", description="Check if you experience or have been treated for fainting spells"
    )

    fainting_spells_no: BooleanLike = Field(
        default="", description="Check if you have never had fainting spells"
    )

    fainting_spells_explain: str = Field(
        default="",
        description=(
            "Provide details about any fainting spells .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    thyroid_disease_yes: BooleanLike = Field(
        default="", description="Check if you have or have been treated for thyroid disease"
    )

    thyroid_disease_no: BooleanLike = Field(
        default="", description="Check if you have never had thyroid disease"
    )

    thyroid_disease_explain: str = Field(
        default="",
        description=(
            "Provide details about any thyroid disease .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    kidney_disease_yes: BooleanLike = Field(
        default="", description="Check if you have or have been treated for kidney disease"
    )

    kidney_disease_no: BooleanLike = Field(
        default="", description="Check if you have never had kidney disease"
    )

    kidney_disease_explain: str = Field(
        default="",
        description=(
            "Provide details about any kidney disease .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    sickle_cell_disease_yes: BooleanLike = Field(
        default="", description="Check if you have or have been treated for sickle cell disease"
    )

    sickle_cell_disease_no: BooleanLike = Field(
        default="", description="Check if you have never had sickle cell disease"
    )

    sickle_cell_disease_explain: str = Field(
        default="",
        description=(
            "Provide details about sickle cell disease .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    seizures_yes: BooleanLike = Field(
        default="", description="Check if you experience or have been treated for seizures"
    )

    seizures_no: BooleanLike = Field(default="", description="Check if you have never had seizures")

    seizures_explain: str = Field(
        default="",
        description=(
            "Provide details about any seizure history .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    seizures_last_seizure_mm_yy: str = Field(
        default="",
        description=(
            "Month and year of your last seizure (MM/YY) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    sleep_disorders_eg_sleep_walking_sleep_apnea_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if you have or have been treated for sleep disorders such as sleep "
            "walking or sleep apnea"
        ),
    )

    sleep_disorders_eg_sleep_walking_sleep_apnea_no: BooleanLike = Field(
        default="", description="Check if you have never had sleep disorders"
    )

    sleep_disorders_eg_sleep_walking_sleep_apnea_explain: str = Field(
        default="",
        description=(
            "Provide details about any sleep disorders .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    sleep_disorders_eg_sleep_walking_sleep_apnea_use_cpap: BooleanLike = Field(
        default="", description="Indicate if you use a CPAP machine for sleep apnea"
    )

    abdominal_digestive_problems_yes: BooleanLike = Field(
        default="",
        description="Check if you have or have been treated for abdominal or digestive problems",
    )

    abdominal_digestive_problems_no: BooleanLike = Field(
        default="", description="Check if you have never had abdominal or digestive problems"
    )

    abdominal_digestive_problems_explain: str = Field(
        default="",
        description=(
            "Provide details about any abdominal or digestive problems .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    surgery_yes: BooleanLike = Field(default="", description="Check if you have had any surgeries")

    surgery_no: BooleanLike = Field(default="", description="Check if you have never had surgery")

    surgery_explain: str = Field(
        default="",
        description=(
            "Provide details about any surgeries you have had .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    surgery_last_surgery_mm_yy: str = Field(
        default="",
        description=(
            "Month and year of your most recent surgery (MM/YY) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    serious_injury_yes: BooleanLike = Field(
        default="", description="Check if you have had any serious injuries"
    )

    serious_injury_no: BooleanLike = Field(
        default="", description="Check if you have never had a serious injury"
    )

    serious_injury_explain: str = Field(
        default="",
        description=(
            "Provide details about any serious injuries .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    excessive_fatigue_or_shortness_of_breath_with_exercise_yes: BooleanLike = Field(
        default="",
        description="Check if you experience excessive fatigue or shortness of breath with exercise",
    )

    excessive_fatigue_or_shortness_of_breath_with_exercise_no: BooleanLike = Field(
        default="",
        description=(
            "Check if you do not experience excessive fatigue or shortness of breath with exercise"
        ),
    )

    excessive_fatigue_or_shortness_of_breath_with_exercise_explain: str = Field(
        default="",
        description=(
            "Provide details about excessive fatigue or shortness of breath with exercise "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    other_yes: BooleanLike = Field(
        default="",
        description="Check if you have any other significant medical conditions not listed",
    )

    other_no: BooleanLike = Field(
        default="", description="Check if you have no other significant medical conditions"
    )

    other_explain: str = Field(
        default="",
        description=(
            "Describe any other medical conditions not covered above .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class TrailLifeUsaAdultMemberparticipantHealthMedicalForm(BaseModel):
    """Trail Life USA Adult Member/Participant Health & Medical Form"""

    participant_information: ParticipantInformation = Field(
        ..., description="Participant Information"
    )
    health_history: HealthHistory = Field(..., description="Health History")
