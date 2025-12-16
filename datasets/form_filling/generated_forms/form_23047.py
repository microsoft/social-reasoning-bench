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
    """Type of request and STAT indication"""

    new_referral: BooleanLike = Field(
        default="", description="Check if this is a new referral for Lemtrada infusion services"
    )

    order_renewal: BooleanLike = Field(
        default="", description="Check if this order is a renewal of a previous Lemtrada order"
    )

    medication_order_change: BooleanLike = Field(
        default="", description="Check if this is a change to an existing medication or order"
    )

    benefits_verification_only: BooleanLike = Field(
        default="", description="Check if the request is only for insurance benefits verification"
    )

    discontinuation_order: BooleanLike = Field(
        default="", description="Check if this order is to discontinue Lemtrada therapy"
    )

    stat_request: BooleanLike = Field(
        default="", description="Check if this is an urgent STAT request"
    )

    reason_must_be_provided_below: str = Field(
        ...,
        description=(
            "Provide the clinical reason for the STAT request .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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

    email_for_updates: str = Field(
        default="",
        description=(
            "Email address to receive updates about this order .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LEMTRADAOrderDetails(BaseModel):
    """LEMTRADA regimen, diagnosis coding, and order authorization"""

    lemtrada_order: Literal[
        "First Course: 12mg/day on 5 consecutive days",
        "Maintenance Dosing: 12mg/day on 3 consecutive days every 12 months.",
        "N/A",
        "",
    ] = Field(..., description="Select the Lemtrada dosing regimen being ordered")

    first_course_12mg_day_on_5_consecutive_days: BooleanLike = Field(
        default="",
        description="Check if ordering the first course: 12 mg/day for 5 consecutive days",
    )

    maintenance_dosing_12mg_day_on_3_consecutive_days_every_12_months: BooleanLike = Field(
        default="",
        description=(
            "Check if ordering maintenance dosing: 12 mg/day for 3 consecutive days every 12 months"
        ),
    )

    icd_10: str = Field(
        ...,
        description=(
            "Primary ICD-10 diagnosis code supporting this order .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    okay_to_infuse_at_multiple_locations: BooleanLike = Field(
        default="", description="Indicate if infusions may be administered at multiple locations"
    )

    okay_to_split_infusions: BooleanLike = Field(
        default="", description="Indicate if infusions may be split across sessions per protocol"
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


class InfusionLocation(BaseModel):
    """Preferred infusion site"""

    tulsa: BooleanLike = Field(
        default="", description="Check if Tulsa is the selected infusion location"
    )


class RequiredDiagnosisSTATReason(BaseModel):
    """Diagnosis selection and STAT justification"""

    relapsing_multiple_sclerosis: BooleanLike = Field(
        ..., description="Check if the required diagnosis is relapsing multiple sclerosis"
    )

    other_diagnosis: str = Field(
        default="",
        description=(
            "Specify other diagnosis if not relapsing multiple sclerosis .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    stat_reason: str = Field(
        ...,
        description=(
            "Explain the reason for the STAT request .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class RequiredDocumentationChecklist(BaseModel):
    """Supporting documents and test results to accompany order"""

    patient_demographics: BooleanLike = Field(
        default="", description="Indicate that patient demographic information is attached"
    )

    insurance_card_information: BooleanLike = Field(
        default="",
        description="Indicate that a copy of the insurance card or insurance information is attached",
    )

    clinical_progress_notes_supporting_dx: BooleanLike = Field(
        default="",
        description="Indicate that clinical or progress notes supporting the diagnosis are attached",
    )

    current_medication_list_and_h_p: BooleanLike = Field(
        default="",
        description="Indicate that the current medication list and history & physical are attached",
    )

    hiv_test_results: BooleanLike = Field(
        default="", description="Indicate that HIV test results are attached"
    )

    varicella_zoster_antibodies: BooleanLike = Field(
        default="", description="Indicate that varicella zoster antibody results are attached"
    )

    tb_results_if_available_if_positive_need_negative_chest_xray_and_negative_tspot: BooleanLike = (
        Field(
            default="",
            description=(
                "Indicate that TB test results (and follow-up imaging/tests if positive) are "
                "attached"
            ),
        )
    )

    last_infusion_injection_date: str = Field(
        default="", description="Date of the patient's last infusion or injection"
    )  # YYYY-MM-DD format


class StandingLabOrders(BaseModel):
    """Ongoing lab orders and frequency"""

    cmp: BooleanLike = Field(
        default="", description="Check to order a Comprehensive Metabolic Panel (CMP)"
    )

    cbc: BooleanLike = Field(default="", description="Check to order a Complete Blood Count (CBC)")

    labs_to_be_drawn_by_infusion_center: BooleanLike = Field(
        default="", description="Indicate if the listed labs should be drawn by the infusion center"
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
    """Free-text notes and additional information"""

    notes_additional_comments_line_1: str = Field(
        default="",
        description=(
            "First line for any additional notes or comments .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    notes_additional_comments_line_2: str = Field(
        default="",
        description=(
            "Second line for any additional notes or comments .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AllergyAsthmaImmunologyInfusionLemtradaOrderForm(BaseModel):
    """
        Allergy, Asthma & Immunology Center, P.C.
    Infusion Services
    LEMTRADA® (ALAMTUZUMAB) ORDER FORM

        ''
    """

    referral_type: ReferralType = Field(..., description="Referral Type")
    patient_information: PatientInformation = Field(..., description="Patient Information")
    physician_information: PhysicianInformation = Field(..., description="Physician Information")
    lemtrada_order_details: LEMTRADAOrderDetails = Field(..., description="LEMTRADA Order Details")
    infusion_location: InfusionLocation = Field(..., description="Infusion Location")
    required_diagnosis__stat_reason: RequiredDiagnosisSTATReason = Field(
        ..., description="Required Diagnosis / STAT Reason"
    )
    required_documentation_checklist: RequiredDocumentationChecklist = Field(
        ..., description="Required Documentation Checklist"
    )
    standing_lab_orders: StandingLabOrders = Field(..., description="Standing Lab Orders")
    notes__additional_comments: NotesAdditionalComments = Field(
        ..., description="Notes / Additional Comments"
    )
