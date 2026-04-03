from pydantic import BaseModel, ConfigDict, Field


class NoticeOfExemption(BaseModel):
    """Notice of Exemption

    Purpose: This form is used to notify government agencies of a project's exemption from environmental review requirements under the California Environmental Quality Act (CEQA). It documents the basis for exemption and provides project details for official records.
    Recipient: State and county government officials, specifically the Office of Planning and Research and the County Clerk, who are responsible for processing and recording environmental compliance documents.
    """

    model_config = ConfigDict(extra="forbid")

    project_location_specific: str = Field(..., description='Specific project location. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    project_description: str = Field(..., description='Nature, purpose, and beneficiaries of project. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    contact_person: str = Field(..., description='Contact person name. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')