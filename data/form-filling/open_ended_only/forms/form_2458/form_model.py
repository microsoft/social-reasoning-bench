from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class GeneralInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Basic patient and transport details"""

    patients_name: str = Field(
        ...,
        description=(
            "Full legal name of the patient .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    date_of_birth: str = Field(
        ...,
        description="Patient's date of birth"
    )  # YYYY-MM-DD format

    medicare_number: str = Field(
        ...,
        description=(
            "Patient's Medicare number .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    transport_date: str = Field(
        ...,
        description="Date of ambulance transport"
    )  # YYYY-MM-DD format

    origin: str = Field(
        ...,
        description=(
            "Location where transport began .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    destination: str = Field(
        ...,
        description=(
            "Destination of transport .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    is_the_patients_stay_covered_under_medicare_part_a_yes: BooleanLike = Field(
        ...,
        description="Check YES if patient's stay is covered under Medicare Part A"
    )

    is_the_patients_stay_covered_under_medicare_part_a_no: BooleanLike = Field(
        ...,
        description="Check NO if patient's stay is not covered under Medicare Part A"
    )

    closest_appropriate_facility_yes: BooleanLike = Field(
        ...,
        description="Check YES if this is the closest appropriate facility"
    )

    closest_appropriate_facility_no: BooleanLike = Field(
        ...,
        description="Check NO if this is not the closest appropriate facility"
    )

    if_no_why_was_the_patient_transported_to_another_facility: str = Field(
        ...,
        description=(
            "Reason for transport to a facility other than the closest appropriate one .If "
            "you cannot fill this, write \"N/A\". If this field should not be filled by you "
            "(for example, it belongs to another person or office), leave it blank (empty "
            "string \"\")."
        )
    )

    if_hospital_to_hospital_transfer_describe_services_needed_at_2nd_facility_not_available_at_1st_facility: str = Field(
        ...,
        description=(
            "Describe services at 2nd facility not available at 1st facility .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )

    if_hospice_pt_is_this_transport_related_to_pts_terminal_illness_yes: BooleanLike = Field(
        ...,
        description="Check YES if transport is related to hospice patient's terminal illness"
    )

    if_hospice_pt_is_this_transport_related_to_pts_terminal_illness_no: BooleanLike = Field(
        ...,
        description="Check NO if transport is not related to hospice patient's terminal illness"
    )

    describe_hospice_transport_related_to_terminal_illness: str = Field(
        ...,
        description=(
            "Describe how transport is related to terminal illness for hospice patient .If "
            "you cannot fill this, write \"N/A\". If this field should not be filled by you "
            "(for example, it belongs to another person or office), leave it blank (empty "
            "string \"\")."
        )
    )


class MedicalNecessityQuestionnaire(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Assessment of medical necessity for ambulance transport"""

    describe_the_medical_condition_of_this_patient_at_the_time_of_ambulance_transport: str = Field(
        ...,
        description=(
            "Describe the patient's medical condition and why ambulance transport is "
            "required .If you cannot fill this, write \"N/A\". If this field should not be "
            "filled by you (for example, it belongs to another person or office), leave it "
            "blank (empty string \"\")."
        )
    )

    is_this_patient_bed_confined_as_defined_below_yes: BooleanLike = Field(
        ...,
        description="Check YES if patient is bed confined as defined"
    )

    is_this_patient_bed_confined_as_defined_below_no: BooleanLike = Field(
        ...,
        description="Check NO if patient is not bed confined as defined"
    )

    can_this_patient_safely_be_transported_by_car_or_wheelchair_van_yes: BooleanLike = Field(
        ...,
        description="Check YES if patient can be safely transported by car or wheelchair van"
    )

    can_this_patient_safely_be_transported_by_car_or_wheelchair_van_no: BooleanLike = Field(
        ...,
        description="Check NO if patient cannot be safely transported by car or wheelchair van"
    )

    contractures: BooleanLike = Field(
        ...,
        description="Check if patient has contractures"
    )

    non_healed_fractures: BooleanLike = Field(
        ...,
        description="Check if patient has non-healed fractures"
    )

    patient_is_confused: BooleanLike = Field(
        ...,
        description="Check if patient is confused"
    )

    patient_is_comatose: BooleanLike = Field(
        ...,
        description="Check if patient is comatose"
    )

    moderate_severe_pain_on_movement: BooleanLike = Field(
        ...,
        description="Check if patient has moderate or severe pain on movement"
    )

    danger_to_self_others: BooleanLike = Field(
        ...,
        description="Check if patient is a danger to self or others"
    )

    iv_meds_fluids_required: BooleanLike = Field(
        ...,
        description="Check if IV medications or fluids are required"
    )

    patient_is_combative: BooleanLike = Field(
        ...,
        description="Check if patient is combative"
    )

    need_or_possible_need_for_restraints: BooleanLike = Field(
        ...,
        description="Check if there is a need or possible need for restraints"
    )

    dvt_requires_elevation_of_a_lower_extremity: BooleanLike = Field(
        ...,
        description="Check if DVT requires elevation of a lower extremity"
    )

    medical_attention_required: BooleanLike = Field(
        ...,
        description="Check if medical attention is required during transport"
    )

    requires_oxygen_unable_to_self_administer: BooleanLike = Field(
        ...,
        description="Check if patient requires oxygen and is unable to self-administer"
    )

    special_handling_isolation_infection_control_precautions_required: BooleanLike = Field(
        ...,
        description=(
            "Check if special handling, isolation, or infection control precautions are "
            "required"
        )
    )

    unable_to_tolerate_seated_position_for_time_needed_to_transport: BooleanLike = Field(
        ...,
        description="Check if patient is unable to tolerate seated position for transport duration"
    )

    hemodynamic_monitoring_required_enroute: BooleanLike = Field(
        ...,
        description="Check if hemodynamic monitoring is required during transport"
    )

    unable_to_sit_in_a_chair_or_wheelchair_due_to_decubitus_ulcers_or_other_wounds: BooleanLike = Field(
        ...,
        description="Check if patient cannot sit in a chair or wheelchair due to ulcers or wounds"
    )

    cardiac_monitoring_required_enroute: BooleanLike = Field(
        ...,
        description="Check if cardiac monitoring is required during transport"
    )

    morbid_obesity_requires_additional_personnel_equipment_to_safely_handle_patient: BooleanLike = Field(
        ...,
        description="Check if morbid obesity requires extra personnel/equipment"
    )

    orthopedic_device_requiring_special_handling_during_transport: BooleanLike = Field(
        ...,
        description="Check if orthopedic device requires special handling during transport"
    )

    other_specify: str = Field(
        ...,
        description=(
            "Specify any other relevant condition .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class SignatureofPhysicianorOtherAuthorizedHealthcareProfessional(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Certification and signature by healthcare professional"""

    if_this_box_is_checked_i_also_certify_that_the_patient_is_physically_or_mentally_incapable_of_signing_the_ambulance_services_claim_form: BooleanLike = Field(
        ...,
        description="Check if patient is incapable of signing the ambulance service claim form"
    )

    specific_reasons_that_the_patient_is_physically_or_mentally_incapable_of_signing_the_claim_form: str = Field(
        ...,
        description=(
            "Describe why the patient is incapable of signing the claim form .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )

    signature_of_physician_or_authorized_healthcare_professional: str = Field(
        ...,
        description=(
            "Signature of physician or authorized healthcare professional .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )

    date_signed: str = Field(
        ...,
        description="Date the form was signed"
    )  # YYYY-MM-DD format

    printed_name_and_credentials_of_physician_or_authorized_healthcare_professional: str = Field(
        ...,
        description=(
            "Printed name and credentials of the signing physician or healthcare "
            "professional .If you cannot fill this, write \"N/A\". If this field should not "
            "be filled by you (for example, it belongs to another person or office), leave "
            "it blank (empty string \"\")."
        )
    )

    physician_assistant: BooleanLike = Field(
        ...,
        description="Check if signer is a Physician Assistant"
    )

    clinical_nurse_specialist: BooleanLike = Field(
        ...,
        description="Check if signer is a Clinical Nurse Specialist"
    )

    licensed_practical_nurse: BooleanLike = Field(
        ...,
        description="Check if signer is a Licensed Practical Nurse"
    )

    case_manager: BooleanLike = Field(
        ...,
        description="Check if signer is a Case Manager"
    )

    nurse_practitioner: BooleanLike = Field(
        ...,
        description="Check if signer is a Nurse Practitioner"
    )

    registered_nurse: BooleanLike = Field(
        ...,
        description="Check if signer is a Registered Nurse"
    )

    social_worker: BooleanLike = Field(
        ...,
        description="Check if signer is a Social Worker"
    )

    discharge_planner: BooleanLike = Field(
        ...,
        description="Check if signer is a Discharge Planner"
    )


class UniversalAmbulanceService(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    UNIVERSAL AMBULANCE SERVICE

    Ambulance Transportation is medically necessary only if other means of transport are contraindicated or would be potentially harmful to the patient. To meet this requirement, the patient must be either “bed confined” or suffer from a condition such that transport by means other than an ambulance is contraindicated by the patient’s condition. The following questions must be answered by the healthcare professional signing below for this form to be valid. This information will be used by the Centers for Medicare and Medicaid Services (CMS) to support the determination of medical necessity for ambulance services.
    """

    general_information: GeneralInformation = Field(
        ...,
        description="General Information"
    )
    medical_necessity_questionnaire: MedicalNecessityQuestionnaire = Field(
        ...,
        description="Medical Necessity Questionnaire"
    )
    signature_of_physician_or_other_authorized_healthcare_professional: SignatureofPhysicianorOtherAuthorizedHealthcareProfessional = Field(
        ...,
        description="Signature of Physician or Other Authorized Healthcare Professional"
    )