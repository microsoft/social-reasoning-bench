from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class WestSpecialEventPermitApplicationForm(BaseModel):
    """
    WEST SPECIAL EVENT PERMIT APPLICATION FORM

    • Complete and return the application to the City Clerk with the $50 application initial processing fee. Applications filed within 45 days of the event must pay an expedited processing fee of $250. CASH OR CHECK ONLY
    • Additional information regarding special events and fees are available here.
    • Anyone who organizes a gathering of at least 21 people that impedes the normal use of public property (i.e.—block party, church festival, concert, parade, carnival, or other large gathering on public property) is required to have a special event permit issued for their event.
    • Class 1 Event - means a special event that includes at least one of the following features: alcohol is available for consumption, electronically amplified outdoor sound is utilized, or more than 400 square feet of ground is covered by a tent or other temporary structure that provides shelter from the elements.
    • Class 2 Event - an organized gathering on public property that does not meet the definition of a Class 1 Event.
    • Please note: Service of alcohol will require an alcohol license, use of a tent may require a permit, and food service may require a food license from the Health Department (414-302-8600).
    """

    event_name: str = Field(
        ...,
        description=(
            'Official name or title of the event .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_or_location_of_event: str = Field(
        ...,
        description=(
            "Street address or detailed location description of where the event will take "
            'place .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    event_involves_closing_the_street_yes: BooleanLike = Field(
        ..., description="Select Yes if the event will require closing any street"
    )

    event_involves_closing_the_street_no: BooleanLike = Field(
        ..., description="Select No if the event will not require closing any street"
    )

    type_of_event_block_party: BooleanLike = Field(
        ..., description="Check if the event is a block party"
    )

    type_of_event_church_festival: BooleanLike = Field(
        ..., description="Check if the event is a church festival"
    )

    type_of_event_concert: BooleanLike = Field(..., description="Check if the event is a concert")

    type_of_event_parade: BooleanLike = Field(..., description="Check if the event is a parade")

    type_of_event_carnival: BooleanLike = Field(..., description="Check if the event is a carnival")

    type_of_event_other_describe: str = Field(
        default="",
        description=(
            "If the event type is not listed, briefly describe the type of event .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    describe_the_type_of_entertainment_that_will_be_provided: str = Field(
        ...,
        description=(
            "Describe the entertainment activities that will take place at the event .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    alcohol_is_available_yes: BooleanLike = Field(
        ..., description="Select Yes if alcohol will be available at the event"
    )

    alcohol_is_available_no: BooleanLike = Field(
        ..., description="Select No if alcohol will not be available at the event"
    )

    electronic_amplified_sound_outdoors_yes: BooleanLike = Field(
        ..., description="Select Yes if electronically amplified sound will be used outdoors"
    )

    electronic_amplified_sound_outdoors_no: BooleanLike = Field(
        ..., description="Select No if electronically amplified sound will not be used outdoors"
    )

    tent_or_structure_400_feet_or_larger_present_yes: BooleanLike = Field(
        ...,
        description=(
            "Select Yes if a tent or structure of 400 square feet or larger will be present "
            "at the event"
        ),
    )

    tent_or_structure_400_feet_or_larger_present_no: BooleanLike = Field(
        ...,
        description=(
            "Select No if no tent or structure of 400 square feet or larger will be present "
            "at the event"
        ),
    )

    maximum_capacity_of_the_premises: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Maximum number of people allowed at the event location"
    )
