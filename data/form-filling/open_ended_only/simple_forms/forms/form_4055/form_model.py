from pydantic import BaseModel, ConfigDict, Field
from typing import List


class ChainOfCustodyAnalysisRequestForm(BaseModel):
    """Chain-of-Custody / Analysis Request Form"""

    model_config = ConfigDict(extra="forbid")

    client_contact_phone: str = Field(
        ..., description='Contact phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    client_contact_reference_number: str = Field(
        ..., description='Reference number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    client_company_address_line2: str = Field(
        ..., description='Client/company address line 2. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    site_address_line2: str = Field(
        ..., description='Site address line 2. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    comments_line1: str = Field(
        ..., description='Comments line 1. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    comments_line2: str = Field(
        ..., description='Comments line 2. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    comments_line3: str = Field(
        ..., description='Comments line 3. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    requested_analysis_other_specify: str = Field(
        ..., description='Requested analysis: Other (please specify). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    submitted_relinquished_date_time: str = Field(
        ..., description='Submitted/relinquished date/time. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )