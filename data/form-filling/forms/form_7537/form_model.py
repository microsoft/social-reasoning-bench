from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProgramDisciplineSelection(BaseModel):
    """Requested multidisciplinary program disciplines"""

    psychiatry: BooleanLike = Field(default="", description="Tick if referral is for Psychiatry")

    psychology: BooleanLike = Field(default="", description="Tick if referral is for Psychology")

    exercise_physiology: BooleanLike = Field(
        default="", description="Tick if referral is for Exercise Physiology"
    )

    physiotherapy: BooleanLike = Field(
        default="", description="Tick if referral is for Physiotherapy"
    )


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
        default="",
        description=(
            "Phone number for the referring doctor or practice .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    referring_doctor_fax: str = Field(
        default="",
        description=(
            "Fax number for the referring doctor or practice .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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
    """Patient demographic and funding details"""

    patient_name: str = Field(
        ...,
        description=(
            'Full name of the patient .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    patient_dob: str = Field(..., description="Patient date of birth")  # YYYY-MM-DD format

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
            'Primary phone number for the patient .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    patient_mobile: str = Field(
        default="",
        description=(
            'Mobile phone number for the patient .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
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
        default="",
        description=(
            'Patient Medicare number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    medicare_exp: str = Field(
        default="",
        description=(
            'Medicare card expiry date .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
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
        default="", description="Tick if the DVA At Risk Client Assessment Form has been completed"
    )

    dva_at_risk_client_assessment_form_to_be_reviewed_at_3_mths: BooleanLike = Field(
        default="", description="Tick if review is scheduled at 3 months"
    )

    dva_at_risk_client_assessment_form_to_be_reviewed_at_6_mths: BooleanLike = Field(
        default="", description="Tick if review is scheduled at 6 months"
    )

    dva_at_risk_client_assessment_form_to_be_reviewed_at_12_mths: BooleanLike = Field(
        default="", description="Tick if review is scheduled at 12 months"
    )


class ClinicalInformation(BaseModel):
    """Presenting issues, approved conditions, goals and precautions"""

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
            "Outline the goals of treatment for this referral .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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


class PsychiatryInvolvement(BaseModel):
    """Information about existing treating psychiatrist for GP referrals"""

    if_gp_referral_does_patient_have_a_treating_psychiatrist_no: BooleanLike = Field(
        default="", description="Tick if the patient does not have a treating psychiatrist"
    )

    if_gp_referral_does_patient_have_a_treating_psychiatrist_yes: BooleanLike = Field(
        default="", description="Tick if the patient has a treating psychiatrist"
    )

    treating_psychiatrist_name: str = Field(
        default="",
        description=(
            "Name of the treating psychiatrist (if applicable) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ReferrerDeclaration(BaseModel):
    """Referring doctor's signature and date"""

    doctor_signature: str = Field(
        ...,
        description=(
            'Signature of the referring doctor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    doctor_signature_date_day: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day of doctor signature"
    )

    doctor_signature_date_month: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month of doctor signature"
    )

    doctor_signature_date_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year of doctor signature"
    )


class VeteranHealthAssociationBetterLifeProgramReferralForm(BaseModel):
    """
        Veteran Health Association
    Better Life program

    Referral Form

        ''
    """

    program__discipline_selection: ProgramDisciplineSelection = Field(
        ..., description="Program / Discipline Selection"
    )
    referring_doctor: ReferringDoctor = Field(..., description="Referring Doctor")
    patient_details: PatientDetails = Field(..., description="Patient Details")
    clinical_information: ClinicalInformation = Field(..., description="Clinical Information")
    psychiatry_involvement: PsychiatryInvolvement = Field(..., description="Psychiatry Involvement")
    referrer_declaration: ReferrerDeclaration = Field(..., description="Referrer Declaration")
