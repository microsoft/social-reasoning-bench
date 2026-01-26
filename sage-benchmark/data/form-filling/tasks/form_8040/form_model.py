from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PaymentFees(BaseModel):
    """Deposit and connection fee payment details"""

    check_number: str = Field(
        ...,
        description=(
            "Check number for the required $1000.00 deposit .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Applicant(BaseModel):
    """Information about the applicant submitting the permit application"""

    applicant_name: str = Field(
        ...,
        description=(
            'Applicant\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    applicant_address: str = Field(
        ...,
        description=(
            'Applicant\'s mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    applicant_phone: str = Field(
        ...,
        description=(
            'Applicant\'s primary phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    applicant_email: str = Field(
        default="",
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    nature_of_work: str = Field(
        ...,
        description=(
            "Brief description of the nature of the work to be performed .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class Project(BaseModel):
    """Details about the project and work to be performed"""

    name_of_party_performing_work: str = Field(
        ...,
        description=(
            "Name of the contractor or party performing the work .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    storm_sewer: BooleanLike = Field(
        default="", description="Check if the project involves work with the storm sewer"
    )

    sanitary_sewer: BooleanLike = Field(
        default="", description="Check if the project involves work with the sanitary sewer"
    )

    replace_sanitary_sewer_service_line: BooleanLike = Field(
        default="", description="Check if the project will replace the sanitary sewer service line"
    )

    foundation_drain_foundation_repair: BooleanLike = Field(
        default="",
        description="Check if the project involves a foundation drain or foundation repair",
    )

    repair_sanitary_sewer_service_line: BooleanLike = Field(
        default="", description="Check if the project will repair the sanitary sewer service line"
    )

    roof_drain: BooleanLike = Field(
        default="", description="Check if the project involves a roof drain"
    )

    new_connection: BooleanLike = Field(
        default="", description="Check if the project is for a new sanitary sewer connection"
    )

    sump_pump: BooleanLike = Field(
        default="", description="Check if the project involves a sump pump"
    )

    disconnect_sanitary_sewer_service_line: BooleanLike = Field(
        default="",
        description="Check if the project will disconnect the sanitary sewer service line",
    )

    other: str = Field(
        default="",
        description=(
            "Describe other types of work not listed above .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    work_to_start_within_days: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of days within which work will start"
    )

    project_summary_line_1: str = Field(
        default="",
        description=(
            'First line of brief project summary .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    project_summary_line_2: str = Field(
        default="",
        description=(
            'Second line of brief project summary .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class PropertyOwner(BaseModel):
    """Contact information for the property owner"""

    property_owner_name: str = Field(
        ...,
        description=(
            'Property owner\'s full name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    property_owner_address: str = Field(
        ...,
        description=(
            'Property owner\'s mailing address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_phone: str = Field(
        ...,
        description=(
            'Property owner\'s primary phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_email: str = Field(
        default="",
        description=(
            'Property owner\'s email address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class SanitarySewerConnectionPermitApplication(BaseModel):
    """
        SANITARY SEWER CONNECTION
    PERMIT APPLICATION

        Deposit of $1000.00 required and will be returned upon inspection.
    """

    payment__fees: PaymentFees = Field(..., description="Payment / Fees")
    applicant: Applicant = Field(..., description="Applicant")
    project: Project = Field(..., description="Project")
    property_owner: PropertyOwner = Field(..., description="Property Owner")
