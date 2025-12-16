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
    """Basic identifying and contact information for the student"""

    last_name: str = Field(
        ...,
        description=(
            'Student\'s legal last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Student\'s legal first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    middle_name: str = Field(
        default="",
        description=(
            'Student\'s middle name or initial .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    home_address: str = Field(
        ...,
        description=(
            'Student\'s full street address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of residence .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of residence")

    zip: str = Field(..., description="5-digit ZIP code")

    county: str = Field(
        default="",
        description=(
            'County of residence .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class CurrentHealthStatus(BaseModel):
    """Current health, demographics, and provider/medication information within the past 12 months"""

    male: BooleanLike = Field(..., description="Check if the student is male")

    female: BooleanLike = Field(..., description="Check if the student is female")

    height: str = Field(
        ...,
        description=(
            "Student's height (include units, e.g., feet/inches) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    weight: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Student's weight (in pounds)"
    )

    eye_color: str = Field(
        ...,
        description=(
            'Student\'s natural eye color .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    hair_color: str = Field(
        ...,
        description=(
            'Student\'s natural hair color .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    physician: str = Field(
        default="",
        description=(
            "Primary physician's name or N/A if none .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    physician_phone: str = Field(
        default="",
        description=(
            'Primary physician\'s phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    dentist: str = Field(
        default="",
        description=(
            'Dentist\'s name or N/A if none .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    dentist_phone: str = Field(
        default="",
        description=(
            'Dentist\'s phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    current_medications_1: str = Field(
        default="",
        description=(
            "First current medication name, or N/A if none .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    current_medications_2: str = Field(
        default="",
        description=(
            "Second current medication name, or N/A if none .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    current_medications_3: str = Field(
        default="",
        description=(
            "Third current medication name, or N/A if none .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    current_medications_4: str = Field(
        default="",
        description=(
            "Fourth current medication name, or N/A if none .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dosage_1: str = Field(
        default="",
        description=(
            'Dosage for current medication 1 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    dosage_2: str = Field(
        default="",
        description=(
            'Dosage for current medication 2 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    dosage_3: str = Field(
        default="",
        description=(
            'Dosage for current medication 3 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    dosage_4: str = Field(
        default="",
        description=(
            'Dosage for current medication 4 .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    times_given_1: str = Field(
        default="",
        description=(
            "Administration time(s) for current medication 1 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    times_given_2: str = Field(
        default="",
        description=(
            "Administration time(s) for current medication 2 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    times_given_3: str = Field(
        default="",
        description=(
            "Administration time(s) for current medication 3 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    times_given_4: str = Field(
        default="",
        description=(
            "Administration time(s) for current medication 4 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class MedicalHistoryGeneralConditionsPast12Months(BaseModel):
    """General medical conditions checklist within the past 12 months (first group)"""

    tuberculosis_or_positive_tb_test: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has had tuberculosis or a positive TB test within the "
            "past 12 months"
        ),
    )

    blood_in_sputum_or_when_coughing: BooleanLike = Field(
        default="",
        description=(
            "Check if blood has been present in sputum or when coughing within the past 12 months"
        ),
    )

    excessive_bleeding_after_injury_or_dental_work: BooleanLike = Field(
        default="",
        description=(
            "Check if there has been excessive bleeding after injury or dental work within "
            "the past 12 months"
        ),
    )

    attempted_suicide: BooleanLike = Field(
        default="",
        description="Check if the student has attempted suicide within the past 12 months",
    )

    sleepwalking: BooleanLike = Field(
        default="",
        description="Check if the student has experienced sleepwalking within the past 12 months",
    )

    wear_corrective_lenses: BooleanLike = Field(
        default="", description="Check if the student wears glasses or contact lenses"
    )

    eye_surgery_to_correct_vision: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has had eye surgery to correct vision within the past 12 months"
        ),
    )

    lack_vision_in_either_eye: BooleanLike = Field(
        default="", description="Check if the student lacks vision in either eye"
    )

    hearing_loss: BooleanLike = Field(
        default="", description="Check if the student has hearing loss"
    )

    wear_a_hearing_aid: BooleanLike = Field(
        default="", description="Check if the student wears a hearing aid"
    )

    stutter_or_stammer: BooleanLike = Field(
        default="", description="Check if the student stutters or stammers"
    )

    wear_a_brace_or_back_support: BooleanLike = Field(
        default="", description="Check if the student wears a brace or back support"
    )

    rheumatic_fever: BooleanLike = Field(
        default="",
        description="Check if the student has had rheumatic fever within the past 12 months",
    )

    swollen_or_painful_joints: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has experienced swollen or painful joints within the past "
            "12 months"
        ),
    )

    frequent_or_severe_headaches: BooleanLike = Field(
        default="",
        description="Check if the student has frequent or severe headaches within the past 12 months",
    )

    dizziness_or_fainting_spells: BooleanLike = Field(
        default="",
        description="Check if the student has dizziness or fainting spells within the past 12 months",
    )

    recurrent_ear_infections: BooleanLike = Field(
        default="",
        description="Check if the student has recurrent ear infections within the past 12 months",
    )

    chronic_or_frequent_colds: BooleanLike = Field(
        default="",
        description="Check if the student has chronic or frequent colds within the past 12 months",
    )

    severe_tooth_or_gum_trouble: BooleanLike = Field(
        default="",
        description="Check if the student has severe tooth or gum trouble within the past 12 months",
    )

    sinusitis: BooleanLike = Field(
        default="", description="Check if the student has had sinusitis within the past 12 months"
    )

    head_injury: BooleanLike = Field(
        default="",
        description="Check if the student has had a head injury within the past 12 months",
    )

    asthma: BooleanLike = Field(default="", description="Check if the student has asthma")


class MedicalHistoryOrganSystemsOtherConditionsPast12Months(BaseModel):
    """Organ system-related and other medical conditions checklist within the past 12 months (second group)"""

    arthritis_rheumatism_or_bursitis: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has arthritis, rheumatism, or bursitis within the past 12 months"
        ),
    )

    shortness_of_breath: BooleanLike = Field(
        default="",
        description="Check if the student experiences shortness of breath within the past 12 months",
    )

    pain_or_pressure_in_chest: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has pain or pressure in the chest within the past 12 months"
        ),
    )

    chronic_cough: BooleanLike = Field(
        default="", description="Check if the student has a chronic cough within the past 12 months"
    )

    palpitation_or_pounding_heart: BooleanLike = Field(
        default="",
        description=(
            "Check if the student experiences palpitations or a pounding heart within the "
            "past 12 months"
        ),
    )

    heart_trouble: BooleanLike = Field(
        default="", description="Check if the student has heart trouble within the past 12 months"
    )

    high_or_low_blood_pressure: BooleanLike = Field(
        default="",
        description="Check if the student has high or low blood pressure within the past 12 months",
    )

    cramps_in_your_legs: BooleanLike = Field(
        default="",
        description="Check if the student has cramps in the legs within the past 12 months",
    )

    frequent_indigestion: BooleanLike = Field(
        default="",
        description="Check if the student has frequent indigestion within the past 12 months",
    )

    stomach_liver_or_intestinal_trouble: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has stomach, liver, or intestinal trouble within the past "
            "12 months"
        ),
    )

    gall_bladder_trouble_or_gallstones: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has gall bladder trouble or gallstones within the past 12 months"
        ),
    )

    jaundice_or_hepatitis: BooleanLike = Field(
        default="",
        description="Check if the student has had jaundice or hepatitis within the past 12 months",
    )

    broken_bones: BooleanLike = Field(
        default="",
        description="Check if the student has had broken bones within the past 12 months",
    )

    adverse_reaction_to_medication: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has had an adverse reaction to medication within the past "
            "12 months"
        ),
    )

    skin_disease: BooleanLike = Field(
        default="",
        description="Check if the student has had a skin disease within the past 12 months",
    )

    tumor_growth_cyst_cancer: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has had a tumor, growth, cyst, or cancer within the past "
            "12 months"
        ),
    )

    hernia: BooleanLike = Field(
        default="", description="Check if the student has a hernia within the past 12 months"
    )

    hemorrhoids_or_rectal_disease: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has hemorrhoids or rectal disease within the past 12 months"
        ),
    )

    frequent_or_painful_urination: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has frequent or painful urination within the past 12 months"
        ),
    )

    kidney_stone_or_blood_in_urine: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has had kidney stones or blood in urine within the past 12 months"
        ),
    )

    sugar_or_albumin_in_urine: BooleanLike = Field(
        default="",
        description=(
            "Check if sugar or albumin has been present in the student's urine within the "
            "past 12 months"
        ),
    )

    sexually_transmitted_disease: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has had a sexually transmitted disease within the past 12 months"
        ),
    )

    recent_gain_or_loss_of_weight: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has had a recent significant gain or loss of weight "
            "within the past 12 months"
        ),
    )

    eating_disorder: BooleanLike = Field(
        default="",
        description="Check if the student has an eating disorder within the past 12 months",
    )


