from pydantic import BaseModel, ConfigDict, Field


class ExemptionForCertainIllegalDivisionsOfLandForm(BaseModel):
    """Exemption for Certain Illegal Divisions of Land"""

    model_config = ConfigDict(extra="forbid")

    exemption_type: str = Field(..., description='Type of exemption selected (Unimproved, Improved with Valid County Occupancy Approval, Improved without Proper County Occupancy Approval). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    legal_description: str = Field(..., description='Legal description of property. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    parcel_identification_number: str = Field(..., description='Parcel Identification Number (PIN). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    reason_for_request: str = Field(..., description='Describe reason for request. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')