from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MemberInformation(BaseModel):
    """Basic identifying information about the CAP member"""

    name_last_first_middle: str = Field(
        ...,
        description=(
            "Member's full legal name in Last, First, Middle format .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    grade: str = Field(
        ...,
        description=(
            'Current CAP grade or rank .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    capid: str = Field(
        ...,
        description=(
            "Civil Air Patrol member identification number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    charter_number: str = Field(
        ...,
        description=(
            'Unit charter number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Member's date of birth")  # YYYY-MM-DD format

    height: str = Field(
        ...,
        description=(
            "Height (include units, e.g., feet/inches or centimeters) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    weight: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Body weight (include units, e.g., pounds or kilograms)"
    )

    hair_color: str = Field(
        ...,
        description=(
            'Natural hair color .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    eye_color: str = Field(
        ...,
        description=(
            'Natural eye color .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    gender: str = Field(
        ...,
        description=(
            'Gender of the member .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class Allergies(BaseModel):
    """Allergy details and related conditions"""

    allergies_list_names_of_medication_or_other_allergies_i_e_bee_sting_food_plants_and_types_of_reactions_please_note_food_allergy_details_with_dietary_restrictions_below_on_back_as_well: str = Field(
        default="",
        description=(
            "List all medication, food, environmental, or other allergies and describe the "
            'type of reaction .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    allergies_nasal_stuffiness: BooleanLike = Field(
        default="", description="Chronic allergies or nasal congestion"
    )

    anaphylaxis_serious_allergic_reaction: BooleanLike = Field(
        default="", description="History of anaphylaxis or other serious allergic reactions"
    )

    special_diet_food_allergies: BooleanLike = Field(
        default="", description="Need for a special diet or presence of food allergies"
    )


class MedicalHistory(BaseModel):
    """History of medical conditions that may affect participation"""

    decreased_vision_glaucoma_contacts: BooleanLike = Field(
        default="",
        description="Indicate if you have decreased vision, glaucoma, or use contact lenses",
    )

    ear_infections_perforation: BooleanLike = Field(
        default="", description="History of ear infections or eardrum perforation"
    )

    difficulty_equalizing_ears: BooleanLike = Field(
        default="", description="Difficulty equalizing ear pressure (e.g., during altitude changes)"
    )

    hearing_loss_hearing_aid: BooleanLike = Field(
        default="", description="Hearing loss or use of a hearing aid"
    )

    asthma_emphysema_copd: BooleanLike = Field(
        default="",
        description="History of asthma or chronic obstructive pulmonary disease (emphysema)",
    )

    ever_use_an_inhaler: BooleanLike = Field(
        default="", description="Indicate if you currently or previously used an inhaler"
    )

    short_of_breath_with_activity: BooleanLike = Field(
        default="", description="Shortness of breath during physical activity"
    )

    heart_attack_chest_pain_angina: BooleanLike = Field(
        default="", description="History of heart attack, chest pain, or angina"
    )

    heart_murmur_heart_problems: BooleanLike = Field(
        default="", description="Heart murmur or other heart problems"
    )

    congestive_heart_failure: BooleanLike = Field(
        default="", description="History of congestive heart failure"
    )

    irregular_or_rapid_heartbeat: BooleanLike = Field(
        default="", description="Irregular or unusually rapid heartbeat (arrhythmia)"
    )

    high_or_low_blood_pressure: BooleanLike = Field(
        default="", description="History of high or low blood pressure"
    )

    stomach_trouble_ulcers: BooleanLike = Field(
        default="", description="Chronic stomach problems or ulcers"
    )

    hepatitis_or_liver_problems: BooleanLike = Field(
        default="", description="History of hepatitis or other liver disease"
    )

    diarrhea_constipation: BooleanLike = Field(
        default="", description="Chronic or recurring diarrhea or constipation"
    )

    hernia_or_rupture: BooleanLike = Field(default="", description="History of hernia or rupture")

    kidney_disease_or_stones: BooleanLike = Field(
        default="", description="History of kidney disease or kidney stones"
    )

    prostate_problems_men: BooleanLike = Field(
        default="", description="History of prostate problems (for male members)"
    )

    frequent_urination: BooleanLike = Field(
        default="", description="Frequent or urgent need to urinate"
    )

    menstrual_cramps_women: BooleanLike = Field(
        default="", description="Significant menstrual cramps (for female members)"
    )

    broken_bone_joint_problems: BooleanLike = Field(
        default="", description="History of broken bones or joint problems"
    )

    chronic_or_recurring_injuries: BooleanLike = Field(
        default="", description="Chronic or frequently recurring injuries"
    )

    activity_mobility_restrictions: BooleanLike = Field(
        default="", description="Any restrictions on physical activity or mobility"
    )

    use_of_cane_walker_wheelchair: BooleanLike = Field(
        default="", description="Use of assistive devices such as cane, walker, or wheelchair"
    )

    back_or_neck_pain_or_injury: BooleanLike = Field(
        default="", description="History of back or neck pain or injury"
    )

    migraine_or_severe_headaches: BooleanLike = Field(
        default="", description="History of migraines or severe headaches"
    )

    dizziness_or_fainting_spells: BooleanLike = Field(
        default="", description="Episodes of dizziness or fainting"
    )

    head_injury_unconsciousness: BooleanLike = Field(
        default="", description="History of head injury or loss of consciousness"
    )

    epilepsy_or_seizure: BooleanLike = Field(
        default="", description="History of epilepsy or seizures"
    )

    stroke_paralysis: BooleanLike = Field(default="", description="History of stroke or paralysis")

    thyroid_problems_low_or_high: BooleanLike = Field(
        default="", description="Thyroid disease, including underactive or overactive thyroid"
    )

    diabetes_high_or_low_blood_sugars: BooleanLike = Field(
        default="", description="Diabetes or frequent high/low blood sugar episodes"
    )

    cancer_leukemia: BooleanLike = Field(default="", description="History of cancer or leukemia")

    blood_disease_hemophilia: BooleanLike = Field(
        default="", description="Blood disorders including hemophilia"
    )

    motion_sickness: BooleanLike = Field(
        default="", description="History of motion sickness (e.g., in vehicles, aircraft, boats)"
    )

    current_bedwetting_problems: BooleanLike = Field(
        default="", description="Current issues with bedwetting"
    )

    add_attention_deficit_disorder: BooleanLike = Field(
        default="", description="Diagnosis of Attention Deficit Disorder (ADD)"
    )

    mental_illness_bipolar_other: BooleanLike = Field(
        default="",
        description="History of mental illness such as bipolar disorder or other conditions",
    )

    depression_anxiety_suicidal: BooleanLike = Field(
        default="", description="History of depression, anxiety, or suicidal thoughts/behavior"
    )

    admission_to_the_hospital: BooleanLike = Field(
        default="", description="Previous admissions to a hospital for any reason"
    )

    other_chronic_medical_illnesses: BooleanLike = Field(
        default="", description="Any other chronic medical illnesses not listed above"
    )

    sleep_disorder_sleep_apnea: BooleanLike = Field(
        default="", description="Sleep disorders including sleep apnea"
    )

    serious_injury: BooleanLike = Field(default="", description="History of any serious injury")


class CapMemberHealthHistoryForm(BaseModel):
    """
    CAP MEMBER HEALTH HISTORY FORM

    This information is CONFIDENTIAL and for official use only. It cannot be released to unauthorized persons. Answer all questions as accurately as possible so that the activity or encampment staff can make themselves aware of any pre-existing medical problems or conditions and be alert to help you. This form will also provide medical information in a case when you are unable to do so.
    """

    member_information: MemberInformation = Field(..., description="Member Information")
    allergies: Allergies = Field(..., description="Allergies")
    medical_history: MedicalHistory = Field(..., description="Medical History")
