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
    """For internal processing and tracking of the form"""

    received: str = Field(
        default="", description="Date this form was received (for official use only)"
    )  # YYYY-MM-DD format

    new: BooleanLike = Field(
        default="", description="Indicate if this is a new agritourism profile"
    )

    update: BooleanLike = Field(
        default="", description="Indicate if this is an update to an existing agritourism profile"
    )

    new_file_yes: BooleanLike = Field(
        default="", description="Check if a new file should be created (for official use only)"
    )

    new_file_no: BooleanLike = Field(
        default="", description="Check if a new file should not be created (for official use only)"
    )

    completed: str = Field(
        default="", description="Date the form was completed/processed (for official use only)"
    )  # YYYY-MM-DD format


class ContactInfo(BaseModel):
    """Primary contact and location information for the farm/business"""

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
            "Primary contact person or persons for the business/farm .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    physical_address: str = Field(
        ...,
        description=(
            "Physical location address of the business/farm .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
            "Email address for the business or contact person .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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


class BusinessDescription(BaseModel):
    """Public-facing description of the business and/or products"""

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


class FarmFunScAgritourismSouthCarolinaAgritourismFarmProfile(BaseModel):
    """
        FARM FUN
    SC Agritourism

    SOUTH CAROLINA AGRITOURISM
    FARM PROFILE

        The SC Agritourism Program is an exciting effort established to assist consumers in locating farm experiences as well as helping farm producers plan, develop, and promote tourist attractions on their farm. From pick your own berry operations, to major consumer events, Agritourism takes on many shapes and forms throughout South Carolina. Please take a few minutes to fill out this form to update your information and return it today!
    """

    official_use_only: OfficialUseOnly = Field(..., description="Official Use Only")
    contact_info: ContactInfo = Field(..., description="Contact Info")
    business_description: BusinessDescription = Field(..., description="Business Description")
