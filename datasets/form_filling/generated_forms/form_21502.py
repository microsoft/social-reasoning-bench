from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PermitCoordinatorInformation(BaseModel):
    """Basic permit details and primary special effects coordinator information"""

    permit_number: str = Field(
        ...,
        description=(
            "Film permit number assigned to this application .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    permit_date: str = Field(
        ..., description="Date the worksheet is completed"
    )  # YYYY-MM-DD format

    special_effects_coordinator: str = Field(
        ...,
        description=(
            "Full name of the special effects coordinator .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    special_effects_coordinator_license_number: str = Field(
        ...,
        description=(
            "License number of the special effects coordinator .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    company: str = Field(
        ...,
        description=(
            'Name of the production company .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    telephone_number: str = Field(
        ...,
        description=(
            "Primary contact telephone number for the company or coordinator .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing or business address of the company or coordinator .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    locations: str = Field(
        ...,
        description=(
            "Filming location or locations where special effects will be used .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Assistants(BaseModel):
    """Assistant pyrotechnicians and their license numbers"""

    assistant_1_name: str = Field(
        default="",
        description=(
            "Name of first assistant or pyrotechnician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    assistant_1_license_number: str = Field(
        default="",
        description=(
            "License number for the first assistant or pyrotechnician .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    assistant_2_name: str = Field(
        default="",
        description=(
            "Name of second assistant or pyrotechnician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    assistant_2_license_number: str = Field(
        default="",
        description=(
            "License number for the second assistant or pyrotechnician .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ActivityDetails(BaseModel):
    """Details of the special effects activity and materials used"""

    activity_special_fx_materials: str = Field(
        ...,
        description=(
            "Describe the planned activities and list all special effects materials with "
            'quantities to be used .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    dates_of_activity: str = Field(
        ...,
        description=(
            "Date or range of dates when the special effects activity will occur .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    times_of_activity: str = Field(
        ...,
        description=(
            "Time or time range when the special effects activity will occur .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class Signatures(BaseModel):
    """Signatures and dates for coordinator and production company"""

    sfx_coord_signature: str = Field(
        ...,
        description=(
            "Signature of the special effects coordinator .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    sfx_coord_signature_date: str = Field(
        ..., description="Date the special effects coordinator signed"
    )  # YYYY-MM-DD format

    production_co_signature: str = Field(
        ...,
        description=(
            "Signature of the production company representative .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    production_co_signature_date: str = Field(
        ..., description="Date the production company representative signed"
    )  # YYYY-MM-DD format


class ForSBCFCUseOnly(BaseModel):
    """Internal fire and sheriff approval information"""

    fire_approval_initial: str = Field(
        default="",
        description=(
            "Initials of fire department representative granting approval .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    fire_approval_date: str = Field(
        default="", description="Date of fire department approval"
    )  # YYYY-MM-DD format

    fire_approval_by: str = Field(
        default="",
        description=(
            "Printed name of the fire department representative granting approval .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    sheriff_approval_initial: str = Field(
        default="",
        description=(
            "Initials of sheriff's department representative granting approval .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    sheriff_approval_date: str = Field(
        default="", description="Date of sheriff's department approval"
    )  # YYYY-MM-DD format

    sheriff_approval_by: str = Field(
        default="",
        description=(
            "Printed name of the sheriff's department representative granting approval .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SanBernardinoFilmOfficeEffectsAndHazardsWorksheet(BaseModel):
    """
        SAN BERNARDINO COUNTY
    Film Office

    Special Effects and Hazardous Conditions Worksheet

        This form and a copy of your State Pyrotechnics license(s) are required before a permit can be issued.
    """

    permit__coordinator_information: PermitCoordinatorInformation = Field(
        ..., description="Permit & Coordinator Information"
    )
    assistants: Assistants = Field(..., description="Assistants")
    activity_details: ActivityDetails = Field(..., description="Activity Details")
    signatures: Signatures = Field(..., description="Signatures")
    for_sbcfc_use_only: ForSBCFCUseOnly = Field(..., description="For SBCFC Use Only")
