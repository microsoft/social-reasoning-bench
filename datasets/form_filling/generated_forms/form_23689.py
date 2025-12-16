from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ConsultingProviderServiceReferredTo(BaseModel):
    """Information about the provider/service to whom the patient is being referred and appointment details"""

    provider_referred_to: BooleanLike = Field(
        default="", description="Check if the referral is to a specific provider"
    )

    date_referred_to: str = Field(
        ..., description="Date the consultation request is made"
    )  # YYYY-MM-DD format

    uwmc_referred_to: BooleanLike = Field(
        default="", description="Check if the referral destination is UWMC"
    )

    hmc_referred_to: BooleanLike = Field(
        default="", description="Check if the referral destination is HMC"
    )

    chmc_referred_to: BooleanLike = Field(
        default="", description="Check if the referral destination is CHMC"
    )

    other_referred_to: str = Field(
        default="",
        description=(
            "If other destination, specify the facility or provider .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    provider_name_referred_to: str = Field(
        ...,
        description=(
            "Name of the provider to whom the patient is being referred .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    patient_name: str = Field(
        ...,
        description=(
            "Full name of the patient being referred .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    specialty_service_referred_to: str = Field(
        ...,
        description=(
            "Specialty or service to which the patient is being referred .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address_referred_to_line_1: str = Field(
        ...,
        description=(
            "First line of the address for the referred-to provider or service .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address_referred_to_line_2: str = Field(
        default="",
        description=(
            "Second line of the address for the referred-to provider or service .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    city_state_referred_to_line_2: str = Field(
        ...,
        description=(
            "City and state for the referred-to provider or service (associated with second "
            'line of address) .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    city_state_referred_to_line_3: str = Field(
        default="",
        description=(
            "Additional city/state information if needed for the referred-to provider .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    zip_referred_to_first: str = Field(
        ..., description="Primary ZIP code for the referred-to provider or service"
    )

    telephone_number_referred_to: str = Field(
        ...,
        description=(
            "Primary telephone number for the referred-to provider or service .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    zip_referred_to_second: str = Field(
        default="",
        description="Secondary ZIP code if applicable for the referred-to provider or service",
    )

    telephone_number_referred_to_second: str = Field(
        default="",
        description=(
            "Additional telephone number for the referred-to provider or service .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    appointment_admit_date: str = Field(
        default="", description="Scheduled appointment or admission date for the patient"
    )  # YYYY-MM-DD format

    appointment_date: str = Field(
        default="", description="Specific appointment date if different from admit date"
    )  # YYYY-MM-DD format


class ReasonforConsultation(BaseModel):
    """Type of consult requested and clinical information supporting the consult"""

    opinion_only: BooleanLike = Field(
        default="", description="Check if consultation is for opinion only"
    )

    assume_charge_of_aspect_of_patient: BooleanLike = Field(
        default="",
        description="Check if consultant should assume charge of a specific aspect of patient care",
    )

    assume_charge_or_transfer_patient: BooleanLike = Field(
        default="",
        description="Check if consultant should assume full charge or accept transfer of the patient",
    )

    primary_diagnosis: str = Field(
        ...,
        description=(
            "Primary diagnosis prompting the consultation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    diagnosis_that_suggests_consult: str = Field(
        default="",
        description=(
            "Diagnosis or condition that indicates the need for consultation .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    pertinent_history_and_physical: str = Field(
        default="",
        description=(
            "Relevant history and physical examination findings .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ReferringProviderInformation(BaseModel):
    """Details about the provider and clinic requesting the consultation"""

    provider_referred_by: BooleanLike = Field(
        default="", description="Check if the referring party is a provider"
    )

    date_referred_by: str = Field(
        ..., description="Date the referral was made by the referring provider"
    )  # YYYY-MM-DD format

    uwmc_referred_by: BooleanLike = Field(
        default="", description="Check if the referring site is UWMC"
    )

    hmc_referred_by: BooleanLike = Field(
        default="", description="Check if the referring site is HMC"
    )

    chmc_referred_by: BooleanLike = Field(
        default="", description="Check if the referring site is CHMC"
    )

    other_referred_by: str = Field(
        default="",
        description=(
            "If other referring site, specify the facility .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    provider_name_referred_by: str = Field(
        ...,
        description=(
            "Name of the provider making the referral .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    upin: str = Field(
        default="",
        description=(
            "UPIN (Unique Physician Identification Number) of the referring provider .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_returning_to_referring_clinic: str = Field(
        default="", description="Date the patient is expected to return to the referring clinic"
    )  # YYYY-MM-DD format

    specialty_service_referred_by: str = Field(
        default="",
        description=(
            "Specialty or service of the referring provider .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_ms: str = Field(
        default="",
        description=(
            "Mailing address or mail stop for the referring provider .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_referred_by: str = Field(
        default="",
        description=(
            "City and state of the referring provider .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    zip_referred_by: str = Field(default="", description="ZIP code of the referring provider")

    telephone_number_referred_by: str = Field(
        default="",
        description=(
            "Telephone number of the referring provider .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    interpreter: BooleanLike = Field(default="", description="Check if an interpreter is needed")

    notify_referring_physician_when_scheduled: BooleanLike = Field(
        default="",
        description=(
            "Check if the consulting service should notify the referring physician when the "
            "appointment is scheduled"
        ),
    )


class PatientIdentification(BaseModel):
    """Basic patient identifiers used on the consultation request"""

    pt_no: str = Field(
        ...,
        description=(
            "Patient number or medical record number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name: str = Field(
        ...,
        description=(
            'Patient\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(..., description="Patient's date of birth")  # YYYY-MM-DD format


class ProfessionalConsultationRequest(BaseModel):
    """
    PROFESSIONAL CONSULTATION REQUEST

    PROFESSIONAL CONSULTATION REQUEST
    """

    consulting_provider__service_referred_to: ConsultingProviderServiceReferredTo = Field(
        ..., description="Consulting Provider / Service (Referred To)"
    )
    reason_for_consultation: ReasonforConsultation = Field(
        ..., description="Reason for Consultation"
    )
    referring_provider_information: ReferringProviderInformation = Field(
        ..., description="Referring Provider Information"
    )
    patient_identification: PatientIdentification = Field(..., description="Patient Identification")
