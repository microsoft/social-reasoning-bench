from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ParticipantInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Basic information about the participant"""

    name: str = Field(
        ...,
        description=(
            "Full legal name of the participant .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    date_of_birth: str = Field(
        ...,
        description="Date of birth (MM/DD/YYYY)"
    )  # YYYY-MM-DD format

    age: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Age in years"
    )

    sex: Literal["Male", "Female", "Other", "N/A", ""] = Field(
        ...,
        description="Sex of the participant"
    )

    height: str = Field(
        ...,
        description=(
            "Height (in inches or centimeters) .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    weight: str = Field(
        ...,
        description=(
            "Weight (in pounds or kilograms) .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    body_fat_percent_optional: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Percent body fat (optional)"
    )

    pulse: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Pulse rate (beats per minute)"
    )

    bp_systolic_1: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="First systolic blood pressure reading"
    )

    bp_diastolic_1: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="First diastolic blood pressure reading"
    )

    bp_systolic_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Second systolic blood pressure reading"
    )

    bp_diastolic_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Second diastolic blood pressure reading"
    )

    bp_systolic_3: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Third systolic blood pressure reading"
    )

    bp_diastolic_3: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Third diastolic blood pressure reading"
    )

    vision_r20: str = Field(
        ...,
        description=(
            "Right eye vision (20/___) .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    vision_l20: str = Field(
        ...,
        description=(
            "Left eye vision (20/___) .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    corrected_y: BooleanLike = Field(
        ...,
        description="Vision corrected (Yes)"
    )

    corrected_n: BooleanLike = Field(
        ...,
        description="Vision corrected (No)"
    )

    pupils_equal: BooleanLike = Field(
        ...,
        description="Pupils are equal"
    )

    pupils_unequal: BooleanLike = Field(
        ...,
        description="Pupils are unequal"
    )


class MedicalExamination(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Medical assessment and findings"""

    appearance_normal: BooleanLike = Field(
        ...,
        description="Appearance is normal"
    )

    appearance_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for appearance .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    appearance_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for appearance .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    eyes_ears_throat_nose_normal: BooleanLike = Field(
        ...,
        description="Eyes/Ears/Throat/Nose are normal"
    )

    eyes_ears_throat_nose_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for Eyes/Ears/Throat/Nose .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    eyes_ears_throat_nose_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for Eyes/Ears/Throat/Nose .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    hearing_normal: BooleanLike = Field(
        ...,
        description="Hearing is normal"
    )

    hearing_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for hearing .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    hearing_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for hearing .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    lymph_nodes_normal: BooleanLike = Field(
        ...,
        description="Lymph nodes are normal"
    )

    lymph_nodes_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for lymph nodes .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    lymph_nodes_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for lymph nodes .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    heart_normal: BooleanLike = Field(
        ...,
        description="Heart is normal"
    )

    heart_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for heart .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    heart_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for heart .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    murmurs_normal: BooleanLike = Field(
        ...,
        description="Murmurs are normal"
    )

    murmurs_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for murmurs .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    murmurs_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for murmurs .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    pulses_normal: BooleanLike = Field(
        ...,
        description="Pulses are normal"
    )

    pulses_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for pulses .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    pulses_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for pulses .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    lungs_normal: BooleanLike = Field(
        ...,
        description="Lungs are normal"
    )

    lungs_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for lungs .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    lungs_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for lungs .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    abdomen_normal: BooleanLike = Field(
        ...,
        description="Abdomen is normal"
    )

    abdomen_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for abdomen .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    abdomen_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for abdomen .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    genitourinary_and_normal: BooleanLike = Field(
        ...,
        description="Genitourinary is normal"
    )

    genitourinary_and_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for genitourinary .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    genitourinary_and_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for genitourinary .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    skin_normal: BooleanLike = Field(
        ...,
        description="Skin is normal"
    )

    skin_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for skin .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    skin_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for skin .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )


