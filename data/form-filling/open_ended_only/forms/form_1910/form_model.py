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
    """Basic personal details and background information about the applicant."""

    surname: str = Field(
        ...,
        description=(
            "Applicant's last name .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    first_name: str = Field(
        ...,
        description=(
            "Applicant's first name .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    second_name: str = Field(
        ...,
        description=(
            "Applicant's middle name (if any) .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    preferred_name: str = Field(
        ...,
        description=(
            "Name you prefer to be called .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    address: str = Field(
        ...,
        description=(
            "Full mailing address .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    postal_code: str = Field(
        ...,
        description="Postal code"
    )

    primary_phone: str = Field(
        ...,
        description=(
            "Primary phone number .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    alternate_phone: str = Field(
        ...,
        description=(
            "Alternate phone number .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    e_mail: str = Field(
        ...,
        description=(
            "Email address .If you cannot fill this, write \"N/A\". If this field should "
            "not be filled by you (for example, it belongs to another person or office), "
            "leave it blank (empty string \"\")."
        )
    )

    do_you_have_any_criminal_convictions_for_which_a_pardon_has_not_been_granted: BooleanLike = Field(
        ...,
        description=(
            "Indicate if you have any criminal convictions for which a pardon has not been "
            "granted"
        )
    )

    yes_criminal_convictions: BooleanLike = Field(
        ...,
        description="Check if you have criminal convictions for which a pardon has not been granted"
    )

    no_criminal_convictions: BooleanLike = Field(
        ...,
        description=(
            "Check if you do not have criminal convictions for which a pardon has not been "
            "granted"
        )
    )

    required_for_school: BooleanLike = Field(
        ...,
        description="Check if volunteering is required for school"
    )

    number_of_hours_required: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of volunteer hours required for school"
    )

    personal_growth_and_satisfaction: BooleanLike = Field(
        ...,
        description="Check if volunteering for personal growth and satisfaction"
    )

    other_reason_for_volunteering: BooleanLike = Field(
        ...,
        description="Check if volunteering for another reason"
    )

    other_reason_for_volunteering_more_information: str = Field(
        ...,
        description=(
            "Provide more information if you selected 'Other' as your reason for "
            "volunteering .If you cannot fill this, write \"N/A\". If this field should not "
            "be filled by you (for example, it belongs to another person or office), leave "
            "it blank (empty string \"\")."
        )
    )

    why_do_you_want_to_volunteer_at_carewest_additional_information: str = Field(
        ...,
        description=(
            "Explain why you want to volunteer at Carewest .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    what_are_some_of_your_hobbies_and_interests: str = Field(
        ...,
        description=(
            "List your hobbies and interests .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class VolunteeringPreferences(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Applicant's preferences for volunteer roles, availability, and time commitment."""

    community_outing: BooleanLike = Field(
        ...,
        description="Check if applying for Community Outing area"
    )

    leisure_activities: BooleanLike = Field(
        ...,
        description="Check if applying for Leisure Activities area"
    )

    one_to_one_visiting: BooleanLike = Field(
        ...,
        description="Check if applying for One to One Visiting area"
    )

    pastoral_care: BooleanLike = Field(
        ...,
        description="Check if applying for Pastoral Care area"
    )

    non_resident_activities: BooleanLike = Field(
        ...,
        description="Check if applying for Non Resident Activities area"
    )

    rehab_and_recovery: BooleanLike = Field(
        ...,
        description="Check if applying for Rehab and Recovery area"
    )

    gift_stores: BooleanLike = Field(
        ...,
        description="Check if applying for Gift Stores area"
    )

    community_programs: BooleanLike = Field(
        ...,
        description="Check if applying for Community Programs area"
    )

    palliative_care: BooleanLike = Field(
        ...,
        description="Check if applying for Palliative Care area"
    )

    no_preference_unknown: BooleanLike = Field(
        ...,
        description="Check if you have no preference or are unsure"
    )

    other_area_s_applying_for: str = Field(
        ...,
        description=(
            "Specify another area you are applying for .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    one_time_frequency: BooleanLike = Field(
        ...,
        description="Check if you are available one time only"
    )

    weekly_frequency: BooleanLike = Field(
        ...,
        description="Check if you are available weekly"
    )

    monthly_frequency: BooleanLike = Field(
        ...,
        description="Check if you are available monthly"
    )

    would_like_to_discuss_in_person_frequency: BooleanLike = Field(
        ...,
        description="Check if you would like to discuss your availability in person"
    )

    sunday_day_of_week_preference: BooleanLike = Field(
        ...,
        description="Check if you are available on Sundays"
    )

    monday_day_of_week_preference: BooleanLike = Field(
        ...,
        description="Check if you are available on Mondays"
    )

    tuesday_day_of_week_preference: BooleanLike = Field(
        ...,
        description="Check if you are available on Tuesdays"
    )

    wednesday_day_of_week_preference: BooleanLike = Field(
        ...,
        description="Check if you are available on Wednesdays"
    )

    thursday_day_of_week_preference: BooleanLike = Field(
        ...,
        description="Check if you are available on Thursdays"
    )

    friday_day_of_week_preference: BooleanLike = Field(
        ...,
        description="Check if you are available on Fridays"
    )

    saturday_day_of_week_preference: BooleanLike = Field(
        ...,
        description="Check if you are available on Saturdays"
    )

    morning_shift_preference: BooleanLike = Field(
        ...,
        description="Check if you prefer morning shifts"
    )

    afternoon_shift_preference: BooleanLike = Field(
        ...,
        description="Check if you prefer afternoon shifts"
    )

    evening_shift_preference: BooleanLike = Field(
        ...,
        description="Check if you prefer evening shifts"
    )

    weekend_shift_preference: BooleanLike = Field(
        ...,
        description="Check if you prefer weekend shifts"
    )

    available_volunteer_time_commitment_per_shift: str = Field(
        ...,
        description=(
            "Indicate your available time commitment per shift (e.g., hours/week) .If you "
            "cannot fill this, write \"N/A\". If this field should not be filled by you "
            "(for example, it belongs to another person or office), leave it blank (empty "
            "string \"\")."
        )
    )


class VolunteerApplication(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    Volunteer Application

    Thank you for your interest in volunteering with Carewest. We encourage all applicants to visit our website www.carewest.ca to learn more about our company and current volunteer openings. A fillable PDF version of this form can also be found on our website. Note: The minimum age to volunteer is 16 years. Please submit your completed application form using one of the provided methods. If you have any questions regarding your volunteer application and/or Carewest’s volunteer opportunities please contact Recruitment.
    """

    personal_information: PersonalInformation = Field(
        ...,
        description="Personal Information"
    )
    volunteering_preferences: VolunteeringPreferences = Field(
        ...,
        description="Volunteering Preferences"
    )