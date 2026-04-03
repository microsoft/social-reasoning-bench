from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FormDateandSchoolYear(BaseModel):
    """Date of completion and applicable school year"""

    date: str = Field(..., description="Date this refusal form is completed")  # YYYY-MM-DD format

    school_year_start_20: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Four-digit year when the school year begins (e.g., 2025)"
    )

    school_year_end_20: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Four-digit year when the school year ends (e.g., 2026)"
    )


class StudentInformation(BaseModel):
    """Identifying information about the student"""

    students_legal_first_name: str = Field(
        ...,
        description=(
            "Student’s legal first name as it appears on official records .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    students_legal_middle_initial: str = Field(
        default="",
        description=(
            "Student’s legal middle initial (leave blank if none) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    students_legal_last_name: str = Field(
        ...,
        description=(
            "Student’s legal last name as it appears on official records .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    students_date_of_birth: str = Field(
        ..., description="Student’s date of birth"
    )  # YYYY-MM-DD format

    students_district_school: str = Field(
        ...,
        description=(
            "Name of the student’s school district and/or school .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    grade: str = Field(
        ...,
        description=(
            'Student’s current grade level .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    student_id_or_marss_number: str = Field(
        default="",
        description=(
            "Student’s district ID or MARSS number (for school or district staff use) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class OptOutAcknowledgmentandReason(BaseModel):
    """Parent/guardian acknowledgment of information and reason for refusal"""

    i_received_information_on_statewide_assessments_and_choose_to_opt_my_student_out: BooleanLike = Field(
        ...,
        description=(
            "Indicate by initialing/checking that you received information and are opting "
            "the student out"
        ),
    )

    reason_for_refusal: str = Field(
        default="",
        description=(
            "Explanation of why you are refusing participation in statewide assessments .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AssessmentstoOptOutOf(BaseModel):
    """Specific statewide assessments the student is being opted out of"""

    mca_mtas_reading: BooleanLike = Field(
        default="", description="Check if opting the student out of the MCA/MTAS Reading assessment"
    )

    mca_mtas_science: BooleanLike = Field(
        default="", description="Check if opting the student out of the MCA/MTAS Science assessment"
    )

    mca_mtas_mathematics: BooleanLike = Field(
        default="",
        description="Check if opting the student out of the MCA/MTAS Mathematics assessment",
    )

    access_or_alternate_access_for_ells: BooleanLike = Field(
        default="",
        description="Check if opting the student out of ACCESS or Alternate ACCESS for ELLs",
    )


class ParentGuardianAuthorization(BaseModel):
    """Parent/guardian identification and signature"""

    parent_guardian_name_print: str = Field(
        ...,
        description=(
            "Printed name of the parent or guardian completing this form .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    parent_guardian_signature: str = Field(
        ...,
        description=(
            "Signature of the parent or guardian authorizing the refusal .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ParentGuardianStateAssessmentRefusal(BaseModel):
    """
    Parent/Guardian Refusal for Student Participation in Statewide Assessments

    Minnesota Statutes, section 120B.31, subdivision 4a, requires the commissioner to create and publish a form for parents and guardians to complete if they refuse to have their student participate in state-required standardized assessments. Your student’s district may require additional information. School districts must post this form on the district website and include it in district student handbooks.
    To opt out of statewide assessments, the parent/guardian must complete this form and return it to the student’s school.
    To best support school district planning, please submit this form to the student’s school no later than January 15 of the academic school year. For students who enroll after statewide testing window begins, please submit the form within two weeks of enrollment. A new refusal form is required each year parents/guardians wish to opt the student out of statewide assessments.
    """

    form_date_and_school_year: FormDateandSchoolYear = Field(
        ..., description="Form Date and School Year"
    )
    student_information: StudentInformation = Field(..., description="Student Information")
    opt_out_acknowledgment_and_reason: OptOutAcknowledgmentandReason = Field(
        ..., description="Opt-Out Acknowledgment and Reason"
    )
    assessments_to_opt_out_of: AssessmentstoOptOutOf = Field(
        ..., description="Assessments to Opt Out Of"
    )
    parentguardian_authorization: ParentGuardianAuthorization = Field(
        ..., description="Parent/Guardian Authorization"
    )
