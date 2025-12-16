from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CurrentLeaseInformation(BaseModel):
    """Details about where you are living now"""

    current_address: str = Field(
        ...,
        description=(
            "Street address where you are currently living .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    current_address_from_date: str = Field(
        ..., description="Date you started living at your current address"
    )  # YYYY-MM-DD format

    current_address_to_date: str = Field(
        default="", description="Date you stopped or expect to stop living at your current address"
    )  # YYYY-MM-DD format

    current_landlords_name: str = Field(
        ...,
        description=(
            "Full name of your current landlord or property manager .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    current_monthly_rent: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Amount of rent you pay each month at your current address"
    )

    current_landlords_address: str = Field(
        default="",
        description=(
            "Mailing address of your current landlord or property manager .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    current_landlords_phone: str = Field(
        ...,
        description=(
            "Primary phone number for your current landlord or property manager .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    current_landlords_alternate_phone: str = Field(
        default="",
        description=(
            "Alternate or secondary phone number for your current landlord .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class PreviousLeaseInformation(BaseModel):
    """Details about where you were living before your current address"""

    previous_address: str = Field(
        default="",
        description=(
            "Street address where you lived immediately before your current address .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    previous_address_from_date: str = Field(
        default="", description="Date you started living at your previous address"
    )  # YYYY-MM-DD format

    previous_address_to_date: str = Field(
        default="", description="Date you stopped living at your previous address"
    )  # YYYY-MM-DD format

    previous_landlords_name: str = Field(
        default="",
        description=(
            "Full name of your previous landlord or property manager .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    previous_monthly_rent: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount of rent you paid each month at your previous address"
    )

    previous_landlords_address: str = Field(
        default="",
        description=(
            "Mailing address of your previous landlord or property manager .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    previous_landlords_phone: str = Field(
        default="",
        description=(
            "Primary phone number for your previous landlord or property manager .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    previous_landlords_alternate_phone: str = Field(
        default="",
        description=(
            "Alternate or secondary phone number for your previous landlord .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class LeaseHistory(BaseModel):
    """History of leases, evictions, and prior rentals with this company"""

    ever_broken_lease: BooleanLike = Field(
        ..., description="Indicate whether you have ever broken a lease agreement"
    )

    broken_lease_explanation_line_1: str = Field(
        default="",
        description=(
            "First line of explanation if you have broken a lease .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    broken_lease_explanation_line_2: str = Field(
        default="",
        description=(
            "Second line of explanation if you have broken a lease .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    broken_lease_explanation_line_3: str = Field(
        default="",
        description=(
            "Third line of explanation if you have broken a lease .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ever_been_evicted: BooleanLike = Field(
        ..., description="Indicate whether you have ever been evicted from a rental"
    )

    eviction_explanation_line_1: str = Field(
        default="",
        description=(
            "First line of explanation if you have been evicted .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    eviction_explanation_line_2: str = Field(
        default="",
        description=(
            "Second line of explanation if you have been evicted .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    eviction_explanation_line_3: str = Field(
        default="",
        description=(
            "Third line of explanation if you have been evicted .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    rented_from_us_before_yes: BooleanLike = Field(
        default="", description="Check if you have rented from CORE Management before"
    )

    previous_address_with_us: str = Field(
        default="",
        description=(
            "Address you previously rented from this company .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    previous_address_with_us_from_date: str = Field(
        default="", description="Date you started renting at the previous address with this company"
    )  # YYYY-MM-DD format

    previous_address_with_us_to_date: str = Field(
        default="", description="Date you stopped renting at the previous address with this company"
    )  # YYYY-MM-DD format


class CoreManagement(BaseModel):
    """
    CORE MANAGEMENT

    ''
    """

    current_lease_information: CurrentLeaseInformation = Field(
        ..., description="Current Lease Information"
    )
    previous_lease_information: PreviousLeaseInformation = Field(
        ..., description="Previous Lease Information"
    )
    lease_history: LeaseHistory = Field(..., description="Lease History")
