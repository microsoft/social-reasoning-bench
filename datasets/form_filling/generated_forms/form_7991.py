from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class GeneralMeasurementsandSODA(BaseModel):
    """Basic measurements and Statement of Demonstrated Ability"""

    height_cm: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Applicant's height in centimeters"
    )

    weight_kg: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Applicant's weight in kilograms"
    )

    statement_of_demonstrated_ability_soda_yes: BooleanLike = Field(
        default="",
        description="Check if a Statement of Demonstrated Ability (SODA) has been issued",
    )

    statement_of_demonstrated_ability_soda_no: BooleanLike = Field(
        default="",
        description="Check if no Statement of Demonstrated Ability (SODA) has been issued",
    )

    defect_noted: str = Field(
        default="",
        description=(
            "Describe the defect for which SODA was issued .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    soda_no: str = Field(
        default="",
        description=(
            "Statement of Demonstrated Ability (SODA) number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PhysicalExaminationSystemsReviewItems2548(BaseModel):
    """Checklist of normal/abnormal findings by body system"""

    item_25_head_face_neck_scalp_normal: BooleanLike = Field(
        default="", description="Check if head, face, neck and scalp are normal"
    )

    item_25_head_face_neck_scalp_abnormal: BooleanLike = Field(
        default="", description="Check if head, face, neck or scalp are abnormal"
    )

    item_26_nose_normal: BooleanLike = Field(default="", description="Check if nose is normal")

    item_26_nose_abnormal: BooleanLike = Field(default="", description="Check if nose is abnormal")

    item_27_sinuses_normal: BooleanLike = Field(
        default="", description="Check if sinuses are normal"
    )

    item_27_sinuses_abnormal: BooleanLike = Field(
        default="", description="Check if sinuses are abnormal"
    )

    item_28_mouth_throat_normal: BooleanLike = Field(
        default="", description="Check if mouth and throat are normal"
    )

    item_28_mouth_throat_abnormal: BooleanLike = Field(
        default="", description="Check if mouth or throat are abnormal"
    )

    item_29_ears_general_normal: BooleanLike = Field(
        default="", description="Check if general ear examination is normal"
    )

    item_29_ears_general_abnormal: BooleanLike = Field(
        default="", description="Check if general ear examination is abnormal"
    )

    item_30_ear_drums_normal: BooleanLike = Field(
        default="", description="Check if ear drums are normal"
    )

    item_30_ear_drums_abnormal: BooleanLike = Field(
        default="", description="Check if ear drums are abnormal"
    )

    item_31_eyes_general_normal: BooleanLike = Field(
        default="", description="Check if general eye examination is normal"
    )

    item_31_eyes_general_abnormal: BooleanLike = Field(
        default="", description="Check if general eye examination is abnormal"
    )

    item_32_ophthalmoscopic_normal: BooleanLike = Field(
        default="", description="Check if ophthalmoscopic findings are normal"
    )

    item_32_ophthalmoscopic_abnormal: BooleanLike = Field(
        default="", description="Check if ophthalmoscopic findings are abnormal"
    )

    item_33_pupils_normal: BooleanLike = Field(
        default="", description="Check if pupils are normal in equality and reaction"
    )

    item_33_pupils_abnormal: BooleanLike = Field(
        default="", description="Check if pupils are abnormal in equality or reaction"
    )

    item_34_ocular_motility_normal: BooleanLike = Field(
        default="", description="Check if ocular motility is normal"
    )

    item_34_ocular_motility_abnormal: BooleanLike = Field(
        default="", description="Check if ocular motility is abnormal"
    )

    item_35_lungs_chest_normal: BooleanLike = Field(
        default="", description="Check if lungs and chest are normal"
    )

    item_35_lungs_chest_abnormal: BooleanLike = Field(
        default="", description="Check if lungs or chest are abnormal"
    )

    item_36_heart_normal: BooleanLike = Field(
        default="", description="Check if heart examination is normal"
    )

    item_36_heart_abnormal: BooleanLike = Field(
        default="", description="Check if heart examination is abnormal"
    )

    item_37_vascular_system_normal: BooleanLike = Field(
        default="", description="Check if vascular system is normal"
    )

    item_37_vascular_system_abnormal: BooleanLike = Field(
        default="", description="Check if vascular system is abnormal"
    )

    item_38_abdomen_viscera_normal: BooleanLike = Field(
        default="", description="Check if abdomen and viscera are normal"
    )

    item_38_abdomen_viscera_abnormal: BooleanLike = Field(
        default="", description="Check if abdomen or viscera are abnormal"
    )

    item_39_anus_normal: BooleanLike = Field(
        default="", description="Check if anus examination is normal"
    )

    item_39_anus_abnormal: BooleanLike = Field(
        default="", description="Check if anus examination is abnormal"
    )

    item_40_skin_normal: BooleanLike = Field(
        default="", description="Check if skin examination is normal"
    )

    item_40_skin_abnormal: BooleanLike = Field(
        default="", description="Check if skin examination is abnormal"
    )

    item_41_gu_system_normal: BooleanLike = Field(
        default="", description="Check if genitourinary system is normal"
    )

    item_41_gu_system_abnormal: BooleanLike = Field(
        default="", description="Check if genitourinary system is abnormal"
    )

    item_42_extremities_normal: BooleanLike = Field(
        default="", description="Check if upper and lower extremities are normal"
    )

    item_42_extremities_abnormal: BooleanLike = Field(
        default="", description="Check if upper or lower extremities are abnormal"
    )

    item_43_spine_musculoskeletal_normal: BooleanLike = Field(
        default="", description="Check if spine and other musculoskeletal findings are normal"
    )

    item_43_spine_musculoskeletal_abnormal: BooleanLike = Field(
        default="", description="Check if spine or other musculoskeletal findings are abnormal"
    )

    item_44_identifying_marks_normal: BooleanLike = Field(
        default="",
        description="Check if identifying body marks, scars, or tattoos are normal/insignificant",
    )

    item_44_identifying_marks_abnormal: BooleanLike = Field(
        default="",
        description="Check if identifying body marks, scars, or tattoos are abnormal/significant",
    )

    item_45_lymphatics_normal: BooleanLike = Field(
        default="", description="Check if lymphatic examination is normal"
    )

    item_45_lymphatics_abnormal: BooleanLike = Field(
        default="", description="Check if lymphatic examination is abnormal"
    )

    item_46_neurologic_normal: BooleanLike = Field(
        default="", description="Check if neurologic examination is normal"
    )

    item_46_neurologic_abnormal: BooleanLike = Field(
        default="", description="Check if neurologic examination is abnormal"
    )

    item_47_psychiatric_normal: BooleanLike = Field(
        default="", description="Check if psychiatric evaluation is normal"
    )

    item_47_psychiatric_abnormal: BooleanLike = Field(
        default="", description="Check if psychiatric evaluation is abnormal"
    )

    item_48_general_systemic_normal: BooleanLike = Field(
        default="", description="Check if general systemic examination is normal"
    )

    item_48_general_systemic_abnormal: BooleanLike = Field(
        default="", description="Check if general systemic examination is abnormal"
    )


class NotesonAbnormalFindings(BaseModel):
    """Free-text notes describing abnormalities (linked to items 25–48)"""

    notes_line_1: str = Field(
        default="",
        description=(
            "First line of notes describing abnormalities .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    notes_line_2: str = Field(
        default="",
        description=(
            "Second line of notes describing abnormalities .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    notes_line_3: str = Field(
        default="",
        description=(
            "Third line of notes describing abnormalities .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    notes_line_4: str = Field(
        default="",
        description=(
            "Fourth line of notes describing abnormalities .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class HearingAssessmentItem49(BaseModel):
    """Conversational voice test and audiometry"""

    conversational_voice_test_pass: BooleanLike = Field(
        default="", description="Check if applicant passed the conversational voice test at 2 ft"
    )

    conversational_voice_test_fail: BooleanLike = Field(
        default="", description="Check if applicant failed the conversational voice test at 2 ft"
    )

    audiometer_threshold_right_500: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Right ear audiometric threshold at 500 Hz (dB)"
    )

    audiometer_threshold_right_1000: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Right ear audiometric threshold at 1000 Hz (dB)"
    )

    audiometer_threshold_right_2000: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Right ear audiometric threshold at 2000 Hz (dB)"
    )

    audiometer_threshold_right_3000: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Right ear audiometric threshold at 3000 Hz (dB)"
    )

    audiometer_threshold_right_4000: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Right ear audiometric threshold at 4000 Hz (dB)"
    )

    audiometer_threshold_left_500: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Left ear audiometric threshold at 500 Hz (dB)"
    )

    audiometer_threshold_left_1000: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Left ear audiometric threshold at 1000 Hz (dB)"
    )

    audiometer_threshold_left_2000: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Left ear audiometric threshold at 2000 Hz (dB)"
    )

    audiometer_threshold_left_3000: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Left ear audiometric threshold at 3000 Hz (dB)"
    )

    audiometer_threshold_left_4000: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Left ear audiometric threshold at 4000 Hz (dB)"
    )


