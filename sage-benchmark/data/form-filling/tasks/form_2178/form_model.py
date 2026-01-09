from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class IndividualInfo(BaseModel):
    """Information about the sponsoring individual and their organization"""

    full_name: str = Field(
        ...,
        description=(
            'Individual sponsor\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    company_org: str = Field(
        default="",
        description=(
            "Name of the company or organization represented (if applicable) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street mailing address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    city_state: str = Field(
        ...,
        description=(
            "City and state for the mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    zip_code: str = Field(..., description="Postal ZIP code")

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the individual .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Primary email address for the individual .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class EmergencyContact(BaseModel):
    """Emergency contact details for the individual"""

    emergency_contact_full_name: str = Field(
        ...,
        description=(
            "Full name of the emergency contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_phone: str = Field(
        ...,
        description=(
            "Phone number for the emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_email: str = Field(
        default="",
        description=(
            "Email address for the emergency contact (if available) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    relationship_to_individual_spouse_sibling_etc: str = Field(
        ...,
        description=(
            "Describe how the emergency contact is related to the individual .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class EventInfo(BaseModel):
    """Meal selections, tours, and other event-related information"""

    tues_breakfast: BooleanLike = Field(
        default="", description="Select if you will eat Tuesday breakfast with the group"
    )

    tues_lunch: BooleanLike = Field(
        default="", description="Select if you will eat Tuesday lunch with the group"
    )

    tues_dinner: BooleanLike = Field(
        default="", description="Select if you will eat Tuesday dinner with the group"
    )

    wed_breakfast: BooleanLike = Field(
        default="", description="Select if you will eat Wednesday breakfast with the group"
    )

    wed_lunch: BooleanLike = Field(
        default="", description="Select if you will eat Wednesday lunch with the group"
    )

    wed_dinner: BooleanLike = Field(
        default="", description="Select if you will eat Wednesday dinner with the group"
    )

    no_meals: BooleanLike = Field(
        default="", description="Select if you will not be eating any meals with the group"
    )

    tuesday_tour: BooleanLike = Field(
        default="", description="Select if you plan to attend the Tuesday tour"
    )

    wednesday_tour: BooleanLike = Field(
        default="", description="Select if you plan to attend the Wednesday tour"
    )

    special_needs_or_medical_conditions_we_should_be_aware_of: str = Field(
        default="",
        description=(
            "Describe any special needs, accommodations, or medical conditions .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    anything_else_we_should_know_about_you: str = Field(
        default="",
        description=(
            "Any additional information you would like the organizers to know .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SponsorRegistrationForm(BaseModel):
    """
    Sponsor Registration Form

    ''
    """

    individual_info: IndividualInfo = Field(..., description="Individual Info")
    emergency_contact: EmergencyContact = Field(..., description="Emergency Contact")
    event_info: EventInfo = Field(..., description="Event Info")
