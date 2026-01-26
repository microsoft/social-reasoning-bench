from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OfficialUseOnly(BaseModel):
    """For office processing and tracking only"""

    received: str = Field(
        default="", description="Date the form was received (for official use only)"
    )  # YYYY-MM-DD format

    new: BooleanLike = Field(
        default="", description="Indicate if this is a new record (for official use only)"
    )

    update: BooleanLike = Field(
        default="",
        description="Indicate if this is an update to an existing record (for official use only)",
    )

    new_file_yes: BooleanLike = Field(
        default="", description="Check if a new file should be created (for official use only)"
    )

    new_file_no: BooleanLike = Field(
        default="", description="Check if a new file should not be created (for official use only)"
    )

    completed: str = Field(
        default="", description="Date processing of this form was completed (for official use only)"
    )  # YYYY-MM-DD format


class ContactInfo(BaseModel):
    """Primary business and contact information"""

    business_farm_name: str = Field(
        ...,
        description=(
            "Legal or commonly used name of the business or farm .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_persons: str = Field(
        ...,
        description=(
            "Primary contact person or persons for the business/farm .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    physical_address: str = Field(
        ...,
        description=(
            "Street/physical location of the business or farm .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    county_where_business_is_located: str = Field(
        ...,
        description=(
            "County in which the business or farm is physically located .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_if_different_from_above: str = Field(
        default="",
        description=(
            "Mailing address if different from the physical address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_numbers: str = Field(
        ...,
        description=(
            "Primary phone number(s) for the business or contact person .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Primary email address for the business or contact person .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    website: str = Field(
        default="",
        description=(
            'Business or farm website URL .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    facebook: str = Field(
        default="",
        description=(
            "Facebook page or profile URL or handle for the business .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    twitter: str = Field(
        default="",
        description=(
            "Twitter handle or profile URL for the business .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    brief_description_of_your_business_and_or_products: str = Field(
        ...,
        description=(
            "Short description of the business and products for listing on SCFarmFun.org "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class ContactInfo(BaseModel):
    """
    CONTACT INFO

    Please provide a brief description of your business and/or products. Please include information relevant to potential buyers/visitors. The information provided will be listed on SCFarmFun.org as a way to help promote your farm/business.
    """

    official_use_only: OfficialUseOnly = Field(..., description="Official Use Only")
    contact_info: ContactInfo = Field(..., description="Contact Info")
