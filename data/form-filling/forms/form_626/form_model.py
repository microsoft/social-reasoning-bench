from pydantic import BaseModel, ConfigDict, Field


class ConfidentialPrintAndMailServicesSubmission(BaseModel):
    """CONFIDENTIAL PRINT AND MAIL SERVICES SUBMISSION OF CONFIDENTIAL INFORMATION

    State agencies submit this form to notify IDOA Print/Mail Services and the printing
    contractor that a print/mail job includes confidential information (such as Social
    Security numbers) and to coordinate required handling instructions. The agency’s
    Account Manager, the contractor contact, and IDOA Print/Mail Services staff review
    it to confirm the job details, determine how samples/overprints/misprints must be
    handled (pickup, delivery, or destruction), and ensure compliance steps are followed
    before the job is submitted.
    """

    model_config = ConfigDict(extra="forbid")


    customer_information_contact_telephone_number: str = Field(
        ...,
        description='Primary contact phone.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    job_information_job_number: str = Field(
        ...,
        description='Job number.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    job_information_samples_overprints_misprints_pickup_by_telephone_number: str = Field(
        ...,
        description='Pickup contact phone.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    job_information_ongoing_time_frame: str = Field(
        ...,
        description='Ongoing job time frame.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    job_information_comments_additional_details: str = Field(
        ...,
        description='Comments / additional details.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )