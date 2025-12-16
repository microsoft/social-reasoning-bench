from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FunctionalStatus(BaseModel):
    """Assistance with hygiene and ability to walk, including walking aids"""

    assistance_hygiene_complete: BooleanLike = Field(
        default="",
        description="Check if you need complete assistance with essential hygiene tasks.",
    )

    assistance_hygiene_none: BooleanLike = Field(
        default="",
        description="Check if you do not need any assistance with essential hygiene tasks.",
    )

    assistance_hygiene_some: str = Field(
        default="",
        description=(
            "Describe the specific hygiene tasks for which you need some assistance. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    walk_independently_yes: BooleanLike = Field(
        default="", description="Check if you are able to walk independently."
    )

    walk_independently_distance_metres: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Approximate distance in metres you can walk independently."
    )

    walk_independently_no: BooleanLike = Field(
        default="", description="Check if you are not able to walk independently."
    )

    walking_aid_crutches: BooleanLike = Field(
        default="", description="Check if you use crutches while walking."
    )

    walking_aid_wheelchair: BooleanLike = Field(
        default="", description="Check if you use a wheelchair while moving around."
    )

    walking_aid_cane: BooleanLike = Field(
        default="", description="Check if you use a cane while walking."
    )

    walking_aid_walker: BooleanLike = Field(
        default="", description="Check if you use a walker while walking."
    )


class MedicalandDietaryInformation(BaseModel):
    """Medication, diabetes, diet status, and initial diet preferences"""

    medication_yes: BooleanLike = Field(
        default="", description="Check if you are currently taking any medication."
    )

    medication_no: BooleanLike = Field(
        default="", description="Check if you are not currently taking any medication."
    )

    medication_list: str = Field(
        default="",
        description=(
            "List all medications you are currently taking. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    diabetes_yes: BooleanLike = Field(
        default="", description="Check if you have been diagnosed with diabetes."
    )

    diabetes_no: BooleanLike = Field(
        default="", description="Check if you have not been diagnosed with diabetes."
    )

    diet_yes: BooleanLike = Field(
        default="", description="Check if you are currently following a specific diet."
    )

    diet_no: BooleanLike = Field(
        default="", description="Check if you are not currently following a specific diet."
    )

    diet_list: str = Field(
        default="",
        description=(
            "Describe the diet you are currently following. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    personalized_diet_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if you are interested in purchasing a personalized diet plan during your stay."
        ),
    )

    personalized_diet_no: BooleanLike = Field(
        default="",
        description=(
            "Check if you are not interested in purchasing a personalized diet plan during "
            "your stay."
        ),
    )

    initial_diet_general: BooleanLike = Field(
        default="",
        description=(
            "Select if you prefer a general initial diet until an individual diet is prepared."
        ),
    )

    initial_diet_easy_to_digest: BooleanLike = Field(
        default="",
        description=(
            "Select if you prefer an easy-to-digest initial diet until an individual diet "
            "is prepared."
        ),
    )

    initial_diet_vegan: BooleanLike = Field(
        default="",
        description="Select if you prefer a vegan initial diet until an individual diet is prepared.",
    )

    initial_diet_gluten_free: BooleanLike = Field(
        default="",
        description=(
            "Select if you prefer a gluten-free initial diet until an individual diet is prepared."
        ),
    )


class ReferralSource(BaseModel):
    """How the patient heard about Columna Medica"""

    referral_friends: BooleanLike = Field(
        default="", description="Check if you heard about Columna Medica from friends."
    )

    referral_internet: BooleanLike = Field(
        default="", description="Check if you heard about Columna Medica via the internet."
    )

    referral_doctor_name: str = Field(
        default="",
        description=(
            "Name of the doctor who referred you to Columna Medica. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    referral_doctor_specialization: str = Field(
        default="",
        description=(
            "Specialization of the doctor who referred you. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    referral_others: BooleanLike = Field(
        default="", description="Check if you heard about Columna Medica through another source."
    )


class ColumnaMedicaPatientFormPrequalificationFormForPhysiotherapy(BaseModel):
    """
    COLUMNA MEDICA             PATIENT FORM - PRE-QUALIFICATION FORM FOR PHYSIOTHERAPY

    ''
    """

    functional_status: FunctionalStatus = Field(..., description="Functional Status")
    medical_and_dietary_information: MedicalandDietaryInformation = Field(
        ..., description="Medical and Dietary Information"
    )
    referral_source: ReferralSource = Field(..., description="Referral Source")
