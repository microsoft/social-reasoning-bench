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
    """Basic personal contact details for the minister"""

    your_full_name: str = Field(
        ...,
        description=(
            'Your full legal name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    home_address: str = Field(
        ...,
        description=(
            "Your full home mailing address (street, city, state) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    home_zip: str = Field(..., description="ZIP code for your home address")

    home_phone: str = Field(
        default="",
        description=(
            'Your home telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        default="",
        description=(
            'Your personal mobile phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    personal_email: str = Field(
        ...,
        description=(
            'Your personal email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class EmploymentInformation(BaseModel):
    """Current employment and work contact details"""

    name_of_employer: str = Field(
        default="",
        description=(
            'The name of your current employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    position_title: str = Field(
        default="",
        description=(
            "Your job or position title with your employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    full_time: BooleanLike = Field(default="", description="Check if this position is full-time")

    part_time: BooleanLike = Field(default="", description="Check if this position is part-time")

    work_phone: str = Field(
        default="",
        description=(
            "Main telephone number at your workplace .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_cell_phone: str = Field(
        default="",
        description=(
            "Your work-issued mobile phone number, if any .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_email: str = Field(
        default="",
        description=(
            "Your work or professional email address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_address: str = Field(
        default="",
        description=(
            "The mailing address of your workplace (street, city, state) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    work_zip: str = Field(default="", description="ZIP code for your work address")


class MinistryFormAnnualReportToPresbyteryCommitteeGracePresbytery(BaseModel):
    """
        COM Validated Ministry Form E-4
    Member-at-Large Annual Report to the Presbytery
    Committee on Ministry -- Grace Presbytery

        According to the Book of Order (G-2.0503), “A minister of the Word and Sacrament is a member of a presbytery and shall be engaged in a ministry validated by that presbytery, a member-at-large as determined by the presbytery, or honorably retired.” In addition, the Book of Order (G-2.0503b) states that “A member-at-large is a minister of the Word and Sacrament who has previously been engaged in a validated ministry, and who now, without intentional abandonment of the exercise of ministry, is no longer engaged in a ministry that complies with all the criteria in G-2.0503a. …A member-at-large shall comply with as many of the criteria in G-2.0503a as possible and shall actively participate in the life of a congregation. … The status of member-at-large shall be reviewed annually.” This form is provided to facilitate that annual review.
    """

    personal_information: PersonalInformation = Field(..., description="Personal Information")
    employment_information: EmploymentInformation = Field(..., description="Employment Information")
