from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class GeneralInformation(BaseModel):
    """Basic personal and contact information"""

    first: str = Field(
        ...,
        description=(
            'Applicant\'s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    middle: str = Field(
        default="",
        description=(
            'Applicant\'s middle name or initial .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    last: str = Field(
        ...,
        description=(
            'Applicant\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    street_address: str = Field(
        ...,
        description=(
            "Street address portion of the applicant's mailing address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City for the mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for the mailing address")

    zip: str = Field(..., description="ZIP or postal code for the mailing address")

    cell_phone: str = Field(
        ...,
        description=(
            'Applicant\'s mobile/cell phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    home_phone: str = Field(
        default="",
        description=(
            "Applicant's home/landline phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        ...,
        description=(
            'Applicant\'s primary email address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    emergency_name_phone_number: str = Field(
        ...,
        description=(
            "Name and phone number of an emergency contact person .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    special_conditions_affecting_ability_to_work_in_educational_setting: str = Field(
        default="",
        description=(
            "Describe any medical, physical, or other conditions that may affect your "
            "ability to work in an educational setting .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PresentEmployment(BaseModel):
    """Current employment details and related experience"""

    present_employment: str = Field(
        default="",
        description=(
            "Brief description or title of current employment situation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    place_where_presently_employed_if_applicable: str = Field(
        default="",
        description=(
            "Name of the organization or employer where you are currently employed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    position: str = Field(
        default="",
        description=(
            "Job title or position at your present place of employment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    present_employer_address: str = Field(
        default="",
        description=(
            "Mailing address of your present employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    subjects_taught_if_applicable: str = Field(
        default="",
        description=(
            "List of subjects you currently teach, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    grades: str = Field(
        default="",
        description=(
            "Grade levels of students you currently teach, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    reasons_for_leaving_present_position: str = Field(
        default="",
        description=(
            "Explain why you are leaving or wish to leave your present position .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    may_we_contact_your_present_employer: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the organization has permission to contact your current employer"
        ),
    )

    experience_working_with_young_people_out_of_school_programs: str = Field(
        default="",
        description=(
            "Describe your experience working with young people in organized out-of-school "
            'or extracurricular programs .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    extra_curricular_activities_line_1: str = Field(
        default="",
        description=(
            "First line to list extra-curricular student activities in which you are "
            'currently involved .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    extra_curricular_activities_line_2: str = Field(
        default="",
        description=(
            "Second line to list extra-curricular student activities in which you are "
            'currently involved .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    extra_curricular_activities_line_3: str = Field(
        default="",
        description=(
            "Third line to list extra-curricular student activities in which you are "
            'currently involved .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    extra_curricular_activities_line_4: str = Field(
        default="",
        description=(
            "Fourth line to list extra-curricular student activities in which you are "
            'currently involved .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class GeneralInformation(BaseModel):
    """
    GENERAL INFORMATION

    ''
    """

    general_information: GeneralInformation = Field(..., description="General Information")
    present_employment: PresentEmployment = Field(..., description="Present Employment")
