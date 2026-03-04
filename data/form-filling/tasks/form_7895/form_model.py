from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OrganizationContactInformation(BaseModel):
    """Basic organizational identity and primary contact details"""

    legal_name_of_organization: str = Field(
        ...,
        description=(
            "Full legal name of the organization as registered .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            "Primary mailing address for the organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    organization_phone: str = Field(
        ...,
        description=(
            "Main phone number for the organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            "Fax number for the organization, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ein: str = Field(
        ...,
        description=(
            "Employer Identification Number for the organization .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    website: str = Field(
        default="",
        description=(
            'Organization’s website URL .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    organization_email_address: str = Field(
        ...,
        description=(
            "General contact email address for the organization .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_ceo_or_executive_director: str = Field(
        ...,
        description=(
            "Full name of the CEO or Executive Director .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ceo_phone: str = Field(
        ...,
        description=(
            "Phone number for the CEO or Executive Director .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ceo_email: str = Field(
        ...,
        description=(
            "Email address for the CEO or Executive Director .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    application_contact_title_if_not_the_ceo_or_executive_director: str = Field(
        default="",
        description=(
            "Name and title of the primary contact for this application, if different from "
            'the CEO or Executive Director .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    application_contact_phone: str = Field(
        default="",
        description=(
            "Phone number for the application contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    application_contact_email: str = Field(
        default="",
        description=(
            "Email address for the application contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class OrganizationInformation(BaseModel):
    """Background and status information about the organization"""

    year_founded: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year the organization was founded"
    )

    tax_exemption_status_501c3: BooleanLike = Field(
        ..., description="Indicate whether the organization is a 501(c)(3) tax-exempt entity"
    )

    tax_exempt_number: str = Field(
        ...,
        description=(
            "Tax exemption identification number assigned to the organization .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mission_statement: str = Field(
        ...,
        description=(
            'Organization’s mission statement .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    geographic_area_served: str = Field(
        ...,
        description=(
            "Primary geographic region(s) the organization serves .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class BuffaloRenaissanceFoundationGrantApplicationForm(BaseModel):
    """
        BUFFALO
    RENAISSANCE FOUNDATION

    GRANT APPLICATION FORM

        ''
    """

    organization_contact_information: OrganizationContactInformation = Field(
        ..., description="Organization Contact Information"
    )
    organization_information: OrganizationInformation = Field(
        ..., description="Organization Information"
    )
