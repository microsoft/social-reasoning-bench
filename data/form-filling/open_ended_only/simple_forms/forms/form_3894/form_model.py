from pydantic import BaseModel, ConfigDict, Field


class NoticeOfExemptionAppendixEForm(BaseModel):
    """Notice of Exemption Appendix E"""

    model_config = ConfigDict(extra="forbid")

    county_clerk_address: str = Field(..., description='County Clerk address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    project_location_specific: str = Field(..., description='Specific project location. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    project_description_nature_purpose_beneficiaries: str = Field(..., description='Nature, purpose, beneficiaries of project. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')