from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class StudentInformation(BaseModel):
    """Basic information about the student and school year"""

    date: str = Field(..., description="Date this refusal form is completed")  # YYYY-MM-DD format

    school_year_start_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Four-digit year when the school year begins (e.g., 2024)"
    )

    school_year_end_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Four-digit year when the school year ends (e.g., 2025)"
    )

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


class AssessmentRefusalDetails(BaseModel):
    """Parent/guardian refusal, reasons, and selected statewide assessments"""

    initial_received_information_and_opt_out: str = Field(
        ...,
        description=(
            "Parent/guardian initials confirming receipt of information and choice to opt "
            'the student out .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    reason_for_refusal: str = Field(
        default="",
        description=(
            "Explanation of why the student is being opted out of statewide assessments .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mca_mtas_reading: BooleanLike = Field(
        default="",
        description="Check or mark if opting the student out of the MCA/MTAS Reading assessment",
    )

    mca_mtas_science: BooleanLike = Field(
        default="",
        description="Check or mark if opting the student out of the MCA/MTAS Science assessment",
    )

    mca_mtas_mathematics: BooleanLike = Field(
        default="",
        description="Check or mark if opting the student out of the MCA/MTAS Mathematics assessment",
    )

    access_or_alternate_access_for_ells: BooleanLike = Field(
        default="",
        description=(
            "Check or mark if opting the student out of the ACCESS or Alternate ACCESS for "
            "ELLs assessment"
        ),
    )


class ParentGuardianAuthorization(BaseModel):
    """Parent/guardian identification and signature"""

    parent_guardian_name_print: str = Field(
        ...,
        description=(
            "Printed full name of the parent or guardian completing the form .If you cannot "
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


class SchoolDistrictUseOnly(BaseModel):
    """To be completed by school or district staff only"""

    student_id_or_marss_number: str = Field(
        default="",
        description=(
            "Student’s ID or MARSS number (for school or district staff use) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class pythonParentRefusalForStateAssessments(BaseModel):
    """
    Parent/Guardian Refusal for Student Participation in Statewide Assessments

    Minnesota Statutes, section 120B.31, subdivision 4a, requires the commissioner to create and publish a form for parents and guardians to complete if they refuse to have their student participate in state-required standardized assessments. Your student’s district may require additional information. School districts must post this three page form on the district website and include it in district student handbooks.
    To opt out of statewide assessments, the parent/guardian must complete this form and return it to the student’s school.
    To best support school district planning, please submit this form to the student’s school no later than January 15 of the academic school year. For students who enroll after a statewide testing window begins, please submit the form within two weeks of enrollment. A new refusal form is required each year parents/guardians wish to opt the student out of statewide assessments.
    """

    student_information: StudentInformation = Field(..., description="Student Information")
    assessment_refusal_details: AssessmentRefusalDetails = Field(
        ..., description="Assessment Refusal Details"
    )
    parentguardian_authorization: ParentGuardianAuthorization = Field(
        ..., description="Parent/Guardian Authorization"
    )
    schooldistrict_use_only: SchoolDistrictUseOnly = Field(
        ..., description="School/District Use Only"
    )
