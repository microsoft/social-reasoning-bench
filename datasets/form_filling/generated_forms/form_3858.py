from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FamilyHistoryQuestions(BaseModel):
    """Family cardiac and related medical history"""

    family_sudden_unexpected_death_before_50: BooleanLike = Field(
        ...,
        description=(
            "Indicate if any family member had sudden, unexpected, or unexplained death "
            "before age 50, including SIDS, car accidents, drowning or near drowning."
        ),
    )

    family_died_suddenly_heart_problems_before_50: BooleanLike = Field(
        ...,
        description=(
            "Indicate if any family member died suddenly of heart-related problems before age 50."
        ),
    )

    family_unexplained_fainting_or_seizures: BooleanLike = Field(
        ...,
        description="Indicate if any family member has unexplained fainting episodes or seizures.",
    )

    enlarged_heart: BooleanLike = Field(
        default="",
        description="Indicate if any relative has been diagnosed with an enlarged heart.",
    )

    hypertrophic_cardiomyopathy_hcm: BooleanLike = Field(
        default="", description="Indicate if any relative has hypertrophic cardiomyopathy (HCM)."
    )

    dilated_cardiomyopathy_dcm: BooleanLike = Field(
        default="", description="Indicate if any relative has dilated cardiomyopathy (DCM)."
    )

    heart_rhythm_problems: BooleanLike = Field(
        default="", description="Indicate if any relative has heart rhythm problems (arrhythmias)."
    )

    long_qt_syndrome_lqts: BooleanLike = Field(
        default="", description="Indicate if any relative has long QT syndrome (LQTS)."
    )

    short_qt_syndrome: BooleanLike = Field(
        default="", description="Indicate if any relative has short QT syndrome."
    )

    brugada_syndrome: BooleanLike = Field(
        default="", description="Indicate if any relative has Brugada syndrome."
    )

    catecholaminergic_polymorphic_ventricular_tachycardia_cpvt: BooleanLike = Field(
        default="",
        description=(
            "Indicate if any relative has catecholaminergic polymorphic ventricular "
            "tachycardia (CPVT)."
        ),
    )

    arrhythmogenic_right_ventricular_cardiomyopathy_arvc: BooleanLike = Field(
        default="",
        description=(
            "Indicate if any relative has arrhythmogenic right ventricular cardiomyopathy (ARVC)."
        ),
    )

    marfan_syndrome_aortic_rupture: BooleanLike = Field(
        default="",
        description=(
            "Indicate if any relative has Marfan syndrome or aortic rupture related to "
            "Marfan syndrome."
        ),
    )

    heart_attack_age_50_or_younger: BooleanLike = Field(
        default="", description="Indicate if any relative had a heart attack at age 50 or younger."
    )

    pacemaker_or_implanted_defibrillator: BooleanLike = Field(
        default="",
        description="Indicate if any relative has a pacemaker or implanted defibrillator.",
    )

    deaf_at_birth: BooleanLike = Field(
        default="", description="Indicate if any relative was deaf at birth."
    )

    explain_yes_answers_here: str = Field(
        default="",
        description=(
            'Provide details or explanations for any questions answered "Yes" above. .If '
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SignaturesandCertification(BaseModel):
    """Attestations by student, parent/guardian, and medical provider"""

    signature_of_student_athlete: str = Field(
        ...,
        description=(
            "Signature of the student-athlete confirming the accuracy of the information "
            'provided. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    signature_of_parent_guardian: str = Field(
        ...,
        description=(
            "Signature of the parent or guardian confirming the accuracy of the information "
            'provided. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    date_student_parent_signatures: str = Field(
        ..., description="Date the student-athlete and parent/guardian signed the form."
    )  # YYYY-MM-DD format

    signature_of_md_do_nd_nmd_np_pa_c_ccsp: str = Field(
        ...,
        description=(
            "Signature of the examining medical provider (MD, DO, ND, NMD, NP, PA-C, or "
            'CCSP). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    date_provider_signature: str = Field(
        ..., description="Date the medical provider signed the form."
    )  # YYYY-MM-DD format


class FamilyHistoryQuestions(BaseModel):
    """Family History Questions"""

    family_history_questions: FamilyHistoryQuestions = Field(
        ..., description="Family History Questions"
    )
    signatures_and_certification: SignaturesandCertification = Field(
        ..., description="Signatures and Certification"
    )
