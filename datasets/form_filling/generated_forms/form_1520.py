from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ParticipantDetails(BaseModel):
    """Basic personal and contact information for the course participant"""

    course_date: str = Field(
        ..., description="Date of the woodturning weekend course you are booking"
    )  # YYYY-MM-DD format

    name: str = Field(
        ...,
        description=(
            'Your full name .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Your date of birth")  # YYYY-MM-DD format

    address: str = Field(
        ...,
        description=(
            'Your full postal address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Your email address for course correspondence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            "Your main telephone number (include country code if outside UK) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    mobile: str = Field(
        default="",
        description=(
            'Your mobile phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class EmergencyContact(BaseModel):
    """Emergency contact details for the participant"""

    emergency_contact_name_and_relationship: str = Field(
        ...,
        description=(
            "Name of your emergency contact and their relationship to you .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    emergency_contact_telephone_number: str = Field(
        ...,
        description=(
            "Telephone number for your emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class TravelAccommodationandOtherInformation(BaseModel):
    """Logistics, medical information, and marketing source"""

    how_will_you_be_travelling_to_us: str = Field(
        default="",
        description=(
            "Describe how you plan to travel to the school (e.g. car, train, bus) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    do_you_require_information_about_local_accommodation: BooleanLike = Field(
        default="",
        description="Indicate whether you would like information about nearby accommodation",
    )

    any_medical_conditions_of_which_we_should_be_aware: str = Field(
        default="",
        description=(
            "List any medical conditions or relevant health information .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    where_did_you_hear_about_us: str = Field(
        default="",
        description=(
            "Explain how you found out about the course or school .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class BookingForm(BaseModel):
    """
    BOOKING FORM

    WOODTURNING WEEKEND COURSE   FEE 400
    To be held at THE CHIPPENDALE INTERNATIONAL SCHOOL OF FURNITURE, Saturday and Sunday from 9am to 4.30pm
    """

    participant_details: ParticipantDetails = Field(..., description="Participant Details")
    emergency_contact: EmergencyContact = Field(..., description="Emergency Contact")
    travel_accommodation_and_other_information: TravelAccommodationandOtherInformation = Field(
        ..., description="Travel, Accommodation and Other Information"
    )
