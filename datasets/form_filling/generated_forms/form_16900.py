from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class HighSchoolEducation(BaseModel):
    """Details about high school education"""

    high_school: str = Field(
        default="",
        description=(
            'Name of the high school attended .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    high_school_address_number: str = Field(
        default="",
        description=(
            "Street number of the high school address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    high_school_address_street: str = Field(
        default="",
        description=(
            "Street name of the high school address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    high_school_address_city: str = Field(
        default="",
        description=(
            'City of the high school address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    high_school_address_state: str = Field(
        default="", description="State of the high school address"
    )

    high_school_address_zip_code: str = Field(
        default="", description="ZIP code of the high school address"
    )

    high_school_phone: str = Field(
        default="",
        description=(
            'Phone number of the high school .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    high_school_dates_attended_from_month_year: str = Field(
        default="",
        description=(
            "Start date attended at high school (month/year) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    high_school_dates_attended_to_month_year: str = Field(
        default="",
        description=(
            "End date attended at high school (month/year) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    high_school_gpa: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Grade point average achieved in high school"
    )

    high_school_diploma_yes: BooleanLike = Field(
        default="", description="Check if a high school diploma was received"
    )

    high_school_diploma_no: BooleanLike = Field(
        default="", description="Check if a high school diploma was not received"
    )

    high_school_ged_yes: BooleanLike = Field(default="", description="Check if a GED was received")

    high_school_ged_no: BooleanLike = Field(
        default="", description="Check if a GED was not received"
    )


class CollegeUniversityEducation1(BaseModel):
    """Details about first college or university attended"""

    college_university_name_1: str = Field(
        default="",
        description=(
            "Name of the first college or university attended .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_university_1_address_number: str = Field(
        default="",
        description=(
            "Street number of the first college/university address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_university_1_address_street: str = Field(
        default="",
        description=(
            "Street name of the first college/university address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_university_1_address_city: str = Field(
        default="",
        description=(
            "City of the first college/university address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    college_university_1_address_state: str = Field(
        default="", description="State of the first college/university address"
    )

    college_university_1_address_zip_code: str = Field(
        default="", description="ZIP code of the first college/university address"
    )

    college_university_1_phone: str = Field(
        default="",
        description=(
            "Phone number of the first college or university .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_university_1_dates_attended_from_month_year: str = Field(
        default="",
        description=(
            "Start date attended at the first college/university (month/year) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    college_university_1_dates_attended_to_month_year: str = Field(
        default="",
        description=(
            "End date attended at the first college/university (month/year) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    college_university_1_gpa: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Grade point average at the first college/university"
    )

    college_university_1_graduation_date_month_year: str = Field(
        default="",
        description=(
            "Graduation date from the first college/university (month/year) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    college_university_1_type_of_degree: str = Field(
        default="",
        description=(
            "Type of degree earned at the first college/university .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_university_1_number_of_credits: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of credits earned at the first college/university"
    )

    college_university_1_major_field_of_study: str = Field(
        default="",
        description=(
            "Major field of study at the first college/university .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CollegeUniversityEducation2(BaseModel):
    """Details about second college or university attended"""

    college_university_name_2: str = Field(
        default="",
        description=(
            "Name of the second college or university attended .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_university_2_address_number: str = Field(
        default="",
        description=(
            "Street number of the second college/university address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_university_2_address_street: str = Field(
        default="",
        description=(
            "Street name of the second college/university address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_university_2_address_city: str = Field(
        default="",
        description=(
            "City of the second college/university address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    college_university_2_address_state: str = Field(
        default="", description="State of the second college/university address"
    )

    college_university_2_address_zip_code: str = Field(
        default="", description="ZIP code of the second college/university address"
    )

    college_university_2_phone: str = Field(
        default="",
        description=(
            "Phone number of the second college or university .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_university_2_dates_attended_from_month_year: str = Field(
        default="",
        description=(
            "Start date attended at the second college/university (month/year) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    college_university_2_dates_attended_to_month_year: str = Field(
        default="",
        description=(
            "End date attended at the second college/university (month/year) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    college_university_2_gpa: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Grade point average at the second college/university"
    )

    college_university_2_graduation_date_month_year: str = Field(
        default="",
        description=(
            "Graduation date from the second college/university (month/year) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    college_university_2_type_of_degree: str = Field(
        default="",
        description=(
            "Type of degree earned at the second college/university .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_university_2_number_of_credits: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of credits earned at the second college/university"
    )

    college_university_2_major_field_of_study: str = Field(
        default="",
        description=(
            "Major field of study at the second college/university .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class OrganizationsandHonors(BaseModel):
    """Memberships, honors, awards, and recognitions"""

    organizations_belonged_to_excluding_race_religion_national_group: str = Field(
        default="",
        description=(
            "List organizations you belong to, excluding those indicating race, religion, "
            'or national group .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    honors_awards_or_other_forms_of_recognition: str = Field(
        default="",
        description=(
            "List honors, awards, or other recognition received for scholarship, athletics, "
            'or other achievements .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class EducationalBackground(BaseModel):
    """
    Educational Background

    ''
    """

    high_school_education: HighSchoolEducation = Field(..., description="High School Education")
    collegeuniversity_education_1: CollegeUniversityEducation1 = Field(
        ..., description="College/University Education (1)"
    )
    collegeuniversity_education_2: CollegeUniversityEducation2 = Field(
        ..., description="College/University Education (2)"
    )
    organizations_and_honors: OrganizationsandHonors = Field(
        ..., description="Organizations and Honors"
    )
