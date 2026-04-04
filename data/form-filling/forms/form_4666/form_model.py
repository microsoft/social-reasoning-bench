from pydantic import BaseModel, ConfigDict, Field


class OregonDeathCertWorksheetFuneralHomes(BaseModel):
    """OREGON DEATH CERTIFICATE WORKSHEET FOR FUNERAL HOMES

    Funeral home staff use this worksheet to capture the informant’s and funeral director’s
    attestations and to document whether the decedent was a veteran who served in specific
    U.S. Department of Veterans Affairs–defined combat zones (or other locations). The
    funeral director uses the information to complete and file the death certificate, and
    state vital records personnel review it to register the certificate and ensure veteran/
    combat-zone details are recorded correctly.
    """

    model_config = ConfigDict(extra="forbid")




    combat_zone_other_locations: str = Field(
        ...,
        description='Other combat-zone locations served. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )