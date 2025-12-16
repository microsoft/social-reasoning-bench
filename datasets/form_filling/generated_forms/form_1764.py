from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OrderTypeSTATRequest(BaseModel):
    """Type of order being requested and STAT request reason"""

    new_referral: BooleanLike = Field(
        default="", description="Check if this is a new referral for ADAKVEO"
    )

    order_renewal: BooleanLike = Field(
        default="", description="Check if this is a renewal of an existing ADAKVEO order"
    )

    medication_order_change: BooleanLike = Field(
        default="",
        description="Check if this is a change to the existing ADAKVEO medication or order",
    )

    benefits_verification_only: BooleanLike = Field(
        default="", description="Check if the request is only for insurance benefits verification"
    )

    discontinuation_order: BooleanLike = Field(
        default="", description="Check if this order is to discontinue ADAKVEO therapy"
    )

    stat_request_reason: str = Field(
        default="",
        description=(
            "Clinical reason for STAT (urgent) request .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Location(BaseModel):
    """Infusion service location selection"""

    tulsa_location: BooleanLike = Field(
        default="", description="Check if the patient will receive infusion at the Tulsa location"
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

    address: str = Field(
        default="",
        description=(
            'Patient\'s full mailing address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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

    physician_address: str = Field(
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

    physician_phone: str = Field(
        default="",
        description=(
            'Physician office phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    physician_fax: str = Field(
        default="",
        description=(
            'Physician office fax number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    physician_email_for_updates: str = Field(
        default="",
        description=(
            "Email address to receive updates about this order .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ADAKVEOOrderDetails(BaseModel):
    """ADAKVEO order selection, dosing, and provider signature"""

    adakveo_order_selection: Literal[
        "Initial/Reloading Dosing and then Maintenance Dosing",
        "Maintenance Dosing: 5 mg/kg IV every 4 weeks",
        "N/A",
        "",
    ] = Field(..., description="Select the type of ADAKVEO order being requested")

    icd_10: str = Field(
        ...,
        description=(
            "Primary ICD-10 diagnosis code for this therapy .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    initial_reloading_dosing_then_maintenance: BooleanLike = Field(
        default="",
        description="Check if ordering initial/reloading dosing followed by maintenance dosing",
    )

    dose_5_mgkg_iv_day_0_2_weeks_every_4_weeks: BooleanLike = Field(
        default="",
        description="Check to specify dosing of 5 mg/kg IV on day 0, at 2 weeks, then every 4 weeks",
    )

    maintenance_dosing_5_mgkg_iv_every_4_weeks: BooleanLike = Field(
        default="", description="Check if ordering maintenance dosing of 5 mg/kg IV every 4 weeks"
    )

    physician_signature: str = Field(
        ...,
        description=(
            "Ordering physician's signature authorizing this order .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    order_date: str = Field(
        ..., description="Date the order is signed; order is valid for one year from this date"
    )  # YYYY-MM-DD format


class DiagnosisSTATReason(BaseModel):
    """Required diagnosis and STAT justification"""

    sickle_cell_disease_diagnosis: BooleanLike = Field(
        ..., description="Check if the required diagnosis is Sickle Cell Disease"
    )

    other_diagnosis: BooleanLike = Field(
        default="", description="Check if the required diagnosis is other than Sickle Cell Disease"
    )

    other_diagnosis_description: str = Field(
        default="",
        description=(
            "Describe the diagnosis if 'Other' is selected .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    stat_reason: str = Field(
        default="",
        description=(
            "Detailed explanation for requesting STAT processing .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RequiredDocumentationChecklist(BaseModel):
    """Supporting documents required with the order"""

    patient_demographics_documentation: BooleanLike = Field(
        default="", description="Check to confirm patient demographics documentation is attached"
    )

    insurance_card_information_documentation: BooleanLike = Field(
        default="",
        description="Check to confirm insurance card or insurance information is attached",
    )

    clinical_progress_notes_supporting_dx_documentation: BooleanLike = Field(
        default="",
        description=(
            "Check to confirm clinical or progress notes supporting the diagnosis are attached"
        ),
    )

    current_medication_list_hp_documentation: BooleanLike = Field(
        default="",
        description="Check to confirm current medication list and history & physical are attached",
    )


class InfusionLabOrders(BaseModel):
    """Last infusion date and standing lab orders"""

    last_infusion_injection_date: str = Field(
        default="", description="Date of the patient's most recent infusion or injection"
    )  # YYYY-MM-DD format

    cmp_lab_order: BooleanLike = Field(
        default="", description="Check to order a Comprehensive Metabolic Panel (CMP)"
    )

    cbc_lab_order: BooleanLike = Field(
        default="", description="Check to order a Complete Blood Count (CBC)"
    )

    labs_drawn_by_infusion_center: BooleanLike = Field(
        default="", description="Check if labs are to be drawn by the Infusion Center"
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

    notes_additional_comments: str = Field(
        default="",
        description=(
            "Additional notes or special instructions related to this order .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class AllergyAsthmaImmunologyCenterPcInfusionServicesAdakveoOrderForm(BaseModel):
    """
        Allergy, Asthma & Immunology Center, P.C.
    Infusion Services

    ADAKVEO ORDER FORM

        ''
    """

    order_type__stat_request: OrderTypeSTATRequest = Field(
        ..., description="Order Type & STAT Request"
    )
    location: Location = Field(..., description="Location")
    patient_information: PatientInformation = Field(..., description="Patient Information")
    physician_information: PhysicianInformation = Field(..., description="Physician Information")
    adakveo_order_details: ADAKVEOOrderDetails = Field(..., description="ADAKVEO Order Details")
    diagnosis__stat_reason: DiagnosisSTATReason = Field(..., description="Diagnosis & STAT Reason")
    required_documentation_checklist: RequiredDocumentationChecklist = Field(
        ..., description="Required Documentation Checklist"
    )
    infusion__lab_orders: InfusionLabOrders = Field(..., description="Infusion & Lab Orders")
    notes__additional_comments: NotesAdditionalComments = Field(
        ..., description="Notes / Additional Comments"
    )
