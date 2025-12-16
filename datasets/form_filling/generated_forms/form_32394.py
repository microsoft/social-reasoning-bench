from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


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

    property_owner_email: str = Field(
        ...,
        description=(
            'Email address of the property owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_mailing_address: str = Field(
        ...,
        description=(
            "Mailing street address of the property owner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_city: str = Field(
        ...,
        description=(
            "City for the property owner's mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_state: str = Field(
        ..., description="State for the property owner's mailing address"
    )

    property_owner_zip_code: str = Field(
        ..., description="ZIP code for the property owner's mailing address"
    )

    property_owner_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the property owner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ForesterIfApplicable(BaseModel):
    """Contact information for the forester responsible for the project"""

    forester_name: str = Field(
        default="",
        description=(
            "Full name of the forester, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    forester_email: str = Field(
        default="",
        description=(
            "Email address of the forester, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    forester_mailing_address: str = Field(
        default="",
        description=(
            "Mailing street address of the forester, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    forester_city: str = Field(
        default="",
        description=(
            "City for the forester's mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    forester_state: str = Field(default="", description="State for the forester's mailing address")

    forester_zip_code: str = Field(
        default="", description="ZIP code for the forester's mailing address"
    )

    forester_phone: str = Field(
        default="",
        description=(
            'Primary phone number for the forester .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class Logger(BaseModel):
    """Contact information for the logger"""

    logger_name: str = Field(
        ...,
        description=(
            'Full name of the logger .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    logger_email: str = Field(
        ...,
        description=(
            'Email address of the logger .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    logger_mailing_address: str = Field(
        ...,
        description=(
            'Mailing street address of the logger .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    logger_city: str = Field(
        ...,
        description=(
            'City for the logger\'s mailing address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    logger_state: str = Field(..., description="State for the logger's mailing address")

    logger_zip_code: str = Field(..., description="ZIP code for the logger's mailing address")

    logger_phone: str = Field(
        ...,
        description=(
            'Primary phone number for the logger .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ProjectLocation(BaseModel):
    """Location details and current development status of the property"""

    project_location_ticonderoga: BooleanLike = Field(
        default="", description="Check if the project location is in Ticonderoga"
    )

    project_location_dresden: BooleanLike = Field(
        default="", description="Check if the project location is in Dresden"
    )

    project_location_section: str = Field(
        default="",
        description=(
            "Tax map section number for the project location .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    project_location_block: str = Field(
        default="",
        description=(
            "Tax map block number for the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    project_location_lot: str = Field(
        default="",
        description=(
            "Tax map lot number for the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    project_location_hague: BooleanLike = Field(
        default="", description="Check if the project location is in Hague"
    )

    project_location_fort_ann: BooleanLike = Field(
        default="", description="Check if the project location is in Fort Ann"
    )

    project_location_putnam: BooleanLike = Field(
        default="", description="Check if the project location is in Putnam"
    )

    project_location_street_address: str = Field(
        ...,
        description=(
            "Street address of the project location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    property_is_presently_undeveloped: BooleanLike = Field(
        default="", description="Check if the property is currently undeveloped"
    )

    property_is_presently_partially_developed: BooleanLike = Field(
        default="", description="Check if the property is currently partially developed"
    )

    property_is_presently_developed_occupied: BooleanLike = Field(
        default="", description="Check if the property is currently developed and occupied"
    )


class ForestManagementOperations(BaseModel):
    """Objectives, best practices, and schedule for the logging operations"""

    forest_management_objective: str = Field(
        ...,
        description=(
            "Describe the primary objectives of the forest management activities .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    best_management_practices_to_be_utilized_onsite_to_protect_water_quality: str = Field(
        ...,
        description=(
            "List and describe best management practices that will be used onsite to "
            'protect water quality .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    schedule_for_road_building_and_harvesting_operations: str = Field(
        ...,
        description=(
            "Provide the planned schedule and timing for road building and harvesting "
            'operations .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class LoggingInTheLakeGeorgeParkNoticeOfIntentSoilConservationPlanForm(BaseModel):
    """
        LOGGING IN THE LAKE GEORGE PARK
    NOTICE OF INTENT / SOIL CONSERVATION PLAN FORM

        Certain Silviculture Activities are exempt from Stormwater Management and Stream Corridor regulations. To qualify for exemption, submit this completed form and a site plan to the Lake George Park Commission* 15 days prior to undertaking land disturbance in furtherance of silvicultural activity.
    """

    property_owner: PropertyOwner = Field(..., description="Property Owner")
    forester_if_applicable: ForesterIfApplicable = Field(
        ..., description="Forester (If Applicable)"
    )
    logger: Logger = Field(..., description="Logger")
    project_location: ProjectLocation = Field(..., description="Project Location")
    forest_management__operations: ForestManagementOperations = Field(
        ..., description="Forest Management & Operations"
    )
