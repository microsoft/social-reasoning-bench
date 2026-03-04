from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CourseTableRow(BaseModel):
    """Single row in Course List Table"""

    course_dept: str = Field(default="", description="Course_Dept")
    course_number: str = Field(default="", description="Course_Number")
    course_name: str = Field(default="", description="Course_Name")
    credits: str = Field(default="", description="Credits")


class StudentInformation(BaseModel):
    """Basic student details and academic standing"""

    name: str = Field(
        ...,
        description=(
            'Student\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    banner_id: str = Field(
        ...,
        description=(
            'Student\'s Banner ID number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        ...,
        description=(
            'Student\'s mobile phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    iup_email: str = Field(
        ...,
        description=(
            'Student\'s official IUP email address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    major: str = Field(
        ...,
        description=(
            'Student\'s declared major .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    cgpa: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Current cumulative grade point average (CGPA)"
    )

    iup_credits_attempted: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of IUP credits attempted"
    )

    iup_credits_earned: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of IUP credits successfully earned"
    )

    iup_credit_completion_rate_credits_attempted_credits_earned: Union[
        float, Literal["N/A", ""]
    ] = Field(
        ...,
        description=(
            "IUP credit completion rate percentage (credits earned divided by credits attempted)"
        ),
    )


class Justification(BaseModel):
    """Student’s explanation for requesting excess credits"""

    justification_for_the_request: str = Field(
        ...,
        description=(
            "Explanation of why excess credit approval is being requested .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class PlannedCourses(BaseModel):
    """Courses to be taken in the requested semester and total requested credits"""

    semester: str = Field(
        ...,
        description=(
            "Semester for which excess credits are requested (e.g., Fall, Spring, Winter) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    year_20: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Calendar year of the semester (last two digits, e.g., 24 for 2024)"
    )

    course_table: List[CourseTableRow] = Field(
        ..., description="Table listing all planned courses for the specified semester"
    )  # List of table rows

    total_number_of_credits_for_which_approval_is_requested: Union[float, Literal["N/A", ""]] = (
        Field(
            ...,
            description="Sum of all credits for which excess credit approval is being requested",
        )
    )


class Approvals(BaseModel):
    """Advisor, chairperson, and assistant dean approvals"""

    advisor_signature: str = Field(
        ...,
        description=(
            "Academic advisor's signature indicating review of the request .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    advisor_signature_date: str = Field(
        ..., description="Date the advisor signed the form"
    )  # YYYY-MM-DD format

    advisor_approval_approved: BooleanLike = Field(
        ..., description="Advisor indicates the excess credit request is approved"
    )

    advisor_approval_denied: BooleanLike = Field(
        ..., description="Advisor indicates the excess credit request is denied"
    )

    chairperson_signature: str = Field(
        ...,
        description=(
            "Department chairperson's signature indicating review of the request .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    chairperson_signature_date: str = Field(
        ..., description="Date the chairperson signed the form"
    )  # YYYY-MM-DD format

    chairperson_approval_approved: BooleanLike = Field(
        ..., description="Chairperson indicates the excess credit request is approved"
    )

    chairperson_approval_denied: BooleanLike = Field(
        ..., description="Chairperson indicates the excess credit request is denied"
    )

    assistant_dean_signature: str = Field(
        ...,
        description=(
            "Assistant dean's signature indicating final review of the request .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    assistant_dean_signature_date: str = Field(
        ..., description="Date the assistant dean signed the form"
    )  # YYYY-MM-DD format

    assistant_dean_approval_approved: BooleanLike = Field(
        ..., description="Assistant dean indicates the excess credit request is approved"
    )

    assistant_dean_approval_denied: BooleanLike = Field(
        ..., description="Assistant dean indicates the excess credit request is denied"
    )


class ProcessingInformation(BaseModel):
    """Administrative processing dates"""

    entered_in_banner_date: str = Field(
        default="", description="Date the excess credit approval was entered into the Banner system"
    )  # YYYY-MM-DD format

    student_notified_date: str = Field(
        default="", description="Date the student was notified of the decision"
    )  # YYYY-MM-DD format


class ExcessCreditApplicationEberlyBusinessAndInformationTechnology(BaseModel):
    """
        APPLICATION FOR EXCESS CREDIT
    Eberly College of Business and Information Technology

        ''
    """

    student_information: StudentInformation = Field(..., description="Student Information")
    justification: Justification = Field(..., description="Justification")
    planned_courses: PlannedCourses = Field(..., description="Planned Courses")
    approvals: Approvals = Field(..., description="Approvals")
    processing_information: ProcessingInformation = Field(..., description="Processing Information")
