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
    """Medical conditions and diseases the patient has or has had"""

    acid_reflux_bulimia: BooleanLike = Field(
        default="", description="Indicate if you have or have had acid reflux or bulimia"
    )

    aids_hiv_positive: BooleanLike = Field(
        default="", description="Indicate if you are AIDS or HIV positive"
    )

    alzheimers_disease: BooleanLike = Field(
        default="", description="Indicate if you have been diagnosed with Alzheimer's disease"
    )

    anaphylaxis: BooleanLike = Field(
        default="",
        description="Indicate if you have a history of anaphylaxis (severe allergic reaction)",
    )

    anemia: BooleanLike = Field(default="", description="Indicate if you have or have had anemia")

    angina: BooleanLike = Field(
        default="",
        description=(
            "Indicate if you experience or have experienced angina (chest pain due to heart "
            "disease)"
        ),
    )

    arthritis_gout: BooleanLike = Field(
        default="", description="Indicate if you have arthritis or gout"
    )

    artificial_heart_valve: BooleanLike = Field(
        default="", description="Indicate if you have an artificial heart valve"
    )

    artificial_joint: BooleanLike = Field(
        default="", description="Indicate if you have any artificial joints"
    )

    asthma: BooleanLike = Field(default="", description="Indicate if you have asthma")

    blood_disease: BooleanLike = Field(
        default="", description="Indicate if you have any blood disease"
    )

    blood_transfusion: BooleanLike = Field(
        default="", description="Indicate if you have ever had a blood transfusion"
    )

    breathing_problem: BooleanLike = Field(
        default="", description="Indicate if you have or have had breathing problems"
    )

    bruise_easy: BooleanLike = Field(default="", description="Indicate if you bruise easily")

    cancer: BooleanLike = Field(default="", description="Indicate if you have or have had cancer")

    chemotherapy: BooleanLike = Field(
        default="", description="Indicate if you have received chemotherapy"
    )

    chest_pains: BooleanLike = Field(
        default="", description="Indicate if you experience or have experienced chest pains"
    )

    cold_sores_fever_blisters: BooleanLike = Field(
        default="", description="Indicate if you get cold sores or fever blisters"
    )

    congenital_heart_disorder: BooleanLike = Field(
        default="", description="Indicate if you have a congenital heart disorder"
    )

    convulsions: BooleanLike = Field(
        default="", description="Indicate if you have a history of convulsions"
    )

    cortisone_medicine: BooleanLike = Field(
        default="",
        description="Indicate if you are currently taking or have taken cortisone medicine",
    )

    diabetes: BooleanLike = Field(default="", description="Indicate if you have diabetes")

    drug_addiction: BooleanLike = Field(
        default="", description="Indicate if you have a history of drug addiction"
    )

    easily_winded: BooleanLike = Field(
        default="", description="Indicate if you become easily winded"
    )

    emphysema: BooleanLike = Field(default="", description="Indicate if you have emphysema")

    epilepsy_or_seizures: BooleanLike = Field(
        default="", description="Indicate if you have epilepsy or a history of seizures"
    )

    excessive_bleeding: BooleanLike = Field(
        default="", description="Indicate if you have a tendency for excessive bleeding"
    )

    excessive_thirst: BooleanLike = Field(
        default="", description="Indicate if you experience excessive thirst"
    )

    fainting_dizzy_spells: BooleanLike = Field(
        default="", description="Indicate if you have fainting episodes or dizzy spells"
    )

    frequent_cough: BooleanLike = Field(
        default="", description="Indicate if you have a frequent cough"
    )

    frequent_diarrhea: BooleanLike = Field(
        default="", description="Indicate if you experience frequent diarrhea"
    )

    frequent_headaches: BooleanLike = Field(
        default="", description="Indicate if you experience frequent headaches"
    )

    genital_herpes: BooleanLike = Field(
        default="", description="Indicate if you have genital herpes"
    )

    glaucoma: BooleanLike = Field(default="", description="Indicate if you have glaucoma")

    hay_fever: BooleanLike = Field(default="", description="Indicate if you have hay fever")

    heart_attack_failure: BooleanLike = Field(
        default="", description="Indicate if you have had a heart attack or heart failure"
    )

    heart_murmur: BooleanLike = Field(default="", description="Indicate if you have a heart murmur")

    heart_pacemaker: BooleanLike = Field(
        default="", description="Indicate if you have a heart pacemaker"
    )

    heart_trouble_disease: BooleanLike = Field(
        default="", description="Indicate if you have heart trouble or heart disease"
    )

    hemophilia: BooleanLike = Field(default="", description="Indicate if you have hemophilia")

    hepatitis_a: BooleanLike = Field(default="", description="Indicate if you have had hepatitis A")

    hepatitis_b_or_c: BooleanLike = Field(
        default="", description="Indicate if you have had hepatitis B or C"
    )

    herpes: BooleanLike = Field(
        default="", description="Indicate if you have herpes (non-genital or unspecified)"
    )

    high_blood_pressure: BooleanLike = Field(
        default="", description="Indicate if you have high blood pressure"
    )

    high_cholesterol: BooleanLike = Field(
        default="", description="Indicate if you have high cholesterol"
    )

    hives_or_rash: BooleanLike = Field(
        default="", description="Indicate if you experience hives or skin rashes"
    )

    hypoglycemia: BooleanLike = Field(
        default="", description="Indicate if you have hypoglycemia (low blood sugar)"
    )

    irregular_heartbeat: BooleanLike = Field(
        default="", description="Indicate if you have an irregular heartbeat"
    )

    kidney_problems: BooleanLike = Field(
        default="", description="Indicate if you have kidney problems"
    )

    leukemia: BooleanLike = Field(
        default="", description="Indicate if you have or have had leukemia"
    )

    liver_disease: BooleanLike = Field(default="", description="Indicate if you have liver disease")

    low_blood_pressure: BooleanLike = Field(
        default="", description="Indicate if you have low blood pressure"
    )

    lung_disease: BooleanLike = Field(default="", description="Indicate if you have lung disease")

    mitral_valve_prolapse: BooleanLike = Field(
        default="", description="Indicate if you have mitral valve prolapse"
    )

    osteoporosis: BooleanLike = Field(default="", description="Indicate if you have osteoporosis")

    pain_in_jaw_joints: BooleanLike = Field(
        default="", description="Indicate if you experience pain in your jaw joints"
    )

    parathyroid_disease: BooleanLike = Field(
        default="", description="Indicate if you have parathyroid disease"
    )

    psychiatric_care: BooleanLike = Field(
        default="", description="Indicate if you are or have been under psychiatric care"
    )

    radiation_treatments: BooleanLike = Field(
        default="", description="Indicate if you have received radiation treatments"
    )

    recent_weight_loss: BooleanLike = Field(
        default="", description="Indicate if you have had a recent unexplained weight loss"
    )

    renal_dialysis: BooleanLike = Field(
        default="", description="Indicate if you are on or have had renal dialysis"
    )

    rheumatic_fever: BooleanLike = Field(
        default="", description="Indicate if you have had rheumatic fever"
    )

    rheumatism: BooleanLike = Field(default="", description="Indicate if you have rheumatism")

    scarlet_fever: BooleanLike = Field(
        default="", description="Indicate if you have had scarlet fever"
    )

    shingles: BooleanLike = Field(default="", description="Indicate if you have had shingles")

    sickle_cell_disease: BooleanLike = Field(
        default="", description="Indicate if you have sickle cell disease"
    )

    sinus_trouble: BooleanLike = Field(default="", description="Indicate if you have sinus trouble")

    spina_bifida: BooleanLike = Field(default="", description="Indicate if you have spina bifida")

    stomach_intestinal_disease: BooleanLike = Field(
        default="", description="Indicate if you have stomach or intestinal disease"
    )

    stroke: BooleanLike = Field(default="", description="Indicate if you have had a stroke")

    swelling_of_limbs: BooleanLike = Field(
        default="", description="Indicate if you experience swelling of your limbs"
    )

    thyroid_disease: BooleanLike = Field(
        default="", description="Indicate if you have thyroid disease"
    )

    tonsillitis: BooleanLike = Field(
        default="", description="Indicate if you have frequent or chronic tonsillitis"
    )

    tuberculosis: BooleanLike = Field(
        default="", description="Indicate if you have had tuberculosis"
    )

    tumors_or_growths: BooleanLike = Field(
        default="", description="Indicate if you have or have had tumors or abnormal growths"
    )

    ulcers: BooleanLike = Field(default="", description="Indicate if you have ulcers")

    venereal_disease: BooleanLike = Field(
        default="",
        description="Indicate if you have or have had a venereal (sexually transmitted) disease",
    )

    yellow_jaundice: BooleanLike = Field(
        default="", description="Indicate if you have had yellow jaundice"
    )


