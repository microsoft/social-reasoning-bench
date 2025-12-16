from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
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
            "Detailed description of the planned activity or event and the specific "
            'location(s) within the forest .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
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
    """Requested dates and times for the activity or event, including continuing activities"""

    requested_dates: str = Field(
        ...,
        description=(
            "Requested calendar date or range of dates for the activity or event .If you "
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

    starting_date_for_continuing_activities: str = Field(
        default="", description="Start date for ongoing or recurring activities"
    )  # YYYY-MM-DD format

    ending_date_for_continuing_activities: str = Field(
        default="", description="End date for ongoing or recurring activities"
    )  # YYYY-MM-DD format


class Participants(BaseModel):
    """Estimated number of participants by mode of travel"""

    on_foot_users_per_group: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of participants per group who will be on foot"
    )

    on_foot_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of groups of participants who will be on foot"
    )

    on_foot_total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of participants on foot (all groups combined)"
    )

    on_bikes_users_per_group: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of participants per group who will be on bikes"
    )

    on_bikes_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of groups of participants who will be on bikes"
    )

    on_bikes_total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of participants on bikes (all groups combined)"
    )

    on_horseback_users_per_group: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of participants per group who will be on horseback"
    )

    on_horseback_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of groups of participants who will be on horseback"
    )

    on_horseback_total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of participants on horseback (all groups combined)"
    )

    in_vehicles_users_per_group: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of participants per group who will be in vehicles"
    )

    in_vehicles_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of groups of participants who will be in vehicles"
    )

    in_vehicles_total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of participants in vehicles (all groups combined)"
    )

    other_users_per_group: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of participants per group using other modes not listed above",
    )

    other_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of groups of participants using other modes not listed above",
    )

    other_total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Total number of participants using other modes (all groups combined)",
    )


class Insurance(BaseModel):
    """Liability insurance information for the event"""

    liability_insurance_company_name: str = Field(
        ...,
        description=(
            "Name of the liability insurance company providing coverage for the event .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class DupontStateRecreationalForestCommercialUsePermitApplication(BaseModel):
    """DuPont State Recreational Forest Commercial Use Permit Application"""

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    activity_or_event_details: ActivityorEventDetails = Field(
        ..., description="Activity or Event Details"
    )
    access_areas_to_be_used: AccessAreastobeUsed = Field(..., description="Access Areas to be Used")
    timeframe: Timeframe = Field(..., description="Timeframe")
    participants: Participants = Field(..., description="Participants")
    insurance: Insurance = Field(..., description="Insurance")
