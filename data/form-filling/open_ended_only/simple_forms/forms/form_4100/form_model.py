from pydantic import BaseModel, ConfigDict, Field


class AdditionalInformationForm(BaseModel):
    """Additional Information"""

    model_config = ConfigDict(extra="forbid")

    contact_info_primary_telephone_number: str = Field(
        ..., description='Primary telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    contact_info_secondary_telephone_number: str = Field(
        ..., description='Secondary telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    contact_info_date_of_birth: str = Field(
        ..., description='Date of birth. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    contact_info_contact_person_address: str = Field(
        ..., description='Contact person address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    contact_info_contact_person_relationship: str = Field(
        ..., description='Contact person relationship to you. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )

    special_needs_accommodations_description: str = Field(
        ..., description='Accommodations needed. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    special_needs_other_description: str = Field(
        ..., description='Other special needs description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )

    settlement_conciliation_accept: str = Field(
        ..., description='Settlement/conciliation request. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
