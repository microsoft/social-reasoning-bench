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
    """Basic personal and contact details for the applicant"""

    name_last_first_middle: str = Field(
        ...,
        description=(
            "Applicant's full legal name in the order last, first, middle .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date: str = Field(..., description="Date this application is completed")  # YYYY-MM-DD format

    present_address: str = Field(
        ...,
        description=(
            "Current mailing or residential address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            "Primary phone number at present address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    permanent_address: str = Field(
        default="",
        description=(
            "Permanent mailing address if different from present address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    permanent_phone: str = Field(
        default="",
        description=(
            "Phone number associated with permanent address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        default="",
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    work_permit: BooleanLike = Field(
        default="", description="Indicate if you can furnish a valid work permit if under 18"
    )


class PositionAppliedFor(BaseModel):
    """Details about the position and type of work being sought"""

    full_time: BooleanLike = Field(
        default="", description="Check if applying for full-time employment"
    )

    part_time: BooleanLike = Field(
        default="", description="Check if applying for part-time employment"
    )

    seasonal: BooleanLike = Field(
        default="", description="Check if applying for seasonal employment"
    )

    temporary: BooleanLike = Field(
        default="", description="Check if applying for temporary employment"
    )

    other_employment_type: str = Field(
        default="",
        description=(
            "Specify other type of employment if not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    recreation: BooleanLike = Field(
        default="", description="Check if applying to work in Recreation"
    )

    parks: BooleanLike = Field(default="", description="Check if applying to work in Parks")

    aquatics: BooleanLike = Field(default="", description="Check if applying to work in Aquatics")

    office: BooleanLike = Field(default="", description="Check if applying to work in Office")

    title_of_job_position_desired_if_known: str = Field(
        default="",
        description=(
            "Specific job title you are applying for, if known .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Education(BaseModel):
    """Educational background including high school, trade school, college, and post-graduate"""

    high_school_name_and_location: str = Field(
        default="",
        description=(
            "Name and city/state of high school attended .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    high_school_course_of_study: str = Field(
        default="",
        description=(
            "Major area of study or program in high school .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    high_school_circle_highest_grade_completed: Literal["9", "10", "11", "12", "N/A", ""] = Field(
        default="", description="Highest grade level completed in high school"
    )

    high_school_type_of_degree_or_certificate_received: str = Field(
        default="",
        description=(
            "Diploma, GED, or other certificate received from high school .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    high_school_date_of_leaving: str = Field(
        default="", description="Date you left or graduated from high school"
    )  # YYYY-MM-DD format

    trade_school_name_and_location: str = Field(
        default="",
        description=(
            "Name and city/state of trade or vocational school attended .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    trade_school_course_of_study: str = Field(
        default="",
        description=(
            "Major area of study or program in trade school .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    trade_school_circle_highest_grade_completed: str = Field(
        default="",
        description=(
            "Highest level or year completed in trade school .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    trade_school_type_of_degree_or_certificate_received: str = Field(
        default="",
        description=(
            "Degree, license, or certificate received from trade school .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    trade_school_date_of_leaving: str = Field(
        default="", description="Date you left or completed trade school"
    )  # YYYY-MM-DD format

    college_name_and_location: str = Field(
        default="",
        description=(
            "Name and city/state of college or university attended .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_course_of_study: str = Field(
        default="",
        description=(
            'Major field of study in college .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    college_circle_highest_grade_completed: Literal["1", "2", "3", "4", "5", "N/A", ""] = Field(
        default="", description="Highest year or level completed in college"
    )

    college_type_of_degree_or_certificate_received: str = Field(
        default="",
        description=(
            "Degree or certificate received from college (e.g., AA, BA, BS) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    college_date_of_leaving: str = Field(
        default="", description="Date you left or graduated from college"
    )  # YYYY-MM-DD format

    post_graduate_name_and_location: str = Field(
        default="",
        description=(
            "Name and city/state of post-graduate institution attended .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    post_graduate_course_of_study: str = Field(
        default="",
        description=(
            'Field of study for post-graduate work .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    post_graduate_circle_highest_grade_completed: str = Field(
        default="",
        description=(
            "Highest level or year completed in post-graduate studies .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    post_graduate_type_of_degree_or_certificate_received: str = Field(
        default="",
        description=(
            "Post-graduate degree or certificate received (e.g., MA, MS, PhD) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    post_graduate_date_of_leaving: str = Field(
        default="", description="Date you left or completed post-graduate studies"
    )  # YYYY-MM-DD format


class SkillsandLanguages(BaseModel):
    """Additional training, skills, and language abilities"""

    other_training_or_work_related_skills: str = Field(
        default="",
        description=(
            "List any additional training, certifications, or job-related skills .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    what_languages_do_you_speak_fluently_other_than_english: str = Field(
        default="",
        description=(
            "List all non-English languages you speak fluently .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class EmploymentHistory(BaseModel):
    """Previous employment details, starting with the most recent job"""

    employment_1_name_address_phone: str = Field(
        default="",
        description=(
            "Name, address, and phone number of most recent or current employer .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    employment_1_dates_month_year: str = Field(
        default="",
        description=(
            "Start and end dates (month/year) for this employment .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    employment_1_your_position_duties_supervisor: str = Field(
        default="",
        description=(
            "Job title, main duties, and name of supervisor for this employment .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    employment_1_position_type_full_part_other: Literal["Full", "Part", "Other", "N/A", ""] = Field(
        default="", description="Indicate whether this job was full-time, part-time, or other"
    )

    employment_1_explain_your_reason_for_leaving: str = Field(
        default="",
        description=(
            'Reason you left this position .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    employment_1_may_we_contact_this_employer: BooleanLike = Field(
        default="", description="Indicate whether the employer may be contacted for a reference"
    )

    employment_2_name_address_phone: str = Field(
        default="",
        description=(
            "Name, address, and phone number of second most recent employer .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    employment_2_dates_month_year: str = Field(
        default="",
        description=(
            "Start and end dates (month/year) for this employment .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    employment_2_your_position_duties_supervisor: str = Field(
        default="",
        description=(
            "Job title, main duties, and name of supervisor for this employment .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    employment_2_position_type_full_part_other: Literal["Full", "Part", "Other", "N/A", ""] = Field(
        default="", description="Indicate whether this job was full-time, part-time, or other"
    )

    employment_2_explain_your_reason_for_leaving: str = Field(
        default="",
        description=(
            'Reason you left this position .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    employment_2_may_we_contact_this_employer: BooleanLike = Field(
        default="", description="Indicate whether the employer may be contacted for a reference"
    )

    employment_3_name_address_phone: str = Field(
        default="",
        description=(
            "Name, address, and phone number of third most recent employer .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    employment_3_dates_month_year: str = Field(
        default="",
        description=(
            "Start and end dates (month/year) for this employment .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    employment_3_your_position_duties_supervisor: str = Field(
        default="",
        description=(
            "Job title, main duties, and name of supervisor for this employment .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    employment_3_position_type_full_part_other: Literal["Full", "Part", "Other", "N/A", ""] = Field(
        default="", description="Indicate whether this job was full-time, part-time, or other"
    )

    employment_3_explain_your_reason_for_leaving: str = Field(
        default="",
        description=(
            'Reason you left this position .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    employment_3_may_we_contact_this_employer: BooleanLike = Field(
        default="", description="Indicate whether the employer may be contacted for a reference"
    )

    employment_4_name_address_phone: str = Field(
        default="",
        description=(
            "Name, address, and phone number of fourth most recent employer .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    employment_4_dates_month_year: str = Field(
        default="",
        description=(
            "Start and end dates (month/year) for this employment .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    employment_4_your_position_duties_supervisor: str = Field(
        default="",
        description=(
            "Job title, main duties, and name of supervisor for this employment .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    employment_4_position_type_full_part_other: Literal["Full", "Part", "Other", "N/A", ""] = Field(
        default="", description="Indicate whether this job was full-time, part-time, or other"
    )

    employment_4_explain_your_reason_for_leaving: str = Field(
        default="",
        description=(
            'Reason you left this position .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    employment_4_may_we_contact_this_employer: BooleanLike = Field(
        default="", description="Indicate whether the employer may be contacted for a reference"
    )


class TruckeedonnerRecreationParkDistrict(BaseModel):
    """
    TRUCKEE-DONNER RECREATION & PARK DISTRICT

    We consider applicants for all positions without regard to race, color, national origin, sex, religious creed, age, mental or physical disability, veteran status, medical condition, marital status, sexual orientation or any other legally protected status.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    position_applied_for: PositionAppliedFor = Field(..., description="Position Applied For")
    education: Education = Field(..., description="Education")
    skills_and_languages: SkillsandLanguages = Field(..., description="Skills and Languages")
    employment_history: EmploymentHistory = Field(..., description="Employment History")
