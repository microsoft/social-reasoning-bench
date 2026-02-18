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
    """Basic details about the student submitting the complaint"""

    family_name: str = Field(
        ...,
        description=(
            "Student's family name (surname) as enrolled with RMIT .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the complaint form is completed")  # YYYY-MM-DD format

    given_name: str = Field(
        ...,
        description=(
            "Student's given name (first name) as enrolled with RMIT .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    student_number: str = Field(
        ...,
        description=(
            "Student's RMIT student identification number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    class_: str = Field(
        ...,
        description=(
            "Class or course group the student is enrolled in .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    students_rmit_email_address: str = Field(
        ...,
        description=(
            "Official RMIT student email address used for correspondence .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ComplaintDetails(BaseModel):
    """Information about the nature and details of the complaint"""

    problem_with_class: BooleanLike = Field(
        default="", description="Tick if the complaint is about a class"
    )

    problem_with_teacher: BooleanLike = Field(
        default="", description="Tick if the complaint is about a teacher"
    )

    problem_with_classmate: BooleanLike = Field(
        default="", description="Tick if the complaint is about a classmate"
    )

    problem_with_other: str = Field(
        default="",
        description=(
            "If the problem is not listed, describe the other issue .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    detailed_description_of_your_complaint: str = Field(
        ...,
        description=(
            "Provide a detailed description of the complaint, including what happened, "
            'when, and who was involved .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class OfficeUseOnly(BaseModel):
    """Administrative fields for internal processing"""

    date_time_received: str = Field(
        default="",
        description=(
            "Date and time the complaint form was received (office use only) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    received_by: str = Field(
        default="",
        description=(
            "Name of staff member who received the complaint form (office use only) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class StudentComplaintForm(BaseModel):
    """Student Complaint Form"""

    student_information: StudentInformation = Field(..., description="Student Information")
    complaint_details: ComplaintDetails = Field(..., description="Complaint Details")
    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
