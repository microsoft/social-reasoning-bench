from pydantic import BaseModel, ConfigDict, Field


class SubdivisionCertificateApplication2122(BaseModel):
    """Subdivision Certificate Application 21/22"""

    model_config = ConfigDict(extra="forbid")

    application_no: str = Field(..., description='Application number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    receipt_no: str = Field(..., description='Receipt number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    site_details_dp_sp: str = Field(..., description='DP/SP number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    site_details_description: str = Field(..., description='Description of subdivision certificate. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')