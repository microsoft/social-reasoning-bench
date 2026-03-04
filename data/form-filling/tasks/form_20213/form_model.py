from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PersonalInformation(BaseModel):
    """Basic personal and contact information for the deacon"""

    name: str = Field(
        ...,
        description=(
            'Full name of the deacon .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    congregation_serving: str = Field(
        ...,
        description=(
            "Name of the congregation where you are currently serving as deacon .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    are_you_a_member_of_the_above_congregation_yes: BooleanLike = Field(
        ..., description="Indicate YES if you are a member of the congregation you are serving"
    )

    are_you_a_member_of_the_above_congregation_no: BooleanLike = Field(
        ..., description="Indicate NO if you are not a member of the congregation you are serving"
    )

    if_no_indicate_current_congregational_membership: str = Field(
        default="",
        description=(
            "Name of the congregation where you currently hold membership, if different .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    home_address: str = Field(
        ...,
        description=(
            'Street address of your home residence .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_home: str = Field(
        ...,
        description=(
            'Home city .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    state_home: str = Field(..., description="Home state abbreviation")

    zip_code_home: str = Field(..., description="Home ZIP code")

    cell_phone: str = Field(
        ...,
        description=(
            'Primary mobile phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    home_phone: str = Field(
        default="",
        description=(
            "Home landline phone number, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_home: str = Field(
        ...,
        description=(
            'Personal or home email address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    office_address: str = Field(
        default="",
        description=(
            "Street address of your office or workplace .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_office: str = Field(
        default="",
        description=(
            'Work or office email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city_office: str = Field(
        default="",
        description=(
            'Office city .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    state_office: str = Field(default="", description="Office state abbreviation")

    zip_code_office: str = Field(default="", description="Office ZIP code")

    office_phone: str = Field(
        default="",
        description=(
            'Office or work phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Your date of birth")  # YYYY-MM-DD format

    place_of_birth: str = Field(
        ...,
        description=(
            "City and state or country where you were born .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    marital_status: str = Field(
        default="",
        description=(
            "Current marital status (e.g., single, married, widowed) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_marriage: str = Field(
        default="", description="Date of your marriage, if applicable"
    )  # YYYY-MM-DD format

    name_of_wife: str = Field(
        default="",
        description=(
            'Full name of your wife, if married .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    wifes_birth_date: str = Field(
        default="", description="Birth date of your wife, if applicable"
    )  # YYYY-MM-DD format


class Education(BaseModel):
    """College education history"""

    college_1: str = Field(
        default="",
        description=(
            'Name of first college attended .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    degree_year_graduated_college_1: str = Field(
        default="",
        description=(
            "Degree earned and year of graduation for first college .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_2: str = Field(
        default="",
        description=(
            'Name of second college attended .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    degree_year_graduated_college_2: str = Field(
        default="",
        description=(
            "Degree earned and year of graduation for second college .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class WorkExperience(BaseModel):
    """Current occupational information"""

    current_occupation: str = Field(
        default="",
        description=(
            'Your present occupation or job title .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class CongregationalExperience(BaseModel):
    """Service history and responsibilities in congregations"""

    congregation_served_1: str = Field(
        default="",
        description=(
            "Name of first congregation where you have served .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    location_dates_1: str = Field(
        default="",
        description=(
            "Location and dates of service for first congregation listed .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    congregation_served_2: str = Field(
        default="",
        description=(
            "Name of second congregation where you have served .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    location_dates_2: str = Field(
        default="",
        description=(
            "Location and dates of service for second congregation listed .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    congregation_served_3: str = Field(
        default="",
        description=(
            "Name of third congregation where you have served .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    location_dates_3: str = Field(
        default="",
        description=(
            "Location and dates of service for third congregation listed .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    other_congregational_responsibilities_held: str = Field(
        default="",
        description=(
            "List other congregational responsibilities you have held and the congregations "
            'where they were held .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class MichiganDistrictDeaconInformationForm(BaseModel):
    """
    Michigan District Deacon Information Form

    ''
    """

    personal_information: PersonalInformation = Field(..., description="Personal Information")
    education: Education = Field(..., description="Education")
    work_experience: WorkExperience = Field(..., description="Work Experience")
    congregational_experience: CongregationalExperience = Field(
        ..., description="Congregational Experience"
    )
