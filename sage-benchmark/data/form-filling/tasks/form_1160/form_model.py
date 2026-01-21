from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class UsersNumberTotalRow(BaseModel):
    """Single row in Users Number Total"""

    mode: str = Field(default="", description="Mode")
    users: str = Field(default="", description="Users")
    per_group: str = Field(default="", description="Per_Group")
    number_of_groups: str = Field(default="", description="Number_Of_Groups")
    total_participants: str = Field(default="", description="Total_Participants")


class ApplicantInformation(BaseModel):
    """Company and primary contact details for the permit applicant"""

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


class ActivityorEventDescription(BaseModel):
    """Description of the proposed activity or event and its location"""

    describe_the_activity_or_event_and_the_location_you_wish_to_have_permitted: str = Field(
        ...,
        description=(
            "Description of the planned activity or event and the specific locations within "
            'the forest to be used .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class AccessAreastobeUsed(BaseModel):
    """Forest access areas requested for this activity or event"""

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
            "Requested date or range of dates for the activity or event .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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


class ParticipantsandGroupBreakdown(BaseModel):
    """Estimated number of participants by mode of travel and group structure"""

    users_number_total: List[UsersNumberTotalRow] = Field(
        ...,
        description=(
            "Table summarizing estimated number of users, group sizes, number of groups, "
            "and total participants by mode of travel"
        ),
    )  # List of table rows

    per_group: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Typical number of users per group for the specified mode of travel"
    )

    number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of groups for the specified mode of travel"
    )

    total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of participants for the specified mode of travel"
    )

    on_foot_users: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of users on foot"
    )

    on_foot_per_group: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Typical group size for users on foot"
    )

    on_foot_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of groups on foot"
    )

    on_foot_total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of participants on foot"
    )

    on_bikes_users: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of users on bikes"
    )

    on_bikes_per_group: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Typical group size for users on bikes"
    )

    on_bikes_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of groups on bikes"
    )

    on_bikes_total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of participants on bikes"
    )

    on_horseback_users: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of users on horseback"
    )

    on_horseback_per_group: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Typical group size for users on horseback"
    )

    on_horseback_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of groups on horseback"
    )

    on_horseback_total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of participants on horseback"
    )

    in_vehicles_users: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of users in vehicles"
    )

    in_vehicles_per_group: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Typical group size for users in vehicles"
    )

    in_vehicles_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of groups in vehicles"
    )

    in_vehicles_total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of participants in vehicles"
    )

    other_users: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of users in other modes not listed"
    )

    other_per_group: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Typical group size for users in other modes not listed"
    )

    other_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of groups in other modes not listed"
    )

    other_total_participants: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of participants in other modes not listed"
    )


class InsuranceInformation(BaseModel):
    """Liability insurance details for the event"""

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
    activity_or_event_description: ActivityorEventDescription = Field(
        ..., description="Activity or Event Description"
    )
    access_areas_to_be_used: AccessAreastobeUsed = Field(..., description="Access Areas to be Used")
    timeframe: Timeframe = Field(..., description="Timeframe")
    participants_and_group_breakdown: ParticipantsandGroupBreakdown = Field(
        ..., description="Participants and Group Breakdown"
    )
    insurance_information: InsuranceInformation = Field(..., description="Insurance Information")