class VisionAssessmentItems5054(BaseModel):
    """Distant, near, intermediate, colour vision, field of vision, and heterophoria"""

    distant_vision_right: str = Field(
        default="",
        description=(
            "Uncorrected distant visual acuity in the right eye .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    distant_vision_right_corrected_to: str = Field(
        default="",
        description=(
            "Corrected distant visual acuity in the right eye .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    distant_vision_left: str = Field(
        default="",
        description=(
            "Uncorrected distant visual acuity in the left eye .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    distant_vision_left_corrected_to: str = Field(
        default="",
        description=(
            "Corrected distant visual acuity in the left eye .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    distant_vision_both: str = Field(
        default="",
        description=(
            "Uncorrected distant visual acuity with both eyes .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    distant_vision_both_corrected_to: str = Field(
        default="",
        description=(
            "Corrected distant visual acuity with both eyes .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    near_vision_right: str = Field(
        default="",
        description=(
            "Uncorrected near visual acuity in the right eye .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    near_vision_right_corrected_to: str = Field(
        default="",
        description=(
            "Corrected near visual acuity in the right eye .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    near_vision_left: str = Field(
        default="",
        description=(
            "Uncorrected near visual acuity in the left eye .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    near_vision_left_corrected_to: str = Field(
        default="",
        description=(
            "Corrected near visual acuity in the left eye .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    near_vision_both: str = Field(
        default="",
        description=(
            "Uncorrected near visual acuity with both eyes .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    near_vision_both_corrected_to: str = Field(
        default="",
        description=(
            "Corrected near visual acuity with both eyes .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    intermediate_vision_right: str = Field(
        default="",
        description=(
            "Uncorrected intermediate visual acuity in the right eye .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    intermediate_vision_right_corrected_to: str = Field(
        default="",
        description=(
            "Corrected intermediate visual acuity in the right eye .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    intermediate_vision_left: str = Field(
        default="",
        description=(
            "Uncorrected intermediate visual acuity in the left eye .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    intermediate_vision_left_corrected_to: str = Field(
        default="",
        description=(
            "Corrected intermediate visual acuity in the left eye .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    intermediate_vision_both: str = Field(
        default="",
        description=(
            "Uncorrected intermediate visual acuity with both eyes .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    intermediate_vision_both_corrected_to: str = Field(
        default="",
        description=(
            "Corrected intermediate visual acuity with both eyes .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    colour_vision_pass: BooleanLike = Field(
        default="", description="Check if colour vision test is passed"
    )

    colour_vision_fail: BooleanLike = Field(
        default="", description="Check if colour vision test is failed"
    )

    mode_used: str = Field(
        default="",
        description=(
            "Mode or test method used for colour vision assessment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    field_of_vision_normal: BooleanLike = Field(
        default="", description="Check if field of vision is normal"
    )

    field_of_vision_abnormal: BooleanLike = Field(
        default="", description="Check if field of vision is abnormal"
    )

    heterophoria_esophoria: BooleanLike = Field(
        default="", description="Select if esophoria is present at 20 feet"
    )

    heterophoria_exophoria: BooleanLike = Field(
        default="", description="Select if exophoria is present at 20 feet"
    )

    heterophoria_right_hyperphoria: BooleanLike = Field(
        default="", description="Select if right hyperphoria is present at 20 feet"
    )

    heterophoria_left_hyperphoria: BooleanLike = Field(
        default="", description="Select if left hyperphoria is present at 20 feet"
    )


class VitalSignsandLaboratoryTestsItems5559(BaseModel):
    """Blood pressure, pulse, urinalysis, ECG, and other tests"""

    blood_pressure_systolic: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Systolic blood pressure (mm Hg)"
    )

    blood_pressure_diastolic: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Diastolic blood pressure (mm Hg)"
    )

    blood_pressure_sitting_mm_hg: str = Field(
        default="",
        description=(
            "Additional notes on sitting blood pressure measurement in mm of mercury .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    pulse_resting: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Resting pulse rate (beats per minute)"
    )

    urinalysis_normal: BooleanLike = Field(default="", description="Check if urinalysis is normal")

    urinalysis_abnormal: BooleanLike = Field(
        default="", description="Check if urinalysis is abnormal"
    )

    albumin: str = Field(
        default="",
        description=(
            'Albumin result from urinalysis .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    sugar: str = Field(
        default="",
        description=(
            "Sugar (glucose) result from urinalysis .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ecg_date_dd: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day of ECG examination"
    )

    ecg_date_mm: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month of ECG examination"
    )

    ecg_date_yyyy: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year of ECG examination"
    )

    other_tests_given_line_1: str = Field(
        default="",
        description=(
            "First line describing other tests given .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_tests_given_line_2: str = Field(
        default="",
        description=(
            "Second line describing other tests given .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_tests_given_line_3: str = Field(
        default="",
        description=(
            "Third line describing other tests given .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CommentsonHistoryandFindingsItem60(BaseModel):
    """AME comments on medical history and abnormal findings"""

    comments_history_findings_line_1: str = Field(
        default="",
        description=(
            "First line of comments on medical history and findings .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    comments_history_findings_line_2: str = Field(
        default="",
        description=(
            "Second line of comments on medical history and findings .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    comments_history_findings_line_3: str = Field(
        default="",
        description=(
            "Third line of comments on medical history and findings .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    comments_history_findings_line_4: str = Field(
        default="",
        description=(
            "Fourth line of comments on medical history and findings .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CASASUseOnly(BaseModel):
    """Internal coding and clerical review"""

    pathology_codes: str = Field(
        default="",
        description=(
            'Pathology codes assigned by CASAS .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    coded_by: str = Field(
        default="",
        description=(
            "Name or initials of person who coded the pathology .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    clerical_reject: str = Field(
        default="",
        description=(
            "Reason or indication for clerical rejection, if any .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SummaryofSignificantFindings(BaseModel):
    """Summary flags for history and physical findings"""

    significant_medical_history_yes: BooleanLike = Field(
        default="", description="Check if there is significant medical history"
    )

    significant_medical_history_no: BooleanLike = Field(
        default="", description="Check if there is no significant medical history"
    )

    abnormal_physical_findings_yes: BooleanLike = Field(
        default="", description="Check if there are abnormal physical findings"
    )

    abnormal_physical_findings_no: BooleanLike = Field(
        default="", description="Check if there are no abnormal physical findings"
    )


class ApplicantIdentificationItem61(BaseModel):
    """Applicant’s identifying information"""

    applicants_name: str = Field(
        ...,
        description=(
            'Full name of the applicant .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class MedicalAssessmentandDisqualifyingDefectsItems6263(BaseModel):
    """Overall medical assessment and listing of disqualifying defects"""

    medical_assessment_fit: BooleanLike = Field(
        default="", description="Select if applicant is medically fit"
    )

    medical_assessment_temporary_unfit: BooleanLike = Field(
        default="", description="Select if applicant is temporarily unfit"
    )

    medical_assessment_unfit: BooleanLike = Field(
        default="", description="Select if applicant is unfit"
    )

    medical_assessment_deferred: BooleanLike = Field(
        default="", description="Select if assessment is deferred for further evaluation"
    )

    disqualifying_defects_line_1: str = Field(
        default="",
        description=(
            "First line listing disqualifying defects by item number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    disqualifying_defects_line_2: str = Field(
        default="",
        description=(
            "Second line listing disqualifying defects by item number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class MedicalExaminersDeclarationandContactDetailsItem64(BaseModel):
    """AME declaration, signatures, and contact information"""

    aviation_medical_examiner_signature_declaration: str = Field(
        ...,
        description=(
            "Signature of the Aviation Medical Examiner for the declaration .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    aviation_medical_examiner_name: str = Field(
        ...,
        description=(
            "Printed name of the Aviation Medical Examiner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    aviation_medical_examiner_signature_final: str = Field(
        default="",
        description=(
            "Final signature of the Aviation Medical Examiner, if repeated .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address: str = Field(
        default="",
        description=(
            "Mailing address of the Aviation Medical Examiner .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ame_number: str = Field(
        default="",
        description=(
            "Aviation Medical Examiner identification number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ame_telephone: str = Field(
        default="",
        description=(
            "Telephone number of the Aviation Medical Examiner .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ReportOfMedicalExamination(BaseModel):
    """
    REPORT OF MEDICAL EXAMINATION

    ''
    """

    general_measurements_and_soda: GeneralMeasurementsandSODA = Field(
        ..., description="General Measurements and SODA"
    )
    physical_examination___systems_review_items_25_48: PhysicalExaminationSystemsReviewItems2548 = (
        Field(..., description="Physical Examination – Systems Review (Items 25–48)")
    )
    notes_on_abnormal_findings: NotesonAbnormalFindings = Field(
        ..., description="Notes on Abnormal Findings"
    )
    hearing_assessment_item_49: HearingAssessmentItem49 = Field(
        ..., description="Hearing Assessment (Item 49)"
    )
    vision_assessment_items_50_54: VisionAssessmentItems5054 = Field(
        ..., description="Vision Assessment (Items 50–54)"
    )
    vital_signs_and_laboratory_tests_items_55_59: VitalSignsandLaboratoryTestsItems5559 = Field(
        ..., description="Vital Signs and Laboratory Tests (Items 55–59)"
    )
    comments_on_history_and_findings_item_60: CommentsonHistoryandFindingsItem60 = Field(
        ..., description="Comments on History and Findings (Item 60)"
    )
    casas_use_only: CASASUseOnly = Field(..., description="CASAS Use Only")
    summary_of_significant_findings: SummaryofSignificantFindings = Field(
        ..., description="Summary of Significant Findings"
    )
    applicant_identification_item_61: ApplicantIdentificationItem61 = Field(
        ..., description="Applicant Identification (Item 61)"
    )
    medical_assessment_and_disqualifying_defects_items_62_63: MedicalAssessmentandDisqualifyingDefectsItems6263 = Field(
        ..., description="Medical Assessment and Disqualifying Defects (Items 62–63)"
    )
    medical_examiners_declaration_and_contact_details_item_64: MedicalExaminersDeclarationandContactDetailsItem64 = Field(
        ..., description="Medical Examiner’s Declaration and Contact Details (Item 64)"
    )
