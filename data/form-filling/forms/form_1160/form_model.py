from pydantic import BaseModel, ConfigDict, Field


class DuPontStateRecreationalForestCommercialUsePermitApplication(BaseModel):
    """DuPont State Recreational Forest Commercial Use Permit Application

    Companies or organizations submit this application to request permission for a commercial,
    organized activity or event within DuPont State Recreational Forest. DuPont State Recreational
    Forest / North Carolina Forest Service staff review the requested locations, dates/times,
    participant counts, and required insurance/medical documentation to decide whether to approve
    the permit and under what conditions.
    """

    model_config = ConfigDict(extra="forbid")

    phone: str = Field(
        ...,
        description='Contact phone number.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    fax: str = Field(
        ...,
        description='Fax number.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    activity_event_description_location: str = Field(
        ...,
        description='Activity/event and location description.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


    starting_time: str = Field(
        ...,
        description='Starting time.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    ending_time: str = Field(
        ...,
        description='Ending time.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    participants_on_bikes_total_participants: float | None = Field(..., description="On bikes total participants")
