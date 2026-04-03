from pydantic import BaseModel, ConfigDict, Field


class CommunityFuturesCoachingAgreementOnboarding(BaseModel):
    """COMMUNITY FUTURES CAPITAL REGION COACHING AGREEMENT AND ONBOARDING

    Purpose: Business coaching agreement and onboarding form used to collect essential information about a business and its owner for participation in a coaching program.
    Recipient: Staff or coaches at Community Futures Capital Region who will use this information to onboard and provide coaching services to business owners.
    """

    model_config = ConfigDict(extra="forbid")

    business_num_part_time_employees: str = Field(..., description='Number of part-time employees. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    business_products_services: str = Field(..., description='Products or services offered. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    business_typical_customer: str = Field(..., description='Typical customer or client. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')