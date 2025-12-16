from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ForOfficeUseOnly(BaseModel):
    """Internal tracking and approval details"""

    reference_number: str = Field(
        default="",
        description=(
            "Internal reference number for office use only .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_received: str = Field(
        default="", description="Date the application was received (office use only)"
    )  # YYYY-MM-DD format

    date_received_by: str = Field(
        default="",
        description=(
            "Initials or name of staff member who recorded the date received .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_approved: str = Field(
        default="", description="Date the application was approved (office use only)"
    )  # YYYY-MM-DD format

    date_approved_by: str = Field(
        default="",
        description=(
            "Initials or name of staff member who approved the application .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    termination_date: str = Field(
        default="", description="Date the funding or support terminates (office use only)"
    )  # YYYY-MM-DD format

    termination_date_by: str = Field(
        default="",
        description=(
            "Initials or name of staff member who recorded the termination date .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class OrganizationInformation(BaseModel):
    """Basic information about the applying organization"""

    organization_name: str = Field(
        ...,
        description=(
            'Full legal name of the organization .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    charity_registration_number: str = Field(
        ...,
        description=(
            "Official charity registration or nonprofit number .If you cannot fill this, "
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

    head_office_address: str = Field(
        ...,
        description=(
            "Street address of the organization’s head office .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the head office address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    post_code: str = Field(..., description="Postal or ZIP code of the head office address")

    email_address: str = Field(
        ...,
        description=(
            "Primary email address for the organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        ...,
        description=(
            "Primary phone number for the organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    representative_first_name: str = Field(
        ...,
        description=(
            "First name of the main contact person for this application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    representative_last_name: str = Field(
        ...,
        description=(
            "Last name of the main contact person for this application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    representative_phone_number: str = Field(
        default="",
        description=(
            "Phone number for the representative/contact person .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    representative_email: str = Field(
        default="",
        description=(
            "Email address for the representative/contact person .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    best_contact_method_phone: BooleanLike = Field(
        default="", description="Select if phone is the preferred contact method"
    )

    best_contact_method_email: BooleanLike = Field(
        default="", description="Select if email is the preferred contact method"
    )

    referred_by: str = Field(
        default="",
        description=(
            "Name of person or organization that referred you .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class OrganizationPurpose(BaseModel):
    """Details about the purpose and beneficiaries of the organization"""

    purpose_of_the_organization_description: str = Field(
        ...,
        description=(
            "Describe the organization’s purpose, who it benefits, and how .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class SupportRequested(BaseModel):
    """Type of support requested from the foundation"""

    do_you_need_financial_support: BooleanLike = Field(
        default="", description="Indicate whether you are requesting financial support"
    )

    do_you_need_volunteer_support: BooleanLike = Field(
        default="", description="Indicate whether you are requesting volunteer support"
    )

    other_support_needed: str = Field(
        default="",
        description=(
            "Describe any other type of support you are requesting .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Authorization(BaseModel):
    """Applicant authorization and confirmation"""

    signature: str = Field(
        ...,
        description=(
            'Authorized representative’s signature .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class BigWheelCommunityFoundationCharityFundingApplicationForm(BaseModel):
    """
        BIG WHEEL
    COMMUNITY FOUNDATION

    CHARITY FUNDING
    APPLICATION FORM

        ''
    """

    for_office_use_only: ForOfficeUseOnly = Field(..., description="For Office Use Only")
    organization_information: OrganizationInformation = Field(
        ..., description="Organization Information"
    )
    organization_purpose: OrganizationPurpose = Field(..., description="Organization Purpose")
    support_requested: SupportRequested = Field(..., description="Support Requested")
    authorization: Authorization = Field(..., description="Authorization")
