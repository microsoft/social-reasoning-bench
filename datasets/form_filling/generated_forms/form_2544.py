from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AdditionalEmploymentExperiencePosition1(BaseModel):
    """Details for first additional employment experience"""

    name_and_address_of_employer_1: str = Field(
        default="",
        description=(
            "Full name and mailing address of the employer for this position .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    type_of_business_1: str = Field(
        default="",
        description=(
            "Industry or nature of the employer's business .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_employed_1: str = Field(
        default="",
        description=(
            "Dates of employment for this position (e.g., from/to) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    average_hours_per_week_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Average number of hours worked per week in this position"
    )

    your_job_title_1: str = Field(
        default="",
        description=(
            'Official job title for this position .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    full_time_1: BooleanLike = Field(default="", description="Check if this position was full-time")

    part_time_1: BooleanLike = Field(default="", description="Check if this position was part-time")

    volunteer_1: BooleanLike = Field(
        default="", description="Check if this position was volunteer work"
    )

    immediate_supervisors_1: str = Field(
        default="",
        description=(
            "Name(s) of your immediate supervisor(s) for this position .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number_1: str = Field(
        default="",
        description=(
            "Phone number for your immediate supervisor or employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    describe_your_duties_line_1_1: str = Field(
        default="",
        description=(
            "First line describing your duties, required skills, supervision, and "
            'accomplishments for this position .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    describe_your_duties_line_2_1: str = Field(
        default="",
        description=(
            "Second line describing your duties, required skills, supervision, and "
            'accomplishments for this position .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    describe_your_duties_line_3_1: str = Field(
        default="",
        description=(
            "Third line describing your duties, required skills, supervision, and "
            'accomplishments for this position .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    describe_your_duties_line_4_1: str = Field(
        default="",
        description=(
            "Fourth line describing your duties, required skills, supervision, and "
            'accomplishments for this position .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_leaving_1: str = Field(
        default="",
        description=(
            'Primary reason you left this position .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_leaving_additional_line_1: str = Field(
        default="",
        description=(
            "Additional space to explain your reason for leaving this position .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AdditionalEmploymentExperiencePosition2(BaseModel):
    """Details for second additional employment experience"""

    name_and_address_of_employer_2: str = Field(
        default="",
        description=(
            "Full name and mailing address of the second employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    type_of_business_2: str = Field(
        default="",
        description=(
            "Industry or nature of the second employer's business .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_employed_2: str = Field(
        default="",
        description=(
            "Dates of employment for the second position (e.g., from/to) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    average_hours_per_week_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Average number of hours worked per week in the second position"
    )

    your_job_title_2: str = Field(
        default="",
        description=(
            "Official job title for the second position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    full_time_2: BooleanLike = Field(
        default="", description="Check if the second position was full-time"
    )

    part_time_2: BooleanLike = Field(
        default="", description="Check if the second position was part-time"
    )

    volunteer_2: BooleanLike = Field(
        default="", description="Check if the second position was volunteer work"
    )

    immediate_supervisors_2: str = Field(
        default="",
        description=(
            "Name(s) of your immediate supervisor(s) for the second position .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    phone_number_2: str = Field(
        default="",
        description=(
            "Phone number for your supervisor or employer for the second position .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    describe_your_duties_2_line_1: str = Field(
        default="",
        description=(
            "First line describing your duties, required skills, supervision, and "
            "accomplishments for the second position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    describe_your_duties_2_line_2: str = Field(
        default="",
        description=(
            "Second line describing your duties, required skills, supervision, and "
            "accomplishments for the second position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    describe_your_duties_2_line_3: str = Field(
        default="",
        description=(
            "Third line describing your duties, required skills, supervision, and "
            "accomplishments for the second position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    describe_your_duties_2_line_4: str = Field(
        default="",
        description=(
            "Fourth line describing your duties, required skills, supervision, and "
            "accomplishments for the second position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_leaving_2: str = Field(
        default="",
        description=(
            "Primary reason you left the second position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_leaving_2_additional_line: str = Field(
        default="",
        description=(
            "Additional space to explain your reason for leaving the second position .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AdditionalEmploymentExperiencePosition3(BaseModel):
    """Details for third additional employment experience"""

    name_and_address_of_employer_3: str = Field(
        default="",
        description=(
            "Full name and mailing address of the third employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    type_of_business_3: str = Field(
        default="",
        description=(
            "Industry or nature of the third employer's business .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_employed_3: str = Field(
        default="",
        description=(
            "Dates of employment for the third position (e.g., from/to) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    average_hours_per_week_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Average number of hours worked per week in the third position"
    )

    your_job_title_3: str = Field(
        default="",
        description=(
            "Official job title for the third position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    full_time_3: BooleanLike = Field(
        default="", description="Check if the third position was full-time"
    )

    part_time_3: BooleanLike = Field(
        default="", description="Check if the third position was part-time"
    )

    volunteer_3: BooleanLike = Field(
        default="", description="Check if the third position was volunteer work"
    )

    immediate_supervisors_3: str = Field(
        default="",
        description=(
            "Name(s) of your immediate supervisor(s) for the third position .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    phone_number_3: str = Field(
        default="",
        description=(
            "Phone number for your supervisor or employer for the third position .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    describe_your_duties_3_line_1: str = Field(
        default="",
        description=(
            "First line describing your duties, required skills, supervision, and "
            "accomplishments for the third position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    describe_your_duties_3_line_2: str = Field(
        default="",
        description=(
            "Second line describing your duties, required skills, supervision, and "
            "accomplishments for the third position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    describe_your_duties_3_line_3: str = Field(
        default="",
        description=(
            "Third line describing your duties, required skills, supervision, and "
            "accomplishments for the third position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    describe_your_duties_3_line_4: str = Field(
        default="",
        description=(
            "Fourth line describing your duties, required skills, supervision, and "
            "accomplishments for the third position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_leaving_3: str = Field(
        default="",
        description=(
            "Primary reason you left the third position .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalEmploymentExperience(BaseModel):
    """
    ADDITIONAL EMPLOYMENT EXPERIENCE

    ''
    """

    additional_employment_experience___position_1: AdditionalEmploymentExperiencePosition1 = Field(
        ..., description="Additional Employment Experience - Position 1"
    )
    additional_employment_experience___position_2: AdditionalEmploymentExperiencePosition2 = Field(
        ..., description="Additional Employment Experience - Position 2"
    )
    additional_employment_experience___position_3: AdditionalEmploymentExperiencePosition3 = Field(
        ..., description="Additional Employment Experience - Position 3"
    )