class MedicalHistoryMusculoskeletalNeurologicandOtherPast12Months(BaseModel):
    """Musculoskeletal, neurologic, treatment history, and lifestyle factors checklist within the past 12 months (third group)"""

    bone_joint_or_other_deformity: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has a bone, joint, or other deformity within the past 12 months"
        ),
    )

    loss_of_finger_or_toe: BooleanLike = Field(
        default="", description="Check if the student has lost a finger or toe"
    )

    recurrent_back_pain_or_any_back_injury: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has recurrent back pain or any back injury within the "
            "past 12 months"
        ),
    )

    trick_or_locked_knee: BooleanLike = Field(
        default="",
        description="Check if the student has a trick or locked knee within the past 12 months",
    )

    foot_trouble: BooleanLike = Field(
        default="", description="Check if the student has foot trouble within the past 12 months"
    )

    nerve_injury: BooleanLike = Field(
        default="",
        description="Check if the student has had a nerve injury within the past 12 months",
    )

    paralysis_including_infantile: BooleanLike = Field(
        default="", description="Check if the student has paralysis, including infantile paralysis"
    )

    epilepsy_or_seizure: BooleanLike = Field(
        default="",
        description="Check if the student has epilepsy or has had seizures within the past 12 months",
    )

    car_train_sea_or_air_sickness: BooleanLike = Field(
        default="",
        description="Check if the student experiences motion sickness (car, train, sea, or air)",
    )

    frequent_trouble_sleeping: BooleanLike = Field(
        default="",
        description="Check if the student frequently has trouble sleeping within the past 12 months",
    )

    depression_or_excessive_worry: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has depression or excessive worry within the past 12 months"
        ),
    )

    loss_of_memory_or_amnesia: BooleanLike = Field(
        default="",
        description="Check if the student has loss of memory or amnesia within the past 12 months",
    )

    nervous_trouble_of_any_sort: BooleanLike = Field(
        default="",
        description="Check if the student has nervous trouble of any sort within the past 12 months",
    )

    periods_of_unconsciousness: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has had periods of unconsciousness within the past 12 months"
        ),
    )

    x_ray_or_other_radiation_therapy: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has received X-ray or other radiation therapy within the "
            "past 12 months"
        ),
    )

    chemotherapy: BooleanLike = Field(
        default="",
        description="Check if the student has received chemotherapy within the past 12 months",
    )

    plate_pin_or_rod_in_any_bone: BooleanLike = Field(
        default="", description="Check if the student has a plate, pin, or rod in any bone"
    )

    easily_fatigued: BooleanLike = Field(
        default="", description="Check if the student is easily fatigued within the past 12 months"
    )

    alcohol_use: BooleanLike = Field(default="", description="Check if the student uses alcohol")

    used_illegal_substance: BooleanLike = Field(
        default="", description="Check if the student has used illegal substances"
    )

    used_tobacco: BooleanLike = Field(
        default="", description="Check if the student has used tobacco"
    )

    thyroid_trouble_or_goiter: BooleanLike = Field(
        default="",
        description="Check if the student has thyroid trouble or goiter within the past 12 months",
    )

    allergies: str = Field(
        default="",
        description=(
            'List any allergies the student has .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class MentalHealthHistoryPastYear(BaseModel):
    """Counseling and mental health treatment history within the past year"""

    received_counseling_past_year_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if the student has received counseling or been treated in a mental "
            "health facility for a mental health issue within the past year (Yes)"
        ),
    )

    received_counseling_past_year_no: BooleanLike = Field(
        default="",
        description=(
            "Select if the student has NOT received counseling or been treated in a mental "
            "health facility for a mental health issue within the past year (No)"
        ),
    )

    by_a_psychiatrist_yes: BooleanLike = Field(
        default="", description="Select Yes if counseling/treatment was by a psychiatrist"
    )

    by_a_psychiatrist_no: BooleanLike = Field(
        default="", description="Select No if counseling/treatment was not by a psychiatrist"
    )

    mental_health_therapist_yes: BooleanLike = Field(
        default="",
        description="Select Yes if counseling/treatment was by a mental health therapist",
    )

    mental_health_therapist_no: BooleanLike = Field(
        default="",
        description="Select No if counseling/treatment was not by a mental health therapist",
    )

    social_worker_yes: BooleanLike = Field(
        default="", description="Select Yes if counseling/treatment was by a social worker"
    )

    social_worker_no: BooleanLike = Field(
        default="", description="Select No if counseling/treatment was not by a social worker"
    )

    if_yes_how_often_and_for_what_reason: str = Field(
        default="",
        description=(
            "Describe how often counseling/treatment occurred and the reason .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    when_did_it_start: str = Field(
        default="",
        description=(
            "Approximate date when counseling/treatment started .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    when_did_it_end: str = Field(
        default="",
        description=(
            "Approximate date when counseling/treatment ended .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_therapist: str = Field(
        default="",
        description=(
            'Therapist\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    therapist_phone: str = Field(
        default="",
        description=(
            'Therapist\'s phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class AdditionalMedicalHistory(BaseModel):
    """Open-ended additional medical history within the past year"""

    additional_medical_history_within_the_past_year: str = Field(
        default="",
        description=(
            "Provide any additional medical history within the past year (use back of form "
            'if needed) .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class ArkansasGuardYouthChallengeMedicalHistoryReport(BaseModel):
    """
        Arkansas National Guard Youth ChalleNGe Program
    Report of Medical History (within the past 12 months)

        Report of Medical History (within the past 12 months)
    """

    student_information: StudentInformation = Field(..., description="Student Information")
    current_health_status: CurrentHealthStatus = Field(..., description="Current Health Status")
    medical_history___general_conditions_past_12_months: MedicalHistoryGeneralConditionsPast12Months = Field(
        ..., description="Medical History – General Conditions (Past 12 Months)"
    )
    medical_history___organ_systems__other_conditions_past_12_months: MedicalHistoryOrganSystemsOtherConditionsPast12Months = Field(
        ..., description="Medical History – Organ Systems & Other Conditions (Past 12 Months)"
    )
    medical_history___musculoskeletal_neurologic_and_other_past_12_months: MedicalHistoryMusculoskeletalNeurologicandOtherPast12Months = Field(
        ..., description="Medical History – Musculoskeletal, Neurologic, and Other (Past 12 Months)"
    )
    mental_health_history_past_year: MentalHealthHistoryPastYear = Field(
        ..., description="Mental Health History (Past Year)"
    )
    additional_medical_history: AdditionalMedicalHistory = Field(
        ..., description="Additional Medical History"
    )
