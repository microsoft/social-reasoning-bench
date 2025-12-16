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
    """Basic information about the patient"""

    patient_name: str = Field(
        ...,
        description=(
            'Full legal name of the patient .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    patient_address: str = Field(
        ...,
        description=(
            'Full mailing address of the patient .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    patient_phone: str = Field(
        ...,
        description=(
            "Primary contact phone number for the patient .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    gender_identity_male: BooleanLike = Field(
        default="", description="Check if the patient's gender identity is male"
    )

    gender_identity_female: BooleanLike = Field(
        default="", description="Check if the patient's gender identity is female"
    )

    gender_identity_transman: BooleanLike = Field(
        default="", description="Check if the patient's gender identity is transman"
    )

    gender_identity_transwoman: BooleanLike = Field(
        default="", description="Check if the patient's gender identity is transwoman"
    )

    gender_identity_non_binary: BooleanLike = Field(
        default="", description="Check if the patient's gender identity is non-binary"
    )

    gender_identity_other: str = Field(
        default="",
        description=(
            "If gender identity is not listed, specify here .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth_yyyy_mm_dd: str = Field(
        ..., description="Patient's date of birth in YYYY-MM-DD format"
    )  # YYYY-MM-DD format

    date: str = Field(
        ..., description="Date this prescription form is completed"
    )  # YYYY-MM-DD format


class ClinicalInformation(BaseModel):
    """Clinical checks and current medications related to PrEP prescription"""

    hiv_test_completed_negative: BooleanLike = Field(
        ...,
        description=(
            "Indicate that an HIV test was completed and is negative through Public Health Ontario"
        ),
    )

    creatinine_completed_egfr_over_60: BooleanLike = Field(
        ..., description="Indicate that creatinine was checked and eGFR is greater than 60 mls/min"
    )

    counselled_yes: BooleanLike = Field(
        ..., description="Check if you have personally counselled the patient on the medication"
    )

    counselled_no_pharmacist_to_contact: BooleanLike = Field(
        ..., description="Check if you want the pharmacist to contact the patient for counselling"
    )

    other_prescription_medications_line_1: str = Field(
        default="",
        description=(
            "First line to list other prescription medications the patient is taking .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_prescription_medications_line_2: str = Field(
        default="",
        description=(
            "Second line to continue listing other prescription medications .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class PrescriberInformation(BaseModel):
    """Information about the prescribing physician"""

    physician_name: str = Field(
        ...,
        description=(
            "Full name of the prescribing physician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    physician_address_line_1: str = Field(
        ...,
        description=(
            "First line of the physician's mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    physician_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the physician's mailing address (if applicable) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    physician_address_city: str = Field(
        ...,
        description=(
            'City for the physician\'s address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    physician_address_postal_code: str = Field(
        ...,
        description=(
            "Postal code for the physician's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    cpso_number: str = Field(
        ...,
        description=(
            "College of Physicians and Surgeons of Ontario (CPSO) registration number .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    signature: str = Field(
        ...,
        description=(
            'Prescribing physician\'s signature .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class PrepstartPrepstartPrescriptionForm(BaseModel):
    """
        PrEPSTART
    PrEPStart Prescription Form

        To physicians: Please completely fill out all of the information below to ensure that the patient’s prescription can be filled and shipped.
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    clinical_information: ClinicalInformation = Field(..., description="Clinical Information")
    prescriber_information: PrescriberInformation = Field(..., description="Prescriber Information")
