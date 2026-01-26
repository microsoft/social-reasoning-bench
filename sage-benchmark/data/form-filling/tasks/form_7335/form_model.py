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
    """Policy and insured party details"""

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

    expiry_date_dd_mm_yyyy: str = Field(
        ..., description="Current policy expiry date in dd/mm/yyyy format"
    )  # YYYY-MM-DD format

    name_of_intermediary: str = Field(
        default="",
        description=(
            "Name of broker, agent or intermediary handling this policy .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CoverageDetails(BaseModel):
    """Changes to coverage and insured details"""

    coverage_details_changes: str = Field(
        default="",
        description=(
            "Describe any requested changes to sums insured, limits, coverage, insured "
            "persons or time of operation of cover. If no changes, state 'no change'. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class OverseasTravelNext12Months(BaseModel):
    """Estimated overseas travel pattern for the next twelve months"""

    overseas_travel_business_trips: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of overseas business trips in the next 12 months"
    )

    overseas_travel_leisure_trips: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of overseas leisure trips in the next 12 months"
    )

    overseas_travel_average_duration: str = Field(
        default="",
        description=(
            "Average duration of overseas trips (e.g. in days or weeks) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    number_of_overseas_trips_from_australia_excl_usa: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of overseas trips originating from Australia, excluding trips "
            "to the USA"
        ),
    )

    number_of_overseas_to_overseas_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of trips taken between overseas locations without returning "
            "to Australia"
        ),
    )

    number_of_overseas_trips_to_usa: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Estimated number of overseas trips to the USA in the next 12 months, if known",
    )

    number_of_domestic_overseas_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of trips that are classified as domestic overseas trips under "
            "the policy"
        ),
    )

    maximum_duration_of_any_overseas_trip: str = Field(
        default="",
        description=(
            "Maximum expected length of any single overseas trip (e.g. in days or weeks) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class LocalTravelWithinAustraliaNext12Months(BaseModel):
    """Estimated local travel pattern within Australia for the next twelve months"""

    local_travel_business_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Estimated number of business trips within Australia in the next 12 months",
    )

    local_travel_leisure_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Estimated number of leisure trips within Australia in the next 12 months",
    )

    local_travel_average_duration: str = Field(
        default="",
        description=(
            "Average duration of local (within Australia) trips .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    number_of_interstate_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Estimated number of interstate trips within Australia in the next 12 months",
    )

    number_of_intrastate_trips_beyond_50kms: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of intrastate trips within Australia where the distance "
            "travelled is beyond 50 km"
        ),
    )


class NonscheduleandCharterFlights(BaseModel):
    """Charter/non-schedule and helicopter flight details"""

    non_schedule_flights_undertaken: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether any insured person will undertake charter or non-scheduled flights"
        ),
    )

    number_of_flights_overseas: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of overseas charter/non-schedule flights"
    )

    number_of_flights_interstate: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of interstate charter/non-schedule flights"
    )

    number_of_flights_intrastate: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated number of intrastate charter/non-schedule flights"
    )

    charter_non_schedule_flights_details: str = Field(
        default="",
        description=(
            "Provide details of any charter or non-scheduled flights, including operators, "
            'routes and frequency .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    helicopter_flights_details: str = Field(
        default="",
        description=(
            "Provide details of any helicopter flights, including purpose, operators and "
            'frequency .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    maximum_number_of_people_travelling_together: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Maximum number of insured persons expected to travel together on any one trip "
            "or flight"
        ),
    )

    any_additional_comments: str = Field(
        default="",
        description=(
            "Any other relevant information or comments regarding the travel pattern or "
            'coverage .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class InvitationToReapplyCorporateTravel(BaseModel):
    """
    Invitation to re-apply - Corporate Travel

    This Policy will expire at 4.00pm on the date shown above. If you would like to take out another policy with us which starts immediately after this one expires, please complete this application and send it to us more than 21 days prior to the expiry date.
    We will send you an offer for a new policy once we have received and assessed your application form.
    """

    details: Details = Field(..., description="Details")
    coverage_details: CoverageDetails = Field(..., description="Coverage Details")
    overseas_travel_next_12_months: OverseasTravelNext12Months = Field(
        ..., description="Overseas Travel (Next 12 Months)"
    )
    local_travel_within_australia_next_12_months: LocalTravelWithinAustraliaNext12Months = Field(
        ..., description="Local Travel (Within Australia, Next 12 Months)"
    )
    non_schedule_and_charter_flights: NonscheduleandCharterFlights = Field(
        ..., description="Non-schedule and Charter Flights"
    )
