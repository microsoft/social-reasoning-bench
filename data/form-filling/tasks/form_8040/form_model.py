from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PaymentDeposit(BaseModel):
    """Deposit and payment-related information"""

    check_number: str = Field(
        ...,
        description=(
            "Check number for the required $1000.00 deposit .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Applicant(BaseModel):
    """Information about the applicant submitting the permit"""

    applicant_name: str = Field(
        ...,
        description=(
            'Full legal name of the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    applicant_address: str = Field(
        ...,
        description=(
            'Mailing address of the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    applicant_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_email: str = Field(
        default="",
        description=(
            'Email address for the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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
            "Name of the contractor or party who will perform the work .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    storm_sewer_check_all_that_apply: BooleanLike = Field(
        default="", description="Indicate if the project involves work with the storm sewer"
    )

    sanitary_sewer_check_all_that_apply: BooleanLike = Field(
        ..., description="Indicate if the project involves work with the sanitary sewer"
    )

    replace_sanitary_sewer_service_line: BooleanLike = Field(
        default="",
        description="Check if the project includes replacing the sanitary sewer service line",
    )

    foundation_drain_foundation_repair: BooleanLike = Field(
        default="",
        description="Check if the project includes foundation drain work or foundation repair",
    )

    repair_sanitary_sewer_service_line: BooleanLike = Field(
        default="",
        description="Check if the project includes repairing the sanitary sewer service line",
    )

    roof_drain: BooleanLike = Field(
        default="", description="Check if the project includes work on a roof drain"
    )

    new_connection: BooleanLike = Field(
        default="", description="Check if the project involves a new sanitary sewer connection"
    )

    sump_pump: BooleanLike = Field(
        default="", description="Check if the project includes work involving a sump pump"
    )

    disconnect_sanitary_sewer_service_line: BooleanLike = Field(
        default="",
        description="Check if the project includes disconnecting the sanitary sewer service line",
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
        ..., description="Number of days within which work will start"
    )

    project_summary_line_1: str = Field(
        default="",
        description=(
            "First line of project summary; attach sketch or additional information if "
            'necessary .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    project_summary_line_2: str = Field(
        default="",
        description=(
            'Second line of project summary .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class PropertyOwner(BaseModel):
    """Contact information for the property owner"""

    property_owner_name: str = Field(
        ...,
        description=(
            'Full legal name of the property owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_address: str = Field(
        ...,
        description=(
            'Mailing address of the property owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the property owner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_email: str = Field(
        default="",
        description=(
            'Email address for the property owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class TheCityOfBlueEarthSanitarySewerConnectionPermitApplication(BaseModel):
    """
        THE CITY OF
    BLUE EARTH


    SANITARY SEWER CONNECTION
    PERMIT APPLICATION

        ''
    """

    payment__deposit: PaymentDeposit = Field(..., description="Payment / Deposit")
    applicant: Applicant = Field(..., description="Applicant")
    project: Project = Field(..., description="Project")
    property_owner: PropertyOwner = Field(..., description="Property Owner")
