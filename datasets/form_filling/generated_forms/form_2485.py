from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OnboardingInformation(BaseModel):
    """Personal contact details of the participant"""

    your_name: str = Field(
        ...,
        description=(
            "Your full name as the primary contact for this business. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_number: str = Field(
        ...,
        description=(
            "Primary telephone number where you can be reached. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Primary email address for business communication. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    your_role_in_the_business: str = Field(
        ...,
        description=(
            "Describe your position or role in the business (e.g., owner, manager). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class BusinessInformation(BaseModel):
    """Core business details and structure"""

    name_of_the_business: str = Field(
        ...,
        description=(
            "Registered or operating name of the business. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    business_address: str = Field(
        ...,
        description=(
            "Street address where the business operates. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    business_website: str = Field(
        default="",
        description=(
            "URL of your business website, if applicable. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    business_social_media_accounts: str = Field(
        default="",
        description=(
            "Links or handles for your business social media accounts. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    business_status: Literal[
        "Sole Proprietorship",
        "Non-Profit/Charity",
        "Corporation",
        "Franchise",
        "Partnership",
        "N/A",
        "",
    ] = Field(..., description="Select the legal structure or status of your business.")

    sole_proprietorship: BooleanLike = Field(
        default="", description="Indicates that the business is a sole proprietorship."
    )

    non_profit_charity: BooleanLike = Field(
        default="", description="Indicates that the business is a non-profit or charity."
    )

    corporation: BooleanLike = Field(
        default="", description="Indicates that the business is a corporation."
    )

    franchise: BooleanLike = Field(
        default="", description="Indicates that the business is a franchise."
    )

    partnership: BooleanLike = Field(
        default="", description="Indicates that the business is a partnership."
    )

    years_in_operation: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of years the business has been operating."
    )

    is_your_business_based_at_your_home: BooleanLike = Field(
        ..., description="Indicate whether your business operates from your home address."
    )

    yes_business_based_at_home: BooleanLike = Field(
        default="", description="Check if the business is based at your home."
    )

    no_business_based_at_home: BooleanLike = Field(
        default="", description="Check if the business is not based at your home."
    )

    how_do_you_sell_your_products_or_services: Literal[
        "Online Only", "Offline Only", "Both Online and Offline", "N/A", ""
    ] = Field(..., description="Select whether you sell online, offline, or both.")

    online_only: BooleanLike = Field(
        default="", description="Indicates that you sell products or services only online."
    )

    offline_only: BooleanLike = Field(
        default="",
        description="Indicates that you sell products or services only from a physical location.",
    )

    both_online_and_offline: BooleanLike = Field(
        default="", description="Indicates that you sell both online and from a physical location."
    )

    gross_yearly_turnover: Literal[
        "Less than 20k",
        "20k – 50k",
        "50k – 100k",
        "100k – 500k",
        "500k – 1m",
        "More than 1m",
        "N/A",
        "",
    ] = Field(
        ..., description="Select your gross yearly turnover or projected Year 1 income if new."
    )

    less_than_20k: BooleanLike = Field(
        default="", description="Indicates that gross yearly turnover is less than 20k."
    )

    field_20k_50k: BooleanLike = Field(
        default="", description="Indicates that gross yearly turnover is between 20k and 50k."
    )

    field_50k_100k: BooleanLike = Field(
        default="", description="Indicates that gross yearly turnover is between 50k and 100k."
    )

    field_100k_500k: BooleanLike = Field(
        default="", description="Indicates that gross yearly turnover is between 100k and 500k."
    )

    field_500k_1m: BooleanLike = Field(
        default="", description="Indicates that gross yearly turnover is between 500k and 1m."
    )

    more_than_1m: BooleanLike = Field(
        default="", description="Indicates that gross yearly turnover is more than 1m."
    )

    number_of_full_time_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of full-time employees in your business."
    )

    number_of_part_time_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of part-time employees in your business."
    )

    what_products_or_services_do_you_offer: str = Field(
        ...,
        description=(
            "Describe the main products or services your business provides. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    who_is_your_typical_customer_or_client: str = Field(
        ...,
        description=(
            "Describe the type of customer or client you usually serve. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CommunityFuturesCapitalRegionCoachingAgreementAndOnboarding(BaseModel):
    """
    COMMUNITY FUTURES CAPITAL REGION COACHING AGREEMENT AND ONBOARDING

    ''
    """

    onboarding_information: OnboardingInformation = Field(..., description="Onboarding Information")
    business_information: BusinessInformation = Field(..., description="Business Information")
