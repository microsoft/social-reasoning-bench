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
            'Volunteer’s legal first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Volunteer’s legal last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    middle_name: str = Field(
        default="",
        description=(
            'Volunteer’s middle name or initial .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Volunteer’s date of birth")  # YYYY-MM-DD format

    street_address: str = Field(
        ...,
        description=(
            "Street address including apartment or unit number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_and_zip_code: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for the volunteer’s address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_number: str = Field(
        ...,
        description=(
            "Primary phone number for the volunteer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Volunteer’s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_name_and_relationship: str = Field(
        ...,
        description=(
            "Name of emergency contact and their relationship to the volunteer .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    emergency_telephone_number: str = Field(
        ...,
        description=(
            "Phone number for the emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class VolunteerHistoryandRelationships(BaseModel):
    """Previous volunteering with The Waters and family connections"""

    have_you_previously_volunteered_with_the_waters_yes: BooleanLike = Field(
        ..., description="Indicate Yes if the volunteer has previously volunteered with The Waters"
    )

    have_you_previously_volunteered_with_the_waters_no: BooleanLike = Field(
        ...,
        description="Indicate No if the volunteer has not previously volunteered with The Waters",
    )

    yes_dates: str = Field(
        default="",
        description=(
            "Date or dates when the volunteer previously volunteered at The Waters .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    location_previously_volunteered: str = Field(
        default="",
        description=(
            "Location or community where the volunteer previously volunteered at The Waters "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    date_available_to_start_volunteering: str = Field(
        ..., description="Date the volunteer is available to begin volunteering"
    )  # YYYY-MM-DD format

    family_member_at_the_waters_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate Yes if the volunteer has a family member who lives or works at The Waters"
        ),
    )

    family_member_at_the_waters_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate No if the volunteer does not have a family member who lives or works "
            "at The Waters"
        ),
    )

    location_family_member_at_the_waters: str = Field(
        default="",
        description=(
            "Location or community where the family member lives or works at The Waters .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    if_yes_who: str = Field(
        default="",
        description=(
            "Name of the family member who lives or works at The Waters .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AvailabilityandCommitment(BaseModel):
    """Scheduling preferences and length of volunteer commitment"""

    availability_monday: BooleanLike = Field(
        default="", description="Check if available to volunteer on Mondays"
    )

    availability_tuesday: BooleanLike = Field(
        default="", description="Check if available to volunteer on Tuesdays"
    )

    availability_wednesday: BooleanLike = Field(
        default="", description="Check if available to volunteer on Wednesdays"
    )

    availability_thursday: BooleanLike = Field(
        default="", description="Check if available to volunteer on Thursdays"
    )

    availability_friday: BooleanLike = Field(
        default="", description="Check if available to volunteer on Fridays"
    )

    availability_saturday: BooleanLike = Field(
        default="", description="Check if available to volunteer on Saturdays"
    )

    availability_sunday: BooleanLike = Field(
        default="", description="Check if available to volunteer on Sundays"
    )

    availability_mornings: BooleanLike = Field(
        default="", description="Check if available to volunteer in the mornings"
    )

    availability_afternoons: BooleanLike = Field(
        default="", description="Check if available to volunteer in the afternoons"
    )

    availability_evenings: BooleanLike = Field(
        default="", description="Check if available to volunteer in the evenings"
    )

    availability_other: str = Field(
        default="",
        description=(
            "Describe any other availability not covered by the listed options .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    commitment_level_hours_per: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of hours the volunteer commits per selected time period"
    )

    commitment_level_per_day: BooleanLike = Field(
        default="", description="Check if the commitment is measured per day"
    )

    commitment_level_per_week: BooleanLike = Field(
        default="", description="Check if the commitment is measured per week"
    )

    commitment_level_per_month: BooleanLike = Field(
        default="", description="Check if the commitment is measured per month"
    )

    commitment_level_per_other: str = Field(
        default="",
        description=(
            "Describe another time period for the commitment level .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    length_of_commitment: str = Field(
        default="",
        description=(
            "Length of time the volunteer plans to commit (numeric or descriptive) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    length_of_commitment_months: BooleanLike = Field(
        default="", description="Check if the length of commitment is measured in months"
    )

    length_of_commitment_indefinitely: BooleanLike = Field(
        default="", description="Check if the volunteer intends to commit indefinitely"
    )

    length_of_commitment_other: str = Field(
        default="",
        description=(
            "Describe another type or length of commitment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class MotivationInterestsandExperience(BaseModel):
    """Reasons for volunteering and relevant skills/experience"""

    why_are_you_interested_in_volunteering_at_the_waters: str = Field(
        default="",
        description=(
            "Explain the reasons for wanting to volunteer at The Waters .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    areas_of_interest_with_residents_skills_and_previous_experience_volunteering_with_seniors: str = Field(
        default="",
        description=(
            "List areas of interest with residents, relevant skills, and any prior "
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
    volunteer_history_and_relationships: VolunteerHistoryandRelationships = Field(
        ..., description="Volunteer History and Relationships"
    )
    availability_and_commitment: AvailabilityandCommitment = Field(
        ..., description="Availability and Commitment"
    )
    motivation_interests_and_experience: MotivationInterestsandExperience = Field(
        ..., description="Motivation, Interests, and Experience"
    )
