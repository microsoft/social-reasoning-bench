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
            'Applicant\'s street address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    telephone_number: str = Field(
        ...,
        description=(
            "Primary telephone number for the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_and_zip_code: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for the applicant's address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_name_and_relationship: str = Field(
        ...,
        description=(
            "Name of emergency contact and their relationship to the applicant .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    emergency_telephone_number: str = Field(
        ...,
        description=(
            "Telephone number for the emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class VolunteerBackgroundAvailability(BaseModel):
    """Previous volunteering with The Waters, relationships, availability, and commitment"""

    have_you_previously_volunteered_with_the_waters: BooleanLike = Field(
        ..., description="Indicate whether you have previously volunteered with The Waters"
    )

    yes_dates: str = Field(
        default="",
        description=(
            "If yes, list the date or dates you previously volunteered .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    location_previously_volunteered: str = Field(
        default="",
        description=(
            "If yes, specify the location where you previously volunteered .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    no_previously_volunteered: BooleanLike = Field(
        default="", description="Check if you have not previously volunteered with The Waters"
    )

    date_available_to_start_volunteering: str = Field(
        ..., description="Date you are available to begin volunteering"
    )  # YYYY-MM-DD format

    do_you_have_a_family_member_at_or_working_at_the_waters: BooleanLike = Field(
        ...,
        description="Indicate whether you have a family member who lives or works at The Waters",
    )

    yes_family_member_at_working_at_the_waters: BooleanLike = Field(
        default="",
        description="Check if you do have a family member who lives or works at The Waters",
    )

    location_family_member_at_working_at_the_waters: str = Field(
        default="",
        description=(
            "Location of the family member who lives or works at The Waters .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    no_family_member_at_working_at_the_waters: BooleanLike = Field(
        default="",
        description="Check if you do not have a family member who lives or works at The Waters",
    )

    if_yes_who: str = Field(
        default="",
        description=(
            "If you have a family member at The Waters, specify who they are .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    monday_availability: BooleanLike = Field(
        default="", description="Check if you are available on Mondays"
    )

    tuesday_availability: BooleanLike = Field(
        default="", description="Check if you are available on Tuesdays"
    )

    wednesday_availability: BooleanLike = Field(
        default="", description="Check if you are available on Wednesdays"
    )

    thursday_availability: BooleanLike = Field(
        default="", description="Check if you are available on Thursdays"
    )

    friday_availability: BooleanLike = Field(
        default="", description="Check if you are available on Fridays"
    )

    saturday_availability: BooleanLike = Field(
        default="", description="Check if you are available on Saturdays"
    )

    sunday_availability: BooleanLike = Field(
        default="", description="Check if you are available on Sundays"
    )

    mornings_availability: BooleanLike = Field(
        default="", description="Check if you are available in the mornings"
    )

    afternoons_availability: BooleanLike = Field(
        default="", description="Check if you are available in the afternoons"
    )

    evenings_availability: BooleanLike = Field(
        default="", description="Check if you are available in the evenings"
    )

    other_availability: str = Field(
        default="",
        description=(
            "Describe any other availability not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    commitment_level_hours: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of hours you can commit per selected time period"
    )

    commitment_level_per_day: BooleanLike = Field(
        default="", description="Check if the commitment hours are per day"
    )

    commitment_level_per_week: BooleanLike = Field(
        default="", description="Check if the commitment hours are per week"
    )

    commitment_level_per_month: BooleanLike = Field(
        default="", description="Check if the commitment hours are per month"
    )

    commitment_level_per_other: str = Field(
        default="",
        description=(
            "If other, specify the time period for the commitment hours .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    length_of_commitment: str = Field(
        default="",
        description=(
            "Numeric or descriptive length of time you plan to volunteer .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    length_of_commitment_in_months: BooleanLike = Field(
        default="", description="Check if the length of commitment is measured in months"
    )

    length_of_commitment_indefinitely: BooleanLike = Field(
        default="", description="Check if you intend to volunteer indefinitely"
    )

    length_of_commitment_other: str = Field(
        default="",
        description=(
            "If other, describe the length of commitment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
    """
        THE WATERS
    VOLUNTEER APPLICATION

        ''
    """

    personal_information: PersonalInformation = Field(..., description="Personal Information")
    volunteer_background__availability: VolunteerBackgroundAvailability = Field(
        ..., description="Volunteer Background & Availability"
    )
    interest_skills_and_experience: InterestSkillsandExperience = Field(
        ..., description="Interest, Skills, and Experience"
    )
