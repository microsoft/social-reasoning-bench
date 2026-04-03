from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AthleteInformationVitals(BaseModel):
    """Basic identifying information and vital signs at time of exam"""

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
            'Student\'s height (include units) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    weight: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Student's weight (include units if needed)"
    )

    body_fat_optional: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Body fat percentage, if measured"
    )

    pulse: Union[float, Literal["N/A", ""]] = Field(..., description="Resting pulse rate")

    vision_right: str = Field(
        ...,
        description=(
            'Right eye visual acuity (e.g., 20/20) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    vision_left: str = Field(
        ...,
        description=(
            'Left eye visual acuity (e.g., 20/20) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    bp: str = Field(
        ...,
        description=(
            "Primary blood pressure reading (systolic/diastolic) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    bp_second_reading: str = Field(
        default="",
        description=(
            "Second blood pressure reading, if taken .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    bp_third_reading: str = Field(
        default="",
        description=(
            "Third blood pressure reading, if taken .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    pupils_equal: BooleanLike = Field(default="", description="Check if pupils are equal")

    pupils_unequal: BooleanLike = Field(default="", description="Check if pupils are unequal")

    corrected_y: BooleanLike = Field(
        default="", description="Indicate if vision is corrected (yes)"
    )

    corrected_n: BooleanLike = Field(default="", description="Indicate if vision is corrected (no)")


class GeneralMedicalExamination(BaseModel):
    """Overall medical exam findings and examiner initials"""

    medical_normal: BooleanLike = Field(default="", description="Check if medical exam is normal")

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

    appearance_normal: BooleanLike = Field(default="", description="Check if appearance is normal")

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
        default="", description="Check if eyes, ears, throat, and nose are normal"
    )

    eyes_ears_throat_nose_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal findings for eyes, ears, throat, or nose .If you cannot "
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

    hearing_normal: BooleanLike = Field(default="", description="Check if hearing is normal")

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
        default="", description="Check if lymph nodes are normal"
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

    heart_normal: BooleanLike = Field(default="", description="Check if heart exam is normal")

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
        default="", description="Check if no abnormal heart murmurs are present"
    )

    murmurs_abnormal_findings: str = Field(
        default="",
        description=(
            'Describe any abnormal heart murmurs .If you cannot fill this, write "N/A". '
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

    pulses_normal: BooleanLike = Field(
        default="", description="Check if peripheral pulses are normal"
    )

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

    lungs_normal: BooleanLike = Field(default="", description="Check if lung exam is normal")

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

    abdomen_normal: BooleanLike = Field(default="", description="Check if abdominal exam is normal")

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
        default="", description="Check if genitourinary and skin exam is normal"
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
            "Examiner initials for genitourinary & skin section .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class MusculoskeletalExamination(BaseModel):
    """Musculoskeletal system exam findings and examiner initials"""

    musculoskeletal_normal: BooleanLike = Field(
        default="", description="Check if musculoskeletal exam is normal"
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

    neck_normal: BooleanLike = Field(default="", description="Check if neck exam is normal")

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

    back_normal: BooleanLike = Field(default="", description="Check if back exam is normal")

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
        default="", description="Check if shoulder and arm exam is normal"
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
        default="", description="Check if elbow and forearm exam is normal"
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
        default="", description="Check if wrist, hands, and fingers exam is normal"
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
        default="", description="Check if hip and thigh exam is normal"
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

    knee_normal: BooleanLike = Field(default="", description="Check if knee exam is normal")

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
        default="", description="Check if leg and ankle exam is normal"
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
        default="", description="Check if foot and toes exam is normal"
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


class AssessmentNotesClearance(BaseModel):
    """Overall notes, sports clearance status, and recommendations"""

    notes: str = Field(
        default="",
        description=(
            'Additional notes from the examiner .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    cleared_without_restriction: BooleanLike = Field(
        default="", description="Indicate if the student is cleared without restriction"
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
        default="", description="Indicate if the student is not cleared for all sports"
    )

    not_cleared_for_certain_sports: str = Field(
        default="",
        description=(
            "List specific sports for which the student is not cleared .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    not_cleared_reason: str = Field(
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


class PhysicianInformationSignature(BaseModel):
    """Examining provider’s information and signature"""

    name_of_physician_print_type: str = Field(
        ...,
        description=(
            'Physician\'s printed or typed name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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
            "Physician's signature with credentials .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AnnualPreparticipationPhysicalExamination202122(BaseModel):
    """
    2021-22 ANNUAL PREPARTICIPATION PHYSICAL EXAMINATION

    ''
    """

    athlete_information__vitals: AthleteInformationVitals = Field(
        ..., description="Athlete Information & Vitals"
    )
    general_medical_examination: GeneralMedicalExamination = Field(
        ..., description="General Medical Examination"
    )
    musculoskeletal_examination: MusculoskeletalExamination = Field(
        ..., description="Musculoskeletal Examination"
    )
    assessment_notes__clearance: AssessmentNotesClearance = Field(
        ..., description="Assessment Notes & Clearance"
    )
    physician_information__signature: PhysicianInformationSignature = Field(
        ..., description="Physician Information & Signature"
    )
