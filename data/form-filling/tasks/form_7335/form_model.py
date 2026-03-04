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
            "Existing QBE policy number for this corporate travel policy .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    expiry_date_dd_mm_yyyy: str = Field(
        ..., description="Current policy expiry date in dd/mm/yyyy format"
    )  # YYYY-MM-DD format

    name_of_intermediary: str = Field(
        default="",
        description=(
            "Name of the broker or intermediary handling this policy, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class CoverageDetails(BaseModel):
    """Changes to coverage and insured details"""

    coverage_details_changes_to_sums_insured_limits_policy_coverage_insured_person_details_and_time_of_operation_of_cover: str = Field(
        default="",
        description=(
            "Describe any requested changes to sums insured, limits, coverage, insured "
            "persons, or time of operation of cover. If no changes, write “no change”. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class EstimateTravelPatternOverseasTravel(BaseModel):
    """Estimated overseas travel for the next 12 months"""

    number_of_overseas_trips_from_australia_excluding_the_usa_business_trips: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Estimated number of business overseas trips from Australia (excluding USA) in "
            "the next 12 months"
        ),
    )

    number_of_overseas_trips_from_australia_excluding_the_usa_leisure_trips: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Estimated number of leisure overseas trips from Australia (excluding USA) in "
            "the next 12 months"
        ),
    )

    number_of_overseas_trips_from_australia_excluding_the_usa_average_duration: str = Field(
        default="",
        description=(
            "Average duration of these overseas trips from Australia (excluding USA), e.g. "
            'in days or weeks .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    number_of_overseas_to_overseas_trips_business_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of business trips taken from one overseas location to another "
            "(not via Australia) in the next 12 months"
        ),
    )

    number_of_overseas_to_overseas_trips_leisure_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of leisure trips taken from one overseas location to another "
            "(not via Australia) in the next 12 months"
        ),
    )

    number_of_overseas_to_overseas_trips_average_duration: str = Field(
        default="",
        description=(
            "Average duration of overseas-to-overseas trips, e.g. in days or weeks .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    the_number_of_overseas_trips_to_usa_if_known_business_trips: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Estimated number of business trips to the USA in the next 12 months, if known",
    )

    the_number_of_overseas_trips_to_usa_if_known_leisure_trips: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Estimated number of leisure trips to the USA in the next 12 months, if known",
        )
    )

    the_number_of_overseas_trips_to_usa_if_known_average_duration: str = Field(
        default="",
        description=(
            "Average duration of trips to the USA, e.g. in days or weeks .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    number_of_domestic_overseas_trips_business_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of business trips classified as domestic overseas trips in "
            "the next 12 months"
        ),
    )

    number_of_domestic_overseas_trips_leisure_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of leisure trips classified as domestic overseas trips in the "
            "next 12 months"
        ),
    )

    number_of_domestic_overseas_trips_average_duration: str = Field(
        default="",
        description=(
            "Average duration of domestic overseas trips, e.g. in days or weeks .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    maximum_duration_of_any_overseas_trip_business_trips: str = Field(
        default="",
        description=(
            "Maximum expected duration of any single business overseas trip .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    maximum_duration_of_any_overseas_trip_leisure_trips: str = Field(
        default="",
        description=(
            "Maximum expected duration of any single leisure overseas trip .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    maximum_duration_of_any_overseas_trip_average_duration: str = Field(
        default="",
        description=(
            "Average maximum duration measure for overseas trips, if recorded separately "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class EstimateTravelPatternLocalTravel(BaseModel):
    """Estimated local (within Australia) travel for the next 12 months"""

    number_of_interstate_trips_business_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of business interstate trips within Australia in the next 12 months"
        ),
    )

    number_of_interstate_trips_leisure_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of leisure interstate trips within Australia in the next 12 months"
        ),
    )

    number_of_interstate_trips_average_duration: str = Field(
        default="",
        description=(
            "Average duration of interstate trips, e.g. in days or weeks .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    number_of_intrastate_trips_beyond_50kms_business_trips: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description=(
                "Estimated number of business intrastate trips beyond 50km within the same "
                "state in the next 12 months"
            ),
        )
    )

    number_of_intrastate_trips_beyond_50kms_leisure_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of leisure intrastate trips beyond 50km within the same state "
            "in the next 12 months"
        ),
    )

    number_of_intrastate_trips_beyond_50kms_average_duration: str = Field(
        default="",
        description=(
            "Average duration of intrastate trips beyond 50km, e.g. in days or weeks .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class NonscheduleAircraft(BaseModel):
    """Charter, non-schedule and helicopter flight details"""

    charter_non_schedule_flights_overseas: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of overseas charter or non-scheduled flights to be undertaken "
            "by insured persons"
        ),
    )

    charter_non_schedule_flights_interstate: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of interstate charter or non-scheduled flights to be "
            "undertaken by insured persons"
        ),
    )

    charter_non_schedule_flights_intrastate: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of intrastate charter or non-scheduled flights to be "
            "undertaken by insured persons"
        ),
    )

    helicopter_flights_overseas: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of overseas helicopter flights to be undertaken by insured persons"
        ),
    )

    helicopter_flights_interstate: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of interstate helicopter flights to be undertaken by insured persons"
        ),
    )

    helicopter_flights_intrastate: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of intrastate helicopter flights to be undertaken by insured persons"
        ),
    )

    maximum_number_of_people_travelling_together_overseas: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Maximum number of insured persons expected to travel together on any one "
            "overseas charter/non-schedule or helicopter flight"
        ),
    )

    maximum_number_of_people_travelling_together_interstate: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description=(
                "Maximum number of insured persons expected to travel together on any one "
                "interstate charter/non-schedule or helicopter flight"
            ),
        )
    )

    maximum_number_of_people_travelling_together_intrastate: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description=(
                "Maximum number of insured persons expected to travel together on any one "
                "intrastate charter/non-schedule or helicopter flight"
            ),
        )
    )


class AdditionalComments(BaseModel):
    """Any other relevant information"""

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

    This Policy will expire at 4.00pm on the date shown above. If you would like to take out another policy with us which starts immediately after this one expires, please complete this application and send it to us more than 21 days prior to the expiry date. We will send you an offer for a new policy once we have received and assessed your application form.
    """

    details: Details = Field(..., description="Details")
    coverage_details: CoverageDetails = Field(..., description="Coverage Details")
    estimate_travel_pattern___overseas_travel: EstimateTravelPatternOverseasTravel = Field(
        ..., description="Estimate Travel Pattern - Overseas Travel"
    )
    estimate_travel_pattern___local_travel: EstimateTravelPatternLocalTravel = Field(
        ..., description="Estimate Travel Pattern - Local Travel"
    )
    non_schedule_aircraft: NonscheduleAircraft = Field(..., description="Non-schedule Aircraft")
    additional_comments: AdditionalComments = Field(..., description="Additional Comments")
