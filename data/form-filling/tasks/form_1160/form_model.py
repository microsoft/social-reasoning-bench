from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OrganizationInformation(BaseModel):
    """Basic information about the company or organization applying for the permit"""

    company_or_organization_name: str = Field(
        ...,
        description=(
            "Legal name of the company or organization applying for the permit .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing address of the company or organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    key_person_contact: str = Field(
        ...,
        description=(
            'Primary contact person\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    title: str = Field(
        ...,
        description=(
            "Job title or role of the key contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the key contact or organization .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            "Fax number for the organization, if available .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            "Email address for the key contact or organization .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ActivityorEventDetails(BaseModel):
    """Description of the proposed activity or event and its location"""

    describe_the_activity_or_event_and_the_location_you_wish_to_have_permitted: str = Field(
        ...,
        description=(
            "Description of the planned activity or event and the specific location(s) "
            'requested .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class AccessAreastobeUsed(BaseModel):
    """Forest access areas that will be used for the activity or event"""

    corn_mill_shoals: BooleanLike = Field(
        default="", description="Check if the Corn Mill Shoals access area will be used"
    )

    fawn_lake: BooleanLike = Field(
        default="", description="Check if the Fawn Lake access area will be used"
    )

    guion_farm: BooleanLike = Field(
        default="", description="Check if the Guion Farm access area will be used"
    )

    high_falls: BooleanLike = Field(
        default="", description="Check if the High Falls access area will be used"
    )

    hooker_falls: BooleanLike = Field(
        default="", description="Check if the Hooker Falls access area will be used"
    )

    lake_imaging: BooleanLike = Field(
        default="", description="Check if the Lake Imaging access area will be used"
    )


class Timeframe(BaseModel):
    """Dates and times for the activity or event, including continuing activities"""

    requested_dates: str = Field(
        ...,
        description=(
            "Specific date or range of dates requested for the activity or event .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    starting_time: str = Field(
        ...,
        description=(
            "Planned start time for the activity or event .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ending_time: str = Field(
        ...,
        description=(
            "Planned end time for the activity or event .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    starting_date: str = Field(
        default="", description="Start date for continuing or recurring activities"
    )  # YYYY-MM-DD format

    ending_date: str = Field(
        default="", description="End date for continuing or recurring activities"
    )  # YYYY-MM-DD format


class Participants(BaseModel):
    """Estimated number of participants by mode of travel"""

    users_per_group_on_foot: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of on-foot users in each group"
    )

    number_of_groups_on_foot: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of on-foot groups"
    )

    total_participants_on_foot: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of on-foot participants (all groups combined)"
    )

    users_per_group_on_bikes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of bike users in each group"
    )

    number_of_groups_on_bikes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of bike groups"
    )

    total_participants_on_bikes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of bike participants (all groups combined)"
    )

    users_per_group_on_horseback: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of horseback users in each group"
    )

    number_of_groups_on_horseback: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of horseback groups"
    )

    total_participants_on_horseback: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of horseback participants (all groups combined)"
    )

    users_per_group_in_vehicles: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of vehicle users in each group"
    )

    number_of_groups_in_vehicles: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of vehicle groups"
    )

    total_participants_in_vehicles: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of vehicle participants (all groups combined)"
    )

    users_per_group_other: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of users per group for other modes not listed"
    )

    number_of_groups_other: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of groups for other modes not listed"
    )

    total_participants_other: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of participants for other modes not listed"
    )


class Insurance(BaseModel):
    """Liability insurance information for the activity or event"""

    liability_insurance_company_name: str = Field(
        ...,
        description=(
            "Name of the liability insurance company providing coverage .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class DupontStateRecreationalForestCommercialUsePermitApplication(BaseModel):
    """DuPont State Recreational Forest Commercial Use Permit Application"""

    organization_information: OrganizationInformation = Field(
        ..., description="Organization Information"
    )
    activity_or_event_details: ActivityorEventDetails = Field(
        ..., description="Activity or Event Details"
    )
    access_areas_to_be_used: AccessAreastobeUsed = Field(..., description="Access Areas to be Used")
    timeframe: Timeframe = Field(..., description="Timeframe")
    participants: Participants = Field(..., description="Participants")
    insurance: Insurance = Field(..., description="Insurance")
