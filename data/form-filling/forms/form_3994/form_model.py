from pydantic import BaseModel, ConfigDict, Field


class SubdivisionCertificateApplication2122(BaseModel):
    """Subdivision Certificate Application 21/22

    Property owners or their authorised applicants submit this application to Northern Beaches Council to request a Subdivision Certificate for proposed land subdivision or related changes (e.g., Torrens/Strata/Stratum, boundary adjustment, consolidation, road/easement dedication). Council assessment staff review the site details and the requested approvals to determine whether the subdivision certificate can be issued and under what conditions.
    """

    model_config = ConfigDict(extra="forbid")





    part1_description_of_subdivision_certificate: str = Field(
        ...,
        description='What you want approved. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    part1_lots_to_be_created: str = Field(
        ...,
        description='Lots to be created. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )