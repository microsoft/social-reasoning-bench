from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ReferringProviderInformation(BaseModel):
    """Information about the provider making the referral"""

    from_: str = Field(
        ...,
        description=(
            "Name of the referring provider or practice .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    credential: str = Field(
        ...,
        description=(
            "Professional credential(s) of the referring provider (e.g., MD, DO, NP, PA) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    doctors_signature: str = Field(
        ...,
        description=(
            "Signature of the referring doctor or authorized provider .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PatientInformation(BaseModel):
    """Basic information about the patient being referred"""

    name: str = Field(
        ...,
        description=(
            'Patient\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date_of_referral: str = Field(
        ..., description="Date this referral was made"
    )  # YYYY-MM-DD format

    date_of_birth: str = Field(..., description="Patient's date of birth")  # YYYY-MM-DD format


class ReasonforReferral(BaseModel):
    """Clinical reasons and notes for the nutrition consult"""

    obesity_e66_9: BooleanLike = Field(
        default="", description="Check if the referral diagnosis includes obesity (ICD-10 E66.9)"
    )

    overweight_e66_3: BooleanLike = Field(
        default="", description="Check if the referral diagnosis includes overweight (ICD-10 E66.3)"
    )

    type_i_diabetes_e10_8: BooleanLike = Field(
        default="",
        description="Check if the referral diagnosis includes Type I diabetes (ICD-10 E10.8)",
    )

    type_ii_diabetes_e11_8: BooleanLike = Field(
        default="",
        description="Check if the referral diagnosis includes Type II diabetes (ICD-10 E11.8)",
    )

    pregnancy: BooleanLike = Field(default="", description="Check if the patient is pregnant")

    comments: str = Field(
        default="",
        description=(
            "Additional clinical information or notes relevant to the nutrition consult .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class NazMaduroNutrition(BaseModel):
    """
    Naz Maduro NUTRITION

    Nutrition Consult:
    """

    referring_provider_information: ReferringProviderInformation = Field(
        ..., description="Referring Provider Information"
    )
    patient_information: PatientInformation = Field(..., description="Patient Information")
    reason_for_referral: ReasonforReferral = Field(..., description="Reason for Referral")
