from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PrescriptionInformationTableRow(BaseModel):
    """Single row in DRUG"""

    drug: str = Field(default="", description="Drug")
    strength: str = Field(default="", description="Strength")
    direction: str = Field(default="", description="Direction")
    quantity: str = Field(default="", description="Quantity")
    refills: str = Field(default="", description="Refills")


class PatientInformation(BaseModel):
    """Basic information about the patient"""

    last_name: str = Field(
        ...,
        description=(
            'Patient\'s legal last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Patient\'s legal first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    social_security_no: str = Field(default="", description="Patient's Social Security Number")

    date_of_birth: str = Field(..., description="Patient's date of birth")  # YYYY-MM-DD format

    sex_m: BooleanLike = Field(..., description="Check if patient is male")

    sex_f: BooleanLike = Field(..., description="Check if patient is female")

    weight: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Patient's weight (specify units, e.g., kg or lbs)"
    )

    height: str = Field(
        ...,
        description=(
            "Patient's height (include units, e.g., cm or ft/in) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    allergies: str = Field(
        default="",
        description=(
            "List any known drug or other allergies .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    home_phone: str = Field(
        default="",
        description=(
            'Patient\'s home phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    work_mobile: str = Field(
        default="",
        description=(
            'Patient\'s work or mobile phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    home_address: str = Field(
        ...,
        description=(
            'Patient\'s street address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of patient\'s residence .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of patient's residence")

    zip: str = Field(..., description="Zip code of patient's residence")


class PatientInsuranceInformation(BaseModel):
    """Patient’s medical and prescription insurance details"""

    primary_medical_insurance: str = Field(
        ...,
        description=(
            "Name of patient's primary medical insurance .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medical_insurance_phone: str = Field(
        default="",
        description=(
            "Contact phone number for the medical insurance .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    subscriber_name: str = Field(
        ...,
        description=(
            "Name of the insurance policy subscriber .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    rx_card_pbm: str = Field(
        default="",
        description=(
            "Name of the pharmacy benefit manager or Rx card .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    group_no: str = Field(
        default="",
        description=(
            'Insurance group number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    prescription_card_bin: str = Field(
        default="",
        description=(
            'Prescription card BIN number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    pcn: str = Field(
        default="",
        description=(
            'Prescription card PCN number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class TreatmentArrangements(BaseModel):
    """Treatment start date, shipping, and teaching arrangements"""

    start_date: str = Field(
        default="", description="Requested treatment start date"
    )  # YYYY-MM-DD format

    ship_meds_home: BooleanLike = Field(
        default="", description="Check if medications should be shipped to patient's home"
    )

    ship_meds_doctors_office: BooleanLike = Field(
        default="", description="Check if medications should be shipped to the doctor's office"
    )

    teaching_by_doctors_office: BooleanLike = Field(
        default="", description="Check if injection teaching will be done by the doctor's office"
    )

    teaching_by_other: BooleanLike = Field(
        default="", description="Check if injection teaching will be done by another provider"
    )

    teaching_by_other_specify: str = Field(
        default="",
        description=(
            "Specify who will provide teaching if 'Other' is selected .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CertificateofMedicalNecessity(BaseModel):
    """Diagnosis and clinical information supporting medical necessity"""

    diagnosis_icd10_j4540_moderate_persistent_asthma_uncomplicated: BooleanLike = Field(
        default="", description="Check if this ICD-10 diagnosis applies"
    )

    diagnosis_icd10_j4550_severe_persistent_asthma_uncomplicated: BooleanLike = Field(
        default="", description="Check if this ICD-10 diagnosis applies"
    )

    diagnosis_icd10_l209_atopic_dermatitis: BooleanLike = Field(
        default="", description="Check if this ICD-10 diagnosis applies"
    )

    serum_total_immunoglobulin_e_ige_level_iu_ml: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Patient's serum total IgE level in IU/mL"
    )

    body_weight: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Patient's body weight for dosing (specify units)"
    )

    other_diagnosis: str = Field(
        default="",
        description=(
            "Any other relevant diagnosis not listed above .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PrescriptionInformation(BaseModel):
    """Medication orders, dosing, and related prescription details"""

    prescription_information_table: List[PrescriptionInformationTableRow] = Field(
        default="",
        description=(
            "Table for listing prescribed drugs, strengths, directions, quantities, and refills"
        ),
    )  # List of table rows

    strength: str = Field(
        default="",
        description=(
            'Strength of the prescribed medication .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    direction: str = Field(
        default="",
        description=(
            'Directions for use of the medication .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    quantity: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Quantity of medication to dispense"
    )

    refills: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of refills authorized"
    )

    dupixent_others: str = Field(
        default="",
        description=(
            'Other DUPIXENT directions or notes .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    xolair_vial: BooleanLike = Field(
        default="", description="Check if XOLAIR vial formulation is prescribed"
    )

    xolair_prefilled_syringe: BooleanLike = Field(
        default="", description="Check if XOLAIR prefilled syringe formulation is prescribed"
    )

    xolair_75mg: BooleanLike = Field(default="", description="Select 75mg XOLAIR strength")

    xolair_150mg: BooleanLike = Field(default="", description="Select 150mg XOLAIR strength")

    xolair_300mg: BooleanLike = Field(default="", description="Select 300mg XOLAIR strength")

    xolair_375mg: BooleanLike = Field(default="", description="Select 375mg XOLAIR strength")

    xolair_dose_mg_dose_every_2_weeks: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dose of XOLAIR in mg per dose to be given every 2 weeks"
    )

    xolair_dose_mg_dose_every_4_weeks: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dose of XOLAIR in mg per dose to be given every 4 weeks"
    )

    xolair_others: str = Field(
        default="",
        description=(
            'Other XOLAIR directions or notes .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    nucala_100mg: BooleanLike = Field(default="", description="Select 100mg NUCALA dose")

    nucala_others: str = Field(
        default="",
        description=(
            'Other NUCALA directions or notes .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    cinquair_dose_mg_kg: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dose of CINQAIR in mg/kg"
    )

    cinquair_dose_mg_kg_every_4_weeks: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dose of CINQAIR in mg/kg to be given every 4 weeks"
    )

    cinquair_others: str = Field(
        default="",
        description=(
            'Other CINQAIR directions or notes .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    fasenra_30mg: BooleanLike = Field(default="", description="Select 30mg FASENRA dose")

    fasenra_others: str = Field(
        default="",
        description=(
            'Other FASENRA directions or notes .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    skilled_nursing_visit_for_self_injection_training: BooleanLike = Field(
        default="",
        description=(
            "Check to request skilled nursing visit for self-injection training and one "
            "follow-up visit if needed"
        ),
    )


class PrescriberInformationandAuthorization(BaseModel):
    """Physician details, signature, and authorization"""

    physician_signature: str = Field(
        ...,
        description=(
            'Signature of prescribing physician .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    daw_dispense_as_written: BooleanLike = Field(
        default="",
        description="Check if medication must be dispensed as written (no substitutions)",
    )

    date: str = Field(..., description="Date the prescription was signed")  # YYYY-MM-DD format

    physician_name: str = Field(
        ...,
        description=(
            'Name of prescribing physician .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Physician\'s office phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            'Physician\'s office fax number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    office_contact: str = Field(
        default="",
        description=(
            "Primary contact person at the physician's office .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    physician_address: str = Field(
        ...,
        description=(
            "Mailing address of the physician's office .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    npi: str = Field(
        ...,
        description=(
            "Physician's National Provider Identifier (NPI) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dea: str = Field(
        default="",
        description=(
            'Physician\'s DEA registration number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class AllergicSpecialtyMedicationsForm(BaseModel):
    """
    ALLERGIC SPECIALTY MEDICATIONS FORM

    By Signing this prescription and using Southside pharmacy's services you authorize Southside Pharmacy to contact insurance companies for prior authorization purposes on your behalf.
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    patient_insurance_information: PatientInsuranceInformation = Field(
        ..., description="Patient Insurance Information"
    )
    treatment_arrangements: TreatmentArrangements = Field(..., description="Treatment Arrangements")
    certificate_of_medical_necessity: CertificateofMedicalNecessity = Field(
        ..., description="Certificate of Medical Necessity"
    )
    prescription_information: PrescriptionInformation = Field(
        ..., description="Prescription Information"
    )
    prescriber_information_and_authorization: PrescriberInformationandAuthorization = Field(
        ..., description="Prescriber Information and Authorization"
    )
