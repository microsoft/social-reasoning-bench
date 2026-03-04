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

    date: str = Field(
        ..., description="Date this prescription/form is completed"
    )  # YYYY-MM-DD format

    diagnosis: str = Field(
        ...,
        description=(
            'Primary medical/therapy diagnosis .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    precautions: str = Field(
        default="",
        description=(
            "Any special precautions or contraindications for therapy .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    frequency_times_per_week: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of therapy sessions per week"
    )

    frequency_weeks: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of weeks therapy is prescribed"
    )


class PlanofCareTreatmentOrders(BaseModel):
    """Therapy orders and selected interventions"""

    evaluate_treat: BooleanLike = Field(
        default="", description="Check if the therapist should evaluate and treat the patient"
    )

    therapeutic_exercise: BooleanLike = Field(
        default="", description="Order for therapeutic exercise interventions"
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
        default="", description="Include progressive resistive exercise program"
    )

    strengthening: BooleanLike = Field(default="", description="Include strengthening exercises")

    stabilization_program: BooleanLike = Field(
        default="", description="Include stabilization program activities"
    )

    posture_body_mechanics: BooleanLike = Field(
        default="", description="Include training in posture and body mechanics"
    )

    gait_training: BooleanLike = Field(
        default="", description="Include gait training interventions"
    )

    fall_risk_assessment: BooleanLike = Field(
        default="", description="Order for fall risk assessment"
    )

    home_exercise_program: BooleanLike = Field(
        default="", description="Include development/instruction of a home exercise program"
    )

    manual_therapy: BooleanLike = Field(
        default="", description="Order for manual therapy interventions"
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

    post_operative_rehabilitation_protocol_for: str = Field(
        default="",
        description=(
            "Specify the surgery or body part for the post-operative rehabilitation "
            'protocol .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    date_of_surgery: str = Field(
        default="", description="Date the surgery was performed"
    )  # YYYY-MM-DD format

    neuromuscular_re_education: BooleanLike = Field(
        default="", description="Order for neuromuscular re-education interventions"
    )

    balance_proprioceptive_training: BooleanLike = Field(
        default="", description="Include balance and proprioceptive training"
    )

    modalities: BooleanLike = Field(
        default="", description="Order for use of physical therapy modalities"
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
        default="", description="Include blood flow restriction therapy"
    )

    sports_specific_training: BooleanLike = Field(
        default="", description="Include sports-specific training activities"
    )

    other: str = Field(
        default="",
        description=(
            "Specify any other ordered treatments or instructions .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SpecialInstructions(BaseModel):
    """Additional instructions from the physician"""

    special_instructions_line_1: str = Field(
        default="",
        description=(
            "First line of any special instructions for therapy .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    special_instructions_line_2: str = Field(
        default="",
        description=(
            "Second line of any special instructions for therapy .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PhysicianAuthorization(BaseModel):
    """Physician certification and signature"""

    physicians_signature: str = Field(
        ...,
        description=(
            'Signature of the ordering physician .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    physician_date: str = Field(
        ..., description="Date the physician signed the order"
    )  # YYYY-MM-DD format


class PhysicalTherapyOfProsperSportsMedicineAndRehabilitationCenter(BaseModel):
    """
        PHYSICAL THERAPY
    OF PROSPER
    SPORTS MEDICINE AND REHABILITATION CENTER

        The electronic prescription form is provided for your convenience. With respect to responding to this form, please do not send the prescription via email. Please populate, print and sign a hardcopy that may be faxed, mailed or hand delivered to the clinic.
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    plan_of_care__treatment_orders: PlanofCareTreatmentOrders = Field(
        ..., description="Plan of Care / Treatment Orders"
    )
    special_instructions: SpecialInstructions = Field(..., description="Special Instructions")
    physician_authorization: PhysicianAuthorization = Field(
        ..., description="Physician Authorization"
    )
