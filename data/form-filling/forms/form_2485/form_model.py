from pydantic import BaseModel, ConfigDict, Field


class CommunityFuturesCapitalRegionCoachingAgreementOnboarding(BaseModel):
    """Community Futures Capital Region Coaching Agreement and Onboarding

    Business owners or representatives submit this onboarding form as part of a coaching agreement to provide core business and contact details. Community Futures Capital Region coaching staff review it to set up the client file, understand the business context, and tailor coaching support and planning based on the business structure, operations, sales channels, and current scale.
    """

    model_config = ConfigDict(extra="forbid")

    onboarding_info_business_info_telephone_number: str = Field(
        ...,
        description='Telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    onboarding_info_business_info_your_role_in_business: str = Field(
        ...,
        description='Your role in the business. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    onboarding_info_business_info_business_social_media_accounts: str = Field(
        ...,
        description='Business social media accounts. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


    onboarding_info_business_info_years_in_operation: float | None = Field(
        ...,
        description="Years in operation",
    )




    onboarding_info_business_info_number_part_time_employees: float | None = Field(
        ...,
        description="Number of part-time employees",
    )

    onboarding_info_business_info_products_or_services_offered: str = Field(
        ...,
        description='Products or services offered. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    onboarding_info_business_info_typical_customer_or_client: str = Field(
        ...,
        description='Typical customer or client. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )