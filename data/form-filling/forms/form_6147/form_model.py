from pydantic import BaseModel, ConfigDict, Field


class MissouriWildlifeHobbyPermitAppCode530(BaseModel):
    """Application for Wildlife Hobby Permit (CODE 530)

    Individuals submit this application to the Missouri Department of Conservation to
    request issuance or renewal of a Wildlife Hobby Permit (Code 530), optionally
    request leg band tags, and identify the species and holding location(s) covered
    by the permit. Commercial permits staff and a conservation agent review the
    application for completeness and compliance, then approve or disapprove the
    permit and record signatures and dates.
    """

    model_config = ConfigDict(extra="forbid")


    section2_doing_business_as: str = Field(
        ...,
        description='DBA fictitious business name. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    section2_address: str = Field(
        ...,
        description='Mailing street address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    section2_telephone: str = Field(
        ...,
        description='Applicant telephone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )



    location_other_than_address_section: str = Field(
        ...,
        description='Holding location section. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    location_other_than_address_range: str = Field(
        ...,
        description='Holding location range. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    location_other_than_address_location_address: str = Field(
        ...,
        description='Holding location address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    location_other_than_address_area_acreage: str = Field(
        ...,
        description='Holding location area acreage. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    alternate_contact_directions: str = Field(
        ...,
        description='Directions to location. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    species_list: str = Field(
        ...,
        description='Species covered by permit. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

