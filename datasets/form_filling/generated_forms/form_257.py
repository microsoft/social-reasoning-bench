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
    """Information about the group/company and primary contact"""

    todays_date: str = Field(
        ..., description="Date this proposal form is completed"
    )  # YYYY-MM-DD format

    name_of_group_company_planning_community_initiative: str = Field(
        ...,
        description=(
            "Official name of the group or company organizing the community initiative .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    primary_contact: str = Field(
        ...,
        description=(
            "Full name of the main contact person for this initiative .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    role: str = Field(
        ...,
        description=(
            "Role or position of the primary contact within the group or company .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            "Mailing address for the organizing group or primary contact .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
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

    postal_code: str = Field(..., description="Postal code for the mailing address")

    home_tel: str = Field(
        default="",
        description=(
            "Home telephone number for the primary contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    business: str = Field(
        default="",
        description=(
            "Business or work telephone number for the primary contact .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cell: str = Field(
        default="",
        description=(
            "Cell or mobile phone number for the primary contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        ...,
        description=(
            "Email address for the primary contact or organizing group .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class EventInitiativeInformation(BaseModel):
    """Details about the proposed community initiative"""

    name_of_proposed_initiative: str = Field(
        ...,
        description=(
            "Title or name of the proposed community initiative or event .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    start_date: str = Field(
        ..., description="Date the event or initiative will begin"
    )  # YYYY-MM-DD format

    end_date: str = Field(
        ..., description="Date the event or initiative will end"
    )  # YYYY-MM-DD format

    start_time: str = Field(
        ...,
        description=(
            "Time the event or initiative will start .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    end_time: str = Field(
        ...,
        description=(
            'Time the event or initiative will end .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_of_venue: str = Field(
        ...,
        description=(
            "Name of the venue where the event will be held .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_of_event: str = Field(
        ...,
        description=(
            "General location or description of where the event will take place .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address_event: str = Field(
        ...,
        description=(
            'Street address of the event venue .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    postal_code_event_address: str = Field(
        ..., description="Postal code for the event venue address"
    )


class EventDescriptionFinancials(BaseModel):
    """Event description, attendance, revenue, and agreement questions"""

    briefly_describe_the_event_and_how_the_funds_will_be_raised_line_1: str = Field(
        ...,
        description=(
            "First line of description of the event and how funds will be raised .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    briefly_describe_the_event_and_how_the_funds_will_be_raised_line_2: str = Field(
        default="",
        description=(
            "Second line of description of the event and how funds will be raised .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    briefly_describe_the_event_and_how_the_funds_will_be_raised_line_3: str = Field(
        default="",
        description=(
            "Third line of description of the event and how funds will be raised .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    briefly_describe_the_event_and_how_the_funds_will_be_raised_line_4: str = Field(
        default="",
        description=(
            "Fourth line of description of the event and how funds will be raised .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    how_many_people_do_you_expect_to_attend_the_event: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Estimated number of attendees at the event"
    )

    expected_net_revenue_for_this_event: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Estimated net revenue (after expenses) expected from the event in dollars"
    )

    are_you_planning_on_hosting_a_raffle_yes: BooleanLike = Field(
        ..., description="Indicate YES if you plan to host a raffle (50/50 or prize raffle)"
    )

    are_you_planning_on_hosting_a_raffle_no: BooleanLike = Field(
        ..., description="Indicate NO if you do not plan to host a raffle"
    )

    do_you_understand_and_agree_all_event_costs_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate YES to confirm you understand and agree that all event costs are "
            "covered by the organizer and only proceeds go to Calgary Health Trust"
        ),
    )

    do_you_understand_and_agree_all_event_costs_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate NO if you do not agree to cover all event costs and direct only "
            "proceeds to Calgary Health Trust"
        ),
    )

    does_the_community_group_agree_revenues_within_30_days_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate YES to confirm the community group agrees to remit all event revenues "
            "to Calgary Health Trust within 30 days"
        ),
    )

    does_the_community_group_agree_revenues_within_30_days_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate NO if the community group does not agree to remit all event revenues "
            "within 30 days"
        ),
    )


class CommunityInitiativeToolkitCommunityInitiativeProposalForm(BaseModel):
    """
        COMMUNITY INITIATIVE TOOLKIT

    Community Initiative Proposal Form

        Note: Application must be approved by Calgary Health Trust prior to promoting or hosting the event.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    event__initiative_information: EventInitiativeInformation = Field(
        ..., description="Event / Initiative Information"
    )
    event_description__financials: EventDescriptionFinancials = Field(
        ..., description="Event Description & Financials"
    )
