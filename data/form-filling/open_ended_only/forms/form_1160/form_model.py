from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the company or organization applying for the permit"""

    company_or_organization_name: str = Field(
        ...,
        description=(
            "Full legal name of the company or organization applying .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    address: str = Field(
        ...,
        description=(
            "Mailing address of the company or organization .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    key_person_contact: str = Field(
        ...,
        description=(
            "Name of the primary contact person for this application .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    title: str = Field(
        ...,
        description=(
            "Title or position of the key contact person .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the key contact .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    fax: str = Field(
        ...,
        description=(
            "Fax number for the organization (if available) .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    e_mail: str = Field(
        ...,
        description=(
            "Email address for the key contact .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class ActivityorEventDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details about the activity or event and its location"""

    describe_the_activity_or_event_and_the_location_you_wish_to_have_permitted: str = Field(
        ...,
        description=(
            "Provide a detailed description of the activity or event and the specific "
            "location requested .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )


class AccessAreas(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Areas of DuPont State Recreational Forest to be used"""

    access_areas_to_be_used_corn_mill_shoals: BooleanLike = Field(
        ...,
        description="Check if Corn Mill Shoals will be used for the activity/event"
    )

    access_areas_to_be_used_fawn_lake: BooleanLike = Field(
        ...,
        description="Check if Fawn Lake will be used for the activity/event"
    )

    access_areas_to_be_used_guion_farm: BooleanLike = Field(
        ...,
        description="Check if Guion Farm will be used for the activity/event"
    )

    access_areas_to_be_used_high_falls: BooleanLike = Field(
        ...,
        description="Check if High Falls will be used for the activity/event"
    )

    access_areas_to_be_used_hooker_falls: BooleanLike = Field(
        ...,
        description="Check if Hooker Falls will be used for the activity/event"
    )

    access_areas_to_be_used_lake_imaging: BooleanLike = Field(
        ...,
        description="Check if Lake Imaging will be used for the activity/event"
    )


class EventTiming(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Requested dates and times for the activity or event"""

    requested_dates: str = Field(
        ...,
        description=(
            "Date or dates requested for the activity or event .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    starting_time: str = Field(
        ...,
        description=(
            "Starting time for the activity or event .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    ending_time: str = Field(
        ...,
        description=(
            "Ending time for the activity or event .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    for_continuing_activities_starting_date: str = Field(
        ...,
        description="Starting date for continuing or recurring activities"
    )  # YYYY-MM-DD format

    for_continuing_activities_ending_date: str = Field(
        ...,
        description="Ending date for continuing or recurring activities"
    )  # YYYY-MM-DD format


class ParticipantEstimates(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Estimated number of participants by group and activity type"""

    on_foot_per_group: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of users per group on foot"
    )

    on_foot_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of groups on foot"
    )

    on_foot_total_participants: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Total number of participants on foot"
    )

    on_bikes_per_group: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of users per group on bikes"
    )

    on_bikes_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of groups on bikes"
    )

    on_bikes_total_participants: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Total number of participants on bikes"
    )

    on_horseback_per_group: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of users per group on horseback"
    )

    on_horseback_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of groups on horseback"
    )

    on_horseback_total_participants: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Total number of participants on horseback"
    )

    in_vehicles_per_group: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of users per group in vehicles"
    )

    in_vehicles_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of groups in vehicles"
    )

    in_vehicles_total_participants: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Total number of participants in vehicles"
    )

    other_per_group: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of users per group for other types"
    )

    other_number_of_groups: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of groups for other types"
    )

    other_total_participants: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Total number of participants for other types"
    )


class Insurance(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Liability insurance information"""

    liability_insurance_company_name: str = Field(
        ...,
        description=(
            "Name of the liability insurance company .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )


class DupontStateRecreationalForestCommercialUsePermitApplication(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    DuPont State Recreational Forest Commercial Use Permit Application

    ''
    """

    applicant_information: ApplicantInformation = Field(
        ...,
        description="Applicant Information"
    )
    activity_or_event_details: ActivityorEventDetails = Field(
        ...,
        description="Activity or Event Details"
    )
    access_areas: AccessAreas = Field(
        ...,
        description="Access Areas"
    )
    event_timing: EventTiming = Field(
        ...,
        description="Event Timing"
    )
    participant_estimates: ParticipantEstimates = Field(
        ...,
        description="Participant Estimates"
    )
    insurance: Insurance = Field(
        ...,
        description="Insurance"
    )