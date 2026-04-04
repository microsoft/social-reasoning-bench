from pydantic import BaseModel, ConfigDict, Field


class CharityFundingApplicationForm(BaseModel):
    """Big Wheel Community Foundation Charity Funding Application Form

    Nonprofit organizations submit this application to request financial, volunteer, or other support from the Big Wheel Community Foundation. Foundation staff and internal reviewers use the details provided to log the request, evaluate eligibility and fit, and record receipt, approval, and termination decisions for office administration.
    """

    model_config = ConfigDict(extra="forbid")


    charity_registration_number: str = Field(
        ...,
        description='Charity registration number.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    website: str = Field(
        ...,
        description='Organization website.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    organization_phone_number: str = Field(
        ...,
        description='Organization phone number.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    representative_phone_number: str = Field(
        ...,
        description='Representative phone number.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


    referred_by: str = Field(
        ...,
        description='Referred by (name/organization).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    organization_purpose_description: str = Field(
        ...,
        description='Organization purpose description.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    help_needed_other: str = Field(
        ...,
        description='Other support requested.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
