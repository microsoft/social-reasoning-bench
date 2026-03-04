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
    """Contact information for the applicant or organization"""

    date: str = Field(..., description="Date the application is completed")  # YYYY-MM-DD format

    applicant: str = Field(
        ...,
        description=(
            'Name of the applicant .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    org_business: str = Field(
        default="",
        description=(
            "Name of the organization or business, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Primary contact email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing street address of the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            "City for the applicant mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for the applicant mailing address")

    zip: str = Field(..., description="ZIP code for the applicant mailing address")


class PropertyInformation(BaseModel):
    """Parcel and address information for the property(ies) covered by this request"""

    parcel_1_id: str = Field(
        ...,
        description=(
            'Parcel ID for property 1 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    parcel_1_address: str = Field(
        ...,
        description=(
            'Street address for property 1 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    parcel_1_city: str = Field(
        ...,
        description=(
            'City for property 1 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    parcel_1_zip: str = Field(..., description="ZIP code for property 1")

    parcel_1_township: str = Field(
        ...,
        description=(
            'Township for property 1 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    parcel_2_id: str = Field(
        default="",
        description=(
            "Parcel ID for property 2 (if applicable) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_2_address: str = Field(
        default="",
        description=(
            "Street address for property 2 (if applicable) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_2_city: str = Field(
        default="",
        description=(
            'City for property 2 (if applicable) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    parcel_2_zip: str = Field(default="", description="ZIP code for property 2 (if applicable)")

    parcel_2_township: str = Field(
        default="",
        description=(
            "Township for property 2 (if applicable) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_3_id: str = Field(
        default="",
        description=(
            "Parcel ID for property 3 (if applicable) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_3_address: str = Field(
        default="",
        description=(
            "Street address for property 3 (if applicable) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_3_city: str = Field(
        default="",
        description=(
            'City for property 3 (if applicable) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    parcel_3_zip: str = Field(default="", description="ZIP code for property 3 (if applicable)")

    parcel_3_township: str = Field(
        default="",
        description=(
            "Township for property 3 (if applicable) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CurrentUsesandZoning(BaseModel):
    """Current zoning, use, and legal status of the property"""

    current_zoning: str = Field(
        ...,
        description=(
            "Current zoning designation of the property .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    describe_the_current_uses_of_the_property: str = Field(
        ...,
        description=(
            "Narrative description of the current use or uses of the property .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    property_meets_all_development_standard_requirements_yes: BooleanLike = Field(
        ...,
        description=(
            "Check if the property meets all development standard requirements of the "
            "current ordinance"
        ),
    )

    property_meets_all_development_standard_requirements_no: BooleanLike = Field(
        ...,
        description=(
            "Check if the property does not meet all development standard requirements of "
            "the current ordinance"
        ),
    )

    variance_special_use_yes: BooleanLike = Field(
        default="",
        description="Check if the property has been granted a variance and/or special use/exception",
    )

    variance_special_use_no: BooleanLike = Field(
        default="",
        description=(
            "Check if the property has not been granted a variance and/or special use/exception"
        ),
    )

    variance_special_use_description: str = Field(
        default="",
        description=(
            "Description of the variance and/or special use/exception granted .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    variance_special_use_date_approved: str = Field(
        default="", description="Approval date of the variance and/or special use/exception"
    )  # YYYY-MM-DD format

    certificate_nonconforming_yes: BooleanLike = Field(
        default="",
        description="Check if a Certificate of Legally Established Nonconforming Use has been issued",
    )

    certificate_nonconforming_no: BooleanLike = Field(
        default="",
        description=(
            "Check if a Certificate of Legally Established Nonconforming Use has not been issued"
        ),
    )

    certificate_nonconforming_in_progress: BooleanLike = Field(
        default="",
        description=(
            "Check if a Certificate of Legally Established Nonconforming Use is currently "
            "in progress"
        ),
    )

    certificate_nonconforming_date_approved: str = Field(
        default="",
        description="Approval date of the Certificate of Legally Established Nonconforming Use",
    )  # YYYY-MM-DD format


class RebuildLetterRequest(BaseModel):
    """
    REBUILD LETTER REQUEST

    If you are requesting a rebuild letter for multiple adjacent properties owned by the same person/organization list each parcel. If more than 3 parcels attach a list of the remaining parcels. The properties must all have the same zoning, and same use. Each new zone or use requires a separate application.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    property_information: PropertyInformation = Field(..., description="Property Information")
    current_uses_and_zoning: CurrentUsesandZoning = Field(
        ..., description="Current Uses and Zoning"
    )
