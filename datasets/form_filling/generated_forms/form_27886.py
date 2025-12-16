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
    """Applicant’s personal and contact details"""

    name: str = Field(
        ...,
        description=(
            'Applicant\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    company_if_applicable: str = Field(
        default="",
        description=(
            "Company or organization name, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    main_phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street address .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    alt_phone: str = Field(
        default="",
        description=(
            'Alternate contact phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of residence or mailing address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    province: str = Field(
        ...,
        description=(
            'Province or territory .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Primary email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    postal_code: str = Field(..., description="Postal code for the address")


class ProgramInformation(BaseModel):
    """Details about the proposed program"""

    program_title: str = Field(
        ...,
        description=(
            'Title of the proposed program .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    please_briefly_describe_program: str = Field(
        ...,
        description=(
            "Short description of the program concept and content .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    is_this_a_special_one_time_only_event_please_specify: str = Field(
        default="",
        description=(
            "Indicate if this is a one-time event and provide details .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    languages_please_specify: str = Field(
        ...,
        description=(
            "Languages in which the program will be produced .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    subtitles_please_specify: str = Field(
        default="",
        description=(
            'Subtitle languages, if any .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    how_will_you_promote_the_show_please_specify: str = Field(
        default="",
        description=(
            "Describe how you plan to promote or market the show .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ShawMulticulturalChannelProgramApplication(BaseModel):
    """
    Shaw Multicultural Channel Program Application

    I have a Shaw Multicultural Channel Program request and I understand that the channel operates under the Shaw Multicultural Channel Guidelines and Information. I accept and agree to the provisions contained therein, and will abide by these guidelines as Independent Producer, including but not limited to the use of others’ creative material including music, art and branding.
    """

    contact_information: ContactInformation = Field(..., description="Contact Information")
    program_information: ProgramInformation = Field(..., description="Program Information")
