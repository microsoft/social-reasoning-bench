from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OnboardingInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Personal and contact information of the person completing the form"""

    your_name: str = Field(
        ...,
        description=(
            "Your full name .If you cannot fill this, write \"N/A\". If this field should "
            "not be filled by you (for example, it belongs to another person or office), "
            "leave it blank (empty string \"\")."
        )
    )

    telephone_number: str = Field(
        ...,
        description=(
            "Your primary telephone number .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    email: str = Field(
        ...,
        description=(
            "Your email address .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    your_role_in_the_business: str = Field(
        ...,
        description=(
            "Describe your role in the business .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class BusinessInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details about the business and its operations"""

    name_of_the_business: str = Field(
        ...,
        description=(
            "Official name of your business .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    business_address: str = Field(
        ...,
        description=(
            "Physical address of your business .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    business_website: str = Field(
        ...,
        description=(
            "Website URL for your business .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    business_social_media_accounts: str = Field(
        ...,
        description=(
            "Links or handles for your business social media accounts .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    business_status: Literal["Sole Proprietorship", "Corporation", "Partnership", "Non-Profit/Charity", "Franchise", "N/A", ""] = Field(
        ...,
        description="Select your business legal structure"
    )

    years_in_operation: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of years your business has been operating"
    )

    is_your_business_based_at_your_home: BooleanLike = Field(
        ...,
        description="Indicate if your business operates from your home"
    )

    how_do_you_sell_your_products_or_services: Literal["Online Only", "Offline Only", "Both Online and Offline", "N/A", ""] = Field(
        ...,
        description="Select how you sell your products or services"
    )

    gross_yearly_turnover: Literal["Less than 20k", "20k – 50k", "50k – 100k", "100k – 500k", "500k – 1m", "More than 1m", "N/A", ""] = Field(
        ...,
        description="Select your business's gross yearly turnover or projected income for Year 1"
    )

    number_of_full_time_employees: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of full-time employees in your business"
    )

    number_of_part_time_employees: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of part-time employees in your business"
    )

    what_products_or_services_do_you_offer: str = Field(
        ...,
        description=(
            "Describe the products or services your business offers .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    who_is_your_typical_customer_or_client: str = Field(
        ...,
        description=(
            "Describe the type of customer or client you usually serve .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )


class CommunityFuturesCapitalRegionCoachingAgreementAndOnboarding(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    COMMUNITY FUTURES CAPITAL REGION COACHING AGREEMENT AND ONBOARDING

    ''
    """

    onboarding_information: OnboardingInformation = Field(
        ...,
        description="Onboarding Information"
    )
    business_information: BusinessInformation = Field(
        ...,
        description="Business Information"
    )