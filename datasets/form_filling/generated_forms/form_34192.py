from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Personal and contact details of the scholarship applicant"""

    name: str = Field(
        ...,
        description=(
            'Applicant\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Applicant's mailing address including street, city, state, and ZIP code .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    tel_no: str = Field(
        ...,
        description=(
            "Primary telephone number with area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class EmploymentInformation(BaseModel):
    """Current employer and role details"""

    employer: str = Field(
        default="",
        description=(
            'Name of current employer .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    employer_address: str = Field(
        default="",
        description=(
            "Mailing address of current employer including street, city, state, and ZIP "
            'code .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    occupation: str = Field(
        default="",
        description=(
            'Applicant\'s current job title or role .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    current_field: str = Field(
        default="",
        description=(
            "Applicant's current professional field or industry .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AcademicHistory(BaseModel):
    """Completed courses and grades in the Financial Planning Program"""

    courses_completed_and_grades_received: str = Field(
        ...,
        description=(
            "List of completed courses in the Financial Planning Program and the grades "
            'received for each .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class BUCPEGlovskyScholarshipFundApplication(BaseModel):
    """
        Boston University Metropolitan College
    Center for Professional Education

    Robert J. Glovsky Scholarship Fund Application

        The Robert J. Glovsky Scholarship Fund is a permanently endowed fund, the income of which shall provide annual merit-based scholarship awards to one or more students. Students must be enrolled in the Financial Planning Program at Metropolitan College’s Center for Professional Education. Preference will be given to students who wish to assist traditionally underserved populations, as evidenced by their professional or personal work in the nonprofit sector. The student(s) awarded will receive up to $2,000 (no cash value) per year. Funds will be distributed after successful completion of each course per the conditions of the scholarship.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    employment_information: EmploymentInformation = Field(..., description="Employment Information")
    academic_history: AcademicHistory = Field(..., description="Academic History")
