from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class SchoolYear(BaseModel):
    """Date and applicable school year for this refusal form"""

    date: str = Field(..., description="Date this refusal form is completed")  # YYYY-MM-DD format

    school_year_start_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Four-digit year when the applicable school year begins"
    )

    school_year_end_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Four-digit year when the applicable school year ends"
    )


class StudentInformation(BaseModel):
    """Identifying information about the student"""

    students_legal_first_name: str = Field(
        ...,
        description=(
            "Student’s full legal first name as it appears on official records .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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
            "Student’s full legal last name as it appears on official records .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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
            "Student’s local ID or MARSS number, completed by school or district staff .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AssessmentRefusal(BaseModel):
    """Parent/guardian refusal and selected statewide assessments to opt out of"""

    received_information_and_opt_out: BooleanLike = Field(
        ...,
        description=(
            "Indicates that the parent/guardian received information on statewide "
            "assessments and is choosing to opt the student out"
        ),
    )

    reason_for_refusal: str = Field(
        default="",
        description=(
            "Explanation of why the parent/guardian is refusing participation in statewide "
            'assessments .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    mca_mtas_reading: BooleanLike = Field(
        default="", description="Check to opt the student out of the MCA/MTAS Reading assessment"
    )

    mca_mtas_science: BooleanLike = Field(
        default="", description="Check to opt the student out of the MCA/MTAS Science assessment"
    )

    mca_mtas_mathematics: BooleanLike = Field(
        default="",
        description="Check to opt the student out of the MCA/MTAS Mathematics assessment",
    )

    access_or_alternate_access_for_ells: BooleanLike = Field(
        default="",
        description=(
            "Check to opt the student out of the ACCESS or Alternate ACCESS for ELLs assessment"
        ),
    )


class ParentGuardianInformation(BaseModel):
    """Parent/guardian identification and authorization"""

    parent_guardian_name_print: str = Field(
        ...,
        description=(
            "Printed name of the parent or guardian completing the form .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parent_guardian_signature: str = Field(
        ...,
        description=(
            "Signature of the parent or guardian confirming the opt-out request .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ParentGuardianStateAssessmentRefusal(BaseModel):
    """
    Parent/Guardian Refusal for Student Participation in Statewide Assessments

    Minnesota Statutes, section 120B.31, subdivision 4a, requires the commissioner to create and publish a form for parents and guardians to complete if they refuse to have their student participate in state-required standardized assessments. Your student’s district may require additional information. School districts must post this form on the district website and include it in district student handbooks.
    To opt out of statewide assessments, the parent/guardian must complete this form and return it to the student’s school.
    To best support school district planning, please submit this form to the student’s school no later than January 15 of the academic school year. For students who enroll after statewide testing window begins, please submit the form within two weeks of enrollment. A new refusal form is required each year parents/guardians wish to opt the student out of statewide assessments.
    """

    school_year: SchoolYear = Field(..., description="School Year")
    student_information: StudentInformation = Field(..., description="Student Information")
    assessment_refusal: AssessmentRefusal = Field(..., description="Assessment Refusal")
    parentguardian_information: ParentGuardianInformation = Field(
        ..., description="Parent/Guardian Information"
    )
