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
    """For office processing and file tracking"""

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
    """Primary business and contact information for the farm"""

    business_farm_name: str = Field(
        ...,
        description=(
            'Official name of the business or farm .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_persons: str = Field(
        ...,
        description=(
            "Primary contact person or persons for this business/farm .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    physical_address: str = Field(
        ...,
        description=(
            "Street address where the business/farm is physically located .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    county_where_business_is_located: str = Field(
        ...,
        description=(
            "Name of the South Carolina county where the business is located .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    mailing_address_if_different_from_above: str = Field(
        default="",
        description=(
            "Mailing address if it differs from the physical address .If you cannot fill "
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
            'Website URL for the business or farm .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    facebook: str = Field(
        default="",
        description=(
            "Facebook page or profile URL/handle for the business .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    twitter: str = Field(
        default="",
        description=(
            "Twitter (X) handle or profile URL for the business .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    brief_description_of_your_business_and_or_products: str = Field(
        ...,
        description=(
            "Short description of the business, products, and information relevant to "
            "potential buyers or visitors; will be listed on SCFarmFun.org .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class SouthCarolinaAgritourismFarmProfile(BaseModel):
    """
        SOUTH CAROLINA AGRITOURISM
    FARM PROFILE

        The SC Agritourism Program is an exciting effort established to assist consumers in locating farm experiences as well as helping farm producers plan, develop, and promote tourist attractions on their farm. From pick your own berry operations, to major consumer events, Agritourism takes on many shapes and forms throughout South Carolina. Please take a few minutes to fill out this form to update your information and return it today!
    """

    official_use_only: OfficialUseOnly = Field(..., description="Official Use Only")
    contact_info: ContactInfo = Field(..., description="Contact Info")
