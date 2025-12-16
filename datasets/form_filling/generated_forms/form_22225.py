from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CareerData(BaseModel):
    """Professional background and previous mentoring experience"""

    employment_history: str = Field(
        default="",
        description=(
            "Describe your past employment positions and relevant work experience. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    current_projects_activities: str = Field(
        default="",
        description=(
            "List your current professional projects, research, or activities. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    number_of_employees: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Approximate number of employees in your organization, team, or group.",
    )

    no_are_you_a_member_of_a_network: BooleanLike = Field(
        default="", description="Check if you are not a member of any professional network."
    )

    yes_are_you_a_member_of_a_network: BooleanLike = Field(
        default="", description="Check if you are a member of a professional network."
    )

    which_network: str = Field(
        default="",
        description=(
            "Name of the network you are a member of. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    no_have_you_ever_participated_in_a_mentoring_program_before: BooleanLike = Field(
        default="",
        description="Check if you have never participated in a mentoring program before.",
    )

    yes_have_you_ever_participated_in_a_mentoring_program_before: BooleanLike = Field(
        default="", description="Check if you have participated in a mentoring program before."
    )

    which_mentoring_program: str = Field(
        default="",
        description=(
            "Name of the mentoring program you participated in. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    as_mentee: BooleanLike = Field(
        default="",
        description="Check if your previous mentoring program participation was as a mentee.",
    )

    as_mentor: BooleanLike = Field(
        default="",
        description="Check if your previous mentoring program participation was as a mentor.",
    )


class ExpectationsfromMentee(BaseModel):
    """Preferences regarding the mentee/mentor relationship"""

    female_mentor_preferred: BooleanLike = Field(
        default="", description="Check if you prefer a female mentor."
    )

    male_mentor_preferred: BooleanLike = Field(
        default="", description="Check if you prefer a male mentor."
    )

    mentor_gender_not_important: BooleanLike = Field(
        default="", description="Check if the gender of your mentor is not important to you."
    )


class CareerData(BaseModel):
    """
    Career Data

    ''
    """

    career_data: CareerData = Field(..., description="Career Data")
    expectations_from_mentee: ExpectationsfromMentee = Field(
        ..., description="Expectations from Mentee"
    )
