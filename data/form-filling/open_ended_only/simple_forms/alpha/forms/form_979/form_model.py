from pydantic import BaseModel, ConfigDict, Field


class RequestForIndependentReviewOrg(BaseModel):
    """REQUEST FOR A REVIEW BY AN INDEPENDENT REVIEW ORGANIZATION

    Purpose: This form is used to request an independent review of a denial of health care services or workers' compensation benefits by an insurance company or health plan. It collects information about the denied services, the patient or injured employee, and the relationship of the requester to the case.
    Recipient: Representatives of the insurance company or health plan that denied the health care services or benefits, who will process the request and forward it for independent review as required by regulations.
    """

    model_config = ConfigDict(extra="forbid")

    todays_date_year: str = Field(..., description='Year of today\'s date. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    denied_services_description: str = Field(..., description='Description of denied health care services. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    patient_id_number: str = Field(..., description='Health plan or claim identification number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    patient_street: str = Field(..., description='Patient street address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    patient_fax: str = Field(..., description='Patient fax number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')