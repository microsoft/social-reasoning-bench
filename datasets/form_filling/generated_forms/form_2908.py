from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PatientInformation(BaseModel):
    """Basic patient demographics and contact details"""

    patient_name: str = Field(
        ...,
        description=(
            'Patient\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(..., description="Patient's date of birth")  # YYYY-MM-DD format

    phone: str = Field(
        ...,
        description=(
            'Primary phone number for the patient .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    gender_m: BooleanLike = Field(..., description="Select if the patient's gender is male")

    gender_f: BooleanLike = Field(..., description="Select if the patient's gender is female")

    patient_address: str = Field(
        ...,
        description=(
            'Patient\'s full mailing address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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

    insurance: str = Field(
        ...,
        description=(
            "Primary insurance provider name or plan .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalInformationNeeded(BaseModel):
    """Documents and supplemental information to be faxed"""

    fax_front_back_of_insurance_card: BooleanLike = Field(
        default="",
        description="Indicate that copies of the front and back of the insurance card are faxed",
    )

    fax_clinical_progress_notes: BooleanLike = Field(
        default="", description="Indicate that clinical or progress notes are faxed"
    )

    fax_labs: BooleanLike = Field(default="", description="Indicate that lab results are faxed")

    fax_patient_demographics: BooleanLike = Field(
        default="", description="Indicate that patient demographic information is faxed"
    )

    fax_current_medication_list: BooleanLike = Field(
        default="", description="Indicate that the current medication list is faxed"
    )

    fax_tb_and_hep_b_results: BooleanLike = Field(
        default="", description="Indicate that TB and Hepatitis B test results are faxed"
    )


class DiagnosisandClinicalInformation(BaseModel):
    """Diagnosis codes and relevant clinical background"""

    diagnosis_icd10_m800: BooleanLike = Field(
        default="",
        description=(
            "Select if diagnosis is M80.0 Age-related osteoporosis with current "
            "pathological fracture"
        ),
    )

    diagnosis_icd10_m810: BooleanLike = Field(
        default="",
        description=(
            "Select if diagnosis is M81.0 Age-related osteoporosis without current "
            "pathological fracture"
        ),
    )

    diagnosis_icd10_m818: BooleanLike = Field(
        default="",
        description=(
            "Select if diagnosis is M81.8 Other osteoporosis without current pathological fracture"
        ),
    )

    diagnosis_icd10_other: BooleanLike = Field(
        default="", description="Select if diagnosis is another ICD-10 code not listed"
    )

    other_code: str = Field(
        default="",
        description=(
            'ICD-10 code for other diagnosis .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    other_description: str = Field(
        default="",
        description=(
            'Description of the other diagnosis .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    new_therapy_induction: BooleanLike = Field(
        default="", description="Indicate that this is a new therapy induction"
    )

    therapy_change: BooleanLike = Field(
        default="", description="Indicate that this order is for a change in therapy"
    )

    therapy_continuation: BooleanLike = Field(
        default="", description="Indicate that this order is for continuation of existing therapy"
    )

    patient_weight_lbs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Patient's weight in pounds"
    )

    patient_weight_kg: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Patient's weight in kilograms"
    )

    patient_height_in: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Patient's height in inches"
    )

    patient_height_cm: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Patient's height in centimeters"
    )

    allergies: str = Field(
        default="",
        description=(
            "List all known drug and other allergies .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    therapies_tried_and_failed: str = Field(
        default="",
        description=(
            "List prior osteoporosis therapies tried and failed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tb_test_date: str = Field(
        default="", description="Date of the most recent TB test"
    )  # YYYY-MM-DD format

    tb_test_results: str = Field(
        default="",
        description=(
            "Result of the TB test (e.g., positive, negative, indeterminate) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    hep_b_test_date: str = Field(
        default="", description="Date of the most recent Hepatitis B test"
    )  # YYYY-MM-DD format

    hep_b_test_results: str = Field(
        default="",
        description=(
            'Result of the Hepatitis B test .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    calcium_vitd_yes: BooleanLike = Field(
        default="",
        description="Select if the patient is currently taking a Calcium/Vitamin D supplement",
    )

    calcium_vitd_no: BooleanLike = Field(
        default="",
        description="Select if the patient is not currently taking a Calcium/Vitamin D supplement",
    )

    date_last_calcium_vitd: str = Field(
        default="", description="Date the patient last took a Calcium/Vitamin D supplement"
    )  # YYYY-MM-DD format

    history_of_fractures_yes: BooleanLike = Field(
        default="", description="Select if the patient has a history of fractures"
    )

    history_of_fractures_no: BooleanLike = Field(
        default="", description="Select if the patient does not have a history of fractures"
    )

    date_last_dexa_scan: str = Field(
        default="", description="Date of the patient's most recent DEXA scan"
    )  # YYYY-MM-DD format

    clinical_note_last_dexa_yes: BooleanLike = Field(
        default="", description="Select if a clinical note for the last DEXA scan is attached"
    )

    clinical_note_last_dexa_no: BooleanLike = Field(
        default="", description="Select if a clinical note for the last DEXA scan is not attached"
    )


class LabOrders(BaseModel):
    """Laboratory tests requested and who will perform them"""

    cbc: BooleanLike = Field(default="", description="Order a Complete Blood Count (CBC)")

    cmp: BooleanLike = Field(default="", description="Order a Comprehensive Metabolic Panel (CMP)")

    esr: BooleanLike = Field(
        default="", description="Order an Erythrocyte Sedimentation Rate (ESR)"
    )

    crp: BooleanLike = Field(default="", description="Order a C-reactive protein (CRP) test")

    hbsag: BooleanLike = Field(
        default="", description="Order Hepatitis B surface antigen (HBsAg) test"
    )

    hbsab: BooleanLike = Field(
        default="", description="Order Hepatitis B surface antibody (HBsAB) test"
    )

    hbcab: BooleanLike = Field(
        default="", description="Order Hepatitis B core antibody (HBcAB) test"
    )

    quantiferon_gold: BooleanLike = Field(default="", description="Order Quantiferon Gold TB test")

    lab_orders_other: str = Field(
        default="",
        description=(
            'Specify any additional lab orders .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    lab_orders_oklahoma_infusion_services: BooleanLike = Field(
        default="", description="Select if Oklahoma Infusion Services will perform the lab orders"
    )

    lab_orders_referring_provider: BooleanLike = Field(
        default="", description="Select if the referring provider will perform the lab orders"
    )


class PrescriptionInformation(BaseModel):
    """Evenity prescription details"""

    evenity: BooleanLike = Field(
        ...,
        description="Indicate that Evenity is being prescribed per the listed dose and frequency",
    )


class PreMedicationOrders(BaseModel):
    """Medications to be given prior to infusion"""

    pre_med_solu_cortef_50_100mg_sivp: BooleanLike = Field(
        default="", description="Order Solu-Cortef 50–100 mg SIVP as pre-medication"
    )

    pre_med_benadryl_25mg_po_prn: BooleanLike = Field(
        default="", description="Order Benadryl 25 mg PO as needed as pre-medication"
    )

    pre_med_tylenol_500_1000mg_po_prn: BooleanLike = Field(
        default="", description="Order Tylenol 500–1000 mg PO as needed as pre-medication"
    )

    pre_med_other: str = Field(
        default="",
        description=(
            "Specify any other pre-medication orders .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class StandingOrdersforAdverseReactions(BaseModel):
    """Orders to follow in case of infusion-related adverse reactions"""

    standing_stop_infusion_ns_bolus: BooleanLike = Field(
        default="",
        description=(
            "Standing order to stop infusion and start normal saline bolus for adverse reactions"
        ),
    )

    standing_notify_supervising_physician: BooleanLike = Field(
        default="",
        description=(
            "Standing order to notify supervising physician and ordering provider for "
            "adverse reactions"
        ),
    )

    standing_solu_cortef_100mg_sivp: BooleanLike = Field(
        default="",
        description="Standing order for Solu-Cortef 100 mg SIVP for signs of adverse reaction",
    )

    standing_benadryl_25mg_sivp: BooleanLike = Field(
        default="",
        description="Standing order for Benadryl 25 mg SIVP for hives or bronchial inflammation",
    )

    standing_epi_1_1000_1ml: BooleanLike = Field(
        default="",
        description="Standing order for epinephrine 1:1000 1 mL IM, IV, or SQ for anaphylaxis",
    )

    standing_oxygen_2_5l_nc: BooleanLike = Field(
        default="", description="Standing order for oxygen 2–5 L via nasal cannula"
    )

    standing_albuterol_2_5mg_inhaled_prn: BooleanLike = Field(
        default="",
        description="Standing order for Albuterol 2.5 mg inhaled as needed for chest tightness",
    )

    standing_other: str = Field(
        default="",
        description=(
            "Specify any additional standing orders for adverse reactions .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class PrescriberInformation(BaseModel):
    """Prescriber contact details and authorization"""

    prescriber_name: str = Field(
        ...,
        description=(
            'Full name of the prescribing provider .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    office_contact_name: str = Field(
        default="",
        description=(
            "Name of the primary office contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    npi: str = Field(
        ...,
        description=(
            "Prescriber's National Provider Identifier (NPI) number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    dea: str = Field(
        default="",
        description=(
            'Prescriber\'s DEA registration number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_phone: str = Field(
        ...,
        description=(
            'Office contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    contact_fax: str = Field(
        default="",
        description=(
            'Office contact fax number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    prescribers_signature: str = Field(
        ...,
        description=(
            "Signature of the prescribing provider authorizing this order .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_prescriber_signature: str = Field(
        ..., description="Date the prescriber signed the order"
    )  # YYYY-MM-DD format


class OklahomaInfusionServicesEvenityOrderForm(BaseModel):
    """
        OKLAHOMA
    INFUSION SERVICES

    Evenity Order Form

        By signing this form, you are authorizing Oklahoma Infusion Services and its employees to act as your designated agent to interact with medical and prescription insurance companies for prior authorization and specialty pharmacy approval to render infusion services.
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    additional_information_needed: AdditionalInformationNeeded = Field(
        ..., description="Additional Information Needed"
    )
    diagnosis_and_clinical_information: DiagnosisandClinicalInformation = Field(
        ..., description="Diagnosis and Clinical Information"
    )
    lab_orders: LabOrders = Field(..., description="Lab Orders")
    prescription_information: PrescriptionInformation = Field(
        ..., description="Prescription Information"
    )
    pre_medication_orders: PreMedicationOrders = Field(..., description="Pre-Medication Orders")
    standing_orders_for_adverse_reactions: StandingOrdersforAdverseReactions = Field(
        ..., description="Standing Orders for Adverse Reactions"
    )
    prescriber_information: PrescriberInformation = Field(..., description="Prescriber Information")
