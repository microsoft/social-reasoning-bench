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
    """High school, college, and other education or training"""

    high_school_name: str = Field(
        ...,
        description=(
            'Name of the high school you attended .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_of_high_school_awarding_diploma_or_equivalency_certificate: str = Field(
        ...,
        description=(
            "Mailing address of the high school that awarded your diploma or equivalency "
            'certificate .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    received_diploma_or_equivalency_certificate_yes: BooleanLike = Field(
        ...,
        description="Indicate if you received a high school diploma or equivalency certificate (Yes)",
    )

    received_diploma_or_equivalency_certificate_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate if you did not receive a high school diploma or equivalency certificate (No)"
        ),
    )

    if_no_highest_grade_completed: str = Field(
        default="",
        description=(
            "Highest grade level completed if you did not receive a diploma or equivalency "
            'certificate .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    college_or_university_name: str = Field(
        default="",
        description=(
            "Name of the college or university you attended .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dates_attended_college_or_university: str = Field(
        default="",
        description=(
            "Date range during which you attended this college or university .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    location_college_or_university: str = Field(
        default="",
        description=(
            "City and state (or country) of the college or university .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    credit_hours_earned: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of credit hours you earned at this institution"
    )

    degrees_received_ba_ma_etc: str = Field(
        default="",
        description=(
            "Degrees received from this institution (e.g., BA, BS, MA) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_degree: str = Field(
        default="", description="Date on which the degree was awarded"
    )  # YYYY-MM-DD format

    major_field: str = Field(
        default="",
        description=(
            'Your major field of study .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    minor_field: str = Field(
        default="",
        description=(
            'Your minor field of study, if any .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    other_schools_training_name: str = Field(
        default="",
        description=(
            "Name of other school or training program that helps you qualify .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    other_schools_training_location: str = Field(
        default="",
        description=(
            "Location of the other school or training program .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_schools_training_dates_attended: str = Field(
        default="",
        description=(
            "Dates you attended the other school or training program .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    did_you_complete_yes: BooleanLike = Field(
        default="", description="Indicate if you completed this other school or training (Yes)"
    )

    did_you_complete_no: BooleanLike = Field(
        default="",
        description="Indicate if you did not complete this other school or training (No)",
    )

    title_description_of_course: str = Field(
        default="",
        description=(
            "Title or brief description of the course or training .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    total_hours: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of instructional hours for the course or training"
    )


class ProfessionalLicensesRegistrationorCertificates(BaseModel):
    """Licensing and certification information"""

    licensing_agency_name_and_complete_address: str = Field(
        default="",
        description=(
            "Full name and mailing address of the licensing agency .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    type_of_license: str = Field(
        default="",
        description=(
            "Type of professional license, registration, or certificate .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    endorsement_restriction_if_applicable: str = Field(
        default="",
        description=(
            "Any endorsements or restrictions on the license, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_licensed: str = Field(
        default="", description="Date on which the license was issued"
    )  # YYYY-MM-DD format


class SpecialSkills(BaseModel):
    """Specific skills and proficiencies"""

    typing_speed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Typing speed (e.g., words per minute)"
    )

    typing_errors: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of allowable errors at the stated typing speed"
    )

    ten_code: BooleanLike = Field(
        default="", description="Check if you are proficient with 10-code communication"
    )

    accident_investigation: BooleanLike = Field(
        default="", description="Check if you have accident investigation skills"
    )

    legal_terminology: BooleanLike = Field(
        default="", description="Check if you are familiar with legal terminology"
    )

    medical_terminology: BooleanLike = Field(
        default="", description="Check if you are familiar with medical terminology"
    )

    photo_skills: BooleanLike = Field(
        default="", description="Check if you have photography skills"
    )

    computer_software: str = Field(
        default="",
        description=(
            "List computer software programs you can use .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    computer_languages: str = Field(
        default="",
        description=(
            "List computer programming languages you know .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_special_skills_line_1: str = Field(
        default="",
        description=(
            "Other special skills or abilities (first line) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_special_skills_line_2: str = Field(
        default="",
        description=(
            "Other special skills or abilities (second line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_special_skills_line_3: str = Field(
        default="",
        description=(
            "Other special skills or abilities (third line) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_special_skills_line_4: str = Field(
        default="",
        description=(
            "Other special skills or abilities (fourth line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CriminalConvictions(BaseModel):
    """Disclosure of any adult criminal convictions"""

    criminal_convictions_line_1: str = Field(
        default="",
        description=(
            "List of criminal convictions as an adult (first line) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    criminal_convictions_line_2: str = Field(
        default="",
        description=(
            "List of criminal convictions as an adult (second line) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Equipment(BaseModel):
    """Equipment you can operate"""

    equipment_you_can_operate_line_1: str = Field(
        default="",
        description=(
            "Types of equipment you can operate (first line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    equipment_you_can_operate_line_2: str = Field(
        default="",
        description=(
            "Types of equipment you can operate (second line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    equipment_you_can_operate_line_3: str = Field(
        default="",
        description=(
            "Types of equipment you can operate (third line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    equipment_you_can_operate_line_4: str = Field(
        default="",
        description=(
            "Types of equipment you can operate (fourth line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    equipment_you_can_operate_line_5: str = Field(
        default="",
        description=(
            "Types of equipment you can operate (fifth line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Education(BaseModel):
    """EDUCATION"""

    education: Education = Field(..., description="Education")
    professional_licenses_registration_or_certificates: ProfessionalLicensesRegistrationorCertificates = Field(
        ..., description="Professional Licenses, Registration or Certificates"
    )
    special_skills: SpecialSkills = Field(..., description="Special Skills")
    criminal_convictions: CriminalConvictions = Field(..., description="Criminal Convictions")
    equipment: Equipment = Field(..., description="Equipment")
