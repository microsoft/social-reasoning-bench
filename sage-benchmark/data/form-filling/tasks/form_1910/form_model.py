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
    """Basic personal and contact details, and background information"""

    surname: str = Field(
        ...,
        description=(
            'Applicant\'s last name (family name) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Applicant\'s first (given) name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    second_name: str = Field(
        default="",
        description=(
            "Applicant's middle or second given name, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    preferred_name: str = Field(
        default="",
        description=(
            "Name the applicant prefers to be called .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Full mailing address including street, city, and province .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    postal_code: str = Field(..., description="Postal code for the mailing address")

    primary_phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    alternate_phone: str = Field(
        default="",
        description=(
            'Secondary contact phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    criminal_convictions_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate YES if the applicant has criminal convictions for which a pardon has "
            "not been granted"
        ),
    )

    criminal_convictions_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate NO if the applicant does not have criminal convictions for which a "
            "pardon has not been granted"
        ),
    )

    required_for_school: BooleanLike = Field(
        default="", description="Check if volunteering is required for a school program"
    )

    number_of_hours_required: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of volunteer hours required for school, if applicable"
    )

    personal_growth_and_satisfaction: BooleanLike = Field(
        default="",
        description="Check if the reason for volunteering is personal growth and satisfaction",
    )

    other_reason_for_wanting_to_volunteer_at_carewest: BooleanLike = Field(
        default="",
        description=(
            "Check if the reason for volunteering is something other than school or personal growth"
        ),
    )

    why_do_you_want_to_volunteer_at_carewest_additional_information: str = Field(
        default="",
        description=(
            "Additional details about why the applicant wants to volunteer at Carewest .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    please_tell_us_what_are_some_of_your_hobbies_and_interests: str = Field(
        default="",
        description=(
            "Description of the applicant's hobbies and interests .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class VolunteeringPreferences(BaseModel):
    """Preferred volunteer areas, schedule, and time commitment"""

    community_outing: BooleanLike = Field(
        default="", description="Check if applying to volunteer in Community Outing area"
    )

    leisure_activities: BooleanLike = Field(
        default="", description="Check if applying to volunteer in Leisure Activities area"
    )

    one_to_one_visiting: BooleanLike = Field(
        default="", description="Check if applying to volunteer in One to One Visiting area"
    )

    pastoral_care: BooleanLike = Field(
        default="", description="Check if applying to volunteer in Pastoral Care area"
    )

    non_resident_activities: BooleanLike = Field(
        default="", description="Check if applying to volunteer in Non Resident Activities area"
    )

    rehab_and_recovery: BooleanLike = Field(
        default="", description="Check if applying to volunteer in Rehab and Recovery area"
    )

    gift_stores: BooleanLike = Field(
        default="", description="Check if applying to volunteer in Gift Stores area"
    )

    community_programs: BooleanLike = Field(
        default="", description="Check if applying to volunteer in Community Programs area"
    )

    palliative_care: BooleanLike = Field(
        default="", description="Check if applying to volunteer in Palliative Care area"
    )

    no_preference_unknown: BooleanLike = Field(
        default="", description="Check if the applicant has no preference or is unsure of area"
    )

    other_area_applying_for: str = Field(
        default="",
        description=(
            "Specify another volunteer area not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    frequency_one_time: BooleanLike = Field(
        default="", description="Check if the volunteer commitment is for a one-time activity"
    )

    frequency_weekly: BooleanLike = Field(
        default="", description="Check if the volunteer commitment is weekly"
    )

    frequency_monthly: BooleanLike = Field(
        default="", description="Check if the volunteer commitment is monthly"
    )

    frequency_would_like_to_discuss_in_person: BooleanLike = Field(
        default="", description="Check if the applicant would like to discuss frequency in person"
    )

    day_of_week_preference_sunday: BooleanLike = Field(
        default="", description="Indicate availability on Sundays"
    )

    day_of_week_preference_monday: BooleanLike = Field(
        default="", description="Indicate availability on Mondays"
    )

    day_of_week_preference_tuesday: BooleanLike = Field(
        default="", description="Indicate availability on Tuesdays"
    )

    day_of_week_preference_wednesday: BooleanLike = Field(
        default="", description="Indicate availability on Wednesdays"
    )

    day_of_week_preference_thursday: BooleanLike = Field(
        default="", description="Indicate availability on Thursdays"
    )

    day_of_week_preference_friday: BooleanLike = Field(
        default="", description="Indicate availability on Fridays"
    )

    day_of_week_preference_saturday: BooleanLike = Field(
        default="", description="Indicate availability on Saturdays"
    )

    shift_preference_morning: BooleanLike = Field(
        default="", description="Indicate preference for morning shifts"
    )

    shift_preference_afternoon: BooleanLike = Field(
        default="", description="Indicate preference for afternoon shifts"
    )

    shift_preference_evening: BooleanLike = Field(
        default="", description="Indicate preference for evening shifts"
    )

    shift_preference_weekend: BooleanLike = Field(
        default="", description="Indicate preference for weekend shifts"
    )

    available_volunteer_time_commitment_per_shift_hours_week: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Approximate number of hours per week the applicant can volunteer per shift",
        )
    )


class VolunteerApplication(BaseModel):
    """
    Volunteer Application

    Thank you for your interest in volunteering with Carewest.
    We encourage all applicants to visit our website www.carewest.ca to learn more about our company and current volunteer openings. A fillable PDF version of this form can also be found on our website.
    Note: The minimum age to volunteer is 16 years.
    Please submit your completed application form using one of the following methods:
    Mail or Deliver to: Carewest Administration, 10101 Southport Road SW, Calgary, AB, T2W 3N2
    Email: carewest.hr@ahs.ca
    If you have any questions regarding your volunteer application and/or Carewest’s volunteer opportunities please contact Recruitment at 403-943-8170 or 403-943-8171.
    """

    personal_information: PersonalInformation = Field(..., description="Personal Information")
    volunteering_preferences: VolunteeringPreferences = Field(
        ..., description="Volunteering Preferences"
    )
