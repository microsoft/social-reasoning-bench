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
    """Basic identifying information about the patient"""

    patient_name: str = Field(
        ...,
        description=(
            'Full legal name of the patient .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    birth_date: str = Field(..., description="Patient's date of birth")  # YYYY-MM-DD format


class GeneralMedicalHistory(BaseModel):
    """Current care, hospitalizations, injuries, medications, and substance use"""

    are_you_under_a_physicians_care_now: BooleanLike = Field(
        ..., description="Indicate if you are currently under the care of a physician"
    )

    if_yes_please_explain_under_physicians_care: str = Field(
        default="",
        description=(
            "If under a physician's care, describe the condition and treatment .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    have_you_ever_been_hospitalized_or_had_a_major_operation: BooleanLike = Field(
        ..., description="Indicate if you have ever been hospitalized or had major surgery"
    )

    if_yes_please_explain_hospitalized_or_major_operation: str = Field(
        default="",
        description=(
            "If hospitalized or had major surgery, provide details .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    have_you_ever_had_a_serious_head_or_neck_injury: BooleanLike = Field(
        ..., description="Indicate if you have ever had a serious head or neck injury"
    )

    if_yes_please_explain_serious_head_or_neck_injury: str = Field(
        default="",
        description=(
            "If you had a serious head or neck injury, describe the injury .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    are_you_taking_any_medication_pills_or_drugs: BooleanLike = Field(
        ..., description="Indicate if you are currently taking any medications, pills, or drugs"
    )

    do_you_take_or_have_you_taken_phen_fen_or_redux: BooleanLike = Field(
        ..., description="Specify if you currently take or have ever taken Phen-Fen or Redux"
    )

    have_you_ever_taken_fosamax_bonivea_actonel_or_any_other_medications_containing_bisphosphonates: BooleanLike = Field(
        ...,
        description=(
            "Indicate if you have ever taken Fosamax, Boniva, Actonel, or other "
            "bisphosphonate medications"
        ),
    )

    are_you_on_a_special_diet: BooleanLike = Field(
        ..., description="Indicate if you are currently following a special diet"
    )

    are_you_a_tobacco_user: BooleanLike = Field(
        ..., description="Indicate if you use any tobacco products"
    )

    do_you_use_controlled_substances: BooleanLike = Field(
        ..., description="Indicate if you use any controlled substances"
    )


class Allergies(BaseModel):
    """Allergy information related to medications and materials"""

    allergy_to_aspirin: BooleanLike = Field(
        default="", description="Check yes if you are allergic to Aspirin"
    )

    allergy_to_penicillin: BooleanLike = Field(
        default="", description="Check yes if you are allergic to Penicillin"
    )

    allergy_to_codeine: BooleanLike = Field(
        default="", description="Check yes if you are allergic to Codeine"
    )

    allergy_to_local_anesthetics: BooleanLike = Field(
        default="", description="Check yes if you are allergic to local anesthetics"
    )

    allergy_to_acrylic: BooleanLike = Field(
        default="", description="Check yes if you are allergic to acrylic"
    )

    allergy_to_metal: BooleanLike = Field(
        default="", description="Check yes if you are allergic to metals"
    )

    allergy_to_latex: BooleanLike = Field(
        default="", description="Check yes if you are allergic to latex"
    )

    allergy_to_sulfa_drugs: BooleanLike = Field(
        default="", description="Check yes if you are allergic to sulfa drugs"
    )

    other_allergy_please_explain: str = Field(
        default="",
        description=(
            "List and describe any other allergies not listed above .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class WomensHealth(BaseModel):
    """Women-specific health information"""

    pregnant_trying_to_get_pregnant: BooleanLike = Field(
        default="",
        description="Indicate if you are currently pregnant or trying to become pregnant",
    )

    taking_oral_contraceptives: BooleanLike = Field(
        default="", description="Indicate if you are currently taking oral contraceptives"
    )

    nursing: BooleanLike = Field(default="", description="Indicate if you are currently nursing")


class MedicalHistory(BaseModel):
    """
    MEDICAL HISTORY

    Although dental personnel primarily treat the area in and around your mouth, your mouth is a part of your entire body. Health problems that you may have, or medication that you may be taking, could have an important interrelationship with the dentistry you will receive. Thank you for answering the following questions.
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    general_medical_history: GeneralMedicalHistory = Field(
        ..., description="General Medical History"
    )
    allergies: Allergies = Field(..., description="Allergies")
    womens_health: WomensHealth = Field(..., description="Women’s Health")
