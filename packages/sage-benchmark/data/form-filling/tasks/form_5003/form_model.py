from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MemberIdentification(BaseModel):
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
            "Member's height (include units, e.g., ft/in or cm) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    weight: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Member's weight (specify units, typically pounds)"
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
            "Gender as recorded for medical purposes .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Allergies(BaseModel):
    """Documented allergies and reactions"""

    allergies_list_names_of_medication_or_other_allergies_and_types_of_reactions: str = Field(
        default="",
        description=(
            "List all medication, food, insect, or environmental allergies and describe the "
            'type of reaction .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    allergies_nasal_stuffiness: BooleanLike = Field(
        default="", description="Nasal allergies or chronic nasal congestion"
    )

    anaphylaxis_serious_allergic_reaction: BooleanLike = Field(
        default="", description="History of anaphylaxis or any life-threatening allergic reaction"
    )

    special_diet_food_allergies: BooleanLike = Field(
        default="", description="Need for a special diet or presence of food allergies"
    )


class MedicalHistory(BaseModel):
    """Current and past medical conditions relevant to CAP activities"""

    decreased_vision_glaucoma_contacts: BooleanLike = Field(
        default="",
        description="Indicate if you have decreased vision, glaucoma, or use contact lenses",
    )

    ear_infections_perforation: BooleanLike = Field(
        default="", description="History of ear infections or eardrum perforation"
    )

    difficulty_equalizing_ears: BooleanLike = Field(
        default="", description="Problems equalizing ear pressure (e.g., during altitude changes)"
    )

    hearing_loss_hearing_aid: BooleanLike = Field(
        default="", description="Any hearing loss or use of a hearing aid"
    )

    asthma_emphysema_copd: BooleanLike = Field(
        default="",
        description="Diagnosis of asthma or chronic obstructive pulmonary disease (emphysema)",
    )

    ever_use_an_inhaler: BooleanLike = Field(
        default="", description="Indicate if you currently or previously used an inhaler"
    )

    short_of_breath_with_activity: BooleanLike = Field(
        default="", description="Shortness of breath during normal physical activity"
    )

    heart_attack_chest_pain_angina: BooleanLike = Field(
        default="", description="History of heart attack, chest pain, or angina"
    )

    heart_murmur_heart_problems: BooleanLike = Field(
        default="", description="Any diagnosed heart murmur or other heart conditions"
    )

    congestive_heart_failure: BooleanLike = Field(
        default="", description="Diagnosis of congestive heart failure"
    )

    irregular_or_rapid_heartbeat: BooleanLike = Field(
        default="", description="History of irregular or unusually rapid heartbeat"
    )

    high_or_low_blood_pressure: BooleanLike = Field(
        default="", description="Diagnosis of hypertension or chronically low blood pressure"
    )

    stomach_trouble_ulcers: BooleanLike = Field(
        default="", description="Chronic stomach problems or peptic ulcers"
    )

    hepatitis_or_liver_problems: BooleanLike = Field(
        default="", description="History of hepatitis or other liver disease"
    )

    diarrhea_constipation: BooleanLike = Field(
        default="", description="Chronic or recurring diarrhea or constipation"
    )

    hernia_or_rupture: BooleanLike = Field(
        default="", description="History of hernia or similar rupture"
    )

    kidney_disease_or_stones: BooleanLike = Field(
        default="", description="Kidney disease or kidney stones"
    )

    prostate_problems_men: BooleanLike = Field(
        default="", description="Any prostate-related medical problems (for male members)"
    )

    frequent_urination: BooleanLike = Field(
        default="", description="Chronic or unexplained frequent urination"
    )

    menstrual_cramps_women: BooleanLike = Field(
        default="", description="Significant or disabling menstrual cramps (for female members)"
    )

    broken_bone_joint_problems: BooleanLike = Field(
        default="", description="History of broken bones or chronic joint problems"
    )

    chronic_or_recurring_injuries: BooleanLike = Field(
        default="", description="Any injuries that recur or have long-term effects"
    )

    activity_mobility_restrictions: BooleanLike = Field(
        default="", description="Any restrictions on physical activity or mobility"
    )

    use_of_cane_walker_wheelchair: BooleanLike = Field(
        default="", description="Current use of a cane, walker, or wheelchair"
    )

    back_or_neck_pain_or_injury: BooleanLike = Field(
        default="", description="Chronic back or neck pain or history of injury"
    )

    migraine_or_severe_headaches: BooleanLike = Field(
        default="", description="History of migraines or other severe headaches"
    )

    dizziness_or_fainting_spells: BooleanLike = Field(
        default="", description="Episodes of dizziness or fainting"
    )

    head_injury_unconsciousness: BooleanLike = Field(
        default="", description="History of head injury or loss of consciousness"
    )

    epilepsy_or_seizure: BooleanLike = Field(
        default="", description="Diagnosis of epilepsy or any seizure disorder"
    )

    stroke_paralysis: BooleanLike = Field(
        default="", description="History of stroke or any form of paralysis"
    )

    thyroid_problems_low_or_high: BooleanLike = Field(
        default="", description="Diagnosis of hypothyroidism or hyperthyroidism"
    )

    diabetes_high_or_low_blood_sugars: BooleanLike = Field(
        default="", description="Diagnosis of diabetes or recurrent abnormal blood sugar levels"
    )

    cancer_leukemia: BooleanLike = Field(
        default="", description="History of any cancer, including leukemia"
    )

    blood_disease_hemophilia: BooleanLike = Field(
        default="", description="Any blood disorder, including hemophilia"
    )

    motion_sickness: BooleanLike = Field(
        default="", description="Tendency to experience motion sickness"
    )

    current_bedwetting_problems: BooleanLike = Field(
        default="", description="Ongoing bedwetting issues"
    )

    add_attention_deficit_disorder: BooleanLike = Field(
        default="", description="Diagnosis of Attention Deficit Disorder (ADD or ADHD)"
    )

    mental_illness_bipolar_other: BooleanLike = Field(
        default="", description="Any diagnosed mental illness, including bipolar disorder"
    )

    depression_anxiety_suicidal: BooleanLike = Field(
        default="", description="History of depression, anxiety, or suicidal thoughts/behavior"
    )

    admission_to_the_hospital: BooleanLike = Field(
        default="",
        description="Any prior admission to a hospital for medical or psychiatric reasons",
    )

    other_chronic_medical_illnesses: BooleanLike = Field(
        default="", description="Presence of any other long-term medical conditions not listed"
    )

    sleep_disorder_sleep_apnea: BooleanLike = Field(
        default="", description="Diagnosis of a sleep disorder, including sleep apnea"
    )

    serious_injury: BooleanLike = Field(
        default="", description="History of any serious injury requiring medical care"
    )


class CapMemberHealthHistoryForm(BaseModel):
    """
    CAP MEMBER HEALTH HISTORY FORM

    This information is CONFIDENTIAL and for official use only. It cannot be released to unauthorized persons. Answer all questions as accurately as possible so that the activity or encampment staff can make themselves aware of any pre-existing medical problems or conditions and be alert to help you. This form will also provide medical information in a case when you are unable to do so.
    """

    member_identification: MemberIdentification = Field(..., description="Member Identification")
    allergies: Allergies = Field(..., description="Allergies")
    medical_history: MedicalHistory = Field(..., description="Medical History")
