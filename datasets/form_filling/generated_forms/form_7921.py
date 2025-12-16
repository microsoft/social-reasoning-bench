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

    applicant: str = Field(
        ...,
        description=(
            "Name of the applicant requesting the rebuild letter .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Date the rebuild letter request application is completed"
    )  # YYYY-MM-DD format

    org_business: str = Field(
        default="",
        description=(
            "Organization or business name associated with the applicant, if applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the applicant or organization .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Email address for the applicant or organization .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing address of the applicant or organization, including street, city, "
            'state, and zip .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class PropertyInformation(BaseModel):
    """Parcel and location details for each property"""

    parcel_id_1: str = Field(
        ...,
        description=(
            "Parcel identification number for property 1 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_1: str = Field(
        ...,
        description=(
            'Street address for property 1 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city_1: str = Field(
        ...,
        description=(
            'City for property 1 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    zip_1: str = Field(..., description="Zip code for property 1")

    township_1: str = Field(
        ...,
        description=(
            'Township for property 1 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    parcel_id_2: str = Field(
        default="",
        description=(
            "Parcel identification number for property 2, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_2: str = Field(
        default="",
        description=(
            "Street address for property 2, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_2: str = Field(
        default="",
        description=(
            'City for property 2, if applicable .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zip_2: str = Field(default="", description="Zip code for property 2, if applicable")

    township_2: str = Field(
        default="",
        description=(
            "Township for property 2, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_id_3: str = Field(
        default="",
        description=(
            "Parcel identification number for property 3, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_3: str = Field(
        default="",
        description=(
            "Street address for property 3, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_3: str = Field(
        default="",
        description=(
            'City for property 3, if applicable .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zip_3: str = Field(default="", description="Zip code for property 3, if applicable")

    township_3: str = Field(
        default="",
        description=(
            "Township for property 3, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CurrentUses(BaseModel):
    """Current zoning, use, and legal status of the property"""

    current_zoning: str = Field(
        ...,
        description=(
            "Current zoning designation for the subject property .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    describe_the_current_uses_of_the_property: str = Field(
        ...,
        description=(
            "Narrative description of how the property is currently being used .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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
        ...,
        description=(
            "Indicate Yes if the property has been granted a variance and/or special use/exception"
        ),
    )

    has_the_property_been_granted_a_variance_and_or_special_use_exception_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate No if the property has not been granted a variance and/or special "
            "use/exception"
        ),
    )

    if_yes_describe_variance_special_use_exception_line_1: str = Field(
        default="",
        description=(
            "First line of description of the variance and/or special use/exception, if "
            'applicable .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    if_yes_describe_variance_special_use_exception_line_2: str = Field(
        default="",
        description=(
            "Second line of description of the variance and/or special use/exception, if "
            'needed .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    if_yes_describe_variance_special_use_exception_line_3: str = Field(
        default="",
        description=(
            "Third line of description of the variance and/or special use/exception, if "
            'needed .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    date_approved_variance_special_use_exception: str = Field(
        default="",
        description="Approval date of the variance and/or special use/exception, if applicable",
    )  # YYYY-MM-DD format

    has_a_certificate_of_legally_established_nonconforming_use_been_issued_for_this_property_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate Yes if a Certificate of Legally Established Nonconforming Use has "
            "been issued for this property"
        ),
    )

    has_a_certificate_of_legally_established_nonconforming_use_been_issued_for_this_property_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate No if a Certificate of Legally Established Nonconforming Use has not "
            "been issued for this property"
        ),
    )

    has_a_certificate_of_legally_established_nonconforming_use_been_issued_for_this_property_in_progress: BooleanLike = Field(
        ...,
        description=(
            "Indicate In progress if a Certificate of Legally Established Nonconforming Use "
            "is currently being processed"
        ),
    )

    date_approved_certificate_of_legally_established_nonconforming_use: str = Field(
        default="",
        description=(
            "Approval date of the Certificate of Legally Established Nonconforming Use, if "
            "applicable"
        ),
    )  # YYYY-MM-DD format


class RebuildLetterRequest(BaseModel):
    """
    REBUILD LETTER REQUEST

    If you are requesting a rebuild letter for multiple adjacent properties owned by the same person/organization list each parcel. If more than 3 parcels attach a list of the remaining parcels. The properties must all have the same zoning, and same use. Each new zone or use requires a separate application.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    property_information: PropertyInformation = Field(..., description="Property Information")
    current_uses: CurrentUses = Field(..., description="Current Uses")
