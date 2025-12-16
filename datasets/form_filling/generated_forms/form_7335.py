from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Details(BaseModel):
    """Basic policy and insured details"""

    name_of_insured: str = Field(
        ...,
        description=(
            "Full legal name of the insured entity or person .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    policy_number: str = Field(
        ...,
        description=(
            "Existing QBE corporate travel policy number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_intermediary: str = Field(
        default="",
        description=(
            "Name of the broker or intermediary handling this policy, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    expiry_date_dd_mm_yyyy: str = Field(
        ..., description="Current policy expiry date in dd/mm/yyyy format"
    )  # YYYY-MM-DD format


class Overseastravel(BaseModel):
    """Estimated overseas travel pattern for the next 12 months"""

    number_of_overseas_trips_from_australia_excluding_the_usa: Union[float, Literal["N/A", ""]] = (
        Field(
            ...,
            description=(
                "Estimated number of return overseas trips originating from Australia, "
                "excluding trips to the USA, for the next 12 months"
            ),
        )
    )

    number_of_overseas_to_overseas_trips: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Estimated number of trips taken between overseas locations that do not start "
            "or end in Australia for the next 12 months"
        ),
    )

    number_of_overseas_trips_to_usa_if_known: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of overseas trips to the USA for the next 12 months, if this "
            "information is available"
        ),
    )

    number_of_domestic_overseas_trips: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Estimated number of domestic overseas trips as defined by the policy for the "
            "next 12 months"
        ),
    )

    maximum_duration_of_any_overseas_trip: str = Field(
        ...,
        description=(
            "Maximum expected length of any single overseas trip (e.g. in days or weeks) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class LocaltravelwithinAustralia(BaseModel):
    """Estimated local travel pattern for the next 12 months"""

    number_of_interstate_trips: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Estimated number of interstate trips within Australia for the next 12 months",
    )

    number_of_intrastate_trips_beyond_50kms: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Estimated number of intrastate trips within 1 state where the distance "
            "travelled is beyond 50 km, for the next 12 months"
        ),
    )


class Nonscheduleaircraft(BaseModel):
    """Charter and helicopter flight details"""

    charter_non_schedule_flights_number_of_flights_overseas: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description=(
                "Estimated number of overseas charter or non-scheduled flights for insured persons"
            ),
        )
    )

    charter_non_schedule_flights_number_of_flights_interstate: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description=(
                "Estimated number of interstate charter or non-scheduled flights within "
                "Australia for insured persons"
            ),
        )
    )

    charter_non_schedule_flights_number_of_flights_intrastate: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description=(
                "Estimated number of intrastate charter or non-scheduled flights within a "
                "single state for insured persons"
            ),
        )
    )

    helicopter_flights_number_of_flights_overseas: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Estimated number of overseas helicopter flights for insured persons",
    )

    helicopter_flights_number_of_flights_interstate: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of interstate helicopter flights within Australia for insured persons"
        ),
    )

    helicopter_flights_number_of_flights_intrastate: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of intrastate helicopter flights within a single state for "
            "insured persons"
        ),
    )

    maximum_number_of_people_travelling_together: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Maximum number of insured persons expected to travel together on the same "
            "charter or helicopter flight"
        ),
    )


class Additionalinformation(BaseModel):
    """Any other relevant comments"""

    any_additional_comments: str = Field(
        default="",
        description=(
            "Any further information or comments relevant to the travel pattern or coverage "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class InvitationToReapplyCorporateTravel(BaseModel):
    """
    Invitation to re-apply – Corporate Travel

    This Policy will expire at 4.00pm on the date shown above. If you would like to take out another policy with us which starts immediately after this one expires, please complete this application and send it to us more than 21 days prior to the expiry date.
    We will send you an offer for a new policy once we have received and assessed your application form.
    """

    details: Details = Field(..., description="Details")
    overseas_travel: Overseastravel = Field(..., description="Overseas travel")
    local_travel_within_australia: LocaltravelwithinAustralia = Field(
        ..., description="Local travel (within Australia)"
    )
    non_schedule_aircraft: Nonscheduleaircraft = Field(..., description="Non schedule aircraft")
    additional_information: Additionalinformation = Field(..., description="Additional information")
