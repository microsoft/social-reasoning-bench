from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectInformation(BaseModel):
    """Core details about the nominated project"""

    project_title: str = Field(
        ...,
        description=(
            'Title of the nominated project .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    project_outline: str = Field(
        ...,
        description=(
            "Brief overview of the project (up to 200 words) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    project_website_link: str = Field(
        default="",
        description=(
            'URL of the project website (optional) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    youtube_video_link: str = Field(
        default="",
        description=(
            "URL of a supporting YouTube video of up to two minutes (optional) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class MainContactfortheNominatedProject(BaseModel):
    """Primary contact details for the nominated project"""

    main_contact_name: str = Field(
        ...,
        description=(
            "Full name of the main contact for the nominated project .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    main_contact_position_role: str = Field(
        ...,
        description=(
            'Job title or role of the main contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    main_contact_organisation: str = Field(
        ...,
        description=(
            "Organisation that the main contact represents .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    main_contact_address_line_1: str = Field(
        ...,
        description=(
            "First line of the main contact's postal address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    main_contact_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the main contact's postal address (if needed) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    main_contact_postcode: str = Field(..., description="Postcode for the main contact's address")

    main_contact_tel: str = Field(
        ...,
        description=(
            'Telephone number for the main contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    main_contact_email: str = Field(
        ...,
        description=(
            'Email address for the main contact .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class NominatedByIfDifferentfromMainContact(BaseModel):
    """Details of the person/organisation nominating the project"""

    nominated_by_name: str = Field(
        default="",
        description=(
            "Full name of the person nominating the project (if different from main "
            'contact) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    nominated_by_position_role: str = Field(
        default="",
        description=(
            'Job title or role of the nominator .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    nominated_by_organisation: str = Field(
        default="",
        description=(
            "Organisation that the nominator represents .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    nominated_by_address_line_1: str = Field(
        default="",
        description=(
            "First line of the nominator's postal address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    nominated_by_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the nominator's postal address (if needed) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    nominated_by_postcode: str = Field(
        default="", description="Postcode for the nominator's address"
    )

    nominated_by_tel: str = Field(
        default="",
        description=(
            'Telephone number for the nominator .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    nominated_by_email: str = Field(
        default="",
        description=(
            'Email address for the nominator .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class SurfAwards2021SupportingYouthEmployabilityApplicationForm(BaseModel):
    """
        SURF Awards 2021
    Supporting Youth Employability Application Form

        Supporting Youth Employability Application Form
    """

    project_information: ProjectInformation = Field(..., description="Project Information")
    main_contact_for_the_nominated_project: MainContactfortheNominatedProject = Field(
        ..., description="Main Contact for the Nominated Project"
    )
    nominated_by_if_different_from_main_contact: NominatedByIfDifferentfromMainContact = Field(
        ..., description="Nominated By (If Different from Main Contact)"
    )
