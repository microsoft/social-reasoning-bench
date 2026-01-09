from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ExperienceGeneralPreference(BaseModel):
    """General question about contacting present employer"""

    informed_before_contact_present_employer: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether you wish to be notified before your present employer is "
            "contacted for a reference."
        ),
    )


class ExperiencePosition1(BaseModel):
    """Details for most recent or first listed position"""

    name_and_address_of_employer: str = Field(
        ...,
        description=(
            "Full name and mailing address of this employer. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    type_of_business: str = Field(
        ...,
        description=(
            "General type of business or industry (e.g., retail, manufacturing, education). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    date_employed: str = Field(
        ..., description="Date you started this employment (and end date if requested on the form)."
    )  # YYYY-MM-DD format

    average_hours_per_week: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Average number of hours you worked per week in this position."
    )

    your_job_title: str = Field(
        ...,
        description=(
            "Official job title you held with this employer. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    full_time: BooleanLike = Field(..., description="Check if this position was full-time.")

    part_time: BooleanLike = Field(..., description="Check if this position was part-time.")

    volunteer: BooleanLike = Field(..., description="Check if this position was a volunteer role.")

    immediate_supervisors: str = Field(
        ...,
        description=(
            "Name(s) of your immediate supervisor(s) for this position. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        ...,
        description=(
            "Phone number for your immediate supervisor or employer contact. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    describe_your_duties_in_detail: str = Field(
        ...,
        description=(
            "Detailed description of your responsibilities, required "
            "knowledge/skills/abilities, staff supervised, and key accomplishments. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reason_for_leaving: str = Field(
        ...,
        description=(
            "Brief explanation of why you left this position. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ExperiencePosition2(BaseModel):
    """Details for second listed position"""

    name_and_address_of_employer_2: str = Field(
        default="",
        description=(
            "Full name and mailing address of your next most recent employer. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    type_of_business_2: str = Field(
        default="",
        description=(
            "General type of business or industry for this employer (e.g., retail, "
            'manufacturing, education). .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_employed_2: str = Field(
        default="",
        description="Date you started this employment (and end date if requested) for this employer.",
    )  # YYYY-MM-DD format

    average_hours_per_week_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Average number of hours you worked per week in this position."
    )

    your_job_title_2: str = Field(
        default="",
        description=(
            "Official job title you held with this employer. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    full_time_2: BooleanLike = Field(
        default="", description="Check if this position was full-time."
    )

    part_time_2: BooleanLike = Field(
        default="", description="Check if this position was part-time."
    )

    volunteer_2: BooleanLike = Field(
        default="", description="Check if this position was a volunteer role."
    )

    immediate_supervisors_2: str = Field(
        default="",
        description=(
            "Name(s) of your immediate supervisor(s) for this position. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number_2: str = Field(
        default="",
        description=(
            "Phone number for your immediate supervisor or employer contact. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    describe_your_duties_in_detail_2: str = Field(
        default="",
        description=(
            "Detailed description of your responsibilities, required "
            "knowledge/skills/abilities, staff supervised, and key accomplishments for this "
            'position. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    reason_for_leaving_2: str = Field(
        default="",
        description=(
            "Brief explanation of why you left this position. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Experience(BaseModel):
    """
    EXPERIENCE

    Begin with your present or most recent job and list your work experience with emphasis on experience that is relevant to the position for which you are applying. Include military service and any volunteer work experience that would help you qualify. List each promotion as a separate position. You may respond to this section on a separate sheet of paper provided you answer all questions in the blocks and follow the same format. On each sheet, write your name and the job title for which you are applying. This information must be completed even if you submit a resume.
    Notice to applicants: Information that you provide on this application is subject to verification. Previous employers may be contacted as references. Do you want to be informed before we contact your present employer? Yes ( ) No ( )
    """

    experience___general_preference: ExperienceGeneralPreference = Field(
        ..., description="Experience - General Preference"
    )
    experience___position_1: ExperiencePosition1 = Field(..., description="Experience - Position 1")
    experience___position_2: ExperiencePosition2 = Field(..., description="Experience - Position 2")
