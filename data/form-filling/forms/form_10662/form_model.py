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
    """Primary applicant details and status"""

    applicants_name: str = Field(
        ...,
        description=(
            "Full name of the person responsible or representative of the organization .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    little_italy_resident_property_owner: BooleanLike = Field(
        default="",
        description="Check if the applicant is a Little Italy resident or property owner",
    )

    little_italy_business_owner: BooleanLike = Field(
        default="", description="Check if the applicant is a Little Italy business owner"
    )

    verified_by: str = Field(
        default="",
        description=(
            "Name or initials of staff verifying Little Italy status .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    non_resident_owner: BooleanLike = Field(
        default="", description="Check if the applicant is not a Little Italy resident or owner"
    )

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    cell: str = Field(
        default="",
        description=(
            'Cell phone number for the applicant .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Email address for the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    company_name: str = Field(
        default="",
        description=(
            "Name of the company or organization, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    website: str = Field(
        default="",
        description=(
            "Website URL for the applicant or organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    non_profit_yes: BooleanLike = Field(
        default="", description="Check if the organization is a non-profit"
    )

    non_profit_no: BooleanLike = Field(
        default="", description="Check if the organization is not a non-profit"
    )

    street_address: str = Field(
        ...,
        description=(
            "Street address of the applicant or organization .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_st_zip_code: str = Field(
        ...,
        description=(
            "City, state abbreviation, and ZIP code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Contacts(BaseModel):
    """Preferred and alternate contact information"""

    preferred_contact: str = Field(
        default="",
        description=(
            "Name of preferred contact person if different from applicant .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    preferred_contact_phone: str = Field(
        default="",
        description=(
            "Phone number for the preferred contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    preferred_contact_cell: str = Field(
        default="",
        description=(
            "Cell phone number for the preferred contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    preferred_contact_email: str = Field(
        default="",
        description=(
            "Email address for the preferred contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    alternate_contact: str = Field(
        default="",
        description=(
            'Name of alternate contact person .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    alternate_contact_phone: str = Field(
        default="",
        description=(
            "Phone number for the alternate contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    alternate_contact_cell: str = Field(
        default="",
        description=(
            "Cell phone number for the alternate contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    alternate_contact_email: str = Field(
        default="",
        description=(
            "Email address for the alternate contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class EventFacilityDetails(BaseModel):
    """Requested area, dates, times, and event specifics"""

    area_requesting_amphitheater: BooleanLike = Field(
        default="", description="Check if requesting use of the Amphitheater area"
    )

    area_requesting_little_italy_dog_park: BooleanLike = Field(
        default="", description="Check if requesting use of the Little Italy Dog Park"
    )

    area_requesting_bocce_ball_courts_both: BooleanLike = Field(
        default="", description="Check if requesting use of both Bocce Ball Courts"
    )

    area_requesting_all: BooleanLike = Field(
        default="", description="Check if requesting use of all listed areas"
    )

    first_choice_date: str = Field(
        ..., description="First choice date requested for the event"
    )  # YYYY-MM-DD format

    first_choice_sun: BooleanLike = Field(
        default="", description="Select if the first choice date falls on Sunday"
    )

    first_choice_mon: BooleanLike = Field(
        default="", description="Select if the first choice date falls on Monday"
    )

    first_choice_tue: BooleanLike = Field(
        default="", description="Select if the first choice date falls on Tuesday"
    )

    first_choice_wed: BooleanLike = Field(
        default="", description="Select if the first choice date falls on Wednesday"
    )

    first_choice_thu: BooleanLike = Field(
        default="", description="Select if the first choice date falls on Thursday"
    )

    first_choice_fri: BooleanLike = Field(
        default="", description="Select if the first choice date falls on Friday"
    )

    first_choice_sat: BooleanLike = Field(
        default="", description="Select if the first choice date falls on Saturday"
    )

    second_choice_date: str = Field(
        default="", description="Second choice date requested for the event"
    )  # YYYY-MM-DD format

    second_choice_sun: BooleanLike = Field(
        default="", description="Select if the second choice date falls on Sunday"
    )

    second_choice_mon: BooleanLike = Field(
        default="", description="Select if the second choice date falls on Monday"
    )

    second_choice_tue: BooleanLike = Field(
        default="", description="Select if the second choice date falls on Tuesday"
    )

    second_choice_wed: BooleanLike = Field(
        default="", description="Select if the second choice date falls on Wednesday"
    )

    second_choice_thu: BooleanLike = Field(
        default="", description="Select if the second choice date falls on Thursday"
    )

    second_choice_fri: BooleanLike = Field(
        default="", description="Select if the second choice date falls on Friday"
    )

    second_choice_sat: BooleanLike = Field(
        default="", description="Select if the second choice date falls on Saturday"
    )

    set_up_time: str = Field(
        ...,
        description=(
            'Time when event setup will begin .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    event_time: str = Field(
        ...,
        description=(
            'Start and end time of the event .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    tear_down_time: str = Field(
        ...,
        description=(
            "Time when event tear-down will be completed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    title_of_the_event: str = Field(
        ...,
        description=(
            'Name or title of the event .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    attendance: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Estimated number of attendees"
    )

    purpose_of_use: str = Field(
        ...,
        description=(
            "Description of the purpose or nature of the event .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    entrance_fee_yes_amount: str = Field(
        default="",
        description=(
            "Indicate if there is an entrance fee and specify the amount .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    food_alcohol_no_food_or_alcohol: BooleanLike = Field(
        default="", description="Select if no food or alcohol will be served"
    )

    food_alcohol_off_site_food: BooleanLike = Field(
        default="",
        description="Select if food will be brought in from off-site (not catered on-site)",
    )

    food_alcohol_catering: BooleanLike = Field(
        default="", description="Select if the event will use catering services"
    )

    food_alcohol_alcohol: BooleanLike = Field(
        default="", description="Select if alcohol will be served at the event"
    )

    special_equipment_to_be_used: str = Field(
        default="",
        description=(
            "List any special equipment to be used (e.g., amplified sound, staging, risers, "
            'tents, canopies) .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class AgreementAuthorization(BaseModel):
    """Applicant agreement to terms and signature"""

    signature: str = Field(
        ...,
        description=(
            "Signature of the applicant agreeing to the terms and conditions .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date: str = Field(..., description="Date the application is signed")  # YYYY-MM-DD format


class LittleItalySanDiegoApplicationForUseOfAmiciPark(BaseModel):
    """
        LITTLE ITALY
    SAN DIEGO

    APPLICATION FOR USE OF AMICI PARK

        APPLICATION FOR USE OF AMICI PARK Managed by the Little Italy Association of San Diego
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    contacts: Contacts = Field(..., description="Contacts")
    event__facility_details: EventFacilityDetails = Field(
        ..., description="Event & Facility Details"
    )
    agreement__authorization: AgreementAuthorization = Field(
        ..., description="Agreement & Authorization"
    )
