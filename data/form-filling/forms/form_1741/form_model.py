from pydantic import BaseModel, ConfigDict, Field


class PreTenancyApplicationForm(BaseModel):
    """TenancyServices Pre-tenancy application form

    Prospective tenants submit this form to apply to rent a specific property. The landlord, property manager, or tenancy
    services staff review the applicant’s personal details, identification, and rental history to assess suitability and
    to decide whether to proceed, including conducting credit and reference checks where permitted.
    """

    model_config = ConfigDict(extra="forbid")

    tenancy_details_property_address: str = Field(
        ...,
        description='Property address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    tenancy_details_commencement_of_tenancy: str = Field(
        ...,
        description='Tenancy start date (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    applicant_details_date_of_birth: str = Field(
        ...,
        description='Date of birth (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    applicant_details_phone_number: str = Field(
        ...,
        description='Phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    applicant_details_reason_for_leaving: str = Field(
        ...,
        description='Reason for leaving current address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    identification_drivers_licence_version_no: str = Field(
        ...,
        description='Driver licence version number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