class OtherSeriousIllnesses(BaseModel):
    """Additional serious illnesses not listed in the main medical history checklist"""

    have_you_ever_had_any_serious_illness_not_listed_above_yes: BooleanLike = Field(
        default="", description="Check YES if you have had any serious illness not listed above"
    )

    have_you_ever_had_any_serious_illness_not_listed_above_no: BooleanLike = Field(
        default="", description="Check NO if you have not had any serious illness not listed above"
    )

    if_yes_please_list_below: str = Field(
        default="",
        description=(
            "Describe any serious illnesses not listed above .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    comments: str = Field(
        default="",
        description=(
            "Additional comments about your medical history .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Authorization(BaseModel):
    """Patient/guardian confirmation and signature"""

    signature_of_patient_parent_or_guardian: str = Field(
        ...,
        description=(
            "Signature of the patient, parent, or legal guardian confirming the accuracy of "
            'the information .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Date this medical history form is signed"
    )  # YYYY-MM-DD format


class MedicalHistory(BaseModel):
    """
    MEDICAL HISTORY

    ''
    """

    medical_history: MedicalHistory = Field(..., description="Medical History")
    other_serious_illnesses: OtherSeriousIllnesses = Field(
        ..., description="Other Serious Illnesses"
    )
    authorization: Authorization = Field(..., description="Authorization")
