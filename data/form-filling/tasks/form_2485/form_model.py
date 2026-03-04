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
    """Contact details and role for the person completing the form"""

    your_name: str = Field(
        ...,
        description=(
            'Your full name .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    telephone_number: str = Field(
        ...,
        description=(
            "Primary telephone number where you can be reached .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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

    your_role_in_the_business: str = Field(
        ...,
        description=(
            "Your position or role in the business (e.g., owner, manager) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class BusinessInformation(BaseModel):
    """Core business details, structure, operations, and customers"""

    name_of_the_business: str = Field(
        ...,
        description=(
            "Registered or operating name of the business .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    business_address: str = Field(
        ...,
        description=(
            'Full mailing address of the business .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    business_website: str = Field(
        default="",
        description=(
            "URL of the business website, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    business_social_media_accounts: str = Field(
        default="",
        description=(
            "Links or handles for your business social media accounts .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    business_status_sole_proprietorship: BooleanLike = Field(
        default="", description="Check if the business is a sole proprietorship"
    )

    business_status_non_profit_charity: BooleanLike = Field(
        default="", description="Check if the business is a non-profit or charity"
    )

    business_status_corporation: BooleanLike = Field(
        default="", description="Check if the business is a corporation"
    )

    business_status_franchise: BooleanLike = Field(
        default="", description="Check if the business is a franchise"
    )

    business_status_partnership: BooleanLike = Field(
        default="", description="Check if the business is a partnership"
    )

    years_in_operation: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years the business has been operating"
    )

    is_your_business_based_at_your_home_yes: BooleanLike = Field(
        default="", description="Select if the business is based at your home"
    )

    is_your_business_based_at_your_home_no: BooleanLike = Field(
        default="", description="Select if the business is not based at your home"
    )

    online_only: BooleanLike = Field(
        default="", description="Select if you sell products or services only online"
    )

    offline_only: BooleanLike = Field(
        default="",
        description="Select if you sell products or services only from a physical location",
    )

    both_online_and_offline: BooleanLike = Field(
        default="",
        description=(
            "Select if you sell products or services both online and from a physical location"
        ),
    )

    gross_yearly_turnover_less_than_20k: BooleanLike = Field(
        default="", description="Select if gross yearly turnover is less than 20k"
    )

    gross_yearly_turnover_20k_50k: BooleanLike = Field(
        default="", description="Select if gross yearly turnover is between 20k and 50k"
    )

    gross_yearly_turnover_50k_100k: BooleanLike = Field(
        default="", description="Select if gross yearly turnover is between 50k and 100k"
    )

    gross_yearly_turnover_100k_500k: BooleanLike = Field(
        default="", description="Select if gross yearly turnover is between 100k and 500k"
    )

    gross_yearly_turnover_500k_1m: BooleanLike = Field(
        default="", description="Select if gross yearly turnover is between 500k and 1m"
    )

    gross_yearly_turnover_more_than_1m: BooleanLike = Field(
        default="", description="Select if gross yearly turnover is more than 1m"
    )

    number_of_full_time_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of full-time employees"
    )

    number_of_part_time_employees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of part-time employees"
    )

    what_products_or_services_do_you_offer: str = Field(
        default="",
        description=(
            "Describe the main products or services your business offers .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    who_is_your_typical_customer_or_client: str = Field(
        default="",
        description=(
            "Describe the type of customer or client you typically serve .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class CommunityFuturesCapitalRegionCoachingAgreementAndOnboarding(BaseModel):
    """
    COMMUNITY FUTURES CAPITAL REGION COACHING AGREEMENT AND ONBOARDING

    ''
    """

    onboarding_information: OnboardingInformation = Field(..., description="Onboarding Information")
    business_information: BusinessInformation = Field(..., description="Business Information")
