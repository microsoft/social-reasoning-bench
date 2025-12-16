from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ReferralType(BaseModel):
    """Type and urgency of referral/order"""

    new_referral: BooleanLike = Field(
        default="", description="Check if this is a new referral for KRYSTEXXA therapy"
    )

    order_renewal: BooleanLike = Field(
        default="", description="Check if this order is a renewal of an existing KRYSTEXXA therapy"
    )

    medication_order_change: BooleanLike = Field(
        default="", description="Check if this is a change to the existing medication or order"
    )

    benefits_verification_only: BooleanLike = Field(
        default="", description="Check if the request is only for insurance benefits verification"
    )

    discontinuation_order: BooleanLike = Field(
        default="", description="Check if this order is to discontinue KRYSTEXXA therapy"
    )

    stat_request: BooleanLike = Field(
        default="", description="Check if this is an urgent (STAT) request"
    )


class Location(BaseModel):
    """Selected infusion service location"""

    tulsa: BooleanLike = Field(
        default="", description="Check if the infusion location is Tulsa, Oklahoma"
    )


class PatientInformation(BaseModel):
    """Patient demographics and contact details"""

    name: str = Field(
        ...,
        description=(
            'Patient\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(..., description="Patient's date of birth")  # YYYY-MM-DD format

    sex_m: BooleanLike = Field(..., description="Check if the patient is male")

    sex_f: BooleanLike = Field(..., description="Check if the patient is female")

    address: str = Field(
        default="",
        description=(
            'Patient\'s mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        default="",
        description=(
            'Patient\'s primary phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    weight_lbs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Patient's weight in pounds"
    )

    weight_kg: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Patient's weight in kilograms"
    )

    height: str = Field(
        default="",
        description=(
            "Patient's height (include units, e.g., inches or cm) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
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
            'List all known patient allergies .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class PhysicianInformation(BaseModel):
    """Ordering physician and practice contact details"""

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

    address_physician: str = Field(
        default="",
        description=(
            'Ordering physician\'s office address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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

    phone_physician: str = Field(
        default="",
        description=(
            'Physician office phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            'Physician office fax number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
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
            "Specific KRYSTEXXA order details (e.g., regimen or instructions) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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
        default="", description="Check to select the standard dosing of 8 mg IV every 2 weeks"
    )

    physician_signature: str = Field(
        ...,
        description=(
            'Signature of the ordering physician .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_order_is_valid_for_one_year: str = Field(
        ..., description="Date the order is signed; order is valid for one year from this date"
    )  # YYYY-MM-DD format


class RequiredDiagnosisDocumentation(BaseModel):
    """Diagnosis selection, STAT reason, and required documentation checklist"""

    chronic_gouty_arthropathy_w_tophus_tophi: BooleanLike = Field(
        ...,
        description=(
            "Check if the required diagnosis is chronic gouty arthropathy with tophus (tophi)"
        ),
    )

    chronic_gouty_arthropathy_w_out_tophus_tophi: BooleanLike = Field(
        ...,
        description=(
            "Check if the required diagnosis is chronic gouty arthropathy without tophus (tophi)"
        ),
    )

    other_diagnosis: str = Field(
        default="",
        description=(
            "Specify another diagnosis if different from the listed options .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    stat_reason: str = Field(
        default="",
        description=(
            "Reason for requesting STAT (urgent) processing .If you cannot fill this, write "
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

    current_medication_list_and_h_p: BooleanLike = Field(
        default="",
        description="Check to confirm current medication list and history & physical are attached",
    )

    g6pd: BooleanLike = Field(
        default="", description="Check to confirm G6PD test results are attached"
    )

    baseline_uric_acid_gt_6_0mg_ds: BooleanLike = Field(
        default="",
        description="Check to confirm baseline uric acid level > 6.0 mg/dL documentation is attached",
    )

    last_infusion_injection_date: str = Field(
        default="", description="Date of the patient's last infusion or injection"
    )  # YYYY-MM-DD format


class StandingLabOrders(BaseModel):
    """Laboratory orders and frequency"""

    cmp: BooleanLike = Field(
        default="", description="Check to order a Comprehensive Metabolic Panel (CMP)"
    )

    cbc: BooleanLike = Field(default="", description="Check to order a Complete Blood Count (CBC)")

    labs_to_be_drawn_by_infusion_center: BooleanLike = Field(
        default="", description="Check if labs will be drawn by the infusion center"
    )

    frequency: str = Field(
        default="",
        description=(
            "Specify the frequency for standing lab orders .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalComments(BaseModel):
    """Free-text notes or additional comments"""

    notes_additional_comments: str = Field(
        default="",
        description=(
            "Additional notes or comments related to this order .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AllergyAsthmaImmunologyInfusionKrystexxaOrderForm(BaseModel):
    """
        Allergy, Asthma & Immunology Center, P.C.
    Infusion Services
    KRYSTEXXA® (PEGLOTICASE) ORDER FORM

        ''
    """

    referral_type: ReferralType = Field(..., description="Referral Type")
    location: Location = Field(..., description="Location")
    patient_information: PatientInformation = Field(..., description="Patient Information")
    physician_information: PhysicianInformation = Field(..., description="Physician Information")
    krystexxa_order: KrystexxaOrder = Field(..., description="Krystexxa Order")
    required_diagnosis__documentation: RequiredDiagnosisDocumentation = Field(
        ..., description="Required Diagnosis & Documentation"
    )
    standing_lab_orders: StandingLabOrders = Field(..., description="Standing Lab Orders")
    additional_comments: AdditionalComments = Field(..., description="Additional Comments")
