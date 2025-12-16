from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EmploymentHistory(BaseModel):
    """Employment history for the last 10 years, including up to three employers"""

    current_employers_name: str = Field(
        ...,
        description=(
            "Name of your current or most recent employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    employers_address: str = Field(
        ...,
        description=(
            "Street address of your current or most recent employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    number: str = Field(
        ...,
        description=(
            "Street number of the employer’s address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    street: str = Field(
        ...,
        description=(
            'Street name of the employer’s address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the employer’s address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of the employer’s address")

    zip_code: str = Field(..., description="ZIP code of the employer’s address")

    phone: str = Field(
        ...,
        description=(
            'Employer’s main phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    name_of_immediate_supervisor: str = Field(
        ...,
        description=(
            "Full name of your immediate supervisor at this employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    dates_of_employment_from_month_year: str = Field(
        ...,
        description=(
            "Start date of employment in month/year format .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dates_of_employment_to_month_year: str = Field(
        ...,
        description=(
            'End date of employment in month/year format (or "Present") .If you cannot '
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    position_title: str = Field(
        ...,
        description=(
            "Your job title or position with this employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    may_we_contact_yes: BooleanLike = Field(
        default="", description="Indicate if the employer may be contacted (Yes option)"
    )

    may_we_contact_no: BooleanLike = Field(
        default="", description="Indicate if the employer may be contacted (No option)"
    )

    description_of_duties_responsibilities_courses_and_accomplishments_employer_1_line_1: str = (
        Field(
            default="",
            description=(
                "First line describing your duties, responsibilities, training, and "
                'accomplishments for employer 1 .If you cannot fill this, write "N/A". If '
                "this field should not be filled by you (for example, it belongs to another "
                'person or office), leave it blank (empty string "").'
            ),
        )
    )

    description_of_duties_responsibilities_courses_and_accomplishments_employer_1_line_2: str = (
        Field(
            default="",
            description=(
                "Second line describing your duties, responsibilities, training, and "
                'accomplishments for employer 1 .If you cannot fill this, write "N/A". If '
                "this field should not be filled by you (for example, it belongs to another "
                'person or office), leave it blank (empty string "").'
            ),
        )
    )

    description_of_duties_responsibilities_courses_and_accomplishments_employer_1_line_3: str = (
        Field(
            default="",
            description=(
                "Third line describing your duties, responsibilities, training, and "
                'accomplishments for employer 1 .If you cannot fill this, write "N/A". If '
                "this field should not be filled by you (for example, it belongs to another "
                'person or office), leave it blank (empty string "").'
            ),
        )
    )

    current_employers_name_2: str = Field(
        default="",
        description=(
            "Name of a second employer within the last 10 years .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    employers_address_2: str = Field(
        default="",
        description=(
            "Street address of the second listed employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    number_2: str = Field(
        default="",
        description=(
            "Street number of the second employer’s address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    street_2: str = Field(
        default="",
        description=(
            "Street name of the second employer’s address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_2: str = Field(
        default="",
        description=(
            'City of the second employer’s address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state_2: str = Field(default="", description="State of the second employer’s address")

    zip_code_2: str = Field(default="", description="ZIP code of the second employer’s address")

    phone_2: str = Field(
        default="",
        description=(
            'Second employer’s main phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_of_immediate_supervisor_2: str = Field(
        default="",
        description=(
            "Full name of your immediate supervisor at the second employer .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    dates_of_employment_from_month_year_2: str = Field(
        default="",
        description=(
            "Start date of employment with the second employer in month/year format .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    dates_of_employment_to_month_year_2: str = Field(
        default="",
        description=(
            "End date of employment with the second employer in month/year format .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    position_title_2: str = Field(
        default="",
        description=(
            "Your job title or position with the second employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    description_of_duties_responsibilities_courses_and_accomplishments_employer_2_line_1: str = (
        Field(
            default="",
            description=(
                "First line describing your duties, responsibilities, training, and "
                'accomplishments for employer 2 .If you cannot fill this, write "N/A". If '
                "this field should not be filled by you (for example, it belongs to another "
                'person or office), leave it blank (empty string "").'
            ),
        )
    )

    description_of_duties_responsibilities_courses_and_accomplishments_employer_2_line_2: str = (
        Field(
            default="",
            description=(
                "Second line describing your duties, responsibilities, training, and "
                'accomplishments for employer 2 .If you cannot fill this, write "N/A". If '
                "this field should not be filled by you (for example, it belongs to another "
                'person or office), leave it blank (empty string "").'
            ),
        )
    )

    description_of_duties_responsibilities_courses_and_accomplishments_employer_2_line_3: str = (
        Field(
            default="",
            description=(
                "Third line describing your duties, responsibilities, training, and "
                'accomplishments for employer 2 .If you cannot fill this, write "N/A". If '
                "this field should not be filled by you (for example, it belongs to another "
                'person or office), leave it blank (empty string "").'
            ),
        )
    )

    current_employers_name_3: str = Field(
        default="",
        description=(
            "Name of a third employer within the last 10 years .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    employers_address_3: str = Field(
        default="",
        description=(
            "Street address of the third listed employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    number_3: str = Field(
        default="",
        description=(
            "Street number of the third employer’s address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    street_3: str = Field(
        default="",
        description=(
            "Street name of the third employer’s address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_3: str = Field(
        default="",
        description=(
            'City of the third employer’s address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state_3: str = Field(default="", description="State of the third employer’s address")

    zip_code_3: str = Field(default="", description="ZIP code of the third employer’s address")

    phone_3: str = Field(
        default="",
        description=(
            'Third employer’s main phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_of_immediate_supervisor_3: str = Field(
        default="",
        description=(
            "Full name of your immediate supervisor at the third employer .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    dates_of_employment_from_month_year_3: str = Field(
        default="",
        description=(
            "Start date of employment with the third employer in month/year format .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    dates_of_employment_to_month_year_3: str = Field(
        default="",
        description=(
            "End date of employment with the third employer in month/year format .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    position_title_3: str = Field(
        default="",
        description=(
            "Your job title or position with the third employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    description_of_duties_responsibilities_courses_and_accomplishments_employer_3_line_1: str = (
        Field(
            default="",
            description=(
                "First line describing your duties, responsibilities, training, and "
                'accomplishments for employer 3 .If you cannot fill this, write "N/A". If '
                "this field should not be filled by you (for example, it belongs to another "
                'person or office), leave it blank (empty string "").'
            ),
        )
    )

    description_of_duties_responsibilities_courses_and_accomplishments_employer_3_line_2: str = (
        Field(
            default="",
            description=(
                "Second line describing your duties, responsibilities, training, and "
                'accomplishments for employer 3 .If you cannot fill this, write "N/A". If '
                "this field should not be filled by you (for example, it belongs to another "
                'person or office), leave it blank (empty string "").'
            ),
        )
    )

    description_of_duties_responsibilities_courses_and_accomplishments_employer_3_line_3: str = (
        Field(
            default="",
            description=(
                "Third line describing your duties, responsibilities, training, and "
                'accomplishments for employer 3 .If you cannot fill this, write "N/A". If '
                "this field should not be filled by you (for example, it belongs to another "
                'person or office), leave it blank (empty string "").'
            ),
        )
    )


class SpecialTrainingExperienceSkillsorAbilities(BaseModel):
    """Additional qualifications of value to the Kalamazoo County Sheriff’s Office"""

    special_training_experience_skills_or_abilities_line_1: str = Field(
        default="",
        description=(
            "First line to describe any special training, experience, skills, or abilities "
            'of value to the Sheriff’s Office .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    special_training_experience_skills_or_abilities_line_2: str = Field(
        default="",
        description=(
            "Second line to describe any special training, experience, skills, or abilities "
            'of value to the Sheriff’s Office .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    special_training_experience_skills_or_abilities_line_3: str = Field(
        default="",
        description=(
            "Third line to describe any special training, experience, skills, or abilities "
            'of value to the Sheriff’s Office .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class EmploymentHistory(BaseModel):
    """
    Employment History

    Please provide your employment history in the last 10 years, starting with your present employer. Account for all periods including casual employment. You may make additional copies of this page if necessary.
    *If you are selected to move to the next step of the process, a KCSO investigator may interview employers, supervisors and co workers.
    """

    employment_history: EmploymentHistory = Field(..., description="Employment History")
    special_training_experience_skills_or_abilities: SpecialTrainingExperienceSkillsorAbilities = (
        Field(..., description="Special Training, Experience, Skills or Abilities")
    )
