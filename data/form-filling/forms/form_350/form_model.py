from pydantic import BaseModel, ConfigDict, Field


class ExemptionCertainIllegalDivisionsOfLandApp(BaseModel):
    """Exemption for Certain Illegal Divisions of Land

    Property owners or their authorized applicants submit this application to the Clear Creek County Planning Department to request an exemption that can legalize certain illegal divisions of land and establish vested property rights, with fees based on whether the property is unimproved or improved and whether it has valid county occupancy approval. County planning staff review the ownership/applicant information, parcel and legal description details, lot/acreage figures, and the stated reason for the request, and may conduct a site visit to evaluate and process the exemption decision.
    """

    model_config = ConfigDict(extra="forbid")

    exemption_type: str = Field(
        ...,
        description='Selected exemption/fee category. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )



    property_legal_description: str = Field(
        ...,
        description='Property legal description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    parcel_identification_number_pin: str = Field(
        ...,
        description='Parcel identification number (PIN). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    current_acreage_of_each: str = Field(
        ...,
        description='Current acreage of each lot. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    proposed_acreage_of_each: str = Field(
        ...,
        description='Proposed acreage of each lot. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    request_reason_description: str = Field(
        ...,
        description='Reason for request. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
