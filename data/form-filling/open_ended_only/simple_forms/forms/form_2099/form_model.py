from pydantic import BaseModel, ConfigDict, Field


class OmniSeqCaresFinancialSupportApplication(BaseModel):
    """OmniSeq CARES – Financial Support Application"""

    model_config = ConfigDict(extra="forbid")

    patient_info_mi: str = Field(..., description='Patient middle initial. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')

    responsible_party_mi: str = Field(..., description='Responsible party middle initial. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    responsible_party_cell_phone_number: str = Field(..., description='Responsible party cell phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')