from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PositionEmployer(BaseModel):
    """Employer and position being applied for"""

    employer: str = Field(
        ...,
        description=(
            "Name of the employer or company receiving this application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    position_applying_for: str = Field(
        ...,
        description=(
            "Title of the position you are applying for .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PersonalData(BaseModel):
    """Applicant personal and contact information"""

    name_last_first_middle: str = Field(
        ...,
        description=(
            "Your full legal name in the order last, first, middle .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    street_address_and_or_mailing_address: str = Field(
        ...,
        description=(
            "Your current street and/or mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of your current address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of your current address")

    zip: str = Field(..., description="ZIP or postal code of your current address")

    home_telephone_number: str = Field(
        default="",
        description=(
            'Home phone number with area code .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    business_telephone_number: str = Field(
        default="",
        description=(
            "Work or business phone number with area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    cellular_telephone_number: str = Field(
        default="",
        description=(
            "Mobile or cellular phone number with area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_you_can_start_work: str = Field(
        ..., description="Earliest date you are available to begin work"
    )  # YYYY-MM-DD format

    salary_desired: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Desired starting salary or pay rate"
    )

    high_school_diploma_or_ged_yes: BooleanLike = Field(
        ..., description="Select if you have a high school diploma or GED"
    )

    high_school_diploma_or_ged_no: BooleanLike = Field(
        ..., description="Select if you do not have a high school diploma or GED"
    )


class PositionInformation(BaseModel):
    """Availability, work status, and eligibility"""

    hours_full_time: BooleanLike = Field(
        default="", description="Check if you are willing to work full-time hours"
    )

    hours_part_time: BooleanLike = Field(
        default="", description="Check if you are willing to work part-time hours"
    )

    hours_days: BooleanLike = Field(
        default="", description="Check if you are willing to work day shifts"
    )

    hours_evenings: BooleanLike = Field(
        default="", description="Check if you are willing to work evening shifts"
    )

    hours_swing: BooleanLike = Field(
        default="", description="Check if you are willing to work swing shifts"
    )

    hours_graveyard: BooleanLike = Field(
        default="", description="Check if you are willing to work graveyard or overnight shifts"
    )

    hours_weekends: BooleanLike = Field(
        default="", description="Check if you are willing to work on weekends"
    )

    status_regular: BooleanLike = Field(
        default="", description="Check if you are willing to work in a regular (ongoing) position"
    )

    status_temporary: BooleanLike = Field(
        default="", description="Check if you are willing to work in a temporary position"
    )

    authorized_to_work_us_yes: BooleanLike = Field(
        ...,
        description="Select if you are legally authorized to work in the U.S. without restrictions",
    )

    authorized_to_work_us_no: BooleanLike = Field(
        ...,
        description=(
            "Select if you are not legally authorized to work in the U.S. without restrictions"
        ),
    )

    felony_conviction_yes: BooleanLike = Field(
        ..., description="Select if you have been convicted of a felony"
    )

    felony_conviction_no: BooleanLike = Field(
        ..., description="Select if you have not been convicted of a felony"
    )

    felony_explanation: str = Field(
        default="",
        description=(
            "If you answered yes to felony conviction, provide details and explanation .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    told_essential_functions_yes: BooleanLike = Field(
        ..., description="Select if you have been informed of or seen the job's essential functions"
    )

    told_essential_functions_no: BooleanLike = Field(
        ...,
        description="Select if you have not been informed of or seen the job's essential functions",
    )

    can_perform_essential_functions_yes: BooleanLike = Field(
        ...,
        description=(
            "Select if you can perform the essential job functions with or without "
            "reasonable accommodation"
        ),
    )

    can_perform_essential_functions_no: BooleanLike = Field(
        ...,
        description=(
            "Select if you cannot perform the essential job functions with or without "
            "reasonable accommodation"
        ),
    )


class Qualifications(BaseModel):
    """Education and training related to the position"""

    school_name_school_row_1: str = Field(
        default="",
        description=(
            "Name of the first school listed under qualifications .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    degree_school_row_1: str = Field(
        default="",
        description=(
            "Degree, certificate, or program for the first school listed .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address_city_state_school_row_1: str = Field(
        default="",
        description=(
            "Address, city, and state for the first school listed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    school_name_school_row_2: str = Field(
        default="",
        description=(
            "Name of the second school listed under qualifications .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    degree_school_row_2: str = Field(
        default="",
        description=(
            "Degree, certificate, or program for the second school listed .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address_city_state_school_row_2: str = Field(
        default="",
        description=(
            "Address, city, and state for the second school listed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    school_name_other_row: str = Field(
        default="",
        description=(
            "Name of any other school, training, or program listed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    degree_other_row: str = Field(
        default="",
        description=(
            "Degree, certificate, or program for the other school or training listed .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address_city_state_other_row: str = Field(
        default="",
        description=(
            "Address, city, and state for the other school or training listed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SpecialSkills(BaseModel):
    """Additional skills or experience relevant to the position"""

    special_skills_or_experience: str = Field(
        default="",
        description=(
            "List any special skills, experience, leadership roles, or organizations "
            'relevant to the position .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class References(BaseModel):
    """Professional or personal references"""

    reference_1_name: str = Field(
        default="",
        description=(
            'Full name of your first reference .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_1_address_city_state: str = Field(
        default="",
        description=(
            "Mailing address, city, and state of your first reference .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_1_phone: str = Field(
        default="",
        description=(
            'Phone number of your first reference .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_1_relationship: str = Field(
        default="",
        description=(
            "Your relationship to the first reference (e.g., supervisor, coworker) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reference_2_name: str = Field(
        default="",
        description=(
            'Full name of your second reference .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_address_city_state: str = Field(
        default="",
        description=(
            "Mailing address, city, and state of your second reference .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_phone: str = Field(
        default="",
        description=(
            'Phone number of your second reference .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_relationship: str = Field(
        default="",
        description=(
            "Your relationship to the second reference (e.g., supervisor, coworker) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reference_3_name: str = Field(
        default="",
        description=(
            'Full name of your third reference .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_3_address_city_state: str = Field(
        default="",
        description=(
            "Mailing address, city, and state of your third reference .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_3_phone: str = Field(
        default="",
        description=(
            'Phone number of your third reference .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_3_relationship: str = Field(
        default="",
        description=(
            "Your relationship to the third reference (e.g., supervisor, coworker) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class StandardApplicationForEmployment(BaseModel):
    """
    Standard Application for Employment

    It is our policy to comply with all applicable state and federal laws prohibiting discrimination in employment based on race, age, color, sex, religion, national origin, disability or other protected classifications.
    Please carefully read and answer all questions. You will not be considered for employment if you fail to completely answer all the questions on this application. You may attach a résumé, but all questions must be answered.
    """

    position__employer: PositionEmployer = Field(..., description="Position & Employer")
    personal_data: PersonalData = Field(..., description="Personal Data")
    position_information: PositionInformation = Field(..., description="Position Information")
    qualifications: Qualifications = Field(..., description="Qualifications")
    special_skills: SpecialSkills = Field(..., description="Special Skills")
    references: References = Field(..., description="References")
