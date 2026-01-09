from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Basic information about the applicant"""

    applicant_name: str = Field(
        ...,
        description=(
            "Full name of the scholarship applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    home_address: str = Field(
        ...,
        description=(
            "Applicant's residential mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        ...,
        description=(
            "Primary phone number for contacting the applicant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Email address for contacting the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class BusinessInformation(BaseModel):
    """Details about the applicant's business"""

    business: str = Field(
        ...,
        description=(
            "Legal or trade name of the applicant's business .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    business_address: str = Field(
        ...,
        description=(
            "Street address of the business location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    tell_us_more_about_your_business: str = Field(
        ...,
        description=(
            "Provide additional details about the business, such as products, services, "
            'history, and goals .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class MinorityOwnershipDemographic(BaseModel):
    """Minority description that best fits the ownership demographic"""

    asian: BooleanLike = Field(default="", description="Check if the business is Asian-owned")

    hispanic: BooleanLike = Field(default="", description="Check if the business is Hispanic-owned")

    woman_owned: BooleanLike = Field(default="", description="Check if the business is woman-owned")

    lgbtq: BooleanLike = Field(default="", description="Check if the business is LGBTQ-owned")

    black: BooleanLike = Field(default="", description="Check if the business is Black-owned")

    native_american: BooleanLike = Field(
        default="", description="Check if the business is Native American-owned"
    )

    veteran: BooleanLike = Field(default="", description="Check if the business is veteran-owned")

    other: BooleanLike = Field(
        default="",
        description=(
            "Check if the ownership demographic is not listed and will be described in the "
            "'If other' field"
        ),
    )

    if_other_please_explain: str = Field(
        default="",
        description=(
            "Describe the ownership demographic if 'Other' is selected .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SmallBizMinorityScholarshipApp(BaseModel):
    """
        Small Business United
    Minority-owned Small Business Scholarship Program
    APPLICATION

        ''
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    business_information: BusinessInformation = Field(..., description="Business Information")
    minority_ownership_demographic: MinorityOwnershipDemographic = Field(
        ..., description="Minority Ownership Demographic"
    )
