from pydantic import BaseModel, ConfigDict, Field


class CommunityFuturesCapitalRegionCoachingAgreementAndOnboarding(BaseModel):
    """COMMUNITY FUTURES CAPITAL REGION COACHING AGREEMENT AND ONBOARDING"""

    model_config = ConfigDict(extra="forbid")

    onboarding_information_telephone_number: str = Field(
        ...,
        description='Telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    onboarding_information_your_role_in_business: str = Field(
        ...,
        description='Your role in the business. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    business_information_business_address: str = Field(
        ...,
        description='Business address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    business_information_years_in_operation: str = Field(
        ...,
        description='Years in operation. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    business_information_number_full_time_employees: str = Field(
        ...,
        description='Number of full-time employees. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    business_information_number_part_time_employees: str = Field(
        ...,
        description='Number of part time employees. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    business_information_products_services_offered: str = Field(
        ...,
        description='Products or services offered. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    business_information_typical_customer: str = Field(
        ...,
        description='Typical customer or client. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )