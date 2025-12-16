from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EventClientInformation(BaseModel):
    """Basic details about the event and the organizing client"""

    event_date: str = Field(
        ..., description="Date on which the event will take place"
    )  # YYYY-MM-DD format

    event_name: str = Field(
        ...,
        description=(
            'Title or name of the event .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    organization_client_name: str = Field(
        ...,
        description=(
            "Name of the organization or client responsible for the event .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing address of the organization or client .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the organization or client .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            "Fax number for the organization or client .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_person: str = Field(
        ...,
        description=(
            'Primary contact person for this event .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contacts_phone: str = Field(
        ...,
        description=(
            'Phone number for the contact person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contacts_fax: str = Field(
        default="",
        description=(
            'Fax number for the contact person .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contacts_e_mail: str = Field(
        ...,
        description=(
            'Email address for the contact person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class LocationSchedule(BaseModel):
    """Requested facility locations and event timing"""

    second_floor_courtyard: BooleanLike = Field(
        default="",
        description="Check if the Second Floor Courtyard is requested as an event location",
    )

    front_lawn: BooleanLike = Field(
        default="", description="Check if the Front Lawn is requested as an event location"
    )

    multipurpose_room: BooleanLike = Field(
        default="", description="Check if the Multipurpose Room is requested as an event location"
    )

    sculpture_garden: BooleanLike = Field(
        default="", description="Check if the Sculpture Garden is requested as an event location"
    )

    galleries_opened_for_public_viewing_from: str = Field(
        default="",
        description=(
            "Start time when galleries will be open for public viewing .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    galleries_opened_for_public_viewing_to: str = Field(
        default="",
        description=(
            "End time when galleries will be open for public viewing .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    event_description: str = Field(
        ...,
        description=(
            "Brief description of the event and its activities .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    event_time_from: str = Field(
        ...,
        description=(
            'Event start time .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    event_time_to: str = Field(
        ...,
        description=(
            'Event end time .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    entrance_time_for_setup: str = Field(
        default="",
        description=(
            "Time when access is needed to begin event setup .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    exit_time_for_cleanup: str = Field(
        default="",
        description=(
            "Time when cleanup will be completed and the space vacated .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    anticipated_attendance: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Estimated number of attendees at the event"
    )


class AlcoholService(BaseModel):
    """Information about alcoholic beverages and permit holder"""

    will_alcoholic_beverages_be_served_at_this_event: BooleanLike = Field(
        default="", description="Indicate whether alcoholic beverages will be served at the event"
    )

    name_of_alcohol_permit_holder_provider_server: str = Field(
        default="",
        description=(
            "Name of the person or company holding the alcohol permit and serving alcohol "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class VendorsServices(BaseModel):
    """Vendors and services employed for the event"""

    caterer: str = Field(
        default="",
        description=(
            "Name of the catering company or individual providing food service .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    valet_parking: str = Field(
        default="",
        description=(
            "Name of the valet parking service provider, if any .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    chairs_tables_linens: str = Field(
        default="",
        description=(
            "Vendor providing chairs, tables, and linens .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    tents: str = Field(
        default="",
        description=(
            'Vendor providing tents or canopies .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    lighting: str = Field(
        default="",
        description=(
            "Vendor providing lighting services or equipment .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    sound: str = Field(
        default="",
        description=(
            "Vendor providing sound or audio services .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    musicians: str = Field(
        default="",
        description=(
            "Name of musicians or musical group performing at the event .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other: str = Field(
        default="",
        description=(
            "Any additional vendors or services not listed above .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FacilityRentalRequestForm(BaseModel):
    """
    FACILITY RENTAL REQUEST FORM

    ''
    """

    event__client_information: EventClientInformation = Field(
        ..., description="Event & Client Information"
    )
    location__schedule: LocationSchedule = Field(..., description="Location & Schedule")
    alcohol_service: AlcoholService = Field(..., description="Alcohol Service")
    vendors__services: VendorsServices = Field(..., description="Vendors & Services")
