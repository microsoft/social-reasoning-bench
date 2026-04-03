from typing import Literal, Optional, List, Union
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
            "Primary phone number for the key contact person or organization .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
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
            "Email address for the key contact person or organization .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ActivityorEventDetails(BaseModel):
    """Description of the proposed activity or event and its location"""

    describe_the_activity_or_event_and_the_location_you_wish_to_have_permitted: str = Field(
        ...,
        description=(
            "Detailed description of the planned activity or event and the specific "
            'location within the forest .If you cannot fill this, write "N/A". If this '
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


class EstimatedNumberofParticipants(BaseModel):
    """Estimated number of users and groups by mode of travel"""

    on_foot_users_per_group: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Average number of on-foot participants in each group"
    )

    on_foot_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of on-foot groups participating"
    )

    on_foot_total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of on-foot participants (all groups combined)"
    )

    on_bikes_users_per_group: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Average number of biking participants in each group"
    )

    on_bikes_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of biking groups participating"
    )

    on_bikes_total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of biking participants (all groups combined)"
    )

    on_horseback_users_per_group: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Average number of horseback participants in each group"
    )

    on_horseback_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of horseback groups participating"
    )

    on_horseback_total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of horseback participants (all groups combined)"
    )

    in_vehicles_users_per_group: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Average number of vehicle occupants in each group"
    )

    in_vehicles_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of vehicle groups participating"
    )

    in_vehicles_total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of participants in vehicles (all groups combined)"
    )

    other_users_per_group: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Average number of participants per group for other modes not listed",
    )

    other_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of groups for other modes not listed"
    )

    other_total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of participants for other modes not listed"
    )


class LiabilityInsurance(BaseModel):
    """Liability insurance information for the activity or event"""

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
    estimated_number_of_participants: EstimatedNumberofParticipants = Field(
        ..., description="Estimated Number of Participants"
    )
    liability_insurance: LiabilityInsurance = Field(..., description="Liability Insurance")
