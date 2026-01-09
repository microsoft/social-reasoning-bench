from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class StudentInformation(BaseModel):
    """Basic information about the student and high school"""

    students_name: str = Field(
        ...,
        description=(
            'Student\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    high_school: str = Field(
        ...,
        description=(
            "Name of the high school currently or most recently attended .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_of_birth: str = Field(..., description="Student's date of birth")  # YYYY-MM-DD format

    gpa: Union[float, Literal["N/A", ""]] = Field(..., description="Current grade point average")


class ContactInformation(BaseModel):
    """Home address and primary contact details"""

    home_address: str = Field(
        ...,
        description=(
            "Street address of student's primary residence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for the home address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    best_number_to_reach_you: str = Field(
        ...,
        description=(
            "Primary phone number where the student can be reached .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Student\'s email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    name_of_parents_or_guardian: str = Field(
        ...,
        description=(
            "Full name(s) of parent(s) or legal guardian .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Phone number for parent or guardian .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ChurchCommunityInvolvement(BaseModel):
    """Church membership, housing, event participation, and community service"""

    member_of_the_hope_church_or_kingdom_harvest_ministries: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you are a member of The Hope Church or Kingdom Harvest Ministries"
        ),
    )

    member_of_the_hope_church_or_kingdom_harvest_ministries_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate that you are not a member of The Hope Church or Kingdom Harvest Ministries"
        ),
    )

    membership_duration_5_plus_years: BooleanLike = Field(
        default="", description="Select if you have been a member for 5 or more years"
    )

    membership_duration_1_4_years: BooleanLike = Field(
        default="", description="Select if you have been a member for 1 to 4 years"
    )

    membership_duration_less_than_1_year: BooleanLike = Field(
        default="", description="Select if you have been a member for less than 1 year"
    )

    membership_duration_not_a_member: BooleanLike = Field(
        default="", description="Select if you are not a member"
    )

    how_long_lived_in_hope_west_campus_property: str = Field(
        default="",
        description=(
            "Length of time you have lived in a Hope West Campus property .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    participated_in_2018_wiggins_scholarship_walk_yes: BooleanLike = Field(
        default="",
        description=(
            "Indicate if you participated in or volunteered at the 2018 Dr. R.W. Wiggins "
            "Scholarship Walk"
        ),
    )

    participated_in_2018_wiggins_scholarship_walk_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate if you did not participate in or volunteer at the 2018 Dr. R.W. "
            "Wiggins Scholarship Walk"
        ),
    )

    describe_your_community_service_activities: str = Field(
        default="",
        description=(
            "Describe the community service activities you have participated in .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class EducationPlans(BaseModel):
    """Planned college and field of study"""

    college_university_you_will_attend: str = Field(
        ...,
        description=(
            "Name of the college, university, or technical school you plan to attend .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    planned_field_of_study: str = Field(
        ...,
        description=(
            'Intended major or field of study .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class RequiredAttachments(BaseModel):
    """Documents and materials to include with the application"""

    high_school_transcript_or_latest_report_card: BooleanLike = Field(
        ...,
        description=(
            "Confirm that you have included your high school transcript or latest report "
            "card with the application"
        ),
    )

    letter_of_recommendation: BooleanLike = Field(
        ...,
        description=(
            "Confirm that you have included one letter of recommendation from an appropriate person"
        ),
    )

    awards_and_honors: str = Field(
        default="",
        description=(
            "List awards and honors received, including other scholarships, with date, "
            "organization, and amount if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    personal_essay: str = Field(
        ...,
        description=(
            "500-word personal essay addressing why you want to attend college or technical "
            "school, your career goals, what this scholarship would mean to you, and the "
            'importance of your faith .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class Certification(BaseModel):
    """Applicant certification and signature"""

    students_signature: str = Field(
        ...,
        description=(
            "Student's signature certifying the accuracy of the application information .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Application(BaseModel):
    """
    APPLICATION

    Please return completed application packet to The Hope Church Administrative Office. Type or print in black ink.
    """

    student_information: StudentInformation = Field(..., description="Student Information")
    contact_information: ContactInformation = Field(..., description="Contact Information")
    church__community_involvement: ChurchCommunityInvolvement = Field(
        ..., description="Church & Community Involvement"
    )
    education_plans: EducationPlans = Field(..., description="Education Plans")
    required_attachments: RequiredAttachments = Field(..., description="Required Attachments")
    certification: Certification = Field(..., description="Certification")
