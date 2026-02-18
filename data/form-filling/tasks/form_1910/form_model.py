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
    """Basic personal and contact details, and criminal record declaration"""

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
            "Applicant's middle or second name, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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
            'Applicant\'s full mailing address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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


class MotivationandBackground(BaseModel):
    """Reasons for volunteering and personal interests"""

    why_do_you_want_to_volunteer_at_carewest: str = Field(
        default="",
        description=(
            "Describe the reasons for wanting to volunteer at Carewest .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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

    other_reason_checkbox: BooleanLike = Field(
        default="", description="Check if the reason for volunteering is other than those listed"
    )

    hobbies_and_interests: str = Field(
        default="",
        description=(
            "List hobbies and interests that may be relevant to volunteering .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
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
        default="", description="Check if there is no specific area preference or it is unknown"
    )

    other_areas_applying_for: str = Field(
        default="",
        description=(
            "Specify another area of interest not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    frequency_one_time: BooleanLike = Field(
        default="", description="Check if available for a one-time volunteer commitment"
    )

    frequency_weekly: BooleanLike = Field(
        default="", description="Check if available to volunteer weekly"
    )

    frequency_monthly: BooleanLike = Field(
        default="", description="Check if available to volunteer monthly"
    )

    frequency_discuss_in_person: BooleanLike = Field(
        default="", description="Check if the applicant would like to discuss frequency in person"
    )

    day_pref_sunday: BooleanLike = Field(
        default="", description="Check if Sunday is a preferred day to volunteer"
    )

    day_pref_monday: BooleanLike = Field(
        default="", description="Check if Monday is a preferred day to volunteer"
    )

    day_pref_tuesday: BooleanLike = Field(
        default="", description="Check if Tuesday is a preferred day to volunteer"
    )

    day_pref_wednesday: BooleanLike = Field(
        default="", description="Check if Wednesday is a preferred day to volunteer"
    )

    day_pref_thursday: BooleanLike = Field(
        default="", description="Check if Thursday is a preferred day to volunteer"
    )

    day_pref_friday: BooleanLike = Field(
        default="", description="Check if Friday is a preferred day to volunteer"
    )

    day_pref_saturday: BooleanLike = Field(
        default="", description="Check if Saturday is a preferred day to volunteer"
    )

    shift_pref_morning: BooleanLike = Field(
        default="", description="Check if morning is a preferred shift time"
    )

    shift_pref_afternoon: BooleanLike = Field(
        default="", description="Check if afternoon is a preferred shift time"
    )

    shift_pref_evening: BooleanLike = Field(
        default="", description="Check if evening is a preferred shift time"
    )

    shift_pref_weekend: BooleanLike = Field(
        default="", description="Check if weekend is a preferred shift time"
    )

    available_time_commitment_per_shift: str = Field(
        default="",
        description=(
            "Indicate the typical time commitment per shift, such as hours per week .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class VolunteerApplication(BaseModel):
    """
    Volunteer Application

    Thank you for your interest in volunteering with Carewest.
    We encourage all applicants to visit our website www.carewest.ca to learn more about our company and current volunteer openings. A fillable PDF version of this form can also be found on our website.
    Note: The minimum age to volunteer is 16 years.
    Please submit your completed application form using one of the following methods:
    Mail or Deliver to: Carewest Administration Email: carewest.hr@ahs.ca
    10101 Southport Road SW, Calgary, AB, T2W 3N2
    If you have any questions regarding your volunteer application and/or Carewest's volunteer opportunities please contact Recruitment at 403-943-8170 or 403-943-8171.
    """

    personal_information: PersonalInformation = Field(..., description="Personal Information")
    motivation_and_background: MotivationandBackground = Field(
        ..., description="Motivation and Background"
    )
    volunteering_preferences: VolunteeringPreferences = Field(
        ..., description="Volunteering Preferences"
    )
