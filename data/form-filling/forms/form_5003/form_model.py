from typing import Literal, Optional, List, Union
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

    capid_number: str = Field(
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
            "Height (specify units, e.g., feet/inches or centimeters) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    weight: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Weight (specify units, e.g., pounds or kilograms)"
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
    """Allergy details and related dietary restrictions"""

    allergies_list_names_of_medication_or_other_allergies_ie_bee_sting_food_plants_and_types_of_reactions_please_note_food_allergy_details_with_dietary_restrictions_below_on_back_as_well: str = Field(
        default="",
        description=(
            "List all medication, food, insect, plant, or other allergies and describe the "
            "type of reaction; include dietary restrictions for food allergies .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    allergies_nasal_stuffiness: BooleanLike = Field(
        default="",
        description="Indicate if you have allergies causing nasal congestion or stuffiness",
    )

    anaphylaxis_serious_allergic_reaction: BooleanLike = Field(
        default="",
        description="Indicate if you have ever had anaphylaxis or a serious allergic reaction",
    )

    special_diet_food_allergies: BooleanLike = Field(
        default="", description="Indicate if you require a special diet or have food allergies"
    )


class MedicalHistory(BaseModel):
    """History of medical conditions and health issues"""

    decreased_vision_glaucoma_contacts: BooleanLike = Field(
        default="",
        description="Indicate if you have decreased vision, glaucoma, or use contact lenses",
    )

    ear_infections_perforation: BooleanLike = Field(
        default="",
        description="Indicate if you have a history of ear infections or eardrum perforation",
    )

    difficulty_equalizing_ears: BooleanLike = Field(
        default="", description="Indicate if you have difficulty equalizing pressure in your ears"
    )

    hearing_loss_hearing_aid: BooleanLike = Field(
        default="", description="Indicate if you have hearing loss or use a hearing aid"
    )

    asthma_emphysema_copd: BooleanLike = Field(
        default="", description="Indicate if you have asthma or emphysema (COPD)"
    )

    ever_use_an_inhaler: BooleanLike = Field(
        default="", description="Indicate if you currently use or have ever used an inhaler"
    )

    short_of_breath_with_activity: BooleanLike = Field(
        default="", description="Indicate if you become short of breath with physical activity"
    )

    heart_attack_chest_pain_angina: BooleanLike = Field(
        default="", description="Indicate if you have had a heart attack, chest pain, or angina"
    )

    heart_murmur_heart_problems: BooleanLike = Field(
        default="", description="Indicate if you have a heart murmur or other heart problems"
    )

    congestive_heart_failure: BooleanLike = Field(
        default="", description="Indicate if you have congestive heart failure"
    )

    irregular_or_rapid_heartbeat: BooleanLike = Field(
        default="", description="Indicate if you have an irregular or rapid heartbeat"
    )

    high_or_low_blood_pressure: BooleanLike = Field(
        default="", description="Indicate if you have high or low blood pressure"
    )

    stomach_trouble_ulcers: BooleanLike = Field(
        default="", description="Indicate if you have stomach problems or ulcers"
    )

    hepatitis_or_liver_problems: BooleanLike = Field(
        default="", description="Indicate if you have hepatitis or other liver problems"
    )

    diarrhea_constipation: BooleanLike = Field(
        default="", description="Indicate if you have chronic diarrhea or constipation"
    )

    hernia_or_rupture: BooleanLike = Field(
        default="", description="Indicate if you have a hernia or rupture"
    )

    kidney_disease_or_stones: BooleanLike = Field(
        default="", description="Indicate if you have kidney disease or kidney stones"
    )

    prostate_problems_men: BooleanLike = Field(
        default="", description="For male members, indicate if you have prostate problems"
    )

    frequent_urination: BooleanLike = Field(
        default="", description="Indicate if you experience frequent urination"
    )

    menstrual_cramps_women: BooleanLike = Field(
        default="",
        description="For female members, indicate if you have significant menstrual cramps",
    )

    broken_bone_joint_problems: BooleanLike = Field(
        default="", description="Indicate if you have a history of broken bones or joint problems"
    )

    chronic_or_recurring_injuries: BooleanLike = Field(
        default="", description="Indicate if you have chronic or frequently recurring injuries"
    )

    activity_mobility_restrictions: BooleanLike = Field(
        default="", description="Indicate if you have any activity or mobility restrictions"
    )

    use_of_cane_walker_wheelchair: BooleanLike = Field(
        default="", description="Indicate if you use a cane, walker, or wheelchair"
    )

    back_or_neck_pain_or_injury: BooleanLike = Field(
        default="", description="Indicate if you have back or neck pain or a history of injury"
    )

    migraine_or_severe_headaches: BooleanLike = Field(
        default="", description="Indicate if you experience migraines or severe headaches"
    )

    dizziness_or_fainting_spells: BooleanLike = Field(
        default="", description="Indicate if you have dizziness or fainting spells"
    )

    head_injury_unconsciousness: BooleanLike = Field(
        default="",
        description="Indicate if you have had a head injury or episodes of unconsciousness",
    )

    epilepsy_or_seizure: BooleanLike = Field(
        default="", description="Indicate if you have epilepsy or a history of seizures"
    )

    stroke_paralysis: BooleanLike = Field(
        default="", description="Indicate if you have had a stroke or paralysis"
    )

    thyroid_problems_low_or_high: BooleanLike = Field(
        default="",
        description="Indicate if you have thyroid problems (hypothyroid or hyperthyroid)",
    )

    diabetes_high_or_low_blood_sugars: BooleanLike = Field(
        default="",
        description="Indicate if you have diabetes or problems with high or low blood sugar",
    )

    cancer_leukemia: BooleanLike = Field(
        default="", description="Indicate if you have or have had cancer or leukemia"
    )

    blood_disease_hemophilia: BooleanLike = Field(
        default="", description="Indicate if you have a blood disease such as hemophilia"
    )

    motion_sickness: BooleanLike = Field(
        default="", description="Indicate if you experience motion sickness"
    )

    current_bedwetting_problems: BooleanLike = Field(
        default="", description="Indicate if you currently have bedwetting problems"
    )

    add_attention_deficit_disorder: BooleanLike = Field(
        default="",
        description="Indicate if you have been diagnosed with Attention Deficit Disorder (ADD)",
    )

    mental_illness_bipolar_other: BooleanLike = Field(
        default="",
        description=(
            "Indicate if you have a mental illness such as bipolar disorder or other conditions"
        ),
    )

    depression_anxiety_suicidal: BooleanLike = Field(
        default="",
        description="Indicate if you have depression, anxiety, or suicidal thoughts or history",
    )

    admission_to_the_hospital: BooleanLike = Field(
        default="", description="Indicate if you have been admitted to a hospital for any condition"
    )

    other_chronic_medical_illnesses: BooleanLike = Field(
        default="",
        description="Indicate if you have any other chronic medical illnesses not listed",
    )

    sleep_disorder_sleep_apnea: BooleanLike = Field(
        default="", description="Indicate if you have a sleep disorder such as sleep apnea"
    )

    serious_injury: BooleanLike = Field(
        default="", description="Indicate if you have had any serious injuries"
    )


class CapMemberHealthHistoryForm(BaseModel):
    """
    CAP MEMBER HEALTH HISTORY FORM

    This information is CONFIDENTIAL and for official use only. It cannot be released to unauthorized persons. Answer all questions as accurately as possible so that the activity or encampment staff can make themselves aware of any pre-existing medical problems or conditions and be alert to help you. This form will also provide medical information in a case when you are unable to do so.
    """

    member_information: MemberInformation = Field(..., description="Member Information")
    allergies: Allergies = Field(..., description="Allergies")
    medical_history: MedicalHistory = Field(..., description="Medical History")
