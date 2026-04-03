from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ReferralType(BaseModel):
    """Type and purpose of the referral/order"""

    new_referral: BooleanLike = Field(
        default="", description="Check if this is a new referral for KRYSTEXXA therapy"
    )

    order_renewal: BooleanLike = Field(
        default="", description="Check if this is a renewal of an existing KRYSTEXXA order"
    )

    medication_order_change: BooleanLike = Field(
        default="", description="Check if this is a change to the existing medication or order"
    )

    benefits_verification_only: BooleanLike = Field(
        default="", description="Check if the request is only for benefits verification"
    )

    discontinuation_order: BooleanLike = Field(
        default="", description="Check if this order is to discontinue KRYSTEXXA therapy"
    )

    stat_reason: str = Field(
        default="",
        description=(
            "Provide the reason for STAT (urgent) request .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PatientInformation(BaseModel):
    """Patient demographics and contact information"""

    name: str = Field(
        ...,
        description=(
            'Patient\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(..., description="Patient's date of birth")  # YYYY-MM-DD format

    sex: Literal["M", "F", "N/A", ""] = Field(..., description="Patient's sex")

    patient_address: str = Field(
        default="",
        description=(
            'Patient\'s mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    patient_phone: str = Field(
        default="",
        description=(
            'Patient\'s primary phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    weight: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Patient's weight; select units as lbs or kg"
    )

    height: str = Field(
        default="",
        description=(
            'Patient\'s height .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    patient_email: str = Field(
        default="",
        description=(
            'Patient\'s email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    allergies: str = Field(
        default="",
        description=(
            "List all known drug and other allergies .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PhysicianInformation(BaseModel):
    """Referring physician and practice details"""

    physician_name: str = Field(
        ...,
        description=(
            'Ordering physician\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    practice_name: str = Field(
        default="",
        description=(
            "Name of the physician's practice or clinic .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    physician_address: str = Field(
        default="",
        description=(
            'Physician or practice address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    office_contact: str = Field(
        ...,
        description=(
            "Primary office contact person for this order .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    physician_phone: str = Field(
        default="",
        description=(
            'Physician or practice phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            'Physician or practice fax number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_for_updates: str = Field(
        default="",
        description=(
            "Email address to receive updates about this order .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class KrystexxaOrder(BaseModel):
    """Medication order details and dosing"""

    krystexxa_order: str = Field(
        ...,
        description=(
            "Details of the KRYSTEXXA order (e.g., dosing selection) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    icd_10: str = Field(
        ...,
        description=(
            "Primary ICD-10 diagnosis code for this therapy .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dosing_8_mg_iv_every_2_weeks: BooleanLike = Field(
        default="", description="Check to select dosing of 8 mg IV every 2 weeks"
    )

    physician_signature: str = Field(
        ...,
        description=(
            'Signature of the ordering physician .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    order_date: str = Field(
        ..., description="Date the physician signed the order"
    )  # YYYY-MM-DD format


class DiagnosisRequiredDocumentation(BaseModel):
    """Required diagnosis and supporting documentation checklist"""

    chronic_gouty_arthropathy_with_tophus_tophi: BooleanLike = Field(
        default="",
        description="Check if diagnosis is chronic gouty arthropathy with tophus (tophi)",
    )

    chronic_gouty_arthropathy_without_tophus_tophi: BooleanLike = Field(
        default="",
        description="Check if diagnosis is chronic gouty arthropathy without tophus (tophi)",
    )

    other_diagnosis: str = Field(
        default="",
        description=(
            "Specify other diagnosis if not listed above .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    patient_demographics: BooleanLike = Field(
        default="", description="Check to confirm patient demographic information is attached"
    )

    insurance_card_information: BooleanLike = Field(
        default="", description="Check to confirm insurance card or information is attached"
    )

    clinical_progress_notes_supporting_dx: BooleanLike = Field(
        default="",
        description=(
            "Check to confirm clinical or progress notes supporting the diagnosis are attached"
        ),
    )

    current_medication_list_and_hp: BooleanLike = Field(
        default="",
        description="Check to confirm current medication list and history & physical are attached",
    )

    g6pd: BooleanLike = Field(
        default="", description="Check to confirm G6PD test results are provided"
    )

    baseline_uric_acid_greater_than_6_0mg_ds: BooleanLike = Field(
        default="",
        description=(
            "Check to confirm baseline uric acid level is greater than 6.0 mg/dL and documented"
        ),
    )


class InfusionLabInformation(BaseModel):
    """Infusion history and standing lab orders"""

    last_infusion_injection_date: str = Field(
        default="", description="Date of the patient's last infusion or injection"
    )  # YYYY-MM-DD format

    standing_lab_orders_cmp: BooleanLike = Field(
        default="", description="Check to order a standing CMP (Comprehensive Metabolic Panel)"
    )

    standing_lab_orders_cbc: BooleanLike = Field(
        default="", description="Check to order a standing CBC (Complete Blood Count)"
    )

    labs_to_be_drawn_by_infusion_center: BooleanLike = Field(
        default="", description="Check if labs are to be drawn by the infusion center"
    )

    frequency: str = Field(
        default="",
        description=(
            "Specify frequency for standing lab orders .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class NotesLocation(BaseModel):
    """Additional comments and selected infusion location"""

    notes_additional_comments: str = Field(
        default="",
        description=(
            "Additional notes or comments related to the order .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tulsa: BooleanLike = Field(default="", description="Select Tulsa as the infusion location")


class AllergyAsthmaImmunologyInfusionKrystexxaOrderForm(BaseModel):
    """Allergy, Asthma & Immunology Center, P.C.
    Infusion Services

    KRYSTEXXA® (PEGLOTICASE) ORDER FORM"""

    referral_type: ReferralType = Field(..., description="Referral Type")
    patient_information: PatientInformation = Field(..., description="Patient Information")
    physician_information: PhysicianInformation = Field(..., description="Physician Information")
    krystexxa_order: KrystexxaOrder = Field(..., description="Krystexxa Order")
    diagnosis__required_documentation: DiagnosisRequiredDocumentation = Field(
        ..., description="Diagnosis & Required Documentation"
    )
    infusion__lab_information: InfusionLabInformation = Field(
        ..., description="Infusion & Lab Information"
    )
    notes__location: NotesLocation = Field(..., description="Notes & Location")
