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
    """Type and urgency of the referral/order"""

    stat_request: BooleanLike = Field(
        default="", description="Check if this is a STAT (urgent) request"
    )

    reason_must_be_provided_below: str = Field(
        default="",
        description=(
            'Explanation for STAT request .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    new_referral: BooleanLike = Field(default="", description="Check if this is a new referral")

    order_renewal: BooleanLike = Field(default="", description="Check if this is an order renewal")

    medication_order_change: BooleanLike = Field(
        default="", description="Check if this is a change to the medication or order"
    )

    benefits_verification_only: BooleanLike = Field(
        default="", description="Check if only benefits verification is requested"
    )

    discontinuation_order: BooleanLike = Field(
        default="", description="Check if this is an order to discontinue therapy"
    )

    stat_reason: str = Field(
        default="",
        description=(
            "Detailed reason for requesting STAT processing .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
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

    sex: Literal["M", "F", "N/A", ""] = Field(default="", description="Patient's sex")

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

    weight: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Patient's weight; specify units as lbs or kg"
    )

    height: str = Field(
        default="",
        description=(
            'Patient\'s height .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
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
            'Physician or practice mailing address .If you cannot fill this, write "N/A". '
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


class KrystexxaOrderDetails(BaseModel):
    """Medication order specifics and authorization"""

    krystexxa_order: str = Field(
        ...,
        description=(
            'Details of the KRYSTEXXA order .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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
        default="", description="Select this dosing regimen if appropriate"
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


class DiagnosisRequiredDocumentation(BaseModel):
    """Required diagnosis and supporting documents"""

    chronic_gouty_arthropathy_w_tophus_tophi: BooleanLike = Field(
        default="", description="Check if diagnosis is chronic gouty arthropathy with tophus"
    )

    chronic_gouty_arthropathy_w_out_tophus_tophi: BooleanLike = Field(
        default="", description="Check if diagnosis is chronic gouty arthropathy without tophus"
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
        default="", description="Indicate that patient demographic information is included"
    )

    insurance_card_information: BooleanLike = Field(
        default="",
        description="Indicate that a copy of the insurance card or insurance information is included",
    )

    clinical_progress_notes_supporting_dx: BooleanLike = Field(
        default="",
        description="Indicate that clinical or progress notes supporting the diagnosis are included",
    )

    current_medication_list_and_hp: BooleanLike = Field(
        default="",
        description="Indicate that the current medication list and history & physical are included",
    )

    g6pd: BooleanLike = Field(
        default="", description="Indicate that G6PD testing documentation is included"
    )

    baseline_uric_acid_greater_than_6_0mg_ds: BooleanLike = Field(
        default="",
        description="Indicate that baseline uric acid level > 6.0 mg/dL documentation is included",
    )

    last_infusion_injection_date: str = Field(
        default="", description="Date of the patient's last infusion or injection"
    )  # YYYY-MM-DD format


class StandingLabOrders(BaseModel):
    """Laboratory orders related to the infusion"""

    cmp: BooleanLike = Field(
        default="", description="Check if CMP (Comprehensive Metabolic Panel) is ordered"
    )

    cbc: BooleanLike = Field(
        default="", description="Check if CBC (Complete Blood Count) is ordered"
    )

    labs_to_be_drawn_by_infusion_center: BooleanLike = Field(
        default="", description="Check if labs are to be drawn by the infusion center"
    )

    frequency: str = Field(
        default="",
        description=(
            "Specify frequency for lab draws or treatments .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class NotesandLocation(BaseModel):
    """Additional comments and infusion location"""

    notes_additional_comments: str = Field(
        default="",
        description=(
            "Any additional notes or special instructions .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    tulsa: BooleanLike = Field(default="", description="Select Tulsa as the infusion location")


class KrystexxaInfusionOrderForm(BaseModel):
    """Allergy, Asthma & Immunology Center, P.C.
    Infusion Services

    KRYSTEXXA® (PEGLOTICASE) ORDER FORM"""

    request_type: RequestType = Field(..., description="Request Type")
    patient_information: PatientInformation = Field(..., description="Patient Information")
    physician_information: PhysicianInformation = Field(..., description="Physician Information")
    krystexxa_order_details: KrystexxaOrderDetails = Field(
        ..., description="Krystexxa Order Details"
    )
    diagnosis__required_documentation: DiagnosisRequiredDocumentation = Field(
        ..., description="Diagnosis & Required Documentation"
    )
    standing_lab_orders: StandingLabOrders = Field(..., description="Standing Lab Orders")
    notes_and_location: NotesandLocation = Field(..., description="Notes and Location")
