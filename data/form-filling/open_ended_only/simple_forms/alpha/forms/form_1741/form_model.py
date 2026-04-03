from pydantic import BaseModel, ConfigDict, Field


class PreTenancyApplicationForm(BaseModel):
    """Pre-tenancy application form

    Purpose: Pre-tenancy application to assess prospective tenants for a rental property, including identity verification and suitability checks such as references and credit history.
    Recipient: Landlords or property managers responsible for selecting tenants for the property; they may not know the applicant personally and will use the information to evaluate tenancy suitability.
    """

    model_config = ConfigDict(extra="forbid")

    tenancy_details_property_address: str = Field(
        ..., description='Rental property address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    tenancy_details_commencement_of_tenancy: str = Field(
        ..., description='Tenancy start date (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    applicant_details_phone_number: str = Field(
        ..., description='Applicant phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    applicant_details_mobile_phone: str = Field(
        ..., description='Applicant mobile phone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    applicant_details_reason_for_leaving: str = Field(
        ..., description='Reason for leaving current address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    identification_alternative_id: str = Field(
        ..., description='Alternative form of ID. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )