from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PreviousTrainingProgramsTableRow(BaseModel):
    """Single row in Program Clinical/Research"""

    program_clinical_research: str = Field(default="", description="Program_Clinical_Research")
    institution_and_country: str = Field(default="", description="Institution_And_Country")
    dates: str = Field(default="", description="Dates")
    purpose: str = Field(default="", description="Purpose")


class EmergencyContactInformation(BaseModel):
    """Emergency contacts, at least one in home country"""

    emergency_contact_1_name: str = Field(
        ...,
        description=(
            "Full name of your first emergency contact person .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_1_relationship: str = Field(
        ...,
        description=(
            "Your relationship to the first emergency contact (e.g., parent, spouse, "
            'friend) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    emergency_contact_1_email: str = Field(
        ...,
        description=(
            "Email address of your first emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_1_phone_with_country_code: str = Field(
        ...,
        description=(
            "Phone number of your first emergency contact, including country code .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    emergency_contact_2_name: str = Field(
        default="",
        description=(
            "Full name of your second emergency contact person .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_2_relationship: str = Field(
        default="",
        description=(
            "Your relationship to the second emergency contact (e.g., parent, spouse, "
            'friend) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    emergency_contact_2_email: str = Field(
        default="",
        description=(
            "Email address of your second emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_2_phone_with_country_code: str = Field(
        default="",
        description=(
            "Phone number of your second emergency contact, including country code .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PreviousInternationalEducationorExperience(BaseModel):
    """Prior and current international training or educational programs"""

    received_training_one_month_or_longer_yes: BooleanLike = Field(
        ...,
        description=(
            "Check if you have received training in the USA or another country for one "
            "month or longer"
        ),
    )

    received_training_one_month_or_longer_no: BooleanLike = Field(
        ...,
        description=(
            "Check if you have not received training in the USA or another country for one "
            "month or longer"
        ),
    )

    previous_training_programs_table: List[PreviousTrainingProgramsTableRow] = Field(
        default="",
        description=(
            "List each prior clinical or research training program, including institution, "
            "country, dates, and purpose"
        ),
    )  # List of table rows

    previous_training_institution_and_country: str = Field(
        default="",
        description=(
            "Name of the institution and the country where the previous program took place "
            '(captured per row in the table) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    previous_training_dates: str = Field(
        default="",
        description=(
            "Start and end dates for each previous program (captured per row in the table) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    previous_training_purpose: str = Field(
        default="",
        description=(
            "Purpose or focus of each previous program (captured per row in the table) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    currently_in_program_yes: BooleanLike = Field(
        ...,
        description=(
            "Check if you are currently participating in an educational program outside "
            "your home country"
        ),
    )

    currently_in_program_no: BooleanLike = Field(
        ...,
        description=(
            "Check if you are not currently participating in an educational program outside "
            "your home country"
        ),
    )

    current_program_institution: str = Field(
        default="",
        description=(
            "Name of the institution where you are currently enrolled, if applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    current_program_clinical: BooleanLike = Field(
        default="", description="Check if your current program is primarily clinical"
    )

    current_program_research: BooleanLike = Field(
        default="", description="Check if your current program is primarily research"
    )

    current_program_other: BooleanLike = Field(
        default="", description="Check if your current program is of another type not listed"
    )

    current_program_name: str = Field(
        default="",
        description=(
            "Official name of your current educational program .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    current_program_dates_from: str = Field(
        default="",
        description=(
            "Start date of your current educational program .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    current_program_dates_to: str = Field(
        default="",
        description=(
            "End date of your current educational program .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class GoalsStatement(BaseModel):
    """Specific goals for participation in the International Scholars Program"""

    goal_1: str = Field(
        ...,
        description=(
            "First specific goal you wish to accomplish during the program .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    goal_2: str = Field(
        ...,
        description=(
            "Second specific goal you wish to accomplish during the program .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    goal_3: str = Field(
        ...,
        description=(
            "Third specific goal you wish to accomplish during the program .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    goal_4: str = Field(
        default="",
        description=(
            "Optional additional goal you wish to accomplish during the program .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    goal_5: str = Field(
        default="",
        description=(
            "Optional additional goal you wish to accomplish during the program .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    goal_6: str = Field(
        default="",
        description=(
            "Optional additional goal you wish to accomplish during the program .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class EmergencyContactInformation(BaseModel):
    """
    Emergency Contact Information

    Emergency Contact Information
    (*at least one person listed must be in home country*)
    """

    emergency_contact_information: EmergencyContactInformation = Field(
        ..., description="Emergency Contact Information"
    )
    previous_international_education_or_experience: PreviousInternationalEducationorExperience = (
        Field(..., description="Previous International Education or Experience")
    )
    goals_statement: GoalsStatement = Field(..., description="Goals Statement")
