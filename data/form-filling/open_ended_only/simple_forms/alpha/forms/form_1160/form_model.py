from pydantic import BaseModel, ConfigDict, Field


class DuPontStateRecForestCommercialUsePermitApp(BaseModel):
    """DuPont State Recreational Forest Commercial Use Permit Application

    Purpose: Application for organizations or companies to obtain a permit for commercial use of areas within DuPont State Recreational Forest, specifying details about the planned activity, location, participant numbers, and required insurance.
    Recipient: DuPont State Recreational Forest administrative staff or officials responsible for reviewing and approving commercial use permits for forest areas.
    """

    model_config = ConfigDict(extra="forbid")

    phone: str = Field(..., description='Contact phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    fax: str = Field(..., description='Contact fax number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    ending_time: str = Field(..., description='Ending time. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')