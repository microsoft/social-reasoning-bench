from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class IdentifyingInformation(BaseModel):
    """Basic student and parent/guardian details"""

    student_name: str = Field(
        ...,
        description=(
            'Full legal name of the student .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    gender_m: BooleanLike = Field(..., description="Check if the student’s gender is male")

    gender_f: BooleanLike = Field(..., description="Check if the student’s gender is female")

    grade: str = Field(
        ...,
        description=(
            'Student’s current grade level .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Student’s date of birth")  # YYYY-MM-DD format

    age_years: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Student’s age in completed years"
    )

    age_months: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Additional months beyond completed years of age"
    )

    preferred_language: str = Field(
        default="",
        description=(
            "Primary language spoken by the student or family .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parent_or_guardian_name: str = Field(
        ...,
        description=(
            "Name of the student’s parent or legal guardian .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class MedicalHistory(BaseModel):
    """Allergies, medications, and significant historical information"""

    allergies_line_1: str = Field(
        default="",
        description=(
            'Allergies, first line of description .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    allergies_line_2: str = Field(
        default="",
        description=(
            'Allergies, second line of description .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    allergies_line_3: str = Field(
        default="",
        description=(
            'Allergies, third line of description .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    allergies_line_4: str = Field(
        default="",
        description=(
            'Allergies, fourth line of description .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    current_prescribed_medications_line_1: str = Field(
        default="",
        description=(
            "Current prescribed medications taken daily at school, first line .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    current_prescribed_medications_line_2: str = Field(
        default="",
        description=(
            "Current prescribed medications taken daily at school, second line .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    current_prescribed_medications_line_3: str = Field(
        default="",
        description=(
            "Current prescribed medications taken daily at school, third line .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    significant_historical_information_line_1: str = Field(
        default="",
        description=(
            "Significant medical history, first line .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    significant_historical_information_line_2: str = Field(
        default="",
        description=(
            "Significant medical history, second line .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    significant_historical_information_line_3: str = Field(
        default="",
        description=(
            "Significant medical history, third line .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    significant_historical_information_line_4: str = Field(
        default="",
        description=(
            "Significant medical history, fourth line .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ScreeningResults(BaseModel):
    """Vital signs, vision, hearing, labs, and physical exam findings"""

    bp: str = Field(
        default="",
        description=(
            'Blood pressure reading .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    height_feet: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Height in whole feet"
    )

    height_inches: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Additional inches beyond whole feet of height"
    )

    weight_lbs: Union[float, Literal["N/A", ""]] = Field(default="", description="Weight in pounds")

    bmi: Union[float, Literal["N/A", ""]] = Field(default="", description="Body Mass Index value")

    bmi_percent: Union[float, Literal["N/A", ""]] = Field(default="", description="BMI percentile")

    vision_right_20: str = Field(
        default="",
        description=(
            "Right eye visual acuity (denominator of 20/x) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    vision_right_passed: BooleanLike = Field(
        default="", description="Check if right eye vision screening was passed"
    )

    vision_right_failed: BooleanLike = Field(
        default="", description="Check if right eye vision screening was failed"
    )

    vision_right_referred: BooleanLike = Field(
        default="", description="Check if right eye vision screening resulted in referral"
    )

    vision_left_20: str = Field(
        default="",
        description=(
            "Left eye visual acuity (denominator of 20/x) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    vision_left_passed: BooleanLike = Field(
        default="", description="Check if left eye vision screening was passed"
    )

    vision_left_failed: BooleanLike = Field(
        default="", description="Check if left eye vision screening was failed"
    )

    vision_left_referred: BooleanLike = Field(
        default="", description="Check if left eye vision screening resulted in referral"
    )

    hearing_right_passed: BooleanLike = Field(
        default="", description="Check if right ear hearing screening was passed"
    )

    hearing_right_failed: BooleanLike = Field(
        default="", description="Check if right ear hearing screening was failed"
    )

    hearing_right_referred: BooleanLike = Field(
        default="", description="Check if right ear hearing screening resulted in referral"
    )

    hearing_left_passed: BooleanLike = Field(
        default="", description="Check if left ear hearing screening was passed"
    )

    hearing_left_failed: BooleanLike = Field(
        default="", description="Check if left ear hearing screening was failed"
    )

    hearing_left_referred: BooleanLike = Field(
        default="", description="Check if left ear hearing screening resulted in referral"
    )

    hct_hgb: str = Field(
        default="",
        description=(
            "Optional hematocrit or hemoglobin result .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    lead: str = Field(
        default="",
        description=(
            'Optional blood lead level result .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    urinalysis: str = Field(
        default="",
        description=(
            'Optional urinalysis result .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    general_appearance_normal: BooleanLike = Field(
        default="", description="Check if general appearance is normal"
    )

    general_appearance_abnormal_description: str = Field(
        default="",
        description=(
            "Describe any abnormal findings for general appearance .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    general_appearance_refer_tx: str = Field(
        default="",
        description=(
            "Referral or treatment plan related to general appearance .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    gross_dental_normal: BooleanLike = Field(
        default="", description="Check if gross dental exam is normal"
    )

    gross_dental_abnormal_description: str = Field(
        default="",
        description=(
            "Describe any abnormal findings for teeth and gums .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    gross_dental_refer_tx: str = Field(
        default="",
        description=(
            "Referral or treatment plan related to dental findings .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    head_scalp_skin_normal: BooleanLike = Field(
        default="", description="Check if head, scalp, and skin exam is normal"
    )

    head_scalp_skin_abnormal_description: str = Field(
        default="",
        description=(
            "Describe any abnormal findings for head, scalp, or skin .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    head_scalp_skin_refer_tx: str = Field(
        default="",
        description=(
            "Referral or treatment plan related to head, scalp, or skin findings .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    eyes_ears_nose_throat_normal: BooleanLike = Field(
        default="", description="Check if eyes, ears, nose, and throat exam is normal"
    )

    eyes_ears_nose_throat_abnormal_description: str = Field(
        default="",
        description=(
            "Describe any abnormal findings for eyes, ears, nose, or throat .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    eyes_ears_nose_throat_refer_tx: str = Field(
        default="",
        description=(
            "Referral or treatment plan related to eyes, ears, nose, or throat findings .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    chest_lung_heart_normal: BooleanLike = Field(
        default="", description="Check if chest, lung, and heart exam is normal"
    )

    chest_lung_heart_abnormal_description: str = Field(
        default="",
        description=(
            "Describe any abnormal findings for chest, lungs, or heart .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    chest_lung_heart_refer_tx: str = Field(
        default="",
        description=(
            "Referral or treatment plan related to chest, lung, or heart findings .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    abdomen_genitalia_normal: BooleanLike = Field(
        default="", description="Check if abdomen and genitalia exam is normal"
    )

    abdomen_genitalia_abnormal_description: str = Field(
        default="",
        description=(
            "Describe any abnormal findings for abdomen or genitalia .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    abdomen_genitalia_refer_tx: str = Field(
        default="",
        description=(
            "Referral or treatment plan related to abdomen or genitalia findings .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    extremities_back_normal: BooleanLike = Field(
        default="", description="Check if extremities and back exam is normal"
    )

    extremities_back_abnormal_description: str = Field(
        default="",
        description=(
            "Describe any abnormal findings for extremities or back .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    extremities_back_refer_tx: str = Field(
        default="",
        description=(
            "Referral or treatment plan related to extremities or back findings .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    neuro_normal: BooleanLike = Field(
        default="", description="Check if neurological exam is normal"
    )

    neuro_abnormal_description: str = Field(
        default="",
        description=(
            "Describe any abnormal neurological findings .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    neuro_refer_tx: str = Field(
        default="",
        description=(
            "Referral or treatment plan related to neurological findings .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class PreventativeHealthCareExaminationForm(BaseModel):
    """
    PREVENTATIVE HEALTH CARE EXAMINATION FORM

    All local boards of education shall require a preventative health care examination of each child first entering a Kentucky public school within a period of twelve (12) months prior to initial admission to school and within one (1) year prior to entry to sixth grade. Local school boards may extend this time not to exceed two (2) months. (702 KAR 1:160)
    """

    identifying_information: IdentifyingInformation = Field(
        ..., description="Identifying Information"
    )
    medical_history: MedicalHistory = Field(..., description="Medical History")
    screening_results: ScreeningResults = Field(..., description="Screening Results")
