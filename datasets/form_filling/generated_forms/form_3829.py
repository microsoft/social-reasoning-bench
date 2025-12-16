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
    """Patient demographics and contact details"""

    patient_name: str = Field(
        ...,
        description=(
            'Patient\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    birthdate: str = Field(..., description="Patient's date of birth")  # YYYY-MM-DD format

    sex_male: BooleanLike = Field(..., description="Check if the patient's sex is male")

    sex_female: BooleanLike = Field(..., description="Check if the patient's sex is female")

    height: str = Field(
        default="",
        description=(
            "Patient's height (specify units, e.g., ft/in or cm) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    weight_lbs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Patient's weight in pounds"
    )

    weight_kg: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Patient's weight in kilograms"
    )

    allergies: str = Field(
        default="",
        description=(
            "List all known drug and other relevant allergies .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    patient_primary_language_english: BooleanLike = Field(
        default="", description="Check if the patient's primary language is English"
    )

    patient_primary_language_spanish: BooleanLike = Field(
        default="", description="Check if the patient's primary language is Spanish"
    )

    patient_primary_language_other: BooleanLike = Field(
        default="", description="Check if the patient's primary language is not English or Spanish"
    )

    other_primary_language: str = Field(
        default="",
        description=(
            "Specify the patient's primary language if 'Other' is selected .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    hearing_impaired: BooleanLike = Field(
        default="", description="Check if the patient is hearing impaired"
    )

    patient_phone: str = Field(
        ...,
        description=(
            'Primary phone number for the patient .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    patient_email: str = Field(
        default="",
        description=(
            'Email address for the patient .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    caregiver_name: str = Field(
        default="",
        description=(
            "Name of the patient's caregiver, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    patient_address: str = Field(
        ...,
        description=(
            'Street address of the patient .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city_patient: str = Field(
        ...,
        description=(
            'City of the patient\'s residence .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state_patient: str = Field(..., description="State of the patient's residence")

    zip_patient: str = Field(..., description="ZIP code of the patient's residence")


class DiagnosisClinicalInformation(BaseModel):
    """Diagnosis, clinical rationale, and prior treatments"""

    diagnosis_type_1_e10_649: BooleanLike = Field(
        default="", description="Check if the diagnosis is Type 1 diabetes with code E10.649"
    )

    diagnosis_type_2_e11_649: BooleanLike = Field(
        default="", description="Check if the diagnosis is Type 2 diabetes with code E11.649"
    )

    diagnosis_other: BooleanLike = Field(
        default="", description="Check if the diagnosis is other than the listed options"
    )

    other_diagnosis: str = Field(
        default="",
        description=(
            "Specify other diagnosis if 'Other' is selected .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    history_of_prior_severe_hypoglycemia: BooleanLike = Field(
        default="", description="Check if the patient has a history of prior severe hypoglycemia"
    )

    prior_history_of_failure_to_correctly_administer_conventional_kits: BooleanLike = Field(
        default="",
        description=(
            "Check if the patient has previously failed to correctly administer conventional kits"
        ),
    )

    er_visits_hospitalizations: BooleanLike = Field(
        default="",
        description=(
            "Check if the patient has had ER visits or hospitalizations related to their condition"
        ),
    )

    impairments: BooleanLike = Field(
        default="", description="Check if the patient has impairments relevant to treatment"
    )

    co_morbidities: BooleanLike = Field(
        default="", description="Check if the patient has co-morbid conditions"
    )

    additional_rationale: str = Field(
        default="",
        description=(
            "Provide any additional clinical rationale for treatment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_previously_tried_treatment: str = Field(
        default="",
        description=(
            "Specify any other previously tried and failed treatments .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PrescriptionInformation(BaseModel):
    """Medication selection, directions, and refills"""

    gvoke_hypopen_2_pack_0_5mg_0_1ml_selection: BooleanLike = Field(
        default="", description="Select if prescribing Gvoke HypoPen 2-Pack 0.5mg/0.1mL"
    )

    gvoke_hypopen_2_pack_1_0mg_0_2ml_selection: BooleanLike = Field(
        default="", description="Select if prescribing Gvoke HypoPen 2-Pack 1.0mg/0.2mL"
    )

    gvoke_hypopen_other_directions: str = Field(
        default="",
        description=(
            "Enter any alternative or additional directions for Gvoke HypoPen .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    gvoke_hypopen_refills: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of refills authorized for Gvoke HypoPen"
    )

    gvoke_pfs_2_pack_0_5mg_0_1ml_selection: BooleanLike = Field(
        default="", description="Select if prescribing Gvoke PFS 2-Pack 0.5mg/0.1mL"
    )

    gvoke_pfs_2_pack_1_0mg_0_2ml_selection: BooleanLike = Field(
        default="", description="Select if prescribing Gvoke PFS 2-Pack 1.0mg/0.2mL"
    )

    gvoke_pfs_other_directions: str = Field(
        default="",
        description=(
            "Enter any alternative or additional directions for Gvoke PFS .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    gvoke_pfs_refills: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of refills authorized for Gvoke PFS"
    )


class ProviderPrescriberInformation(BaseModel):
    """Clinic, prescriber details, and authorization"""

    clinic_name: str = Field(
        ...,
        description=(
            'Name of the clinic or practice .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    provider_name: str = Field(
        ...,
        description=(
            'Name of the prescribing provider .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    provider_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the provider or clinic .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    provider_fax: str = Field(
        ...,
        description=(
            'Fax number for the provider or clinic .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    dea: str = Field(
        default="",
        description=(
            'Provider\'s DEA registration number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    npi: str = Field(
        ...,
        description=(
            "Provider's National Provider Identifier (NPI) number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    provider_address: str = Field(
        ...,
        description=(
            "Street address of the provider or clinic .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_provider: str = Field(
        ...,
        description=(
            'City of the provider or clinic .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state_provider: str = Field(..., description="State of the provider or clinic")

    zip_provider: str = Field(..., description="ZIP code of the provider or clinic")

    signature: str = Field(
        ...,
        description=(
            'Prescriber\'s handwritten signature .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the prescriber signed the form")  # YYYY-MM-DD format

    dispense_as_written_write_daw: BooleanLike = Field(
        default="",
        description="Indicate if the prescription must be dispensed exactly as written (DAW)",
    )


class SterlingPharmacyHypoglycemiaReferralForm(BaseModel):
    """
        Sterling Specialty Pharmacy
    Severe Hypoglycemia
    Prescription Referral Form

        Note: Faxed prescriptions will only be accepted from a prescribing practitioner. Patients must bring an original prescription to the pharmacy. Prescribers are reminded patients may choose any pharmacy of their choice.
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    diagnosis__clinical_information: DiagnosisClinicalInformation = Field(
        ..., description="Diagnosis / Clinical Information"
    )
    prescription_information: PrescriptionInformation = Field(
        ..., description="Prescription Information"
    )
    provider__prescriber_information: ProviderPrescriberInformation = Field(
        ..., description="Provider / Prescriber Information"
    )
