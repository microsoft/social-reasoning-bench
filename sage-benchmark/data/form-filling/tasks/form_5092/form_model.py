from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RequestType(BaseModel):
    """Type of referral or order request"""

    new_referral: BooleanLike = Field(
        default="", description="Check if this is a new referral for KRYSTEXXA therapy"
    )

    order_renewal: BooleanLike = Field(
        default="", description="Check if this is a renewal of a previous KRYSTEXXA order"
    )

    medication_order_change: BooleanLike = Field(
        default="", description="Check if this is a change to an existing medication or order"
    )

    benefits_verification_only: BooleanLike = Field(
        default="", description="Check if the request is only for insurance benefits verification"
    )

    discontinuation_order: BooleanLike = Field(
        default="", description="Check if this order is to discontinue KRYSTEXXA therapy"
    )


class Location(BaseModel):
    """Infusion service location selection"""

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

    sex_m: BooleanLike = Field(..., description="Check if the patient's sex is male")

    sex_f: BooleanLike = Field(..., description="Check if the patient's sex is female")

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
            "List all known drug and other allergies .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PhysicianInformation(BaseModel):
    """Referring/ordering physician details"""

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

    phone_physician: str = Field(
        default="",
        description=(
            "Ordering physician's office phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    fax_physician: str = Field(
        default="",
        description=(
            "Ordering physician's office fax number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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

    email_for_updates: str = Field(
        default="",
        description=(
            "Email address to receive updates about this order .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class KRYSTEXXAOrder(BaseModel):
    """Medication order details and authorization"""

    krystexxa_order_selection: Literal["Dosing: 8 mg IV every 2 weeks", "N/A", ""] = Field(
        ..., description="Selected KRYSTEXXA order regimen"
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
        ..., description="Check to order KRYSTEXXA 8 mg IV every 2 weeks"
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
        ..., description="Date the order is signed; valid for one year from this date"
    )  # YYYY-MM-DD format


class RequiredDiagnosis(BaseModel):
    """Diagnosis selection for KRYSTEXXA therapy"""

    chronic_gouty_arthropathy_w_tophus_tophi: BooleanLike = Field(
        ..., description="Check if diagnosis is chronic gouty arthropathy with tophus (tophi)"
    )

    chronic_gouty_arthropathy_w_out_tophus_tophi: BooleanLike = Field(
        ..., description="Check if diagnosis is chronic gouty arthropathy without tophus (tophi)"
    )

    other_diagnosis_line_1: str = Field(
        default="",
        description=(
            "First line of other diagnosis description if not listed above .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    other_diagnosis_line_2: str = Field(
        default="",
        description=(
            "Second line of other diagnosis description if not listed above .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class STATReason(BaseModel):
    """Reason for STAT (urgent) request"""

    stat_reason: str = Field(
        ...,
        description=(
            'Reason for STAT (urgent) request .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class RequiredDocumentationChecklist(BaseModel):
    """Supporting documents required with the order"""

    patient_demographics: BooleanLike = Field(
        default="", description="Check when patient demographic information is attached"
    )

    insurance_card_information: BooleanLike = Field(
        default="",
        description="Check when a copy of the insurance card or insurance information is attached",
    )

    clinical_progress_notes_supporting_dx: BooleanLike = Field(
        default="",
        description="Check when clinical or progress notes supporting the diagnosis are attached",
    )

    current_medication_list_and_hp: BooleanLike = Field(
        default="",
        description="Check when current medication list and history & physical are attached",
    )

    g6pd: BooleanLike = Field(default="", description="Check when G6PD test results are attached")

    baseline_uric_acid_greater_than_6_0mg_ds: BooleanLike = Field(
        default="",
        description="Check when baseline uric acid level > 6.0 mg/dL documentation is attached",
    )

    last_infusion_injection_date: str = Field(
        default="", description="Date of the patient's last infusion or injection"
    )  # YYYY-MM-DD format


class StandingLabOrders(BaseModel):
    """Laboratory orders associated with infusion"""

    cmp: BooleanLike = Field(
        default="", description="Check to order a Comprehensive Metabolic Panel (CMP)"
    )

    cbc: BooleanLike = Field(default="", description="Check to order a Complete Blood Count (CBC)")

    labs_to_be_drawn_by_infusion_center_frequency: str = Field(
        default="",
        description=(
            "Specify how often labs should be drawn by the infusion center .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class Notes(BaseModel):
    """Additional comments from provider"""

    notes_additional_comments: str = Field(
        default="",
        description=(
            "Any additional notes or special instructions .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AllergyAsthmaImmunologyInfusionKrystexxaOrderForm(BaseModel):
    """Allergy, Asthma & Immunology Center, P.C.
    Infusion Services

    KRYSTEXXA® (PEGLOTICASE) ORDER FORM"""

    request_type: RequestType = Field(..., description="Request Type")
    location: Location = Field(..., description="Location")
    patient_information: PatientInformation = Field(..., description="Patient Information")
    physician_information: PhysicianInformation = Field(..., description="Physician Information")
    krystexxa_order: KRYSTEXXAOrder = Field(..., description="KRYSTEXXA Order")
    required_diagnosis: RequiredDiagnosis = Field(..., description="Required Diagnosis")
    stat_reason: STATReason = Field(..., description="STAT Reason")
    required_documentation_checklist: RequiredDocumentationChecklist = Field(
        ..., description="Required Documentation Checklist"
    )
    standing_lab_orders: StandingLabOrders = Field(..., description="Standing Lab Orders")
    notes: Notes = Field(..., description="Notes")
