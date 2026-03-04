from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ReferringDoctor(BaseModel):
    """Details of the referring doctor"""

    referring_doctor_name: str = Field(
        ...,
        description=(
            'Full name of the referring doctor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    referring_doctor_provider_no: str = Field(
        ...,
        description=(
            "Provider number of the referring doctor .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    referring_doctor_practice_address: str = Field(
        ...,
        description=(
            "Practice address of the referring doctor .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    referring_doctor_phone: str = Field(
        ...,
        description=(
            "Main phone number for the referring doctor's practice .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    referring_doctor_fax: str = Field(
        default="",
        description=(
            "Fax number for the referring doctor's practice .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    referring_doctor_email: str = Field(
        default="",
        description=(
            "Email address for the referring doctor or practice .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PatientDetails(BaseModel):
    """Patient contact and identification details"""

    patient_name: str = Field(
        ...,
        description=(
            'Full name of the patient .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    patient_dob: str = Field(..., description="Patient's date of birth")  # YYYY-MM-DD format

    patient_address: str = Field(
        ...,
        description=(
            'Residential address of the patient .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    patient_phone: str = Field(
        default="",
        description=(
            "Home or primary phone number of the patient .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    patient_mobile: str = Field(
        default="",
        description=(
            'Mobile phone number of the patient .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    patient_email: str = Field(
        default="",
        description=(
            'Email address of the patient .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    medicare_no: str = Field(
        ...,
        description=(
            'Patient\'s Medicare number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    medicare_exp: str = Field(
        ...,
        description=(
            "Expiry date of the patient's Medicare card .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dva_card_no: str = Field(
        default="",
        description=(
            "Department of Veterans' Affairs (DVA) card number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    dva_card_type_white: BooleanLike = Field(
        default="", description="Tick if the patient holds a White DVA card"
    )

    dva_card_type_gold: BooleanLike = Field(
        default="", description="Tick if the patient holds a Gold DVA card"
    )

    dva_card_type_gold_tpi: BooleanLike = Field(
        default="", description="Tick if the patient holds a Gold (TPI) DVA card"
    )

    dva_at_risk_client_assessment_form_completed: BooleanLike = Field(
        default="",
        description="Indicate whether the DVA At Risk Client Assessment Form has been completed",
    )

    to_be_reviewed_at_3_mths: BooleanLike = Field(
        default="", description="Tick if review is scheduled at 3 months"
    )

    to_be_reviewed_at_6_mths: BooleanLike = Field(
        default="", description="Tick if review is scheduled at 6 months"
    )

    to_be_reviewed_at_12_mths: BooleanLike = Field(
        default="", description="Tick if review is scheduled at 12 months"
    )


class ClinicalInformation(BaseModel):
    """Presenting issues, goals, and special considerations"""

    presenting_conditions: str = Field(
        ...,
        description=(
            "Describe the patient's presenting conditions .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    for_white_card_holders_dva_approved_conditions: str = Field(
        default="",
        description=(
            "List DVA-approved conditions for White Card holders .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    treatment_goals: str = Field(
        ...,
        description=(
            "Outline the treatment goals for the patient .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medical_precautions_special_needs: str = Field(
        default="",
        description=(
            "Note any medical precautions or special needs .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PsychiatryInformation(BaseModel):
    """Information about treating psychiatrist where applicable"""

    gp_referral_treating_psychiatrist_no: BooleanLike = Field(
        default="", description="Tick if the patient does not have a treating psychiatrist"
    )

    gp_referral_treating_psychiatrist_yes: BooleanLike = Field(
        default="", description="Tick if the patient has a treating psychiatrist"
    )

    treating_psychiatrist_name_dr: str = Field(
        default="",
        description=(
            "Name of the treating psychiatrist (following 'Dr') .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ReferrerDeclaration(BaseModel):
    """Signature and date of the referring doctor"""

    doctor_signature: str = Field(
        ...,
        description=(
            'Signature of the referring doctor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    doctor_signature_date: str = Field(
        ..., description="Date the referring doctor signed the form"
    )  # YYYY-MM-DD format


class VeteranHealthAssociationBetterLifeProgramReferralForm(BaseModel):
    """
        Veteran Health Association
    Better Life program

    Referral Form

        ''
    """

    referring_doctor: ReferringDoctor = Field(..., description="Referring Doctor")
    patient_details: PatientDetails = Field(..., description="Patient Details")
    clinical_information: ClinicalInformation = Field(..., description="Clinical Information")
    psychiatry_information: PsychiatryInformation = Field(..., description="Psychiatry Information")
    referrer_declaration: ReferrerDeclaration = Field(..., description="Referrer Declaration")
