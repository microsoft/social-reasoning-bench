from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class SectionIGeneralInformation(BaseModel):
    """General patient and transport details"""

    patients_name: str = Field(
        ...,
        description=(
            'Patient’s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Patient’s date of birth")  # YYYY-MM-DD format

    medicare_number: str = Field(
        ...,
        description=(
            "Patient’s Medicare identification number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    transport_date: str = Field(
        ..., description="Date of the ambulance transport"
    )  # YYYY-MM-DD format

    origin: str = Field(
        ...,
        description=(
            "Location patient is being transported from .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    destination: str = Field(
        ...,
        description=(
            "Location patient is being transported to .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medicare_part_a_covered_yes: BooleanLike = Field(
        ..., description="Check if the patient’s stay is covered under Medicare Part A (PPS/DRG)"
    )

    medicare_part_a_covered_no: BooleanLike = Field(
        ...,
        description="Check if the patient’s stay is not covered under Medicare Part A (PPS/DRG)",
    )

    closest_appropriate_facility_yes: BooleanLike = Field(
        ..., description="Check if the destination is the closest appropriate facility"
    )

    closest_appropriate_facility_no: BooleanLike = Field(
        ..., description="Check if the destination is not the closest appropriate facility"
    )

    reason_not_closest_facility: str = Field(
        default="",
        description=(
            "Explain why the patient was transported to a facility other than the closest "
            'appropriate one .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    hospital_to_hospital_services_needed: str = Field(
        default="",
        description=(
            "Describe services at the receiving hospital that are not available at the "
            'sending hospital .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    hospice_transport_related_yes: BooleanLike = Field(
        default="",
        description="Check if the transport is related to the hospice patient’s terminal illness",
    )

    hospice_transport_related_no: BooleanLike = Field(
        default="",
        description="Check if the transport is not related to the hospice patient’s terminal illness",
    )

    hospice_transport_description: str = Field(
        default="",
        description=(
            "Describe how the transport is or is not related to the hospice patient’s "
            'terminal illness .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class SectionIIMedicalNecessityQuestionnaire(BaseModel):
    """Medical condition and necessity for ambulance transport"""

    medical_condition_description: str = Field(
        ...,
        description=(
            "Describe the patient’s physical and/or mental condition at the time of "
            "transport and why other means of transport are contraindicated .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    bed_confined_yes: BooleanLike = Field(
        ..., description="Check if the patient meets the definition of bed confined"
    )

    bed_confined_no: BooleanLike = Field(
        ..., description="Check if the patient does not meet the definition of bed confined"
    )

    can_be_transported_by_car_yes: BooleanLike = Field(
        ..., description="Check if the patient can safely be transported by car or wheelchair van"
    )

    can_be_transported_by_car_no: BooleanLike = Field(
        ...,
        description="Check if the patient cannot safely be transported by car or wheelchair van",
    )

    contractures: BooleanLike = Field(
        default="", description="Check if the patient has contractures"
    )

    non_healed_fractures: BooleanLike = Field(
        default="", description="Check if the patient has non-healed fractures"
    )

    patient_is_confused: BooleanLike = Field(
        default="", description="Check if the patient is confused"
    )

    patient_is_comatose: BooleanLike = Field(
        default="", description="Check if the patient is comatose"
    )

    moderate_severe_pain_on_movement: BooleanLike = Field(
        default="", description="Check if the patient has moderate or severe pain on movement"
    )

    danger_to_self_others: BooleanLike = Field(
        default="", description="Check if the patient poses a danger to self or others"
    )

    iv_meds_fluids_required: BooleanLike = Field(
        default="",
        description="Check if intravenous medications or fluids are required during transport",
    )

    patient_is_combative: BooleanLike = Field(
        default="", description="Check if the patient is combative"
    )

    need_or_possible_need_for_restraints: BooleanLike = Field(
        default="",
        description="Check if there is a need or possible need for restraints during transport",
    )

    dvt_requires_elevation: BooleanLike = Field(
        default="",
        description="Check if deep vein thrombosis requires elevation of a lower extremity",
    )

    medical_attendant_required: BooleanLike = Field(
        default="", description="Check if a medical attendant is required during transport"
    )

    requires_oxygen_unable_to_self_administer: BooleanLike = Field(
        default="",
        description="Check if the patient requires oxygen and is unable to self-administer",
    )

    special_handling_isolation_precautions: BooleanLike = Field(
        default="",
        description=(
            "Check if special handling, isolation, or infection control precautions are required"
        ),
    )

    unable_to_tolerate_seated_position: BooleanLike = Field(
        default="",
        description="Check if the patient cannot tolerate sitting for the duration of transport",
    )

    hemodynamic_monitoring_required_enroute: BooleanLike = Field(
        default="", description="Check if hemodynamic monitoring is required during transport"
    )

    unable_to_sit_due_to_ulcers_or_wounds: BooleanLike = Field(
        default="",
        description="Check if the patient cannot sit due to decubitus ulcers or other wounds",
    )

    cardiac_monitoring_required_enroute: BooleanLike = Field(
        default="", description="Check if cardiac monitoring is required during transport"
    )

    morbid_obesity_requires_additional_personnel: BooleanLike = Field(
        default="",
        description="Check if morbid obesity requires extra personnel or equipment for safe handling",
    )

    orthopedic_device_special_handling: BooleanLike = Field(
        default="",
        description=(
            "Check if an orthopedic device (backboard, halo, pins, traction, brace, wedge, "
            "etc.) requires special handling during transport"
        ),
    )

    other_specify: str = Field(
        default="",
        description=(
            "Specify any other condition not listed above that affects transport .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SectionIIISignatureofPhysicianorOtherAuthorizedHealthcareProfessional(BaseModel):
    """Certifications and signatures by the physician or authorized healthcare professional"""

    patient_unable_to_sign_checkbox: BooleanLike = Field(
        default="",
        description=(
            "Check if signing on behalf of a patient who is physically or mentally "
            "incapable of signing"
        ),
    )

    reason_patient_unable_to_sign: str = Field(
        default="",
        description=(
            "Describe the specific reasons the patient is unable to sign the claim form .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    physician_signature: str = Field(
        ...,
        description=(
            "Signature of the physician or other authorized healthcare professional "
            'certifying medical necessity .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_signed: str = Field(
        ...,
        description="Date the form was signed by the physician or authorized healthcare professional",
    )  # YYYY-MM-DD format

    printed_name_and_credentials: str = Field(
        ...,
        description=(
            "Printed name and professional credentials (e.g., MD, DO, RN) of the signing "
            'provider .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    physician_assistant: BooleanLike = Field(
        default="", description="Check if the signer is a Physician Assistant"
    )

    clinical_nurse_specialist: BooleanLike = Field(
        default="", description="Check if the signer is a Clinical Nurse Specialist"
    )

    licensed_practical_nurse: BooleanLike = Field(
        default="", description="Check if the signer is a Licensed Practical Nurse"
    )

    case_manager: BooleanLike = Field(
        default="", description="Check if the signer is a Case Manager"
    )

    nurse_practitioner: BooleanLike = Field(
        default="", description="Check if the signer is a Nurse Practitioner"
    )

    registered_nurse: BooleanLike = Field(
        default="", description="Check if the signer is a Registered Nurse"
    )

    social_worker: BooleanLike = Field(
        default="", description="Check if the signer is a Social Worker"
    )

    discharge_planner: BooleanLike = Field(
        default="", description="Check if the signer is a Discharge Planner"
    )


class UniversalAmbulanceService(BaseModel):
    """
    UNIVERSAL AMBULANCE SERVICE

    Ambulance Transportation is medically necessary only if other means of transport are contraindicated or would be potentially harmful to the patient. To meet this requirement, the patient must be either “bed confined” or suffer from a condition such that transport by means other than an ambulance is contraindicated by the patient’s condition. The following questions must be answered by the healthcare professional signing below for this form to be valid.
    """

    section_i___general_information: SectionIGeneralInformation = Field(
        ..., description="Section I – General Information"
    )
    section_ii___medical_necessity_questionnaire: SectionIIMedicalNecessityQuestionnaire = Field(
        ..., description="Section II – Medical Necessity Questionnaire"
    )
    section_iii___signature_of_physician_or_other_authorized_healthcare_professional: SectionIIISignatureofPhysicianorOtherAuthorizedHealthcareProfessional = Field(
        ...,
        description="Section III – Signature of Physician or Other Authorized Healthcare Professional",
    )
