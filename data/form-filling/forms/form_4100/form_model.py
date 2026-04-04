from pydantic import BaseModel, ConfigDict, Field


class AdditionalInformationPage1(BaseModel):
    """Additional Information, Page 1

    A complainant submits this page to provide supplemental details supporting a
    discrimination complaint, including contact information, any special needs,
    desired settlement/conciliation terms, and witness information. Division
    intake, investigators, and conciliation staff use it to communicate with the
    complainant and to investigate and resolve the case; it is kept for the
    Division’s records and generally not sent to the respondent, though witness
    information may be shared as needed for the investigation.
    """

    model_config = ConfigDict(extra="forbid")

    contact_info_primary_telephone_number: str = Field(
        ...,
        description='Primary telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    contact_info_secondary_telephone_number: str = Field(
        ...,
        description='Secondary telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    contact_info_date_of_birth: str = Field(
        ...,
        description='Date of birth (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    contact_person_telephone_number: str = Field(
        ...,
        description='Contact person telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    contact_person_address: str = Field(
        ...,
        description='Contact person address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    contact_person_relationship_to_me: str = Field(
        ...,
        description='Contact person relationship to me. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    special_needs_disability_accommodations_details: str = Field(
        ...,
        description='Disability accommodations needed. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    special_needs_other_details: str = Field(
        ...,
        description='Other special needs details. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    settlement_conciliation_acceptable_terms: str = Field(
        ...,
        description='Acceptable settlement terms. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
