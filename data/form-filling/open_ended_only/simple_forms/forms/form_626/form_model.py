from pydantic import BaseModel, ConfigDict, Field


class ConfidentialPrintAndMailServicesSubmissionOfConfidentialInformation(BaseModel):
    """CONFIDENTIAL PRINT AND MAIL SERVICES SUBMISSION OF CONFIDENTIAL INFORMATION"""

    model_config = ConfigDict(extra="forbid")

    customer_info_name_of_agency: str = Field(
        ..., description='Agency name. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    customer_info_agency_number: str = Field(
        ..., description='Agency number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    customer_info_name_of_department: str = Field(
        ..., description='Department name. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    customer_info_name_of_contact: str = Field(
        ..., description='Contact name. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    customer_info_contact_telephone_number: str = Field(
        ..., description='Contact telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    customer_info_contact_email_address: str = Field(
        ..., description='Contact e-mail address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    job_info_job_number: str = Field(
        ..., description='Job number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    job_info_pickup: bool | None = Field(
        ..., description='Should items be picked up?'
    )
    job_info_pickup_by_name_of_contact: str = Field(
        ..., description='Pickup contact name (if different). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    job_info_pickup_by_telephone_number: str = Field(
        ..., description='Pickup contact telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    job_info_pickup_by_email_address: str = Field(
        ..., description='Pickup contact e-mail address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    job_info_deliver: bool | None = Field(
        ..., description='Should items be delivered?'
    )
    job_info_deliver_to: str = Field(
        ..., description='Delivery address/location. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    job_info_destroy: bool | None = Field(
        ..., description='Should items be destroyed?'
    )
    job_info_print_job_one_time: bool | None = Field(
        ..., description='Is print job one time?'
    )
    job_info_print_job_ongoing: bool | None = Field(
        ..., description='Is print job ongoing?'
    )
    job_info_ongoing_time_frame: str = Field(
        ..., description='Ongoing job time frame. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    job_info_comments_additional_details: str = Field(
        ..., description='Comments or additional details. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )