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
    """Information about the applicant and their contact details"""

    applicant_information_date: str = Field(
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
            "Name of the organization or business associated with the applicant, if "
            'applicable .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
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

    address_full: str = Field(
        ...,
        description=(
            "Mailing street address for the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_street: str = Field(
        ...,
        description=(
            "Street portion of the applicant's mailing address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_city: str = Field(
        ...,
        description=(
            "City for the applicant's mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_state: str = Field(..., description="State for the applicant's mailing address")

    address_zip: str = Field(..., description="ZIP code for the applicant's mailing address")


class PropertyInformation(BaseModel):
    """Parcel and address information for the properties covered by this request"""

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
            "Parcel identification number for property 2, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_2_address: str = Field(
        default="",
        description=(
            "Street address for property 2, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_2_city: str = Field(
        default="",
        description=(
            'City for property 2, if applicable .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    parcel_2_zip: str = Field(default="", description="ZIP code for property 2, if applicable")

    parcel_2_township: str = Field(
        default="",
        description=(
            "Township for property 2, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_3_parcel_id: str = Field(
        default="",
        description=(
            "Parcel identification number for property 3, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_3_address: str = Field(
        default="",
        description=(
            "Street address for property 3, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_3_city: str = Field(
        default="",
        description=(
            'City for property 3, if applicable .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    parcel_3_zip: str = Field(default="", description="ZIP code for property 3, if applicable")

    parcel_3_township: str = Field(
        default="",
        description=(
            "Township for property 3, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CurrentUsesandZoning(BaseModel):
    """Current zoning, uses, and compliance/nonconforming status of the property"""

    current_zoning: str = Field(
        ...,
        description=(
            "Current zoning designation for the subject property .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    describe_current_uses_of_the_property: str = Field(
        ...,
        description=(
            "Narrative description of all current uses of the property .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    property_meets_all_development_standards_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether the property meets all development standard requirements of "
            "the current ordinance (select Yes)"
        ),
    )

    property_meets_all_development_standards_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether the property meets all development standard requirements of "
            "the current ordinance (select No)"
        ),
    )

    variance_special_use_yes: BooleanLike = Field(
        default="",
        description=(
            "Indicate Yes if the property has been granted a variance and/or special use/exception"
        ),
    )

    variance_special_use_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate No if the property has not been granted a variance and/or special "
            "use/exception"
        ),
    )

    variance_special_use_description: str = Field(
        default="",
        description=(
            "Brief description of the variance and/or special use/exception granted .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    variance_special_use_date_approved: str = Field(
        default="",
        description="Date on which the variance and/or special use/exception was approved",
    )  # YYYY-MM-DD format

    certificate_nonconforming_use_yes: BooleanLike = Field(
        default="",
        description=(
            "Indicate Yes if a Certificate of Legally Established Nonconforming Use has "
            "been issued for this property"
        ),
    )

    certificate_nonconforming_use_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate No if a Certificate of Legally Established Nonconforming Use has not "
            "been issued for this property"
        ),
    )

    certificate_nonconforming_use_in_progress: BooleanLike = Field(
        default="",
        description=(
            "Indicate In progress if an application for a Certificate of Legally "
            "Established Nonconforming Use is currently being processed"
        ),
    )

    certificate_nonconforming_use_date_approved: str = Field(
        default="",
        description=(
            "Date on which the Certificate of Legally Established Nonconforming Use was approved"
        ),
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
