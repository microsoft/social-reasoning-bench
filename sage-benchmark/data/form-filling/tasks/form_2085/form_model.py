from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Basic personal and contact details for the applicant"""

    last_name: str = Field(
        ...,
        description=(
            'Applicant\'s legal last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Applicant\'s legal first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    mi: str = Field(
        default="",
        description=(
            'Middle initial .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    social_security_number: str = Field(..., description="Applicant's Social Security Number")

    present_address: str = Field(
        ...,
        description=(
            "Street address where you currently reside .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of current residence .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of current residence")

    zip_code: str = Field(..., description="ZIP code of current residence")

    telephone_number: str = Field(
        ...,
        description=(
            'Primary telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    secondary_number: str = Field(
        default="",
        description=(
            'Alternate telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        default="",
        description=(
            'Cell phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        default="",
        description=(
            'Email address for contact .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    are_you_a_previous_member_yes: BooleanLike = Field(
        default="", description="Indicate YES if you have previously been a member"
    )

    are_you_a_previous_member_no: BooleanLike = Field(
        default="", description="Indicate NO if you have not previously been a member"
    )

    do_you_have_a_valid_drivers_license_no: BooleanLike = Field(
        ..., description="Indicate NO if you do not have a valid driver's license"
    )

    do_you_have_a_valid_drivers_license_yes: BooleanLike = Field(
        ..., description="Indicate YES if you have a valid driver's license"
    )

    drivers_license_state: str = Field(..., description="State that issued your driver's license")

    drivers_license_number: str = Field(
        ...,
        description=(
            'Driver\'s license number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    are_you_18_years_of_age_or_older_yes: BooleanLike = Field(
        ..., description="Indicate YES if you are 18 years of age or older"
    )

    are_you_18_years_of_age_or_older_no: BooleanLike = Field(
        ..., description="Indicate NO if you are under 18 years of age"
    )


class AvailabilityandResidency(BaseModel):
    """Duty shift availability, schedule constraints, and residency/employer permissions"""

    monday_am_availability: BooleanLike = Field(
        default="", description="Check if you are available for Monday 6am–6pm shift"
    )

    monday_pm_availability: BooleanLike = Field(
        default="", description="Check if you are available for Monday 6pm–6am shift"
    )

    tuesday_am_availability: BooleanLike = Field(
        default="", description="Check if you are available for Tuesday 6am–6pm shift"
    )

    tuesday_pm_availability: BooleanLike = Field(
        default="", description="Check if you are available for Tuesday 6pm–6am shift"
    )

    wednesday_am_availability: BooleanLike = Field(
        default="", description="Check if you are available for Wednesday 6am–6pm shift"
    )

    wednesday_pm_availability: BooleanLike = Field(
        default="", description="Check if you are available for Wednesday 6pm–6am shift"
    )

    thursday_am_availability: BooleanLike = Field(
        default="", description="Check if you are available for Thursday 6am–6pm shift"
    )

    thursday_pm_availability: BooleanLike = Field(
        default="", description="Check if you are available for Thursday 6pm–6am shift"
    )

    friday_am_availability: BooleanLike = Field(
        default="", description="Check if you are available for Friday 6am–6pm shift"
    )

    friday_pm_availability: BooleanLike = Field(
        default="", description="Check if you are available for Friday 6pm–6am shift"
    )

    saturday_am_availability: BooleanLike = Field(
        default="", description="Check if you are available for Saturday 6am–6pm shift"
    )

    saturday_pm_availability: BooleanLike = Field(
        default="", description="Check if you are available for Saturday 6pm–6am shift"
    )

    sunday_am_availability: BooleanLike = Field(
        default="", description="Check if you are available for Sunday 6am–6pm shift"
    )

    sunday_pm_availability: BooleanLike = Field(
        default="", description="Check if you are available for Sunday 6pm–6am shift"
    )

    times_definitely_not_available_for_duty: str = Field(
        default="",
        description=(
            "List any specific times when you are not available for duty .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    do_you_live_within_5_miles_of_hawley_yes: BooleanLike = Field(
        ..., description="Indicate YES if your residence is within 5 miles of Hawley"
    )

    do_you_live_within_5_miles_of_hawley_no: BooleanLike = Field(
        ..., description="Indicate NO if your residence is more than 5 miles from Hawley"
    )

    if_employed_in_hawley_would_employer_let_you_leave_work_to_respond_to_a_call_yes: BooleanLike = Field(
        default="",
        description="Indicate YES if your employer would allow you to leave work to respond to calls",
    )

    if_employed_in_hawley_would_employer_let_you_leave_work_to_respond_to_a_call_no: BooleanLike = (
        Field(
            default="",
            description=(
                "Indicate NO if your employer would not allow you to leave work to respond to calls"
            ),
        )
    )


class Education(BaseModel):
    """Highest level of education completed"""

    education_high_school: BooleanLike = Field(
        default="", description="Check if high school is your highest level of education completed"
    )

    education_vocational_or_tech_school: BooleanLike = Field(
        default="",
        description=(
            "Check if vocational or technical school is your highest level of education completed"
        ),
    )

    education_college_university: BooleanLike = Field(
        default="",
        description="Check if college or university is your highest level of education completed",
    )

    education_other: BooleanLike = Field(
        default="",
        description="Check if your highest education level is other than the listed options",
    )

    education_other_specify: str = Field(
        default="",
        description=(
            "Specify other highest level of education completed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class WorkHistory(BaseModel):
    """Employment history starting with the present or most recent job"""

    work_history_1_from: str = Field(
        default="", description="Start date for your present or most recent job (first entry)"
    )  # YYYY-MM-DD format

    work_history_1_employer_name_address_phone: str = Field(
        default="",
        description=(
            "Employer name, address, and phone number for first work history entry .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    work_history_1_name_of_supervisor: str = Field(
        default="",
        description=(
            "Supervisor's name for first work history entry .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_1_reason_for_leaving: str = Field(
        default="",
        description=(
            "Reason for leaving this job (first work history entry) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_1_to: str = Field(
        default="", description="End date for your present or most recent job (first entry)"
    )  # YYYY-MM-DD format

    work_history_2_from: str = Field(
        default="", description="Start date for your second most recent job"
    )  # YYYY-MM-DD format

    work_history_2_employer_name_address_phone: str = Field(
        default="",
        description=(
            "Employer name, address, and phone number for second work history entry .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    work_history_2_name_of_supervisor: str = Field(
        default="",
        description=(
            "Supervisor's name for second work history entry .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_2_reason_for_leaving: str = Field(
        default="",
        description=(
            "Reason for leaving this job (second work history entry) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_2_to: str = Field(
        default="", description="End date for your second most recent job"
    )  # YYYY-MM-DD format

    work_history_3_from: str = Field(
        default="", description="Start date for your third most recent job"
    )  # YYYY-MM-DD format

    work_history_3_employer_name_address_phone: str = Field(
        default="",
        description=(
            "Employer name, address, and phone number for third work history entry .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    work_history_3_name_of_supervisor: str = Field(
        default="",
        description=(
            "Supervisor's name for third work history entry .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_3_reason_for_leaving: str = Field(
        default="",
        description=(
            "Reason for leaving this job (third work history entry) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_3_to: str = Field(
        default="", description="End date for your third most recent job"
    )  # YYYY-MM-DD format

    work_history_4_from: str = Field(
        default="", description="Start date for your fourth most recent job"
    )  # YYYY-MM-DD format

    work_history_4_employer_name_address_phone: str = Field(
        default="",
        description=(
            "Employer name, address, and phone number for fourth work history entry .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    work_history_4_name_of_supervisor: str = Field(
        default="",
        description=(
            "Supervisor's name for fourth work history entry .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_4_reason_for_leaving: str = Field(
        default="",
        description=(
            "Reason for leaving this job (fourth work history entry) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_4_to: str = Field(
        default="", description="End date for your fourth most recent job"
    )  # YYYY-MM-DD format

    work_history_5_from: str = Field(
        default="", description="Start date for your fifth most recent job"
    )  # YYYY-MM-DD format

    work_history_5_employer_name_address_phone: str = Field(
        default="",
        description=(
            "Employer name, address, and phone number for fifth work history entry .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    work_history_5_name_of_supervisor: str = Field(
        default="",
        description=(
            "Supervisor's name for fifth work history entry .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_5_reason_for_leaving: str = Field(
        default="",
        description=(
            "Reason for leaving this job (fifth work history entry) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    work_history_5_to: str = Field(
        default="", description="End date for your fifth most recent job"
    )  # YYYY-MM-DD format


class ApplicationForMembershipemployment(BaseModel):
    """
    Application for Membership/Employment

    ''
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    availability_and_residency: AvailabilityandResidency = Field(
        ..., description="Availability and Residency"
    )
    education: Education = Field(..., description="Education")
    work_history: WorkHistory = Field(..., description="Work History")
