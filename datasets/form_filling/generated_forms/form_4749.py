from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ContactInformation(BaseModel):
    """Primary contact details for the person submitting the proposal"""

    name: str = Field(
        ...,
        description=(
            "Instructor's full name, first and last .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        ...,
        description=(
            'Primary email address for contact .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            'Street mailing address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City for mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State abbreviation for mailing address")

    zip: str = Field(..., description="ZIP code for mailing address")

    cell_phone_number: str = Field(
        default="",
        description=(
            'Cell/mobile phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    home_phone_number: str = Field(
        default="",
        description=(
            'Home phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    work_phone_number: str = Field(
        default="",
        description=(
            'Work or office phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class ProposedProgramInformation(BaseModel):
    """Details about the proposed program, schedule, audience, and logistics"""

    program_title: str = Field(
        ...,
        description=(
            'Title of the proposed program .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    program_description: str = Field(
        ...,
        description=(
            "Description of the program to be used for print and other advertising .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    length_of_each_class_hours_minutes: str = Field(
        ...,
        description=(
            "Duration of each class session in hours and/or minutes .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    time_of_class: str = Field(
        ...,
        description=(
            "Start time or time range for each class .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    length_of_session_1_class_number_of_weeks: str = Field(
        ...,
        description=(
            "Overall session length, such as single class or number of weeks .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    dates_of_class: str = Field(
        ...,
        description=(
            "Specific date or range of dates when the class will be held .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    number_of_times_per_week_one: BooleanLike = Field(
        ..., description="Check if the class meets once per week"
    )

    number_of_times_per_week_two: BooleanLike = Field(
        ..., description="Check if the class meets twice per week"
    )

    number_of_times_per_week_three: BooleanLike = Field(
        ..., description="Check if the class meets three times per week"
    )

    number_of_times_per_week_four: BooleanLike = Field(
        ..., description="Check if the class meets four times per week"
    )

    number_of_times_per_week_five: BooleanLike = Field(
        ..., description="Check if the class meets five times per week"
    )

    preferred_days_monday: BooleanLike = Field(
        default="", description="Select if Monday is a preferred day for the class"
    )

    preferred_days_tuesday: BooleanLike = Field(
        default="", description="Select if Tuesday is a preferred day for the class"
    )

    preferred_days_wednesday: BooleanLike = Field(
        default="", description="Select if Wednesday is a preferred day for the class"
    )

    preferred_days_thursday: BooleanLike = Field(
        default="", description="Select if Thursday is a preferred day for the class"
    )

    preferred_days_friday: BooleanLike = Field(
        default="", description="Select if Friday is a preferred day for the class"
    )

    preferred_days_saturday: BooleanLike = Field(
        default="", description="Select if Saturday is a preferred day for the class"
    )

    time_of_year_fall_sept_nov: BooleanLike = Field(
        default="", description="Select if Fall (September–November) is the preferred season"
    )

    time_of_year_winter_dec_feb: BooleanLike = Field(
        default="", description="Select if Winter (December–February) is the preferred season"
    )

    time_of_year_spring_mar_may: BooleanLike = Field(
        default="", description="Select if Spring (March–May) is the preferred season"
    )

    time_of_year_summer_june_aug: BooleanLike = Field(
        default="", description="Select if Summer (June–August) is the preferred season"
    )

    target_audience_female: BooleanLike = Field(
        default="", description="Select if the program is intended for female participants"
    )

    target_audience_male: BooleanLike = Field(
        default="", description="Select if the program is intended for male participants"
    )

    target_audience_co_ed: BooleanLike = Field(
        default="", description="Select if the program is intended for all genders (co-ed)"
    )

    age_or_grade_of_participants: str = Field(
        ...,
        description=(
            "Age range or school grade level of participants .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    minimum_enrollment: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Minimum number of participants required to run the program"
    )

    maximum_enrollment: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Maximum number of participants allowed in the program"
    )

    instructor_compensation_per_participant: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of compensation requested per participant"
    )

    instructor_compensation_waive_fee: BooleanLike = Field(
        default="", description="Check if you wish to waive your instructor fee"
    )

    ideal_type_of_space: str = Field(
        default="",
        description=(
            "Description of the ideal space needed (e.g., open area, classroom) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    equipment_needed_yes: BooleanLike = Field(
        default="", description="Select YES if participants need to bring equipment"
    )

    equipment_needed_no: BooleanLike = Field(
        default="", description="Select NO if participants do not need to bring equipment"
    )

    equipment_needed_description: str = Field(
        default="",
        description=(
            "List any equipment participants must bring .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    materials_supplies_needed_yes: BooleanLike = Field(
        default="", description="Select YES if participants need to bring materials or supplies"
    )

    materials_supplies_needed_no: BooleanLike = Field(
        default="",
        description="Select NO if participants do not need to bring materials or supplies",
    )

    materials_supplies_needed_description: str = Field(
        default="",
        description=(
            "List any materials or supplies participants must bring .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class InstructorFacilitatorInformation(BaseModel):
    """Background information about the instructor or facilitator"""

    instructor_bio: str = Field(
        ...,
        description=(
            "Brief biography of the instructor to be posted on the website .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    instructor_qualifications: str = Field(
        ...,
        description=(
            "Instructor's qualifications, including trainings, education, work experience, "
            'and certifications .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class ProgramProposalForm(BaseModel):
    """
    Program Proposal Form

    Thank you for your interest in offering a program with the Williston Recreation & Parks Department. Please complete this proposal and return with your resume. Your proposal will be reviewed, if determined to meet the needs of our community, you will be contacted and details can be discussed. Please call or email if you have any questions- 876-1160 or recreation@willistonvt.org
    **Note: we attempt to offer programs at the lowest possible price as a service to our community. Instructor compensation is one of the factors considered when determining program offerings. We welcome those who wish to donate their time as a service to our community.
    """

    contact_information: ContactInformation = Field(..., description="Contact Information")
    proposed_program_information: ProposedProgramInformation = Field(
        ..., description="Proposed Program Information"
    )
    instructorfacilitator_information: InstructorFacilitatorInformation = Field(
        ..., description="Instructor/Facilitator Information"
    )
