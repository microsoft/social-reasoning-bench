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
    """Basic personal and contact details for the volunteer"""

    first_name: str = Field(
        ...,
        description=(
            'Applicant\'s legal first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Applicant\'s legal last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    middle_name: str = Field(
        default="",
        description=(
            'Applicant\'s middle name or initial .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Applicant's date of birth")  # YYYY-MM-DD format

    street_address: str = Field(
        ...,
        description=(
            "Street address including apartment or unit number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_number: str = Field(
        ...,
        description=(
            'Primary telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city_state_and_zip_code: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for the address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Primary email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_name_and_relationship: str = Field(
        ...,
        description=(
            "Name of emergency contact and their relationship to you .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_telephone_number: str = Field(
        ...,
        description=(
            "Telephone number for your emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class VolunteerBackgroundandAvailability(BaseModel):
    """Previous involvement with The Waters, family connections, availability, and commitment details"""

    have_you_previously_volunteered_with_the_waters: BooleanLike = Field(
        ..., description="Indicate whether you have volunteered with The Waters before"
    )

    yes_previous_volunteer: BooleanLike = Field(
        default="", description="Check if you have previously volunteered with The Waters"
    )

    dates_previous_volunteer: str = Field(
        default="",
        description=(
            'Dates when you previously volunteered .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    location_previous_volunteer: str = Field(
        default="",
        description=(
            "Location where you previously volunteered with The Waters .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_available_to_start_volunteering: str = Field(
        ..., description="Date you are available to begin volunteering"
    )  # YYYY-MM-DD format

    no_previous_volunteer: BooleanLike = Field(
        default="", description="Check if you have not previously volunteered with The Waters"
    )

    do_you_have_a_family_member_at_the_waters: BooleanLike = Field(
        ...,
        description="Indicate whether you have a family member who lives or works at The Waters",
    )

    yes_family_member_at_the_waters: BooleanLike = Field(
        default="",
        description="Check if you do have a family member who lives or works at The Waters",
    )

    location_family_member_at_the_waters: str = Field(
        default="",
        description=(
            "Location of the family member who lives or works at The Waters .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    if_yes_who: str = Field(
        default="",
        description=(
            "Name and relationship of the family member at The Waters .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    no_family_member_at_the_waters: BooleanLike = Field(
        default="",
        description="Check if you do not have a family member who lives or works at The Waters",
    )

    monday: BooleanLike = Field(default="", description="Available to volunteer on Mondays")

    tuesday: BooleanLike = Field(default="", description="Available to volunteer on Tuesdays")

    wednesday: BooleanLike = Field(default="", description="Available to volunteer on Wednesdays")

    thursday: BooleanLike = Field(default="", description="Available to volunteer on Thursdays")

    friday: BooleanLike = Field(default="", description="Available to volunteer on Fridays")

    saturday: BooleanLike = Field(default="", description="Available to volunteer on Saturdays")

    sunday: BooleanLike = Field(default="", description="Available to volunteer on Sundays")

    mornings: BooleanLike = Field(default="", description="Available to volunteer in the mornings")

    afternoons: BooleanLike = Field(
        default="", description="Available to volunteer in the afternoons"
    )

    evenings: BooleanLike = Field(default="", description="Available to volunteer in the evenings")

    other_availability: str = Field(
        default="",
        description=(
            "Other availability details not covered above .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    commitment_level_hours_per: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of hours you can commit per selected time period"
    )

    day_commitment_frequency: BooleanLike = Field(
        default="", description="Indicate if the commitment is per day"
    )

    week_commitment_frequency: BooleanLike = Field(
        default="", description="Indicate if the commitment is per week"
    )

    month_commitment_frequency: BooleanLike = Field(
        default="", description="Indicate if the commitment is per month"
    )

    other_commitment_frequency: str = Field(
        default="",
        description=(
            "Describe another commitment frequency if not day, week, or month .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    length_of_commitment: str = Field(
        default="",
        description=(
            'Length of time you plan to volunteer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    months_length_of_commitment: BooleanLike = Field(
        default="", description="Indicate if the length of commitment is measured in months"
    )

    indefinitely_length_of_commitment: BooleanLike = Field(
        default="", description="Indicate if you plan to volunteer indefinitely"
    )

    other_length_of_commitment: str = Field(
        default="",
        description=(
            'Describe another length of commitment .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    why_are_you_interested_in_volunteering_at_the_waters: str = Field(
        default="",
        description=(
            "Explain your reasons for wanting to volunteer at The Waters .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class InterestSkillsandExperience(BaseModel):
    """Volunteer’s interests, skills, and experience with seniors"""

    areas_of_interest_with_residents_skills_and_previous_experience_volunteering_with_seniors: str = Field(
        default="",
        description=(
            "List your areas of interest with residents, relevant skills, and any previous "
            'experience volunteering with seniors .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class TheWatersVolunteerApplication(BaseModel):
    """THE WATERS

    VOLUNTEER APPLICATION"""

    personal_information: PersonalInformation = Field(..., description="Personal Information")
    volunteer_background_and_availability: VolunteerBackgroundandAvailability = Field(
        ..., description="Volunteer Background and Availability"
    )
    interest_skills_and_experience: InterestSkillsandExperience = Field(
        ..., description="Interest, Skills, and Experience"
    )
