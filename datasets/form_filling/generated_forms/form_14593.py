from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class GeneralInformation(BaseModel):
    """Personal and contact information for the student"""

    last_name: str = Field(
        ...,
        description=(
            'Applicant\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Applicant\'s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    mi: str = Field(
        default="",
        description=(
            'Middle initial .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    social_security_number: str = Field(..., description="Applicant's Social Security Number")

    students_college_address_number_street_apt_no: str = Field(
        ...,
        description=(
            "Street address of the student's college residence, including apartment number "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    telephone_no_college: str = Field(
        ...,
        description=(
            "Telephone number at the college address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_college_address: str = Field(
        ...,
        description=(
            "City for the student's college address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_college_address: str = Field(..., description="State for the student's college address")

    zip_code_college_address: str = Field(
        ..., description="ZIP code for the student's college address"
    )

    students_permanent_address_number_street_apt_no: str = Field(
        ...,
        description=(
            "Student's permanent street address, including apartment number .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    telephone_no_permanent: str = Field(
        ...,
        description=(
            "Telephone number at the permanent address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_permanent_address: str = Field(
        ...,
        description=(
            "City for the student's permanent address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_permanent_address: str = Field(
        ..., description="State for the student's permanent address"
    )

    zip_code_permanent_address: str = Field(
        ..., description="ZIP code for the student's permanent address"
    )

    email_address: str = Field(
        ...,
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    have_you_previously_worked_with_dced_as_an_intern_yes: BooleanLike = Field(
        default="", description="Select if you have previously worked with DCED as an intern"
    )

    have_you_previously_worked_with_dced_as_an_intern_no: BooleanLike = Field(
        default="", description="Select if you have not previously worked with DCED as an intern"
    )


class EducationSkills(BaseModel):
    """Educational background, skills, and related eligibility information"""

    check_highest_level_completed_high_school: BooleanLike = Field(
        default="", description="Check if High School is the highest level completed"
    )

    check_highest_level_completed_1st_year_college: BooleanLike = Field(
        default="", description="Check if 1st Year College is the highest level completed"
    )

    check_highest_level_completed_2nd_year: BooleanLike = Field(
        default="", description="Check if 2nd Year is the highest level completed"
    )

    check_highest_level_completed_3rd_year: BooleanLike = Field(
        default="", description="Check if 3rd Year is the highest level completed"
    )

    check_highest_level_completed_4th_year: BooleanLike = Field(
        default="", description="Check if 4th Year is the highest level completed"
    )

    check_highest_level_completed_5th_year: BooleanLike = Field(
        default="", description="Check if 5th Year is the highest level completed"
    )

    check_highest_level_completed_6th_year: BooleanLike = Field(
        default="", description="Check if 6th Year is the highest level completed"
    )

    name_location_row_1: str = Field(
        default="",
        description=(
            "Name and location (city and ZIP code) of the first college, university, or "
            'professional school .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    dates_attended_from_row_1: str = Field(
        default="", description="Start date of attendance for the first institution"
    )  # YYYY-MM-DD format

    dates_attended_to_row_1: str = Field(
        default="", description="End date of attendance for the first institution"
    )  # YYYY-MM-DD format

    did_you_graduate_row_1_yes: BooleanLike = Field(
        default="", description="For the first institution, select if you graduated"
    )

    did_you_graduate_row_1_no: BooleanLike = Field(
        default="", description="For the first institution, select if you did not graduate"
    )

    anticipated_date_of_graduation_row_1: str = Field(
        default="",
        description="Anticipated graduation date for the first institution (if applicable)",
    )  # YYYY-MM-DD format

    type_of_degree_row_1: str = Field(
        default="",
        description=(
            "Type of degree earned or expected at the first institution (e.g., B.A., B.S.) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    major_course_of_study_row_1: str = Field(
        default="",
        description=(
            "Major field of study at the first institution .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_location_row_2: str = Field(
        default="",
        description=(
            "Name and location (city and ZIP code) of the second college, university, or "
            'professional school .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    dates_attended_from_row_2: str = Field(
        default="", description="Start date of attendance for the second institution"
    )  # YYYY-MM-DD format

    dates_attended_to_row_2: str = Field(
        default="", description="End date of attendance for the second institution"
    )  # YYYY-MM-DD format

    did_you_graduate_row_2_yes: BooleanLike = Field(
        default="", description="For the second institution, select if you graduated"
    )

    did_you_graduate_row_2_no: BooleanLike = Field(
        default="", description="For the second institution, select if you did not graduate"
    )

    anticipated_date_of_graduation_row_2: str = Field(
        default="",
        description="Anticipated graduation date for the second institution (if applicable)",
    )  # YYYY-MM-DD format

    type_of_degree_row_2: str = Field(
        default="",
        description=(
            "Type of degree earned or expected at the second institution .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    major_course_of_study_row_2: str = Field(
        default="",
        description=(
            "Major field of study at the second institution .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_location_row_3: str = Field(
        default="",
        description=(
            "Name and location (city and ZIP code) of the third college, university, or "
            'professional school .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    dates_attended_from_row_3: str = Field(
        default="", description="Start date of attendance for the third institution"
    )  # YYYY-MM-DD format

    dates_attended_to_row_3: str = Field(
        default="", description="End date of attendance for the third institution"
    )  # YYYY-MM-DD format

    did_you_graduate_row_3_yes: BooleanLike = Field(
        default="", description="For the third institution, select if you graduated"
    )

    did_you_graduate_row_3_no: BooleanLike = Field(
        default="", description="For the third institution, select if you did not graduate"
    )

    anticipated_date_of_graduation_row_3: str = Field(
        default="",
        description="Anticipated graduation date for the third institution (if applicable)",
    )  # YYYY-MM-DD format

    type_of_degree_row_3: str = Field(
        default="",
        description=(
            "Type of degree earned or expected at the third institution .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_course_of_study_row_3: str = Field(
        default="",
        description=(
            "Major field of study at the third institution .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_location_row_4: str = Field(
        default="",
        description=(
            "Name and location (city and ZIP code) of the fourth college, university, or "
            'professional school .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    dates_attended_from_row_4: str = Field(
        default="", description="Start date of attendance for the fourth institution"
    )  # YYYY-MM-DD format

    dates_attended_to_row_4: str = Field(
        default="", description="End date of attendance for the fourth institution"
    )  # YYYY-MM-DD format

    did_you_graduate_row_4_yes: BooleanLike = Field(
        default="", description="For the fourth institution, select if you graduated"
    )

    did_you_graduate_row_4_no: BooleanLike = Field(
        default="", description="For the fourth institution, select if you did not graduate"
    )

    anticipated_date_of_graduation_row_4: str = Field(
        default="",
        description="Anticipated graduation date for the fourth institution (if applicable)",
    )  # YYYY-MM-DD format

    type_of_degree_row_4: str = Field(
        default="",
        description=(
            "Type of degree earned or expected at the fourth institution .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    major_course_of_study_row_4: str = Field(
        default="",
        description=(
            "Major field of study at the fourth institution .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    list_special_qualifications_and_skills: str = Field(
        default="",
        description=(
            "List any special qualifications and skills (e.g., certifications, technical "
            'skills, equipment operation) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    do_you_have_relatives_working_in_dced_yes: BooleanLike = Field(
        default="", description="Select if you have relatives working in DCED"
    )

    do_you_have_relatives_working_in_dced_no: BooleanLike = Field(
        default="", description="Select if you do not have relatives working in DCED"
    )

    name_of_relative_working_in_dced: str = Field(
        default="",
        description=(
            "Name of the relative who works in DCED (if applicable) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    relationship_of_relative_working_in_dced: str = Field(
        default="",
        description=(
            "Relationship of the DCED employee to you (e.g., parent, sibling) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    are_you_currently_enrolled_in_college_full_time_yes: BooleanLike = Field(
        ..., description="Select if you are currently enrolled in college full-time"
    )

    are_you_currently_enrolled_in_college_full_time_no: BooleanLike = Field(
        ..., description="Select if you are not currently enrolled in college full-time"
    )

    are_you_registered_or_intend_to_register_full_time_next_term_yes: BooleanLike = Field(
        ...,
        description=(
            "Select if you are registered or intend to register full-time in college next "
            "term/semester"
        ),
    )

    are_you_registered_or_intend_to_register_full_time_next_term_no: BooleanLike = Field(
        ...,
        description=(
            "Select if you are not registered and do not intend to register full-time in "
            "college next term/semester"
        ),
    )


class PADeptCommunityEconDevInternshipApp(BaseModel):
    """
        COMMONWEALTH OF PENNSYLVANIA
    DEPARTMENT OF COMMUNITY & ECONOMIC DEVELOPMENT
    ADMINISTRATION DEPUTATE

    APPLICATION FOR THE
    DCED INTERNSHIP PROGRAM

        APPLICATION FOR THE DCED INTERNSHIP PROGRAM
    """

    general_information: GeneralInformation = Field(..., description="General Information")
    education__skills: EducationSkills = Field(..., description="Education / Skills")
