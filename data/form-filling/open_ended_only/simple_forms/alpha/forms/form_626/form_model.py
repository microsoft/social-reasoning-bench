from pydantic import BaseModel, ConfigDict, Field


class ConfidentialPrintMailSubmission(BaseModel):
    """CONFIDENTIAL PRINT AND MAIL SERVICES SUBMISSION OF CONFIDENTIAL INFORMATION

    Purpose: Submission of confidential information related to print and mail services, including instructions for handling sensitive materials, to comply with state regulations and ensure proper processing by the Indiana Department of Administration.
    Recipient: Assigned Account Managers, Lora Robinson, and the Indiana Department of Administration Print/Mail Services staff, who are responsible for processing confidential print/mail jobs and ensuring compliance with state confidentiality requirements.
    """

    model_config = ConfigDict(extra="forbid")

    customer_info_contact_phone: str = Field(..., description='Contact telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    job_info_job_number: str = Field(..., description='Job number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    job_info_pickup_contact_phone: str = Field(..., description='Pickup contact telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    job_info_comments: str = Field(..., description='Comments or additional details. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')