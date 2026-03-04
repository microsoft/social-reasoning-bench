from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AthleteInformation(BaseModel):
    """Basic information about the athlete"""

    name: str = Field(
        ...,
        description=(
            'Student\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Student's date of birth")  # YYYY-MM-DD format

    age: Union[float, Literal["N/A", ""]] = Field(..., description="Student's age in years")

    sex: str = Field(
        ...,
        description=(
            'Student\'s sex .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    height: str = Field(
        ...,
        description=(
            "Student's height (include units, e.g., inches) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    weight: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Student's weight (include units if applicable)"
    )

    body_fat_optional: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Body fat percentage, if measured"
    )

    pulse: Union[float, Literal["N/A", ""]] = Field(..., description="Resting pulse rate")

    bp: str = Field(
        ...,
        description=(
            "Blood pressure readings (may include multiple values) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    vision_r20: str = Field(
        ...,
        description=(
            'Right eye visual acuity (20/___) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    vision_l20: str = Field(
        ...,
        description=(
            'Left eye visual acuity (20/___) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    vision_corrected_y: BooleanLike = Field(
        default="", description="Check if vision is corrected (e.g., with glasses or contacts)"
    )

    vision_corrected_n: BooleanLike = Field(
        default="", description="Check if vision is not corrected"
    )


class PhysicalExaminationGeneralMedical(BaseModel):
    """General medical examination findings"""

    medical_normal: BooleanLike = Field(
        default="", description="Indicate if medical exam is normal"
    )

    medical_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal medical findings .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medical_initials: str = Field(
        default="",
        description=(
            'Examiner initials for medical section .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    appearance_normal: BooleanLike = Field(
        default="", description="Indicate if appearance is normal"
    )

    appearance_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal appearance findings .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    appearance_initials: str = Field(
        default="",
        description=(
            "Examiner initials for appearance section .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    eyes_ears_throat_nose_normal: BooleanLike = Field(
        default="", description="Indicate if eyes, ears, throat, and nose exam is normal"
    )

    eyes_ears_throat_nose_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal findings for eyes, ears, throat, and nose .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    eyes_ears_throat_nose_initials: str = Field(
        default="",
        description=(
            "Examiner initials for eyes/ears/throat/nose section .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hearing_normal: BooleanLike = Field(
        default="", description="Indicate if hearing exam is normal"
    )

    hearing_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal hearing findings .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    hearing_initials: str = Field(
        default="",
        description=(
            'Examiner initials for hearing section .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    lymph_nodes_normal: BooleanLike = Field(
        default="", description="Indicate if lymph nodes exam is normal"
    )

    lymph_nodes_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal lymph node findings .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    lymph_nodes_initials: str = Field(
        default="",
        description=(
            "Examiner initials for lymph nodes section .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    heart_normal: BooleanLike = Field(default="", description="Indicate if heart exam is normal")

    heart_abnormal_findings: str = Field(
        default="",
        description=(
            'Describe any abnormal heart findings .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    heart_initials: str = Field(
        default="",
        description=(
            'Examiner initials for heart section .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    murmurs_normal: BooleanLike = Field(
        default="", description="Indicate if murmur assessment is normal"
    )

    murmurs_abnormal_findings: str = Field(
        default="",
        description=(
            'Describe any abnormal murmur findings .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    murmurs_initials: str = Field(
        default="",
        description=(
            'Examiner initials for murmurs section .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    pulses_normal: BooleanLike = Field(default="", description="Indicate if pulses exam is normal")

    pulses_abnormal_findings: str = Field(
        default="",
        description=(
            'Describe any abnormal pulse findings .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    pulses_initials: str = Field(
        default="",
        description=(
            'Examiner initials for pulses section .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    lungs_normal: BooleanLike = Field(default="", description="Indicate if lung exam is normal")

    lungs_abnormal_findings: str = Field(
        default="",
        description=(
            'Describe any abnormal lung findings .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    lungs_initials: str = Field(
        default="",
        description=(
            'Examiner initials for lungs section .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    abdomen_normal: BooleanLike = Field(
        default="", description="Indicate if abdominal exam is normal"
    )

    abdomen_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal abdominal findings .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    abdomen_initials: str = Field(
        default="",
        description=(
            'Examiner initials for abdomen section .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    genitourinary_skin_normal: BooleanLike = Field(
        default="", description="Indicate if genitourinary and skin exam is normal"
    )

    genitourinary_skin_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal genitourinary or skin findings .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    genitourinary_skin_initials: str = Field(
        default="",
        description=(
            "Examiner initials for genitourinary and skin section .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PhysicalExaminationMusculoskeletal(BaseModel):
    """Musculoskeletal examination findings"""

    musculoskeletal_normal: BooleanLike = Field(
        default="", description="Indicate if overall musculoskeletal exam is normal"
    )

    musculoskeletal_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal musculoskeletal findings .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    musculoskeletal_initials: str = Field(
        default="",
        description=(
            "Examiner initials for musculoskeletal section .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    neck_normal: BooleanLike = Field(default="", description="Indicate if neck exam is normal")

    neck_abnormal_findings: str = Field(
        default="",
        description=(
            'Describe any abnormal neck findings .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    neck_initials: str = Field(
        default="",
        description=(
            'Examiner initials for neck section .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    back_normal: BooleanLike = Field(default="", description="Indicate if back exam is normal")

    back_abnormal_findings: str = Field(
        default="",
        description=(
            'Describe any abnormal back findings .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    back_initials: str = Field(
        default="",
        description=(
            'Examiner initials for back section .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    shoulder_arm_normal: BooleanLike = Field(
        default="", description="Indicate if shoulder and arm exam is normal"
    )

    shoulder_arm_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal shoulder or arm findings .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    shoulder_arm_initials: str = Field(
        default="",
        description=(
            "Examiner initials for shoulder/arm section .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    elbow_forearm_normal: BooleanLike = Field(
        default="", description="Indicate if elbow and forearm exam is normal"
    )

    elbow_forearm_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal elbow or forearm findings .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    elbow_forearm_initials: str = Field(
        default="",
        description=(
            "Examiner initials for elbow/forearm section .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    wrist_hands_fingers_normal: BooleanLike = Field(
        default="", description="Indicate if wrist, hands, and fingers exam is normal"
    )

    wrist_hands_fingers_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal wrist, hand, or finger findings .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    wrist_hands_fingers_initials: str = Field(
        default="",
        description=(
            "Examiner initials for wrist/hands/fingers section .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hip_thigh_normal: BooleanLike = Field(
        default="", description="Indicate if hip and thigh exam is normal"
    )

    hip_thigh_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal hip or thigh findings .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    hip_thigh_initials: str = Field(
        default="",
        description=(
            "Examiner initials for hip/thigh section .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    knee_normal: BooleanLike = Field(default="", description="Indicate if knee exam is normal")

    knee_abnormal_findings: str = Field(
        default="",
        description=(
            'Describe any abnormal knee findings .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    knee_initials: str = Field(
        default="",
        description=(
            'Examiner initials for knee section .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    leg_ankle_normal: BooleanLike = Field(
        default="", description="Indicate if leg and ankle exam is normal"
    )

    leg_ankle_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal leg or ankle findings .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    leg_ankle_initials: str = Field(
        default="",
        description=(
            "Examiner initials for leg/ankle section .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    foot_toes_normal: BooleanLike = Field(
        default="", description="Indicate if foot and toes exam is normal"
    )

    foot_toes_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal foot or toe findings .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    foot_toes_initials: str = Field(
        default="",
        description=(
            "Examiner initials for foot/toes section .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ExamNotesandClearance(BaseModel):
    """Overall notes, clearance status, and recommendations"""

    notes: str = Field(
        default="",
        description=(
            'Additional notes from the examiner .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    cleared_without_restriction: BooleanLike = Field(
        default="", description="Check if the student is cleared for all sports without restriction"
    )

    cleared_with_following_restriction: str = Field(
        default="",
        description=(
            "Specify any restrictions if cleared with limitations .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    not_cleared_for_all_sports: BooleanLike = Field(
        default="", description="Check if the student is not cleared for any sports"
    )

    not_cleared_for_certain_sports: str = Field(
        default="",
        description=(
            "List specific sports for which the student is not cleared .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    not_cleared_for_reason: str = Field(
        default="",
        description=(
            'Reason the student is not cleared .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    recommendations: str = Field(
        default="",
        description=(
            "Additional recommendations from the examiner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PhysicianInformation(BaseModel):
    """Physician identification and contact information"""

    name_of_physician_print_type: str = Field(
        ...,
        description=(
            "Physician's full printed or typed name .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    exam_date: str = Field(..., description="Date of the physical examination")  # YYYY-MM-DD format

    address: str = Field(
        default="",
        description=(
            'Physician\'s office address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        default="",
        description=(
            'Physician\'s contact phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_physician: str = Field(
        ...,
        description=(
            "Signature of the examining physician or provider .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AnnualPreparticipationPhysicalExamination202122(BaseModel):
    """
    2021-22 ANNUAL PREPARTICIPATION PHYSICAL EXAMINATION

    ''
    """

    athlete_information: AthleteInformation = Field(..., description="Athlete Information")
    physical_examination___general__medical: PhysicalExaminationGeneralMedical = Field(
        ..., description="Physical Examination – General & Medical"
    )
    physical_examination___musculoskeletal: PhysicalExaminationMusculoskeletal = Field(
        ..., description="Physical Examination – Musculoskeletal"
    )
    exam_notes_and_clearance: ExamNotesandClearance = Field(
        ..., description="Exam Notes and Clearance"
    )
    physician_information: PhysicianInformation = Field(..., description="Physician Information")
