from pydantic import BaseModel, ConfigDict, Field


class OmniSeqCaresFinancialSupportApp(BaseModel):
    """OmniSeq CARES – Financial Support Application

    Purpose: Application for financial support or assistance with medical bills for patients invoiced by OmniSeq, Inc., assessing financial need and eligibility.
    Recipient: OmniSeq CARES financial assistance program staff who process and evaluate patient applications for financial support; they do not personally know the applicant but use the information to determine eligibility.
    """

    model_config = ConfigDict(extra="forbid")

    patient_info_mi: str = Field(..., description='Patient middle initial. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    patient_info_cell_phone: str = Field(..., description='Patient cell phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    patient_info_ordering_physician: str = Field(..., description='Ordering physician/practice. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
