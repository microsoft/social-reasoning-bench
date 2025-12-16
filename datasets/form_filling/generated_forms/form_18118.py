from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicationDetails(BaseModel):
    """General application information"""

    date_received: str = Field(
        default="", description="Date the application was received by the office"
    )  # YYYY-MM-DD format


class ApplicantOrganization(BaseModel):
    """Information about the applying organization"""

    organization_name: str = Field(
        ...,
        description=(
            "Legal name of the organization applying .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing or street address of the organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Primary email address for the organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class RepresentativeInformation(BaseModel):
    """Primary representative’s personal and contact details"""

    representative_full_name: str = Field(
        ...,
        description=(
            "Full name of the representative for the organization .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    representative_address: str = Field(
        ...,
        description=(
            "Mailing or street address of the representative .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    representative_phone: str = Field(
        ...,
        description=(
            'Phone number for the representative .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    representative_email: str = Field(
        ...,
        description=(
            'Email address for the representative .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(
        ..., description="Date of birth of the representative"
    )  # YYYY-MM-DD format

    drivers_license: str = Field(
        ...,
        description=(
            "Driver’s license number of the representative .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProductsandSalesDetails(BaseModel):
    """Description of products and how they will be sold, including dates"""

    description_of_products_and_means_of_sale_line_1: str = Field(
        ...,
        description=(
            "First line describing the products and how they will be sold .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    description_of_products_and_means_of_sale_line_2: str = Field(
        default="",
        description=(
            "Second line for additional description of products and means of sale .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    description_of_products_and_means_of_sale_line_3: str = Field(
        default="",
        description=(
            "Third line for additional description of products and means of sale .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    start_date: str = Field(
        ..., description="Start date for the soliciting, peddling, or transient merchant activity"
    )  # YYYY-MM-DD format

    end_date: str = Field(
        ..., description="End date for the soliciting, peddling, or transient merchant activity"
    )  # YYYY-MM-DD format


class OtherMembersRepresentingtheOrganization(BaseModel):
    """Additional individuals representing the organization"""

    other_member_1: str = Field(
        default="",
        description=(
            "Name of the first additional member representing the organization .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_member_2: str = Field(
        default="",
        description=(
            "Name of the second additional member representing the organization .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_member_3: str = Field(
        default="",
        description=(
            "Name of the third additional member representing the organization .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_member_4: str = Field(
        default="",
        description=(
            "Name of the fourth additional member representing the organization .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SolicitorPeddlerTransientMerchantApplication(BaseModel):
    """SOLICITOR, PEDDLER,
    TRANSIENT MERCHANT
    APPLICATION"""

    application_details: ApplicationDetails = Field(..., description="Application Details")
    applicant_organization: ApplicantOrganization = Field(..., description="Applicant Organization")
    representative_information: RepresentativeInformation = Field(
        ..., description="Representative Information"
    )
    products_and_sales_details: ProductsandSalesDetails = Field(
        ..., description="Products and Sales Details"
    )
    other_members_representing_the_organization: OtherMembersRepresentingtheOrganization = Field(
        ..., description="Other Members Representing the Organization"
    )
