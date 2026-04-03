from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PatientInformation(BaseModel):
    """Basic patient and visit details"""

    patient_name: str = Field(
        ...,
        description=(
            'Full name of the patient .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Date this prescription/form is completed"
    )  # YYYY-MM-DD format

    diagnosis: str = Field(
        ...,
        description=(
            "Primary diagnosis or reason for physical therapy .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    precautions: str = Field(
        default="",
        description=(
            "Any medical or activity precautions to be observed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    frequency_times_per_week: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of therapy sessions per week"
    )

    frequency_for_weeks: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of weeks therapy is prescribed"
    )


class PlanofCareTreatmentOrders(BaseModel):
    """Requested evaluation and treatment plan"""

    evaluate_treat: BooleanLike = Field(
        default="", description="Check if the therapist should evaluate and treat the patient"
    )

    therapeutic_exercise: BooleanLike = Field(
        default="", description="Check if therapeutic exercise is ordered"
    )

    passive_rom: BooleanLike = Field(
        default="", description="Check if passive range of motion exercises are ordered"
    )

    active_rom: BooleanLike = Field(
        default="", description="Check if active range of motion exercises are ordered"
    )

    active_assisted_rom: BooleanLike = Field(
        default="", description="Check if active assisted range of motion exercises are ordered"
    )

    progressive_resistive_exercise: BooleanLike = Field(
        default="", description="Check if progressive resistive exercises are ordered"
    )

    strengthening: BooleanLike = Field(
        default="", description="Check if strengthening exercises are ordered"
    )

    stabilization_program: BooleanLike = Field(
        default="", description="Check if a stabilization program is ordered"
    )

    posture_body_mechanics: BooleanLike = Field(
        default="", description="Check if posture and body mechanics training is ordered"
    )

    gait_training: BooleanLike = Field(default="", description="Check if gait training is ordered")

    fall_risk_assessment: BooleanLike = Field(
        default="", description="Check if a fall risk assessment is ordered"
    )

    home_exercise_program: BooleanLike = Field(
        default="", description="Check if a home exercise program is ordered"
    )

    manual_therapy: BooleanLike = Field(
        default="", description="Check if manual therapy is ordered"
    )

    soft_tissue_mobilization: BooleanLike = Field(
        default="", description="Check if soft tissue mobilization is ordered"
    )

    joint_mobilization: BooleanLike = Field(
        default="", description="Check if joint mobilization is ordered"
    )

    myofascial_mobilization: BooleanLike = Field(
        default="", description="Check if myofascial mobilization is ordered"
    )

    post_operative_rehabilitation_protocol_for: str = Field(
        default="",
        description=(
            "Surgical procedure or body part for which the post-operative rehab protocol "
            'applies .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    date_of_surgery: str = Field(
        default="", description="Date of the surgical procedure"
    )  # YYYY-MM-DD format

    neuromuscular_re_education: BooleanLike = Field(
        default="", description="Check if neuromuscular re-education is ordered"
    )

    balance_proprioceptive_training: BooleanLike = Field(
        default="", description="Check if balance or proprioceptive training is ordered"
    )

    modalities: BooleanLike = Field(
        default="", description="Check if any therapeutic modalities are ordered"
    )

    ultrasound: BooleanLike = Field(
        default="", description="Check if ultrasound modality is ordered"
    )

    phonophoresis: BooleanLike = Field(
        default="", description="Check if phonophoresis modality is ordered"
    )

    iontophoresis: BooleanLike = Field(
        default="", description="Check if iontophoresis modality is ordered"
    )

    electrical_stimulation: BooleanLike = Field(
        default="", description="Check if electrical stimulation modality is ordered"
    )

    mechanical_traction: BooleanLike = Field(
        default="", description="Check if mechanical traction modality is ordered"
    )

    blood_flow_restriction_therapy: BooleanLike = Field(
        default="", description="Check if blood flow restriction therapy is ordered"
    )

    sports_specific_training: BooleanLike = Field(
        default="", description="Check if sports specific training is ordered"
    )

    other: str = Field(
        default="",
        description=(
            "Specify any other treatments or instructions not listed above .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class SpecialInstructions(BaseModel):
    """Additional instructions from the physician"""

    special_instructions: str = Field(
        default="",
        description=(
            "Any special instructions or additional notes for therapy .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PhysicianCertification(BaseModel):
    """Physician authorization and signature"""

    physicians_signature: str = Field(
        ...,
        description=(
            "Signature of the prescribing physician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    physician_signature_date: str = Field(
        ..., description="Date the physician signed the prescription"
    )  # YYYY-MM-DD format


class PhysicalTherapyOfProsperSportsMedicineAndRehabilitationCenter(BaseModel):
    """
        PHYSICAL THERAPY OF PROSPER
    SPORTS MEDICINE AND REHABILITATION CENTER

        The electronic prescription form is provided for your convenience. With respect to responding to this form, please do not send the prescription via email. Please populate, print and sign a hardcopy that may be faxed, mailed or hand delivered to the clinic.
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    plan_of_care__treatment_orders: PlanofCareTreatmentOrders = Field(
        ..., description="Plan of Care / Treatment Orders"
    )
    special_instructions: SpecialInstructions = Field(..., description="Special Instructions")
    physician_certification: PhysicianCertification = Field(
        ..., description="Physician Certification"
    )
