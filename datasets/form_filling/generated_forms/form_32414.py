from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ReferenceTypeandApplicant(BaseModel):
    """Information about who is completing the reference and the applicant being referenced"""

    school_official: BooleanLike = Field(
        default="", description="Check if the reference is being completed by a school official."
    )

    title: str = Field(
        default="",
        description=(
            "Professional title of the school official, if applicable. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    employer: BooleanLike = Field(
        default="", description="Check if the reference is being completed by an employer."
    )

    other: BooleanLike = Field(
        default="",
        description=(
            "Check if the reference is being completed by someone other than a school "
            "official or employer."
        ),
    )

    applicants_name: str = Field(
        ...,
        description=(
            "Full name of the scholarship applicant. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ReferenceEvaluation(BaseModel):
    """Evaluator’s comments on the applicant’s performance, attendance, character, and overall recommendation"""

    academic_or_work_performance_achievement_intellectual_abilities_etc: str = Field(
        ...,
        description=(
            "Comments on the applicant’s academic or work performance, including "
            "achievements and intellectual abilities. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    attendance_record: str = Field(
        ...,
        description=(
            "Comments on the applicant’s attendance record. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    character_leadership_and_school_and_or_community_involvement: str = Field(
        ...,
        description=(
            "Comments on the applicant’s character, leadership, and involvement in school "
            'and/or community activities. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    recommendation: str = Field(
        ...,
        description=(
            "Overall recommendation regarding the applicant. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_remarks_comments_not_addressed_above: str = Field(
        default="",
        description=(
            "Any additional remarks or comments about the applicant not covered in previous "
            'sections. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class EvaluatorInformationandSignature(BaseModel):
    """Signature and contact details of the person completing the reference"""

    signature: str = Field(
        ...,
        description=(
            "Signature of the person completing the reference. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Date the reference form was completed and signed."
    )  # YYYY-MM-DD format

    printed_or_typed_name: str = Field(
        ...,
        description=(
            "Printed or typed name of the person completing the reference. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    contact_phone_number: str = Field(
        ...,
        description=(
            "Contact phone number for the person completing the reference. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    title_position_affiliation_to_student: str = Field(
        ...,
        description=(
            "The reference’s title, position, or relationship/affiliation to the student. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class ScholarshipReferenceForm(BaseModel):
    """
    Scholarship Reference Form

    ''
    """

    reference_type_and_applicant: ReferenceTypeandApplicant = Field(
        ..., description="Reference Type and Applicant"
    )
    reference_evaluation: ReferenceEvaluation = Field(..., description="Reference Evaluation")
    evaluator_information_and_signature: EvaluatorInformationandSignature = Field(
        ..., description="Evaluator Information and Signature"
    )
