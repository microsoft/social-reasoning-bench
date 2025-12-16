from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class SponsoringRotarian(BaseModel):
    """Information completed by the sponsoring Rotarian"""

    sponsoring_rotarian: str = Field(
        ...,
        description=(
            "Name of the Rotarian sponsoring this application .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this application is completed")  # YYYY-MM-DD format


class NewMemberInformation(BaseModel):
    """Personal and contact details for the new member applicant"""

    name: str = Field(
        ...,
        description=(
            'Applicant\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    birthday_mm_dd: str = Field(
        ..., description="Applicant's birthday in MM/DD format"
    )  # YYYY-MM-DD format

    local_address: str = Field(
        ...,
        description=(
            'Applicant\'s local mailing address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Primary phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    phone_home: BooleanLike = Field(
        default="", description="Check if the primary phone is a home number"
    )

    phone_work: BooleanLike = Field(
        default="", description="Check if the primary phone is a work number"
    )

    phone_mobile: BooleanLike = Field(
        default="", description="Check if the primary phone is a mobile number"
    )

    alt_phone: str = Field(
        default="",
        description=(
            'Alternate phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    alt_phone_home: BooleanLike = Field(
        default="", description="Check if the alternate phone is a home number"
    )

    alt_phone_work: BooleanLike = Field(
        default="", description="Check if the alternate phone is a work number"
    )

    alt_phone_mobile: BooleanLike = Field(
        default="", description="Check if the alternate phone is a mobile number"
    )

    email: str = Field(
        ...,
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    residency_full_time: BooleanLike = Field(
        default="", description="Check if the applicant is a full-time resident"
    )

    residency_part_time: BooleanLike = Field(
        default="", description="Check if the applicant is a part-time resident"
    )

    residency_seasonal: BooleanLike = Field(
        default="", description="Check if the applicant is a seasonal resident"
    )

    residency_since_mm_yy: str = Field(
        default="", description="Month and year residency began (MM/YY)"
    )  # YYYY-MM-DD format

    employment_retired: BooleanLike = Field(
        default="", description="Check if the applicant is retired"
    )

    employment_working: BooleanLike = Field(
        default="", description="Check if the applicant is currently working"
    )

    occupation: str = Field(
        default="",
        description=(
            "Applicant's primary occupation or field .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    current_employer: str = Field(
        default="",
        description=(
            'Name of current employer if working .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    no_of_years: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years with current employer"
    )

    job_title: str = Field(
        default="",
        description=(
            'Current job title or position .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    location_city_state: str = Field(
        default="",
        description=(
            'City and state of current employment .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    partner_spouse: str = Field(
        default="",
        description=(
            'Name of partner or spouse .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    anniversary_mm_dd: str = Field(
        default="", description="Wedding or partnership anniversary in MM/DD format"
    )  # YYYY-MM-DD format


class RotaryHistory(BaseModel):
    """Previous Rotary or club membership details"""

    former_rotarian_no: BooleanLike = Field(
        default="",
        description="Check if the applicant has not been a Rotarian or member of another club",
    )

    former_rotarian_yes: BooleanLike = Field(
        default="",
        description="Check if the applicant has been a Rotarian or member of another club",
    )

    former_rotarian_dates: str = Field(
        default="",
        description=(
            "Dates of prior Rotary or club membership .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    club_name: str = Field(
        default="",
        description=(
            "Name of the previous Rotary or other club .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    club_location_city_state: str = Field(
        default="",
        description=(
            'City and state of the previous club .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ExperienceandCommunityInvolvement(BaseModel):
    """Positions, honors, awards, and past community activities"""

    positions_held_honors_awards_line_1: str = Field(
        default="",
        description=(
            "Positions held, honors, or awards (first line) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    positions_held_honors_awards_line_2: str = Field(
        default="",
        description=(
            "Positions held, honors, or awards (second line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    past_community_activities_line_1: str = Field(
        default="",
        description=(
            "Past community activities such as church or volunteer work (first line) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    past_community_activities_line_2: str = Field(
        default="",
        description=(
            "Past community activities such as church or volunteer work (second line) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class TheRotaryClubOfCashiersValleyMembershipApplication(BaseModel):
    """
        The Rotary Club of Cashiers Valley

    Membership Application

        ''
    """

    sponsoring_rotarian: SponsoringRotarian = Field(..., description="Sponsoring Rotarian")
    new_member_information: NewMemberInformation = Field(..., description="New Member Information")
    rotary_history: RotaryHistory = Field(..., description="Rotary History")
    experience_and_community_involvement: ExperienceandCommunityInvolvement = Field(
        ..., description="Experience and Community Involvement"
    )
