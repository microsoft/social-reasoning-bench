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
            "Member's height (include units, e.g., feet/inches or cm) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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
            'Gender of the member .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class Allergies(BaseModel):
    """Detailed information about allergies and reactions"""

    allergies_list_names_of_medication_or_other_allergies_ie_bee_sting_food_plants_and_types_of_reactions_please_note_food_allergy_details_with_dietary_restrictions_below_on_back_as_well: str = Field(
        default="",
        description=(
            "List all medication, food, environmental, or other allergies and describe the "
            "type of reaction; include dietary restrictions for food allergies .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    anaphylaxis_serious_allergic_reaction_no: BooleanLike = Field(
        default="",
        description="Check if member has NOT had anaphylaxis or serious allergic reactions",
    )

    anaphylaxis_serious_allergic_reaction_yes: BooleanLike = Field(
        default="", description="Check if member has had anaphylaxis or serious allergic reactions"
    )

    special_diet_food_allergies_no: BooleanLike = Field(
        default="", description="Indicate no special diet or food allergies"
    )

    special_diet_food_allergies_yes: BooleanLike = Field(
        default="", description="Indicate special diet requirements or food allergies"
    )


class MedicalHistory(BaseModel):
    """Health conditions and medical history relevant to CAP activities"""

    decreased_vision_glaucoma_contacts_no: BooleanLike = Field(
        default="",
        description="Check if member does NOT have decreased vision, glaucoma, or use of contacts",
    )

    decreased_vision_glaucoma_contacts_yes: BooleanLike = Field(
        default="", description="Check if member has decreased vision, glaucoma, or uses contacts"
    )

    ear_infections_perforation_no: BooleanLike = Field(
        default="",
        description="Check if member does NOT have history of ear infections or perforation",
    )

    ear_infections_perforation_yes: BooleanLike = Field(
        default="", description="Check if member has history of ear infections or perforation"
    )

    difficulty_equalizing_ears_no: BooleanLike = Field(
        default="", description="Check if member does NOT have difficulty equalizing ear pressure"
    )

    difficulty_equalizing_ears_yes: BooleanLike = Field(
        default="", description="Check if member has difficulty equalizing ear pressure"
    )

    hearing_loss_hearing_aid_no: BooleanLike = Field(
        default="", description="Check if member does NOT have hearing loss or use a hearing aid"
    )

    hearing_loss_hearing_aid_yes: BooleanLike = Field(
        default="", description="Check if member has hearing loss or uses a hearing aid"
    )

    allergies_nasal_stuffiness_no: BooleanLike = Field(
        default="",
        description="Check if member does NOT have allergies or chronic nasal stuffiness",
    )

    allergies_nasal_stuffiness_yes: BooleanLike = Field(
        default="", description="Check if member has allergies or chronic nasal stuffiness"
    )

    asthma_emphysema_copd_no: BooleanLike = Field(
        default="", description="Check if member does NOT have asthma or emphysema (COPD)"
    )

    asthma_emphysema_copd_yes: BooleanLike = Field(
        default="", description="Check if member has asthma or emphysema (COPD)"
    )

    ever_use_an_inhaler_no: BooleanLike = Field(
        default="", description="Indicate that member has never used an inhaler"
    )

    ever_use_an_inhaler_yes: BooleanLike = Field(
        default="", description="Indicate that member has used an inhaler"
    )

    short_of_breath_with_activity_no: BooleanLike = Field(
        default="", description="Indicate that member does NOT become short of breath with activity"
    )

    short_of_breath_with_activity_yes: BooleanLike = Field(
        default="", description="Indicate that member becomes short of breath with activity"
    )

    heart_attack_chest_pain_angina_no: BooleanLike = Field(
        default="", description="Indicate no history of heart attack, chest pain, or angina"
    )

    heart_attack_chest_pain_angina_yes: BooleanLike = Field(
        default="", description="Indicate history of heart attack, chest pain, or angina"
    )

    heart_murmur_heart_problems_no: BooleanLike = Field(
        default="", description="Indicate no history of heart murmur or heart problems"
    )

    heart_murmur_heart_problems_yes: BooleanLike = Field(
        default="", description="Indicate history of heart murmur or heart problems"
    )

    congestive_heart_failure_no: BooleanLike = Field(
        default="", description="Indicate no history of congestive heart failure"
    )

    congestive_heart_failure_yes: BooleanLike = Field(
        default="", description="Indicate history of congestive heart failure"
    )

    irregular_or_rapid_heartbeat_no: BooleanLike = Field(
        default="", description="Indicate no history of irregular or rapid heartbeat"
    )

    irregular_or_rapid_heartbeat_yes: BooleanLike = Field(
        default="", description="Indicate history of irregular or rapid heartbeat"
    )

    high_or_low_blood_pressure_no: BooleanLike = Field(
        default="", description="Indicate no history of high or low blood pressure"
    )

    high_or_low_blood_pressure_yes: BooleanLike = Field(
        default="", description="Indicate history of high or low blood pressure"
    )

    stomach_trouble_ulcers_no: BooleanLike = Field(
        default="", description="Indicate no history of stomach trouble or ulcers"
    )

    stomach_trouble_ulcers_yes: BooleanLike = Field(
        default="", description="Indicate history of stomach trouble or ulcers"
    )

    hepatitis_or_liver_problems_no: BooleanLike = Field(
        default="", description="Indicate no history of hepatitis or liver problems"
    )

    hepatitis_or_liver_problems_yes: BooleanLike = Field(
        default="", description="Indicate history of hepatitis or liver problems"
    )

    diarrhea_constipation_no: BooleanLike = Field(
        default="", description="Indicate no chronic diarrhea or constipation"
    )

    diarrhea_constipation_yes: BooleanLike = Field(
        default="", description="Indicate chronic diarrhea or constipation"
    )

    hernia_or_rupture_no: BooleanLike = Field(
        default="", description="Indicate no history of hernia or rupture"
    )

    hernia_or_rupture_yes: BooleanLike = Field(
        default="", description="Indicate history of hernia or rupture"
    )

    kidney_disease_or_stones_no: BooleanLike = Field(
        default="", description="Indicate no history of kidney disease or kidney stones"
    )

    kidney_disease_or_stones_yes: BooleanLike = Field(
        default="", description="Indicate history of kidney disease or kidney stones"
    )

    prostate_problems_men_no: BooleanLike = Field(
        default="", description="For male members, indicate no history of prostate problems"
    )

    prostate_problems_men_yes: BooleanLike = Field(
        default="", description="For male members, indicate history of prostate problems"
    )

    frequent_urination_no: BooleanLike = Field(
        default="", description="Indicate no frequent urination"
    )

    frequent_urination_yes: BooleanLike = Field(
        default="", description="Indicate frequent urination"
    )

    menstrual_cramps_women_no: BooleanLike = Field(
        default="", description="For female members, indicate no significant menstrual cramps"
    )

    menstrual_cramps_women_yes: BooleanLike = Field(
        default="", description="For female members, indicate significant menstrual cramps"
    )

    broken_bone_joint_problems_no: BooleanLike = Field(
        default="", description="Indicate no history of broken bones or joint problems"
    )

    broken_bone_joint_problems_yes: BooleanLike = Field(
        default="", description="Indicate history of broken bones or joint problems"
    )

    chronic_or_recurring_injuries_no: BooleanLike = Field(
        default="", description="Indicate no chronic or recurring injuries"
    )

    chronic_or_recurring_injuries_yes: BooleanLike = Field(
        default="", description="Indicate chronic or recurring injuries"
    )

    activity_mobility_restrictions_no: BooleanLike = Field(
        default="", description="Indicate no activity or mobility restrictions"
    )

    activity_mobility_restrictions_yes: BooleanLike = Field(
        default="", description="Indicate presence of activity or mobility restrictions"
    )

    use_of_cane_walker_wheelchair_no: BooleanLike = Field(
        default="", description="Indicate member does not use a cane, walker, or wheelchair"
    )

    use_of_cane_walker_wheelchair_yes: BooleanLike = Field(
        default="", description="Indicate member uses a cane, walker, or wheelchair"
    )

    back_or_neck_pain_or_injury_no: BooleanLike = Field(
        default="", description="Indicate no history of back or neck pain or injury"
    )

    back_or_neck_pain_or_injury_yes: BooleanLike = Field(
        default="", description="Indicate history of back or neck pain or injury"
    )

    migraine_or_severe_headaches_no: BooleanLike = Field(
        default="", description="Indicate no migraines or severe headaches"
    )

    migraine_or_severe_headaches_yes: BooleanLike = Field(
        default="", description="Indicate migraines or severe headaches"
    )

    dizziness_or_fainting_spells_no: BooleanLike = Field(
        default="", description="Indicate no dizziness or fainting spells"
    )

    dizziness_or_fainting_spells_yes: BooleanLike = Field(
        default="", description="Indicate dizziness or fainting spells"
    )

    head_injury_unconsciousness_no: BooleanLike = Field(
        default="", description="Indicate no history of head injury or unconsciousness"
    )

    head_injury_unconsciousness_yes: BooleanLike = Field(
        default="", description="Indicate history of head injury or unconsciousness"
    )

    epilepsy_or_seizure_no: BooleanLike = Field(
        default="", description="Indicate no history of epilepsy or seizures"
    )

    epilepsy_or_seizure_yes: BooleanLike = Field(
        default="", description="Indicate history of epilepsy or seizures"
    )

    stroke_paralysis_no: BooleanLike = Field(
        default="", description="Indicate no history of stroke or paralysis"
    )

    stroke_paralysis_yes: BooleanLike = Field(
        default="", description="Indicate history of stroke or paralysis"
    )

    thyroid_problems_low_or_high_no: BooleanLike = Field(
        default="", description="Indicate no thyroid problems"
    )

    thyroid_problems_low_or_high_yes: BooleanLike = Field(
        default="", description="Indicate thyroid problems (hypo- or hyperthyroidism)"
    )

    diabetes_high_or_low_blood_sugars_no: BooleanLike = Field(
        default="", description="Indicate no diabetes or blood sugar problems"
    )

    diabetes_high_or_low_blood_sugars_yes: BooleanLike = Field(
        default="", description="Indicate diabetes or blood sugar problems"
    )

    cancer_leukemia_no: BooleanLike = Field(
        default="", description="Indicate no history of cancer or leukemia"
    )

    cancer_leukemia_yes: BooleanLike = Field(
        default="", description="Indicate history of cancer or leukemia"
    )

    blood_disease_hemophilia_no: BooleanLike = Field(
        default="", description="Indicate no blood disease or hemophilia"
    )

    blood_disease_hemophilia_yes: BooleanLike = Field(
        default="", description="Indicate blood disease or hemophilia"
    )

    motion_sickness_no: BooleanLike = Field(default="", description="Indicate no motion sickness")

    motion_sickness_yes: BooleanLike = Field(default="", description="Indicate motion sickness")

    current_bedwetting_problems_no: BooleanLike = Field(
        default="", description="Indicate no current bedwetting problems"
    )

    current_bedwetting_problems_yes: BooleanLike = Field(
        default="", description="Indicate current bedwetting problems"
    )

    add_attention_deficit_disorder_no: BooleanLike = Field(
        default="", description="Indicate no diagnosis of ADD"
    )

    add_attention_deficit_disorder_yes: BooleanLike = Field(
        default="", description="Indicate diagnosis of ADD"
    )

    mental_illness_bipolar_other_no: BooleanLike = Field(
        default="", description="Indicate no mental illness such as bipolar disorder or others"
    )

    mental_illness_bipolar_other_yes: BooleanLike = Field(
        default="", description="Indicate mental illness such as bipolar disorder or others"
    )

    depression_anxiety_suicidal_no: BooleanLike = Field(
        default="",
        description="Indicate no history of depression, anxiety, or suicidal thoughts/behavior",
    )

    depression_anxiety_suicidal_yes: BooleanLike = Field(
        default="",
        description="Indicate history of depression, anxiety, or suicidal thoughts/behavior",
    )

    admission_to_the_hospital_no: BooleanLike = Field(
        default="", description="Indicate no prior hospital admissions"
    )

    admission_to_the_hospital_yes: BooleanLike = Field(
        default="", description="Indicate prior hospital admissions"
    )

    other_chronic_medical_illnesses_no: BooleanLike = Field(
        default="", description="Indicate no other chronic medical illnesses"
    )

    other_chronic_medical_illnesses_yes: BooleanLike = Field(
        default="", description="Indicate presence of other chronic medical illnesses"
    )

    sleep_disorder_sleep_apnea_no: BooleanLike = Field(
        default="", description="Indicate no sleep disorder or sleep apnea"
    )

    sleep_disorder_sleep_apnea_yes: BooleanLike = Field(
        default="", description="Indicate sleep disorder or sleep apnea"
    )

    serious_injury_no: BooleanLike = Field(
        default="", description="Indicate no history of serious injury"
    )

    serious_injury_yes: BooleanLike = Field(
        default="", description="Indicate history of serious injury"
    )


class CapMemberHealthHistoryForm(BaseModel):
    """
    CAP MEMBER HEALTH HISTORY FORM

    This information is CONFIDENTIAL and for official use only. It cannot be released to unauthorized persons. Answer all questions as accurately as possible so that the activity or encampment staff can make themselves aware of any pre-existing medical problems or conditions and be alert to help you. This form will also provide medical information in a case when you are unable to do so.
    """

    member_information: MemberInformation = Field(..., description="Member Information")
    allergies: Allergies = Field(..., description="Allergies")
    medical_history: MedicalHistory = Field(..., description="Medical History")
