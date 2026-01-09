from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectOverview(BaseModel):
    """Basic information about the proposed project"""

    project_title: str = Field(
        ...,
        description=(
            "Full title of the proposed innovative teaching project .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    amount_of_grant: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total dollar amount of grant funds requested"
    )

    school: str = Field(
        ...,
        description=(
            "Name of the school where the project will be implemented .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    grades: str = Field(
        ...,
        description=(
            "Grade level or range of grades of participating students .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    subjects: str = Field(
        ...,
        description=(
            "Subject area(s) addressed by the project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    number_of_students_participating: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of students who will participate in the project"
    )

    students_target_group: BooleanLike = Field(
        default="",
        description="Check if the primary target population includes a specific student group",
    )

    students_target_group_description: str = Field(
        default="",
        description=(
            "Description of the specific student target group (e.g., grade, program, "
            'demographic) .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    parents: BooleanLike = Field(
        default="", description="Check if parents are part of the primary target population"
    )

    teachers: BooleanLike = Field(
        default="", description="Check if teachers are part of the primary target population"
    )

    implementation_start_date: str = Field(
        ..., description="Planned date when project implementation will begin"
    )  # YYYY-MM-DD format


class ApplicantInformation(BaseModel):
    """Names and signatures of the project applicants"""

    printed_name_of_applicants_line_1: str = Field(
        ...,
        description=(
            'Printed name of the first applicant .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_applicants_line_1: str = Field(
        ...,
        description=(
            'Signature of the first applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    printed_name_of_applicants_line_2: str = Field(
        default="",
        description=(
            "Printed name of the second applicant (if applicable) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_applicants_line_2: str = Field(
        default="",
        description=(
            "Signature of the second applicant (if applicable) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    printed_name_of_applicants_line_3: str = Field(
        default="",
        description=(
            "Printed name of the third applicant (if applicable) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_applicants_line_3: str = Field(
        default="",
        description=(
            "Signature of the third applicant (if applicable) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectDescription(BaseModel):
    """Short narrative description of the project"""

    description_of_the_project_line_1: str = Field(
        ...,
        description=(
            "First line of the brief project description (overall description limited to "
            'about 100 words) .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    description_of_the_project_line_2: str = Field(
        default="",
        description=(
            "Second line of the brief project description .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    description_of_the_project_line_3: str = Field(
        default="",
        description=(
            "Third line of the brief project description .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    description_of_the_project_line_4: str = Field(
        default="",
        description=(
            "Fourth line of the brief project description .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Approvals(BaseModel):
    """Required signatures and approvals"""

    signature_of_principal: str = Field(
        ...,
        description=(
            "Principal's signature indicating approval of the project .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    principal_title_or_printed_name_following_comma: str = Field(
        ...,
        description=(
            "Principal's printed name or title appearing after the comma .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_principal_signature: str = Field(
        ..., description="Date the principal signed the application"
    )  # YYYY-MM-DD format

    signature_of_director_of_instructional_technology: str = Field(
        default="",
        description=(
            "Signature of the Director of Instructional Technology (required if funds will "
            "be used to purchase technology and/or media equipment) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_director_of_facilities: str = Field(
        default="",
        description=(
            "Signature of the Director of Facilities (required if funds will be used for "
            'construction or maintenance) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class InnovativeTeachingGrantApplicationCoverPage(BaseModel):
    """Innovative Teaching Grant Application
    Cover Page"""

    project_overview: ProjectOverview = Field(..., description="Project Overview")
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    project_description: ProjectDescription = Field(..., description="Project Description")
    approvals: Approvals = Field(..., description="Approvals")
