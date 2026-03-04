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
            'Student\'s RMIT identification number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    class_: str = Field(
        ...,
        description=(
            "Name or code of the class related to the complaint .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    students_rmit_email_address: str = Field(
        ...,
        description=(
            "Official RMIT student email address where responses will be sent .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(..., description="Date the complaint form is completed")  # YYYY-MM-DD format


class ComplaintDetails(BaseModel):
    """Information about the nature and details of the complaint"""

    problem_class: BooleanLike = Field(
        default="", description="Select if the complaint is about a class"
    )

    teacher: BooleanLike = Field(
        default="", description="Select if the complaint is about a teacher"
    )

    classmate: BooleanLike = Field(
        default="", description="Select if the complaint is about a classmate"
    )

    other: str = Field(
        default="",
        description=(
            "If the complaint is about something else, describe it here .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    detailed_description_of_your_complaint: str = Field(
        ...,
        description=(
            "Provide a detailed description of the issue or complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class OfficeUseOnly(BaseModel):
    """Administrative processing information completed by staff"""

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
            "Name of the staff member who received the complaint form (office use only) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class RmitUniversityEnglishWorldwideStudentComplaintForm(BaseModel):
    """
        RMIT UNIVERSITY                                      English Worldwide

    Student Complaint Form

        ''
    """

    student_information: StudentInformation = Field(..., description="Student Information")
    complaint_details: ComplaintDetails = Field(..., description="Complaint Details")
    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
