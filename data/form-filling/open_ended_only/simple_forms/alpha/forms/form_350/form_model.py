from pydantic import BaseModel, ConfigDict, Field


class ExemptionIllegalDivisionsOfLandApp(BaseModel):
    """Exemption for Certain Illegal Divisions of Land

    Purpose: Application to request exemption and legalization for certain illegal
    divisions of land, specifying property details and reasons for the exemption.
    Recipient: Clear Creek County Planning Department staff, who will review the
    application for compliance and process the exemption request.
    """

    model_config = ConfigDict(extra="forbid")

    exemption_type: str = Field(
        ...,
        description='Type of exemption selected (Unimproved, Improved with Valid County Occupancy Approval, Improved without Proper County Occupancy Approval). If you cannot fill this, write "N/A".'
    )
    property_legal_description: str = Field(
        ...,
        description='Legal description of property. If you cannot fill this, write "N/A".'
    )
    property_pin: str = Field(
        ...,
        description='Parcel Identification Number (PIN). If you cannot fill this, write "N/A".'
    )
    reason_for_request: str = Field(
        ...,
        description='Describe reason for request. If you cannot fill this, write "N/A".'
    )
    applicant_certification_date: str = Field(
        ...,
        description='Applicant certification date (YYYY-MM-DD). If you cannot fill this, write "N/A".'
    )