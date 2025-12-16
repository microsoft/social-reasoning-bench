from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ContactInformation(BaseModel):
    """Applicant and primary contact details"""

    applicant_organization: str = Field(
        ...,
        description=(
            "Name of the applicant or organizing organization .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_contact: str = Field(
        ...,
        description=(
            "Full name of the primary contact person for this application .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Street address for the applicant or organization .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City for the mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    province_territory: str = Field(
        ...,
        description=(
            "Province or territory for the mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    postal_code: str = Field(..., description="Postal code for the mailing address")

    phone_number: str = Field(
        ...,
        description=(
            "Primary phone number for the contact person or organization .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Email address for the primary contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class EventInformation(BaseModel):
    """Details about the proposed event"""

    event_date_time: str = Field(
        ...,
        description=(
            'Planned date and time of the event .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    location: str = Field(
        ...,
        description=(
            "Venue or location where the event will take place .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    event_name: str = Field(
        ...,
        description=(
            'Official name or title of the event .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    anticipated_attendance: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Estimated number of attendees expected at the event"
    )

    fundraising_goal: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Monetary fundraising goal for this event"
    )

    target_audience: str = Field(
        ...,
        description=(
            "Description of the primary audience or demographic for the event .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    brief_description_of_the_proposed_event: str = Field(
        ...,
        description=(
            "Short summary of the event, its purpose, and key activities .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    number_of_years_this_event_has_been_hosted: Union[float, Literal["N/A", ""]] = Field(
        default="", description="If applicable, how many years this event has previously been held"
    )

    revenue_from_the_previous_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total revenue generated by this event in the previous year"
    )

    would_you_like_a_capitalize_for_kids_representative_to_attend_the_event: BooleanLike = Field(
        default="",
        description="Indicate whether you would like a Capitalize for Kids representative to attend",
    )

    if_yes_what_involvement_will_they_have: str = Field(
        default="",
        description=(
            "Describe the role or activities you would like the representative to undertake "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    speech: BooleanLike = Field(
        default="", description="Select if you would like the representative to give a speech"
    )

    cheque_presentation: BooleanLike = Field(
        default="",
        description=(
            "Select if you would like the representative to participate in a cheque presentation"
        ),
    )

    press_conference: BooleanLike = Field(
        default="",
        description=(
            "Select if you would like the representative to participate in a press conference"
        ),
    )

    other_involvement: str = Field(
        default="",
        description=(
            "Specify any other type of involvement requested for the representative .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    are_any_other_organizations_affiliated_with_or_receiving_proceeds_from_this_event: BooleanLike = Field(
        default="",
        description="Indicate if other organizations are involved with or benefiting from this event",
    )

    additional_details: str = Field(
        default="",
        description=(
            "Provide any additional information about affiliated organizations or proceeds "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class Acknowledgments(BaseModel):
    """Applicant acknowledgment and signature"""

    applicant_name: str = Field(
        ...,
        description=(
            "Printed name of the applicant submitting this form .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_signature: str = Field(
        ...,
        description=(
            "Signature of the applicant confirming the acknowledgments .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the application is signed")  # YYYY-MM-DD format


class Application(BaseModel):
    """
    APPLICATION

    Note: All fields are required for a complete application to be considered. Submission of a form confirms you have read and agree to all guidelines and regulations outlined. Return form to: info@capitalizeforkids.com
    """

    contact_information: ContactInformation = Field(..., description="Contact Information")
    event_information: EventInformation = Field(..., description="Event Information")
    acknowledgments: Acknowledgments = Field(..., description="Acknowledgments")
