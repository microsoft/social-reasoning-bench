from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Basic details about the grant project"""

    project_title: str = Field(
        ...,
        description=(
            "Title of the proposed project .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    amount_of_grant: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Requested grant amount in dollars"
    )

    school: str = Field(
        ...,
        description=(
            "Name of the school .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    grades: str = Field(
        ...,
        description=(
            "Grade levels involved in the project .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    subjects: str = Field(
        ...,
        description=(
            "Subjects involved in the project .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    number_of_students_participating: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Total number of students participating in the project"
    )

    students_target_group: BooleanLike = Field(
        ...,
        description="Check if students are the primary target group"
    )

    students_target_group_description: str = Field(
        ...,
        description=(
            "Description of the student target group .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    parents: BooleanLike = Field(
        ...,
        description="Check if parents are a target population"
    )

    teachers: BooleanLike = Field(
        ...,
        description="Check if teachers are a target population"
    )

    implementation_start_date: str = Field(
        ...,
        description="Date when project implementation will begin"
    )  # YYYY-MM-DD format

    implementation_start_date_alternate_second_line: str = Field(
        ...,
        description="Alternate or additional implementation start date (if applicable)"
    )  # YYYY-MM-DD format

    description_of_the_project: str = Field(
        ...,
        description=(
            "Brief description of the project (no more than 100 words or 4-5 sentences) .If "
            "you cannot fill this, write \"N/A\". If this field should not be filled by you "
            "(for example, it belongs to another person or office), leave it blank (empty "
            "string \"\")."
        )
    )


class ApplicantInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Names and signatures of applicants"""

    printed_name_of_applicants_1: str = Field(
        ...,
        description=(
            "Printed name of the first applicant .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    signature_of_applicants_1: str = Field(
        ...,
        description=(
            "Signature of the first applicant .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    printed_name_of_applicants_2: str = Field(
        ...,
        description=(
            "Printed name of the second applicant (if applicable) .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    signature_of_applicants_2: str = Field(
        ...,
        description=(
            "Signature of the second applicant (if applicable) .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    printed_name_of_applicants_3: str = Field(
        ...,
        description=(
            "Printed name of the third applicant (if applicable) .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    signature_of_applicants_3: str = Field(
        ...,
        description=(
            "Signature of the third applicant (if applicable) .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    printed_name_of_applicants_4: str = Field(
        ...,
        description=(
            "Printed name of the fourth applicant (if applicable) .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    signature_of_applicants_4: str = Field(
        ...,
        description=(
            "Signature of the fourth applicant (if applicable) .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )


class Authorization(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Signatures required for authorization"""

    signature_of_principal: str = Field(
        ...,
        description=(
            "Signature of the school principal .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    date_principal: str = Field(
        ...,
        description="Date of principal's signature"
    )  # YYYY-MM-DD format

    signature_of_director_of_instructional_technology: str = Field(
        ...,
        description=(
            "Signature of Director of Instructional Technology (required if funds used for "
            "technology/media equipment) .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    signature_of_director_of_facilities: str = Field(
        ...,
        description=(
            "Signature of Director of Facilities (required if funds used for construction "
            "or maintenance) .If you cannot fill this, write \"N/A\". If this field should "
            "not be filled by you (for example, it belongs to another person or office), "
            "leave it blank (empty string \"\")."
        )
    )


class InnovativeTeachingGrantApplicationCoverPage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    Innovative Teaching Grant Application  
Cover Page

    ''
    """

    project_information: ProjectInformation = Field(
        ...,
        description="Project Information"
    )
    applicant_information: ApplicantInformation = Field(
        ...,
        description="Applicant Information"
    )
    authorization: Authorization = Field(
        ...,
        description="Authorization"
    )