class MusculoskeletalExamination(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Musculoskeletal assessment and findings"""

    neck_normal: BooleanLike = Field(
        ...,
        description="Neck is normal"
    )

    neck_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for neck .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    neck_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for neck .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    back_normal: BooleanLike = Field(
        ...,
        description="Back is normal"
    )

    back_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for back .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    back_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for back .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    shoulder_arm_normal: BooleanLike = Field(
        ...,
        description="Shoulder/Arm is normal"
    )

    shoulder_arm_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for shoulder/arm .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    shoulder_arm_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for shoulder/arm .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    elbow_forearm_normal: BooleanLike = Field(
        ...,
        description="Elbow/Forearm is normal"
    )

    elbow_forearm_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for elbow/forearm .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    elbow_forearm_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for elbow/forearm .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    wrist_hands_fingers_normal: BooleanLike = Field(
        ...,
        description="Wrist/Hands/Fingers are normal"
    )

    wrist_hands_fingers_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for wrist/hands/fingers .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    wrist_hands_fingers_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for wrist/hands/fingers .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    hip_thigh_normal: BooleanLike = Field(
        ...,
        description="Hip/Thigh is normal"
    )

    hip_thigh_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for hip/thigh .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    hip_thigh_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for hip/thigh .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    knee_normal: BooleanLike = Field(
        ...,
        description="Knee is normal"
    )

    knee_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for knee .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    knee_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for knee .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    leg_ankle_normal: BooleanLike = Field(
        ...,
        description="Leg/Ankle is normal"
    )

    leg_ankle_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for leg/ankle .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    leg_ankle_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for leg/ankle .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    foot_toes_normal: BooleanLike = Field(
        ...,
        description="Foot/Toes are normal"
    )

    foot_toes_abnormal_findings: str = Field(
        ...,
        description=(
            "Abnormal findings for foot/toes .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    foot_toes_initials: str = Field(
        ...,
        description=(
            "Initials of examiner for foot/toes .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class ClearanceandRecommendations(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Notes, clearance status, recommendations, and physician information"""

    notes: str = Field(
        ...,
        description=(
            "Additional notes from examiner .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    cleared_without_restriction: BooleanLike = Field(
        ...,
        description="Participant is cleared without restriction"
    )

    cleared_with_following_restriction: str = Field(
        ...,
        description=(
            "Participant is cleared with specific restrictions .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    not_cleared_for_all_sports: BooleanLike = Field(
        ...,
        description="Participant is not cleared for any sports"
    )

    not_cleared_for_certain_sports: str = Field(
        ...,
        description=(
            "List of sports participant is not cleared for .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    not_cleared_for_reason: str = Field(
        ...,
        description=(
            "Reason participant is not cleared .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    recommendations: str = Field(
        ...,
        description=(
            "Recommendations from examiner .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    name_of_physician_print_type: str = Field(
        ...,
        description=(
            "Name of physician (printed or typed) .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    exam_date: str = Field(
        ...,
        description="Date of examination"
    )  # YYYY-MM-DD format

    address: str = Field(
        ...,
        description=(
            "Physician's address .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    phone: str = Field(
        ...,
        description=(
            "Physician's phone number .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    signature_of_physician: str = Field(
        ...,
        description=(
            "Signature of physician .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )


class AnnualPreparticipationPhysicalExamination202122(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    2021-22 ANNUAL PREPARTICIPATION PHYSICAL EXAMINATION

    ''
    """

    participant_information: ParticipantInformation = Field(
        ...,
        description="Participant Information"
    )
    medical_examination: MedicalExamination = Field(
        ...,
        description="Medical Examination"
    )
    musculoskeletal_examination: MusculoskeletalExamination = Field(
        ...,
        description="Musculoskeletal Examination"
    )
    clearance_and_recommendations: ClearanceandRecommendations = Field(
        ...,
        description="Clearance and Recommendations"
    )