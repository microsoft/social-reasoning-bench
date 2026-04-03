from pydantic import BaseModel, ConfigDict, Field


class NoticeOfDeterminationAppendixD(BaseModel):
    """Notice of Determination Appendix D"""

    model_config = ConfigDict(extra="forbid")




    project_applicant: str = Field(..., description='Project applicant. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    project_location: str = Field(..., description='Project location (include county). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    project_description: str = Field(..., description='Project description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')

