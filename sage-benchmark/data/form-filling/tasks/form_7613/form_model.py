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
    """Basic patient and visit details"""

    patient_name: str = Field(
        ...,
        description=(
            'Full name of the patient .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_top: str = Field(
        ..., description="Date this prescription form is completed"
    )  # YYYY-MM-DD format

    diagnosis: str = Field(
        ...,
        description=(
            "Primary medical diagnosis related to this therapy referral .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    precautions: str = Field(
        default="",
        description=(
            "Any special precautions or contraindications for treatment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    frequency_times_per_week: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of treatment sessions per week"
    )

    frequency_weeks: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of weeks for the treatment plan"
    )


class TreatmentPlan(BaseModel):
    """Selected therapy services and modalities"""

    evaluate_treat: BooleanLike = Field(
        default="", description="Check if the therapist should evaluate and treat the patient"
    )

    therapeutic_exercise: BooleanLike = Field(
        default="", description="Check to order therapeutic exercise interventions"
    )

    passive_rom: BooleanLike = Field(
        default="", description="Include passive range of motion exercises"
    )

    active_rom: BooleanLike = Field(
        default="", description="Include active range of motion exercises"
    )

    active_assisted_rom: BooleanLike = Field(
        default="", description="Include active assisted range of motion exercises"
    )

    progressive_resistive_exercise: BooleanLike = Field(
        default="", description="Include progressive resistive strengthening exercises"
    )

    strengthening: BooleanLike = Field(
        default="", description="Include general strengthening exercises"
    )

    stabilization_program: BooleanLike = Field(
        default="", description="Include a stabilization program as part of treatment"
    )

    posture_body_mechanics: BooleanLike = Field(
        default="", description="Include training in posture and body mechanics"
    )

    gait_training: BooleanLike = Field(
        default="", description="Include gait training interventions"
    )

    fall_risk_assessment: BooleanLike = Field(
        default="", description="Include assessment of fall risk"
    )

    home_exercise_program: BooleanLike = Field(
        default="", description="Provide a home exercise program for the patient"
    )

    manual_therapy: BooleanLike = Field(
        default="", description="Check to order manual therapy interventions"
    )

    soft_tissue_mobilization: BooleanLike = Field(
        default="", description="Include soft tissue mobilization techniques"
    )

    joint_mobilization: BooleanLike = Field(
        default="", description="Include joint mobilization techniques"
    )

    myofascial_mobilization: BooleanLike = Field(
        default="", description="Include myofascial mobilization techniques"
    )

    neuromuscular_re_education: BooleanLike = Field(
        default="", description="Check to order neuromuscular re-education interventions"
    )

    balance_proprioceptive_training: BooleanLike = Field(
        default="", description="Include balance and proprioceptive training"
    )

    modalities: BooleanLike = Field(
        default="", description="Check to order use of physical therapy modalities"
    )

    ultrasound: BooleanLike = Field(
        default="", description="Include therapeutic ultrasound modality"
    )

    phonophoresis: BooleanLike = Field(default="", description="Include phonophoresis modality")

    iontophoresis: BooleanLike = Field(default="", description="Include iontophoresis modality")

    electrical_stimulation: BooleanLike = Field(
        default="", description="Include electrical stimulation modality"
    )

    mechanical_traction: BooleanLike = Field(
        default="", description="Include mechanical traction modality"
    )

    blood_flow_restriction_therapy: BooleanLike = Field(
        default="", description="Include blood flow restriction therapy modality"
    )

    post_operative_rehabilitation_protocol_for: str = Field(
        default="",
        description=(
            "Specify the surgery or condition for the post-operative rehabilitation "
            'protocol .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    date_of_surgery: str = Field(
        default="", description="Date the surgery was performed"
    )  # YYYY-MM-DD format

    sports_specific_training: BooleanLike = Field(
        default="", description="Check to include sports-specific training"
    )

    other: str = Field(
        default="",
        description=(
            "Specify any other treatment not listed above .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class SpecialInstructions(BaseModel):
    """Additional instructions from the physician"""

    special_instructions: str = Field(
        default="",
        description=(
            "Any additional special instructions for therapy .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PhysicianAuthorization(BaseModel):
    """Physician certification and signature"""

    physicians_signature: str = Field(
        ...,
        description=(
            "Signature of the referring physician certifying medical necessity .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_bottom: str = Field(
        ..., description="Date the physician signs this prescription"
    )  # YYYY-MM-DD format


class DoNotEmailPrescription(BaseModel):
    """
    DO NOT EMAIL PRESCRIPTION

    The electronic prescription form is provided for your convenience. With respect to responding to this form, please do not send the prescription via email. Please populate, print and sign a hardcopy that may be faxed, mailed or hand delivered to the clinic.
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    treatment_plan: TreatmentPlan = Field(..., description="Treatment Plan")
    special_instructions: SpecialInstructions = Field(..., description="Special Instructions")
    physician_authorization: PhysicianAuthorization = Field(
        ..., description="Physician Authorization"
    )
