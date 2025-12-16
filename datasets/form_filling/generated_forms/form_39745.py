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
    """Type and urgency of the Nucala order request"""

    stat_request: BooleanLike = Field(
        default="", description="Check if this is a STAT (urgent) request"
    )

    new_referral: BooleanLike = Field(default="", description="Check if this is a new referral")

    order_renewal: BooleanLike = Field(default="", description="Check if this is an order renewal")

    medication_order_change: BooleanLike = Field(
        default="", description="Check if this is a change to the current medication or order"
    )

    benefits_verification_only: BooleanLike = Field(
        default="", description="Check if this request is for benefits verification only"
    )

    discontinuation_order: BooleanLike = Field(
        default="", description="Check if this is an order to discontinue therapy"
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

    sex_m: BooleanLike = Field(default="", description="Check if patient is male")

    sex_f: BooleanLike = Field(default="", description="Check if patient is female")

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


class NucalaOrder(BaseModel):
    """Medication order details and dosing"""

    nucala_order: str = Field(
        ...,
        description=(
            "Indicates that this is a NUCALA order; details selected below .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    icd_10: str = Field(
        ...,
        description=(
            "Primary ICD-10 diagnosis code for this order .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dosing_100mg_q4w: BooleanLike = Field(
        default="", description="Select this dosing regimen: 100 mg SC once every 4 weeks"
    )

    dosing_300mg_q4w: BooleanLike = Field(
        default="",
        description=(
            "Select this dosing regimen: 300 mg as three 100‑mg SC injections once every 4 weeks"
        ),
    )

    physician_signature: str = Field(
        ...,
        description=(
            'Signature of the ordering physician .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the physician signed the order")  # YYYY-MM-DD format


class RequiredDiagnosis(BaseModel):
    """Diagnosis information and STAT justification"""

    severe_asthma: BooleanLike = Field(
        default="", description="Check if the required diagnosis is severe asthma"
    )

    eosinophilic_asthma: BooleanLike = Field(
        default="", description="Check if the required diagnosis is eosinophilic asthma"
    )

    eosinophilic_granulomatosis_with_polyangiitis: BooleanLike = Field(
        default="",
        description=(
            "Check if the required diagnosis is eosinophilic granulomatosis with polyangiitis"
        ),
    )

    other_diagnosis: str = Field(
        default="",
        description=(
            "Specify other diagnosis if not listed above .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    stat_reason: str = Field(
        ...,
        description=(
            "Clinical reason for STAT (urgent) request .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class RequiredDocumentationChecklist(BaseModel):
    """Supporting documents required with the order"""

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

    absolute_eosinophil_count: BooleanLike = Field(
        default="",
        description=(
            "Check to confirm documentation of required absolute eosinophil count is attached"
        ),
    )

    anca_positive_within_6_months: BooleanLike = Field(
        default="",
        description="Check to confirm ANCA positive result within 6 months is documented",
    )

    last_infusion_injection_date: str = Field(
        default="", description="Date of the patient's last infusion or injection"
    )  # YYYY-MM-DD format


class StandingLabOrders(BaseModel):
    """Laboratory orders and frequency"""

    cmp: BooleanLike = Field(
        default="", description="Check to order a comprehensive metabolic panel (CMP)"
    )

    cbc: BooleanLike = Field(default="", description="Check to order a complete blood count (CBC)")

    labs_to_be_drawn_by_infusion_center: BooleanLike = Field(
        default="", description="Check if labs are to be drawn by the infusion center"
    )

    lab_frequency: str = Field(
        default="",
        description=(
            "Specify how often labs should be drawn .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class NotesAdditionalComments(BaseModel):
    """Free-text notes and additional comments"""

    notes_additional_comments_line_1: str = Field(
        default="",
        description=(
            "First line for additional notes or comments .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    notes_additional_comments_line_2: str = Field(
        default="",
        description=(
            "Second line for additional notes or comments .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Location(BaseModel):
    """Infusion center location selection"""

    tulsa_location: BooleanLike = Field(
        default="", description="Check if the Tulsa location is selected"
    )


class AllergyAsthmaImmunologyInfusionMepolizumabOrderForm(BaseModel):
    """
        Allergy, Asthma & Immunology Center, P.C.
    Infusion Services

    NUCALA® (MEPOLIZUMAB) ORDER FORM

        ''
    """

    request_type: RequestType = Field(..., description="Request Type")
    patient_information: PatientInformation = Field(..., description="Patient Information")
    physician_information: PhysicianInformation = Field(..., description="Physician Information")
    nucala_order: NucalaOrder = Field(..., description="Nucala Order")
    required_diagnosis: RequiredDiagnosis = Field(..., description="Required Diagnosis")
    required_documentation_checklist: RequiredDocumentationChecklist = Field(
        ..., description="Required Documentation Checklist"
    )
    standing_lab_orders: StandingLabOrders = Field(..., description="Standing Lab Orders")
    notes__additional_comments: NotesAdditionalComments = Field(
        ..., description="Notes / Additional Comments"
    )
    location: Location = Field(..., description="Location")
