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
    """Basic personal and physical details"""

    first_name: str = Field(
        ...,
        description=(
            'Client\'s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Client\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Primary email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    how_often_do_you_check_email: str = Field(
        default="",
        description=(
            "Frequency with which you check your email .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_home: str = Field(
        default="",
        description=(
            'Home phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    work: str = Field(
        default="",
        description=(
            'Work phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    mobile: str = Field(
        default="",
        description=(
            'Mobile/cell phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    age: Union[float, Literal["N/A", ""]] = Field(default="", description="Current age in years")

    height: str = Field(
        default="",
        description=(
            "Current height (include units, e.g., ft/in or cm) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    birthdate: str = Field(default="", description="Date of birth")  # YYYY-MM-DD format

    place_of_birth: str = Field(
        default="",
        description=(
            'City, state, and/or country of birth .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    current_weight: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current body weight (include units if applicable)"
    )

    weight_six_months_ago: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Body weight approximately six months ago"
    )

    one_year_ago: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Body weight approximately one year ago"
    )

    would_you_like_your_weight_to_be_different_if_so_what: str = Field(
        default="",
        description=(
            "Describe whether and how you would like your weight to change .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class SocialInformation(BaseModel):
    """Living situation, relationships, and work"""

    relationship_status: str = Field(
        default="",
        description=(
            "Current relationship status (e.g., single, married, partnered) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    where_do_you_currently_live: str = Field(
        default="",
        description=(
            "Current city and state or general location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    children: str = Field(
        default="",
        description=(
            'Number and/or ages of children .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    pets: str = Field(
        default="",
        description=(
            'Types and/or number of pets .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    occupation: str = Field(
        default="",
        description=(
            'Current job or primary occupation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    hours_of_work_per_week: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Approximate number of hours worked per week"
    )


class HealthInformation(BaseModel):
    """Health history, concerns, and family health"""

    please_list_your_main_health_concerns: str = Field(
        default="",
        description=(
            "Describe your primary health concerns or issues .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_concerns_and_or_goals: str = Field(
        default="",
        description=(
            "Any additional health concerns or personal goals .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    at_what_point_in_your_life_did_you_feel_best: str = Field(
        default="",
        description=(
            "Describe the time in your life when you felt your best and why .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    any_serious_illnesses_hospitalizations_injuries: str = Field(
        default="",
        description=(
            "List any serious illnesses, hospitalizations, or injuries with dates if "
            'possible .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    how_is_was_the_health_of_your_mother: str = Field(
        default="",
        description=(
            "Describe your mother's current or past health .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    how_is_was_the_health_of_your_father: str = Field(
        default="",
        description=(
            "Describe your father's current or past health .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class IcraveCoachingMensHealthHistory(BaseModel):
    """
        iCrave COACHING

    Men’s Health History

        Please write or print clearly. All of your information will remain confidential between you and the Health Coach.
    """

    personal_information: PersonalInformation = Field(..., description="Personal Information")
    social_information: SocialInformation = Field(..., description="Social Information")
    health_information: HealthInformation = Field(..., description="Health Information")
