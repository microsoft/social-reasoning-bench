from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Contact and mailing information for the applicant"""

    date: str = Field(
        ..., description="Date the rebuild letter request application is completed"
    )  # YYYY-MM-DD format

    applicant: str = Field(
        ...,
        description=(
            "Name of the applicant requesting the rebuild letter .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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
            "Primary phone number for the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Email address for the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Mailing address for the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_line: str = Field(
        ...,
        description=(
            'Street address line for the applicant .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            "City for the applicant's mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for the applicant's mailing address")

    zip: str = Field(..., description="ZIP code for the applicant's mailing address")


class PropertyInformation(BaseModel):
    """Parcel and location details for up to three properties"""

    parcel_1_parcel_id: str = Field(
        ...,
        description=(
            "Parcel identification number for property 1 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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

    parcel_2_parcel_id: str = Field(
        default="",
        description=(
            "Parcel identification number for property 2 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_2_address: str = Field(
        default="",
        description=(
            'Street address for property 2 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    parcel_2_city: str = Field(
        default="",
        description=(
            'City for property 2 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    parcel_2_zip: str = Field(default="", description="ZIP code for property 2")

    parcel_2_township: str = Field(
        default="",
        description=(
            'Township for property 2 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    parcel_3_parcel_id: str = Field(
        default="",
        description=(
            "Parcel identification number for property 3 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_3_address: str = Field(
        default="",
        description=(
            'Street address for property 3 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    parcel_3_city: str = Field(
        default="",
        description=(
            'City for property 3 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    parcel_3_zip: str = Field(default="", description="ZIP code for property 3")

    parcel_3_township: str = Field(
        default="",
        description=(
            'Township for property 3 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class CurrentUses(BaseModel):
    """Zoning, current use, and compliance/nonconforming status of the property"""

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
            "Describe how the property is currently being used .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    property_meets_all_development_standard_requirements_of_current_ordinance_yes: BooleanLike = (
        Field(
            ...,
            description=(
                "Check if the property meets all development standard requirements of the "
                "current ordinance"
            ),
        )
    )

    property_meets_all_development_standard_requirements_of_current_ordinance_no: BooleanLike = (
        Field(
            ...,
            description=(
                "Check if the property does not meet all development standard requirements of "
                "the current ordinance"
            ),
        )
    )

    has_the_property_been_granted_a_variance_and_or_special_use_exception_yes: BooleanLike = Field(
        default="",
        description="Check if the property has been granted a variance and/or special use/exception",
    )

    has_the_property_been_granted_a_variance_and_or_special_use_exception_no: BooleanLike = Field(
        default="",
        description=(
            "Check if the property has not been granted a variance and/or special use/exception"
        ),
    )

    if_yes_describe_variance_and_or_special_use_exception: str = Field(
        default="",
        description=(
            "Describe the variance and/or special use/exception granted to the property .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    variance_special_use_exception_date_approved: str = Field(
        default="", description="Date the variance and/or special use/exception was approved"
    )  # YYYY-MM-DD format

    has_a_certificate_of_legally_established_nonconforming_use_been_issued_for_this_property_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if a Certificate of Legally Established Nonconforming Use has been "
            "issued for this property"
        ),
    )

    has_a_certificate_of_legally_established_nonconforming_use_been_issued_for_this_property_no: BooleanLike = Field(
        default="",
        description=(
            "Check if a Certificate of Legally Established Nonconforming Use has not been "
            "issued for this property"
        ),
    )

    has_a_certificate_of_legally_established_nonconforming_use_been_issued_for_this_property_in_progress: BooleanLike = Field(
        default="",
        description=(
            "Check if a Certificate of Legally Established Nonconforming Use is currently "
            "in progress for this property"
        ),
    )

    certificate_of_legally_established_nonconforming_use_date_approved: str = Field(
        default="",
        description="Date the Certificate of Legally Established Nonconforming Use was approved",
    )  # YYYY-MM-DD format


class RebuildLetterRequest(BaseModel):
    """
    REBUILD LETTER REQUEST

    ''
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    property_information: PropertyInformation = Field(..., description="Property Information")
    current_uses: CurrentUses = Field(..., description="Current Use(s)")
