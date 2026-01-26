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
    """Single row in Course Dept / Course Number / Course Name / Credits"""

    course_dept: str = Field(default="", description="Course_Dept")
    course_number: str = Field(default="", description="Course_Number")
    course_name: str = Field(default="", description="Course_Name")
    credits: str = Field(default="", description="Credits")


class StudentInformation(BaseModel):
    """Student identification and contact details"""

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
            'Student\'s IUP Banner ID number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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


class AcademicStanding(BaseModel):
    """Current academic performance and credit history"""

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


class RequestDetails(BaseModel):
    """Justification and term for which excess credits are requested"""

    justification_for_the_request: str = Field(
        ...,
        description=(
            "Explanation of why excess credit approval is being requested .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    semester: str = Field(
        ...,
        description=(
            "Semester for which excess credits are requested (e.g., Fall, Spring, Winter, "
            'Summer) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    year_20: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Calendar year of the semester (last two digits, e.g., 24 for 2024)"
    )

    course_table: List[CourseTableRow] = Field(
        ...,
        description=(
            "List of all planned courses for the specified semester, including department, "
            "number, name, and credits"
        ),
    )  # List of table rows

    total_number_of_credits_for_which_approval_is_requested: Union[float, Literal["N/A", ""]] = (
        Field(
            ...,
            description="Sum of all credits for which excess credit approval is being requested",
        )
    )


class Approvals(BaseModel):
    """Advisor, chairperson, and assistant dean approvals and processing dates"""

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
        ..., description="Date the academic advisor signed the form"
    )  # YYYY-MM-DD format

    advisor_approved: BooleanLike = Field(
        default="", description="Indicates that the advisor has approved the excess credit request"
    )

    advisor_denied: BooleanLike = Field(
        default="", description="Indicates that the advisor has denied the excess credit request"
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
        ..., description="Date the department chairperson signed the form"
    )  # YYYY-MM-DD format

    chairperson_approved: BooleanLike = Field(
        default="",
        description="Indicates that the chairperson has approved the excess credit request",
    )

    chairperson_denied: BooleanLike = Field(
        default="",
        description="Indicates that the chairperson has denied the excess credit request",
    )

    assistant_dean_signature: str = Field(
        ...,
        description=(
            "Assistant dean's signature indicating review of the request .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    assistant_dean_signature_date: str = Field(
        ..., description="Date the assistant dean signed the form"
    )  # YYYY-MM-DD format

    assistant_dean_approved: BooleanLike = Field(
        default="",
        description="Indicates that the assistant dean has approved the excess credit request",
    )

    assistant_dean_denied: BooleanLike = Field(
        default="",
        description="Indicates that the assistant dean has denied the excess credit request",
    )

    date_entered_in_banner: str = Field(
        default="",
        description="Office use only: date the excess credit approval was entered in Banner",
    )  # YYYY-MM-DD format

    date_student_notified: str = Field(
        default="", description="Office use only: date the student was notified of the decision"
    )  # YYYY-MM-DD format


class ExcessCreditApplicationEberlyBusinessInfoTech(BaseModel):
    """
        APPLICATION FOR EXCESS CREDIT
    Eberly College of Business and Information Technology

        APPLICATION FOR EXCESS CREDIT – Eberly College of Business and Information Technology. This form is used by students to request approval to register for excess academic credits beyond the standard load, subject to minimum cumulative GPA requirements and review/signature approval of the advisor, department chairperson, and assistant dean. Excess credit approval with an unmet CGPA requirement for the fall or spring semesters will be granted only in consideration of immediate degree completion. Any excess credit approval for the winter term will be granted only in consideration of immediate degree completion.
    """

    student_information: StudentInformation = Field(..., description="Student Information")
    academic_standing: AcademicStanding = Field(..., description="Academic Standing")
    request_details: RequestDetails = Field(..., description="Request Details")
    approvals: Approvals = Field(..., description="Approvals")
