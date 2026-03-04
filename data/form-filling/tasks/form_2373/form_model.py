from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class StudentData(BaseModel):
    """Basic information about the student"""

    first_name: str = Field(
        ...,
        description=(
            'Student\'s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Student\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            'Student\'s email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            'Student\'s telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    university: str = Field(
        ...,
        description=(
            "Name of the university where the student is enrolled .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    faculty: str = Field(
        ...,
        description=(
            'Faculty or department of the student .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    field_of_study: str = Field(
        ...,
        description=(
            "Student's specific field of study or degree program .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SupervisorData(BaseModel):
    """Information about the thesis supervisor"""

    title: str = Field(
        ...,
        description=(
            "Academic or professional title of the supervisor (e.g. Prof., Dr.) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    first_name_supervisor: str = Field(
        ...,
        description=(
            'Supervisor\'s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    last_name_supervisor: str = Field(
        ...,
        description=(
            'Supervisor\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    e_mail_supervisor: str = Field(
        ...,
        description=(
            'Supervisor\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    faculty_supervisor: str = Field(
        ...,
        description=(
            "Faculty or department of the supervisor .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    subject_area: str = Field(
        ...,
        description=(
            "Supervisor's subject area or discipline .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ThesisInformation(BaseModel):
    """Details about the bachelor or master thesis and exposé"""

    title_of_the_bachelor_or_master_thesis: str = Field(
        ...,
        description=(
            "Full title of the bachelor or master thesis .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    text_of_the_expose: str = Field(
        ...,
        description=(
            "Full text of the exposé (maximum length: 3,500 keystrokes including spaces) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class ThesisProposalsSouthTyrolEconomyApplicationForm(BaseModel):
    """
        CALL FOR PROPOSALS "BACHELOR’S AND MASTER’S
    THESES ON THE SOUTH TYROLEAN ECONOMY"

    APPLICATION FORM

        CALL FOR PROPOSALS "BACHELOR’S AND MASTER’S THESES ON THE SOUTH TYROLEAN ECONOMY"
    """

    student_data: StudentData = Field(..., description="Student Data")
    supervisor_data: SupervisorData = Field(..., description="Supervisor Data")
    thesis_information: ThesisInformation = Field(..., description="Thesis Information")
