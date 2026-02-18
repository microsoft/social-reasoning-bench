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

    phone_primary: str = Field(
        ...,
        description=(
            'Main organizational phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            'Organization fax number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
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
            'Organization website URL .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    organization_email_address: str = Field(
        ...,
        description=(
            "Primary email address for the organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
            "Name and title of the primary application contact, if different from the CEO "
            'or Executive Director .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
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
    """Background and mission of the organization"""

    year_founded: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year the organization was founded"
    )

    five01_c_3: BooleanLike = Field(
        default="", description="Indicate whether the organization is a 501(c)(3) tax-exempt entity"
    )

    tax_exempt_number: str = Field(
        default="",
        description=(
            "Organization's tax exemption identification number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mission_statement_line_1: str = Field(
        ...,
        description=(
            "First line of the organization's mission statement .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mission_statement_line_2: str = Field(
        default="",
        description=(
            "Second line of the organization's mission statement .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mission_statement_line_3: str = Field(
        default="",
        description=(
            "Third line of the organization's mission statement .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    geographic_area_served: str = Field(
        ...,
        description=(
            "Primary geographic region(s) where the organization operates or provides "
            'services .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class GrantApplicationForm(BaseModel):
    """
    GRANT APPLICATION FORM

    ''
    """

    organization_contact_information: OrganizationContactInformation = Field(
        ..., description="Organization Contact Information"
    )
    organization_information: OrganizationInformation = Field(
        ..., description="Organization Information"
    )
