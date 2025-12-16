from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CollegeEducationTableRow(BaseModel):
    """Single row in College Name & Location"""

    college_name_location: str = Field(default="", description="College_Name_Location")
    date_graduated: str = Field(default="", description="Date_Graduated")
    degree_earned: str = Field(default="", description="Degree_Earned")
    major_areas_of_study: str = Field(default="", description="Major_Areas_Of_Study")


class BasicInformation(BaseModel):
    """Position and personal/contact details, along with work eligibility"""

    position_applied_for: str = Field(
        ...,
        description=(
            "Job title or position you are applying for .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this application is completed")  # YYYY-MM-DD format

    full_name: str = Field(
        ...,
        description=(
            'Applicant\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address_street: str = Field(
        ...,
        description=(
            'Street address .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    address_city: str = Field(
        ...,
        description=(
            'City of current residence .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address_state: str = Field(..., description="State of current residence")

    address_zip_code: str = Field(..., description="ZIP code of current residence")

    home_phone: str = Field(
        default="",
        description=(
            "Home telephone number including area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_phone: str = Field(
        default="",
        description=(
            "Work telephone number including area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        default="",
        description=(
            'Primary email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    legally_eligible_to_work_us: BooleanLike = Field(
        ..., description="Indicate whether you are legally authorized to work in the United States"
    )

    restrictions_on_eligibility_for_employment: BooleanLike = Field(
        default="", description="Indicate if there are any work authorization restrictions"
    )

    restrictions_explanation: str = Field(
        default="",
        description=(
            "Explanation of any restrictions on your eligibility for employment .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    work_permit_under_16: BooleanLike = Field(
        default="", description="Indicate if you can provide a valid work permit if under age 16"
    )


class Education(BaseModel):
    """Educational background, degrees, and related qualifications"""

    highest_grade_completed: Literal[
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "N/A", ""
    ] = Field(..., description="Highest grade level in school that you completed")

    last_high_school_name_location: str = Field(
        ...,
        description=(
            "Name and city/state of the last high school you attended .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    did_you_graduate: BooleanLike = Field(
        default="", description="Indicate whether you graduated from high school"
    )

    have_ged: BooleanLike = Field(
        default="",
        description="Indicate whether you have a G.E.D. if you did not graduate high school",
    )

    years_post_high_school_education_completed: Literal[
        "1", "2", "3", "4", "5", "6", "7", "N/A", ""
    ] = Field(default="", description="Number of years of education completed after high school")

    college_education_table: List[CollegeEducationTableRow] = Field(
        default="",
        description=(
            "Table to list each college attended, graduation date, degree, and major "
            "area(s) of study"
        ),
    )  # List of table rows

    date_graduated: str = Field(
        default="",
        description="Graduation date for the listed college entry (see college education table)",
    )  # YYYY-MM-DD format

    degree_earned: str = Field(
        default="",
        description=(
            "Degree received for the listed college entry (see college education table) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    major_areas_of_study: str = Field(
        default="",
        description=(
            "Major field(s) of study for the listed college entry (see college education "
            'table) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    special_skills_qualifications: str = Field(
        default="",
        description=(
            "Describe any special skills, training, or qualifications relevant to the "
            'position .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class MassanuttenRegionalLibraryApplicationForEmployment(BaseModel):
    """
        MASSANUTTEN
    REGIONAL
    LIBRARY

    APPLICATION FOR EMPLOYMENT

        APPLICATION FOR EMPLOYMENT
    """

    basic_information: BasicInformation = Field(..., description="Basic Information")
    education: Education = Field(..., description="Education")
