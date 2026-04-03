from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectInformation(BaseModel):
    """Basic details about the proposed project"""

    project_title: str = Field(
        ...,
        description=(
            'Full title of the proposed project .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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
            "Grade level or range of grades participating in the project .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
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

    students_target_group: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of students in the primary target group to be served"
    )

    students_target_group_description: str = Field(
        default="",
        description=(
            "Brief description of the student target group (e.g., grade, program, "
            'characteristics) .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    parents: BooleanLike = Field(
        default="", description="Indicate if parents are part of the primary target population"
    )

    teachers: BooleanLike = Field(
        default="", description="Indicate if teachers are part of the primary target population"
    )

    implementation_start_date: str = Field(
        ..., description="Planned start date for implementing the project"
    )  # YYYY-MM-DD format

    description_of_the_project: str = Field(
        ...,
        description=(
            "Brief description of the project (no more than 100 words or 4–5 sentences) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ApplicantInformation(BaseModel):
    """Names and signatures of project applicants"""

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

    printed_name_of_applicants_line_4: str = Field(
        default="",
        description=(
            "Printed name of the fourth applicant (if applicable) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_applicants_line_4: str = Field(
        default="",
        description=(
            "Signature of the fourth applicant (if applicable) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AuthorizationandApprovals(BaseModel):
    """Required signatures and approvals for the project"""

    signature_of_principal: str = Field(
        ...,
        description=(
            "Principal's signature approving the project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
    """
        Innovative Teaching Grant Application
    Cover Page

        ''
    """

    project_information: ProjectInformation = Field(..., description="Project Information")
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    authorization_and_approvals: AuthorizationandApprovals = Field(
        ..., description="Authorization and Approvals"
    )
