from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PersonalInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Basic personal and contact information for the volunteer"""

    first_name: str = Field(
        ...,
        description=(
            "Applicant's first name .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    last_name: str = Field(
        ...,
        description=(
            "Applicant's last name .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    middle_name: str = Field(
        ...,
        description=(
            "Applicant's middle name .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    date_of_birth: str = Field(
        ...,
        description="Applicant's date of birth"
    )  # YYYY-MM-DD format

    street_address: str = Field(
        ...,
        description=(
            "Applicant's street address .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    telephone_number: str = Field(
        ...,
        description=(
            "Applicant's primary phone number .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    city_state_and_zip_code: str = Field(
        ...,
        description=(
            "Applicant's city, state, and zip code .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    email_address: str = Field(
        ...,
        description=(
            "Applicant's email address .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    emergency_contact_name_and_relationship: str = Field(
        ...,
        description=(
            "Name and relationship of emergency contact .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    emergency_telephone_number: str = Field(
        ...,
        description=(
            "Phone number of emergency contact .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class VolunteerStatusandAvailability(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about previous volunteering, family connections, availability, and commitment"""

    have_you_previously_volunteered_with_the_waters_yes: BooleanLike = Field(
        ...,
        description="Check if you have previously volunteered with The Waters"
    )

    have_you_previously_volunteered_with_the_waters_yes_dates: str = Field(
        ...,
        description=(
            "Dates when you previously volunteered .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    have_you_previously_volunteered_with_the_waters_yes_location: str = Field(
        ...,
        description=(
            "Location where you previously volunteered .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    have_you_previously_volunteered_with_the_waters_no: BooleanLike = Field(
        ...,
        description="Check if you have not previously volunteered with The Waters"
    )

    date_available_to_start_volunteering: str = Field(
        ...,
        description="Date you are available to start volunteering"
    )  # YYYY-MM-DD format

    do_you_have_a_family_member_who_lives_at_the_waters_or_a_family_member_who_works_at_the_waters_yes: BooleanLike = Field(
        ...,
        description="Check if you have a family member who lives or works at The Waters"
    )

    do_you_have_a_family_member_who_lives_at_the_waters_or_a_family_member_who_works_at_the_waters_yes_location: str = Field(
        ...,
        description=(
            "Location of family member at The Waters .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    do_you_have_a_family_member_who_lives_at_the_waters_or_a_family_member_who_works_at_the_waters_no: BooleanLike = Field(
        ...,
        description="Check if you do not have a family member who lives or works at The Waters"
    )

    if_yes_who: str = Field(
        ...,
        description=(
            "Name of the family member if applicable .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    availability_monday: BooleanLike = Field(
        ...,
        description="Available to volunteer on Monday"
    )

    availability_tuesday: BooleanLike = Field(
        ...,
        description="Available to volunteer on Tuesday"
    )

    availability_wednesday: BooleanLike = Field(
        ...,
        description="Available to volunteer on Wednesday"
    )

    availability_thursday: BooleanLike = Field(
        ...,
        description="Available to volunteer on Thursday"
    )

    availability_friday: BooleanLike = Field(
        ...,
        description="Available to volunteer on Friday"
    )

    availability_saturday: BooleanLike = Field(
        ...,
        description="Available to volunteer on Saturday"
    )

    availability_sunday: BooleanLike = Field(
        ...,
        description="Available to volunteer on Sunday"
    )

    availability_mornings: BooleanLike = Field(
        ...,
        description="Available to volunteer in the mornings"
    )

    availability_afternoons: BooleanLike = Field(
        ...,
        description="Available to volunteer in the afternoons"
    )

    availability_evenings: BooleanLike = Field(
        ...,
        description="Available to volunteer in the evenings"
    )

    availability_other: str = Field(
        ...,
        description=(
            "Other availability (please specify) .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    commitment_level_hours_per: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of hours you can commit per period"
    )

    commitment_level_per_day: BooleanLike = Field(
        ...,
        description="Commitment is per day"
    )

    commitment_level_per_week: BooleanLike = Field(
        ...,
        description="Commitment is per week"
    )

    commitment_level_per_month: BooleanLike = Field(
        ...,
        description="Commitment is per month"
    )

    commitment_level_per_other: str = Field(
        ...,
        description=(
            "Other commitment period (please specify) .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    length_of_commitment: str = Field(
        ...,
        description=(
            "Length of time you can commit .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    length_of_commitment_months: BooleanLike = Field(
        ...,
        description="Commitment is for a specified number of months"
    )

    length_of_commitment_indefinitely: BooleanLike = Field(
        ...,
        description="Commitment is indefinite"
    )

    length_of_commitment_other: str = Field(
        ...,
        description=(
            "Other length of commitment (please specify) .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    why_are_you_interested_in_volunteering_at_the_waters: str = Field(
        ...,
        description=(
            "Describe your motivation for volunteering at The Waters .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )


class InterestSkillsandExperience(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Volunteer’s areas of interest, skills, and previous experience"""

    areas_of_interest_skills_and_previous_experience: str = Field(
        ...,
        description=(
            "List your areas of interest, skills, and any previous experience volunteering "
            "with seniors .If you cannot fill this, write \"N/A\". If this field should not "
            "be filled by you (for example, it belongs to another person or office), leave "
            "it blank (empty string \"\")."
        )
    )


class TheWatersVolunteerApplication(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    THE WATERS  
VOLUNTEER APPLICATION

    Volunteer application form for individuals interested in volunteering at The Waters. Collects personal information, emergency contact details, availability, commitment level, reasons for volunteering, and relevant interests, skills, and experience, particularly with seniors.
    """

    personal_information: PersonalInformation = Field(
        ...,
        description="Personal Information"
    )
    volunteer_status_and_availability: VolunteerStatusandAvailability = Field(
        ...,
        description="Volunteer Status and Availability"
    )
    interest_skills_and_experience: InterestSkillsandExperience = Field(
        ...,
        description="Interest, Skills, and Experience"
    )