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
        default="", description="Check if this is a new referral for Injectafer treatment"
    )

    order_renewal: BooleanLike = Field(
        default="", description="Check if this is a renewal of a previous Injectafer order"
    )

    medication_order_change: BooleanLike = Field(
        default="", description="Check if this request is to change an existing medication or order"
    )

    benefits_verification_only: BooleanLike = Field(
        default="", description="Check if this request is only for insurance benefits verification"
    )

    discontinuation_order: BooleanLike = Field(
        default="", description="Check if this order is to discontinue Injectafer treatment"
    )


class PatientInformation(BaseModel):
    """Patient demographics and clinical basics"""

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
            "Patient's height (include units, e.g., ft/in or cm) .If you cannot fill this, "
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


class InjectaferOrder(BaseModel):
    """Injectafer order details and dosing"""

    injectafer_order: str = Field(
        ...,
        description=(
            "Indicates that this section is for the Injectafer order; select appropriate "
            'dosing below .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    icd_10: str = Field(
        ...,
        description=(
            "Primary ICD-10 diagnosis code supporting Injectafer use .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    dosing_750_mg_iv: BooleanLike = Field(
        default="",
        description=(
            "Select this dosing regimen for patients 50 kg or more: 750 mg IV on day 0 and "
            "day 7 or later"
        ),
    )

    dosing_15mg_kg_iv: BooleanLike = Field(
        default="",
        description=(
            "Select this dosing regimen for patients under 50 kg: 15 mg/kg IV on day 0 and "
            "day 7 or later"
        ),
    )

    physician_signature: str = Field(
        ...,
        description=(
            "Ordering physician's signature authorizing this order .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_order_is_valid_for_one_year: str = Field(
        ..., description="Date the order is signed; order is valid for one year from this date"
    )  # YYYY-MM-DD format


class Diagnosis(BaseModel):
    """Required diagnosis information for treatment"""

    iron_deficiency_anemia: BooleanLike = Field(
        default="", description="Check if the required diagnosis is iron deficiency anemia"
    )

    other_diagnosis: str = Field(
        default="",
        description=(
            "Specify other required diagnosis if not iron deficiency anemia .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    secondary_causal_diagnosis_code: str = Field(
        default="",
        description=(
            "Secondary or causal diagnosis code related to the primary condition .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class RequiredDocumentationChecklist(BaseModel):
    """Supporting documents that must accompany the order"""

    patient_demographics: BooleanLike = Field(
        default="", description="Check to confirm patient demographic information is included"
    )

    insurance_card_information: BooleanLike = Field(
        default="",
        description=(
            "Check to confirm a copy of the patient's insurance card or information is included"
        ),
    )

    clinical_progress_notes_supporting_dx: BooleanLike = Field(
        default="",
        description=(
            "Check to confirm clinical or progress notes supporting the diagnosis are included"
        ),
    )

    current_medication_list_and_hp: BooleanLike = Field(
        default="",
        description="Check to confirm current medication list and history & physical are included",
    )

    ferritin_within_past_3_months: BooleanLike = Field(
        default="",
        description="Check to confirm ferritin lab results within the past 3 months are included",
    )

    last_infusion_injection_date: str = Field(
        default="", description="Date of the patient's most recent infusion or injection"
    )  # YYYY-MM-DD format


class StandingLabOrders(BaseModel):
    """Laboratory orders associated with the infusion"""

    cmp: BooleanLike = Field(
        default="", description="Check to order a Comprehensive Metabolic Panel (CMP)"
    )

    cbc: BooleanLike = Field(default="", description="Check to order a Complete Blood Count (CBC)")

    labs_to_be_drawn_by_infusion_center: BooleanLike = Field(
        default="", description="Check if the listed labs should be drawn by the Infusion Center"
    )

    frequency: str = Field(
        default="",
        description=(
            "Specify how often labs should be drawn .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class NotesandLocation(BaseModel):
    """Additional comments and infusion location selection"""

    notes_additional_comments: str = Field(
        default="",
        description=(
            "Additional notes or comments related to this order .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tulsa: BooleanLike = Field(default="", description="Select Tulsa as the infusion location")


class InjectaferferricCarboxyMaltosieInjectionOrderForm(BaseModel):
    """INJECTAFER® (FERRIC CARBOXY MALTOSIE INJECTION) ORDER FORM"""

    request_type: RequestType = Field(..., description="Request Type")
    patient_information: PatientInformation = Field(..., description="Patient Information")
    physician_information: PhysicianInformation = Field(..., description="Physician Information")
    injectafer_order: InjectaferOrder = Field(..., description="Injectafer Order")
    diagnosis: Diagnosis = Field(..., description="Diagnosis")
    required_documentation_checklist: RequiredDocumentationChecklist = Field(
        ..., description="Required Documentation Checklist"
    )
    standing_lab_orders: StandingLabOrders = Field(..., description="Standing Lab Orders")
    notes_and_location: NotesandLocation = Field(..., description="Notes and Location")
