from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class DeliveryFormatTableRow(BaseModel):
    """Single row in Delivery Format"""

    delivery_format: str = Field(default="", description="Delivery_Format")
    live: str = Field(default="", description="Live")
    number_of_live_events: str = Field(default="", description="Number_Of_Live_Events")
    number_of_speakers_faculty_members: str = Field(
        default="", description="Number_Of_Speakers_Faculty_Members"
    )
    geographic_reach: str = Field(default="", description="Geographic_Reach")
    venue_name: str = Field(default="", description="Venue_Name")
    city: str = Field(default="", description="City")
    state: str = Field(default="", description="State")
    zip_code: str = Field(default="", description="Zip_Code")
    audience_group: str = Field(default="", description="Audience_Group")
    specialty: str = Field(default="", description="Specialty")
    total_credit_hours_offered: str = Field(default="", description="Total_Credit_Hours_Offered")
    credit_type: str = Field(default="", description="Credit_Type")
    number_of_attendees: str = Field(default="", description="Number_Of_Attendees")


class ProgramInformation(BaseModel):
    """Overview, needs, objectives, description, outcomes, and financial/relationship details for the program"""

    program_details: str = Field(
        ...,
        description=(
            "Overall description or title/details of the program .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    needs_assessment_summary: str = Field(
        ...,
        description=(
            "Summary of the needs assessment supporting this program .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    learning_objectives: str = Field(
        ...,
        description=(
            "List the specific learning objectives for this program .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    program_activity_description: str = Field(
        ...,
        description=(
            "Detailed description of the planned program or activity .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    methods_measure_educational_outcomes_patient_impact: str = Field(
        ...,
        description=(
            "Describe how you will measure educational outcomes and/or patient impact for "
            'this activity .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    requested_amount: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Dollar amount of funding requested for this program"
    )

    total_program_budget_amount: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total overall budget for the program"
    )

    other_financial_supporters: BooleanLike = Field(
        ...,
        description="Indicate whether other organizations will financially support this program",
    )

    list_other_potential_supporters: str = Field(
        default="",
        description=(
            "List all other potential financial supporters, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    collecting_registration_fees: BooleanLike = Field(
        ..., description="Indicate whether registration fees will be collected from participants"
    )

    using_physicians_hcps_as_faculty: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether physicians or other healthcare professionals will serve as faculty"
        ),
    )

    mec_additional_services_money_required: BooleanLike = Field(
        ...,
        description="Indicate whether MEC requires additional funds for services beyond the grant",
    )

    disclose_relationship_ironwood_organization: str = Field(
        ...,
        description=(
            "Describe any legal, financial, business, or other relationships between "
            'Ironwood and your organization .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class DeliveryFormatAudience(BaseModel):
    """Delivery format, logistics, and audience/credit details"""

    delivery_format_table: List[DeliveryFormatTableRow] = Field(
        ..., description="Table to capture delivery format, event details, and audience information"
    )  # List of table rows

    live: BooleanLike = Field(
        default="", description="Indicate whether the delivery format is live"
    )

    number_of_live_events: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of live events planned"
    )

    number_of_speakers_faculty_members: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of speakers or faculty members participating"
    )

    venue_name: str = Field(
        default="",
        description=(
            "Name of the venue where the event will be held .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        default="",
        description=(
            'City where the event will take place .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(default="", description="State where the event will take place")

    zip_code: str = Field(default="", description="Zip code of the event location")

    audience_group: str = Field(
        default="",
        description=(
            "Primary audience group for the program .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    specialty: str = Field(
        default="",
        description=(
            "Clinical or professional specialty of the target audience .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    total_credit_hours_offered: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of credit hours offered for this activity"
    )

    credit_type: str = Field(
        default="",
        description=(
            "Type of continuing education credit offered (e.g., CME, CEU) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    number_of_attendees: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of attendees"
    )


class DeliveryFormatAudience(BaseModel):
    """
    Delivery Format & Audience

    ''
    """

    program_information: ProgramInformation = Field(..., description="Program Information")
    delivery_format__audience: DeliveryFormatAudience = Field(
        ..., description="Delivery Format & Audience"
    )
