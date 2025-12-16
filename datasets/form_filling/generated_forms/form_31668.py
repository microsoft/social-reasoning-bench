from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Education(BaseModel):
    """Educational background including schools attended, courses of study, years completed, and diplomas/degrees obtained"""

    high_school_name_and_address_of_school: str = Field(
        default="",
        description=(
            "Name and full mailing address of the high school attended .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    high_school_course_of_study: str = Field(
        default="",
        description=(
            "Major area of study or program completed in high school .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    high_school_years_completed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years of high school completed"
    )

    high_school_diploma_degree_obtained: str = Field(
        default="",
        description=(
            "Type of diploma or certificate received from high school .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    undergraduate_college_name_and_address_of_school: str = Field(
        default="",
        description=(
            "Name and full mailing address of the undergraduate college attended .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    undergraduate_college_course_of_study: str = Field(
        default="",
        description=(
            "Major field(s) of study at the undergraduate college .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    undergraduate_college_years_completed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years of undergraduate college completed"
    )

    undergraduate_college_diploma_degree_obtained: str = Field(
        default="",
        description=(
            "Degree or diploma received from the undergraduate college .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    graduate_professional_name_and_address_of_school: str = Field(
        default="",
        description=(
            "Name and full mailing address of the graduate or professional school attended "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    graduate_professional_course_of_study: str = Field(
        default="",
        description=(
            "Graduate or professional program or major field of study .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    graduate_professional_years_completed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years of graduate or professional study completed"
    )

    graduate_professional_diploma_degree_obtained: str = Field(
        default="",
        description=(
            "Graduate or professional degree or diploma received .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_specify_name_and_address_of_school: str = Field(
        default="",
        description=(
            "Name and full mailing address of any other school or training program (specify "
            'type) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    other_specify_course_of_study: str = Field(
        default="",
        description=(
            "Course of study or training for the other school or program .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    other_specify_years_completed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years completed in the other school or program"
    )

    other_specify_diploma_degree_obtained: str = Field(
        default="",
        description=(
            "Diploma, certificate, or degree received from the other school or program .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class RelatedInformationProfessionalOrganizations(BaseModel):
    """Job-related organizations and offices held"""

    related_information_organizations_belong: str = Field(
        default="",
        description=(
            "List job-related professional, trade, or similar organizations you belong to, "
            "excluding any that reveal protected characteristics .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    organization_row_1: str = Field(
        default="",
        description=(
            'Name of the first organization .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    offices_held_row_1: str = Field(
        default="",
        description=(
            "Office or position held in the first organization, if any .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    organization_row_2: str = Field(
        default="",
        description=(
            'Name of the second organization .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    offices_held_row_2: str = Field(
        default="",
        description=(
            "Office or position held in the second organization, if any .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    organization_row_3: str = Field(
        default="",
        description=(
            'Name of the third organization .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    offices_held_row_3: str = Field(
        default="",
        description=(
            "Office or position held in the third organization, if any .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    organization_row_4: str = Field(
        default="",
        description=(
            'Name of the fourth organization .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    offices_held_row_4: str = Field(
        default="",
        description=(
            "Office or position held in the fourth organization, if any .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    organization_row_5: str = Field(
        default="",
        description=(
            'Name of the fifth organization .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    offices_held_row_5: str = Field(
        default="",
        description=(
            "Office or position held in the fifth organization, if any .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class StatementofInterest(BaseModel):
    """Explanation of why the applicant would like to be considered for employment"""

    explain_why_considered_employment_line_1: str = Field(
        default="",
        description=(
            "Explanation of your interest in employment with Sandusky Library (first line) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    explain_why_considered_employment_line_2: str = Field(
        default="",
        description=(
            "Continuation of your explanation (second line) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    explain_why_considered_employment_line_3: str = Field(
        default="",
        description=(
            "Continuation of your explanation (third line) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    explain_why_considered_employment_line_4: str = Field(
        default="",
        description=(
            "Continuation of your explanation (fourth line) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Education(BaseModel):
    """
    EDUCATION

    ''
    """

    education: Education = Field(..., description="Education")
    related_information___professional_organizations: RelatedInformationProfessionalOrganizations = Field(
        ..., description="Related Information - Professional Organizations"
    )
    statement_of_interest: StatementofInterest = Field(..., description="Statement of Interest")
