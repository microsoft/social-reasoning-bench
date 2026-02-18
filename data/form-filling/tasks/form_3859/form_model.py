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
    """Basic identifying and vital information for the participant"""

    name: str = Field(
        ...,
        description=(
            'Athlete\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Athlete's date of birth")  # YYYY-MM-DD format

    age: Union[float, Literal["N/A", ""]] = Field(..., description="Athlete's age in years")

    sex: str = Field(
        ...,
        description=(
            "Sex of the athlete as recorded for medical purposes .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    height: str = Field(
        ...,
        description=(
            "Athlete's height (include units, e.g., ft/in or cm) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    weight: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Athlete's weight (specify units if needed)"
    )

    body_fat_optional: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated or measured body fat percentage (optional)"
    )

    pulse: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Resting pulse rate in beats per minute"
    )

    bp_systolic_first_reading: Union[float, Literal["N/A", ""]] = Field(
        ..., description="First blood pressure reading, systolic (top number)"
    )

    bp_diastolic_first_reading: Union[float, Literal["N/A", ""]] = Field(
        ..., description="First blood pressure reading, diastolic (bottom number)"
    )

    bp_systolic_second_reading: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Second blood pressure reading, systolic (top number) inside parentheses",
    )

    bp_diastolic_second_reading: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Second blood pressure reading, diastolic (bottom number) inside parentheses",
    )

    bp_third_value_first_reading: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "First additional BP-related value (e.g., heart rate or position) inside parentheses"
        ),
    )

    bp_third_value_second_reading: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Second additional BP-related value inside parentheses"
    )

    bp_third_value_third_reading: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Third additional BP-related value inside parentheses"
    )

    vision_r20: str = Field(
        ...,
        description=(
            "Right eye visual acuity (denominator of 20/ value) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    vision_l20: str = Field(
        ...,
        description=(
            "Left eye visual acuity (denominator of 20/ value) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    vision_corrected_y: BooleanLike = Field(
        ..., description="Check if vision is corrected (e.g., with glasses or contacts)"
    )

    vision_corrected_n: BooleanLike = Field(..., description="Check if vision is not corrected")

    pupils_equal: BooleanLike = Field(..., description="Indicate if pupils are equal")

    pupils_unequal: BooleanLike = Field(..., description="Indicate if pupils are unequal")


class MedicalExamination(BaseModel):
    """Physical examination findings and examiner initials"""

    appearance_normal: BooleanLike = Field(..., description="Mark if general appearance is normal")

    appearance_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal findings related to appearance .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    appearance_initials: str = Field(
        default="",
        description=(
            "Examiner initials for appearance assessment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    eyes_ears_throat_nose_normal: BooleanLike = Field(
        ..., description="Mark if eyes, ears, throat, and nose exam is normal"
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
            "Examiner initials for eyes/ears/throat/nose assessment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hearing_normal: BooleanLike = Field(..., description="Mark if hearing exam is normal")

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
            "Examiner initials for hearing assessment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    lymph_nodes_normal: BooleanLike = Field(..., description="Mark if lymph node exam is normal")

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
            "Examiner initials for lymph node assessment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    heart_normal: BooleanLike = Field(..., description="Mark if heart exam is normal")

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
            "Examiner initials for heart assessment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    murmurs_normal: BooleanLike = Field(
        ..., description="Mark if no abnormal heart murmurs are present"
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
            "Examiner initials for murmur assessment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    pulses_normal: BooleanLike = Field(..., description="Mark if peripheral pulses are normal")

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
            "Examiner initials for pulse assessment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    lungs_normal: BooleanLike = Field(..., description="Mark if lung exam is normal")

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
            'Examiner initials for lung assessment .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    abdomen_normal: BooleanLike = Field(..., description="Mark if abdominal exam is normal")

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
            "Examiner initials for abdominal assessment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    genitourinary_normal: BooleanLike = Field(
        default="", description="Mark if genitourinary exam is normal"
    )

    genitourinary_abnormal_findings: str = Field(
        default="",
        description=(
            "Describe any abnormal genitourinary findings .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    genitourinary_initials: str = Field(
        default="",
        description=(
            "Examiner initials for genitourinary assessment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    skin_normal: BooleanLike = Field(..., description="Mark if skin exam is normal")

    skin_abnormal_findings: str = Field(
        default="",
        description=(
            'Describe any abnormal skin findings .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    skin_initials: str = Field(
        default="",
        description=(
            'Examiner initials for skin assessment .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    musculoskeletal_normal: BooleanLike = Field(
        ..., description="Mark if overall musculoskeletal exam is normal"
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
            "Examiner initials for musculoskeletal assessment .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    neck_normal: BooleanLike = Field(..., description="Mark if neck exam is normal")

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
            'Examiner initials for neck assessment .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    back_normal: BooleanLike = Field(..., description="Mark if back exam is normal")

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
            'Examiner initials for back assessment .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    shoulder_arm_normal: BooleanLike = Field(
        ..., description="Mark if shoulder and arm exam is normal"
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
            "Examiner initials for shoulder/arm assessment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    elbow_forearm_normal: BooleanLike = Field(
        ..., description="Mark if elbow and forearm exam is normal"
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
            "Examiner initials for elbow/forearm assessment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    wrist_hands_fingers_normal: BooleanLike = Field(
        ..., description="Mark if wrist, hand, and finger exam is normal"
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
            "Examiner initials for wrist/hands/fingers assessment .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hip_thigh_normal: BooleanLike = Field(..., description="Mark if hip and thigh exam is normal")

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
            "Examiner initials for hip/thigh assessment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    knee_normal: BooleanLike = Field(..., description="Mark if knee exam is normal")

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
            'Examiner initials for knee assessment .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    leg_ankle_normal: BooleanLike = Field(..., description="Mark if leg and ankle exam is normal")

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
            "Examiner initials for leg/ankle assessment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    foot_toes_normal: BooleanLike = Field(..., description="Mark if foot and toe exam is normal")

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
            "Examiner initials for foot/toes assessment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    notes: str = Field(
        default="",
        description=(
            "Additional notes or comments from the examiner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ClearanceandRecommendations(BaseModel):
    """Sports participation clearance, restrictions, and recommendations"""

    cleared_without_restriction: BooleanLike = Field(
        ..., description="Indicate if the athlete is fully cleared without restriction"
    )

    cleared_with_following_restriction: str = Field(
        default="",
        description=(
            "Specify any restrictions under which the athlete is cleared .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    not_cleared_for_all_sports: BooleanLike = Field(
        ..., description="Indicate if the athlete is not cleared for any sports"
    )

    not_cleared_for_certain_sports: BooleanLike = Field(
        default="", description="Indicate if the athlete is not cleared only for certain sports"
    )

    certain_sports: str = Field(
        default="",
        description=(
            "List specific sports for which the athlete is not cleared .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reason: str = Field(
        default="",
        description=(
            "Reason the athlete is not cleared or has restrictions .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    recommendations: str = Field(
        default="",
        description=(
            "Additional recommendations from the physician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PhysicianInformation(BaseModel):
    """Physician identification and contact details"""

    name_of_physician_print_type: str = Field(
        ...,
        description=(
            "Printed or typed full name of the examining physician .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    exam_date: str = Field(
        ..., description="Date the physical examination was performed"
    )  # YYYY-MM-DD format

    address: str = Field(
        default="",
        description=(
            "Mailing address of the physician or clinic .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        default="",
        description=(
            "Contact phone number for the physician or clinic .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_physician: str = Field(
        ...,
        description=(
            "Signature of the examining physician with credentials .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AnnualPreparticipationPhysicalExamination202122(BaseModel):
    """
    2021-22 ANNUAL PREPARTICIPATION PHYSICAL EXAMINATION

    ''
    """

    athlete_information: AthleteInformation = Field(..., description="Athlete Information")
    medical_examination: MedicalExamination = Field(..., description="Medical Examination")
    clearance_and_recommendations: ClearanceandRecommendations = Field(
        ..., description="Clearance and Recommendations"
    )
    physician_information: PhysicianInformation = Field(..., description="Physician Information")
