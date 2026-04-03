from pydantic import BaseModel, ConfigDict, Field


class RequestForReviewByIndependentReviewOrganization(BaseModel):
    """REQUEST FOR A REVIEW BY AN INDEPENDENT REVIEW ORGANIZATION"""

    model_config = ConfigDict(extra="forbid")

    denied_services_description_1: str = Field(..., description='Description of denied health care services. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    denied_services_description_2: str = Field(..., description='Additional description of denied services. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    patient_info_health_plan_id: str = Field(..., description='Health plan or claim ID number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    patient_info_street: str = Field(..., description='Patient street address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    patient_info_fax: str = Field(..., description='Patient fax number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')