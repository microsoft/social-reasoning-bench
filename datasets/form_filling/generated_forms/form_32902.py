from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AgentInformation(BaseModel):
    """Basic personal and contact information for the agent"""

    name: str = Field(
        ...,
        description=(
            'Full legal name of the agent .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    nickname_optional: str = Field(
        default="",
        description=(
            "Preferred nickname, if different from legal name .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(..., description="Date of birth")  # YYYY-MM-DD format

    title_real_estate_agent_agent_broker_etc: str = Field(
        ...,
        description=(
            "Professional title or role (e.g., Real Estate Agent, Broker) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    cell_phone: str = Field(
        ...,
        description=(
            'Primary cell phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    additional_phone_optional: str = Field(
        default="",
        description=(
            "Additional contact phone number, if any .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    fax_optional: str = Field(
        default="",
        description=(
            'Fax number, if applicable .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Primary email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            'Mailing address for correspondence .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class LicensingInformation(BaseModel):
    """Real estate and driver licensing details"""

    state: str = Field(..., description="State where you are licensed")

    mls: str = Field(
        ...,
        description=(
            "Name of the Multiple Listing Service (MLS) you belong to .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    re_license_number: str = Field(
        ...,
        description=(
            'Real estate license number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    exp_date: str = Field(
        ..., description="Real estate license expiration date"
    )  # YYYY-MM-DD format

    lag_number_mls_id: str = Field(
        default="",
        description=(
            'LAG number or MLS ID, if applicable .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    drivers_license_number: str = Field(
        ...,
        description=(
            'Driver\'s license number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    state_drivers_license: str = Field(..., description="State that issued your driver's license")

    hours_you_estimate_youll_be_working_per_month: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of hours you plan to work per month"
    )

    how_did_you_hear_about_kelly_right: str = Field(
        default="",
        description=(
            "Describe how you first heard about Kelly Right .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    referred_by: str = Field(
        default="",
        description=(
            "Name of the person or source that referred you .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class InformationforYourWebsite(BaseModel):
    """Website and social media information to be used online"""

    website_business_social_media_links_tagline_etc_line_1: str = Field(
        default="",
        description=(
            "Website URLs, business social media links, tagline, etc. (first line) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    website_business_social_media_links_tagline_etc_line_2: str = Field(
        default="",
        description=(
            "Continuation of website, social media links, or tagline (second line) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    website_business_social_media_links_tagline_etc_line_3: str = Field(
        default="",
        description=(
            "Continuation of website, social media links, or tagline (third line) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    website_business_social_media_links_tagline_etc_line_4: str = Field(
        default="",
        description=(
            "Continuation of website, social media links, or tagline (fourth line) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AgentInformationPage(BaseModel):
    """
    AGENT INFORMATION PAGE

    Please fill out completely. Be sure to verify all information and print legibly. Please return this form via fax: 509-340-3515 or email: join@kellyright.com
    """

    agent_information: AgentInformation = Field(..., description="Agent Information")
    licensing_information: LicensingInformation = Field(..., description="Licensing Information")
    information_for_your_website: InformationforYourWebsite = Field(
        ..., description="Information for Your Website"
    )
