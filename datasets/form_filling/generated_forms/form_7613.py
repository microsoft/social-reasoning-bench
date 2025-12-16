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
            'Full legal name of the patient .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Date this prescription/form is completed"
    )  # YYYY-MM-DD format

    diagnosis: str = Field(
        ...,
        description=(
            "Primary medical diagnosis or reason for physical therapy .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    precautions: str = Field(
        default="",
        description=(
            "Any precautions, contraindications, or activity restrictions .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    frequency_times_per_week: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of therapy sessions per week"
    )

    frequency_weeks: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of weeks therapy is prescribed"
    )


class TreatmentPlan(BaseModel):
    """Requested evaluation and treatment services"""

    evaluate_treat: BooleanLike = Field(
        default="", description="Check if therapist should evaluate and treat the patient"
    )

    therapeutic_exercise: BooleanLike = Field(
        default="", description="Check to prescribe therapeutic exercise interventions"
    )

    passive_rom: BooleanLike = Field(
        default="", description="Check to include passive range of motion exercises"
    )

    active_rom: BooleanLike = Field(
        default="", description="Check to include active range of motion exercises"
    )

    active_assisted_rom: BooleanLike = Field(
        default="", description="Check to include active assisted range of motion exercises"
    )

    progressive_resistive_exercise: BooleanLike = Field(
        default="", description="Check to include progressive resistive strengthening exercises"
    )

    strengthening: BooleanLike = Field(
        default="", description="Check to include general strengthening exercises"
    )

    stabilization_program: BooleanLike = Field(
        default="", description="Check to include a stabilization program"
    )

    posture_body_mechanics: BooleanLike = Field(
        default="", description="Check to include posture and body mechanics training"
    )

    gait_training: BooleanLike = Field(default="", description="Check to include gait training")

    fall_risk_assessment: BooleanLike = Field(
        default="", description="Check to perform a fall risk assessment"
    )

    home_exercise_program: BooleanLike = Field(
        default="", description="Check to provide a home exercise program"
    )

    manual_therapy: BooleanLike = Field(
        default="", description="Check to prescribe manual therapy interventions"
    )

    soft_tissue_mobilization: BooleanLike = Field(
        default="", description="Check to include soft tissue mobilization"
    )

    joint_mobilization: BooleanLike = Field(
        default="", description="Check to include joint mobilization"
    )

    myofascial_mobilization: BooleanLike = Field(
        default="", description="Check to include myofascial mobilization"
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
        default="", description="Date the surgery was performed"
    )  # YYYY-MM-DD format

    neuromuscular_re_education: BooleanLike = Field(
        default="", description="Check to prescribe neuromuscular re-education"
    )

    balance_proprioceptive_training: BooleanLike = Field(
        default="", description="Check to include balance and proprioceptive training"
    )

    modalities: BooleanLike = Field(
        default="", description="Check to prescribe use of physical therapy modalities"
    )

    ultrasound: BooleanLike = Field(default="", description="Check to use therapeutic ultrasound")

    phonophoresis: BooleanLike = Field(default="", description="Check to use phonophoresis")

    iontophoresis: BooleanLike = Field(default="", description="Check to use iontophoresis")

    electrical_stimulation: BooleanLike = Field(
        default="", description="Check to use electrical stimulation"
    )

    mechanical_traction: BooleanLike = Field(
        default="", description="Check to use mechanical traction"
    )

    blood_flow_restriction_therapy: BooleanLike = Field(
        default="", description="Check to use blood flow restriction therapy"
    )

    sports_specific_training: BooleanLike = Field(
        default="", description="Check to include sports-specific training"
    )

    other_first_line: str = Field(
        default="",
        description=(
            "First line for specifying other treatments or instructions .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_second_line: str = Field(
        default="",
        description=(
            "Second line for additional other treatments or instructions .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class SpecialInstructions(BaseModel):
    """Additional instructions from the physician"""

    special_instructions_first_line: str = Field(
        default="",
        description=(
            "First line for any special instructions to the therapist .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    special_instructions_second_line: str = Field(
        default="",
        description=(
            "Second line for additional special instructions .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PhysicianAuthorization(BaseModel):
    """Physician certification and signature"""

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
    treatment_plan: TreatmentPlan = Field(..., description="Treatment Plan")
    special_instructions: SpecialInstructions = Field(..., description="Special Instructions")
    physician_authorization: PhysicianAuthorization = Field(
        ..., description="Physician Authorization"
    )
