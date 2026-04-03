from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Details(BaseModel):
    """Insured and policy details"""

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
            "Name of the broker or intermediary handling this policy .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CoverageDetails(BaseModel):
    """Changes to coverage and insured details"""

    changes_to_sums_insured_limits_policy_coverage_insured_person_details_and_time_of_operation_of_cover: str = Field(
        default="",
        description=(
            "Describe any changes to sums insured, limits, coverage, insured persons or "
            'period of cover; write "no change" if none .If you cannot fill this, write '
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class EstimateTravelPatternOverseasTravel(BaseModel):
    """Overseas travel from Australia, overseas-to-overseas, USA and domestic overseas trips"""

    number_of_overseas_business_trips_from_australia_excluding_the_usa: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Estimated number of business trips from Australia to overseas destinations "
            "excluding the USA in the next 12 months"
        ),
    )

    number_of_overseas_leisure_trips_from_australia_excluding_the_usa: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Estimated number of leisure trips from Australia to overseas destinations "
            "excluding the USA in the next 12 months"
        ),
    )

    average_duration_of_overseas_trips_from_australia_excluding_the_usa: str = Field(
        default="",
        description=(
            "Average length of each overseas trip from Australia (excluding USA), e.g. in "
            'days .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    number_of_overseas_to_overseas_business_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of business trips between overseas locations (not starting "
            "from Australia) in the next 12 months"
        ),
    )

    number_of_overseas_to_overseas_leisure_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of leisure trips between overseas locations (not starting "
            "from Australia) in the next 12 months"
        ),
    )

    average_duration_of_overseas_to_overseas_trips: str = Field(
        default="",
        description=(
            "Average length of each overseas-to-overseas trip, e.g. in days .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    number_of_overseas_business_trips_to_usa_if_known: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Estimated number of business trips to the USA in the next 12 months, if known",
    )

    number_of_overseas_leisure_trips_to_usa_if_known: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Estimated number of leisure trips to the USA in the next 12 months, if known",
    )

    average_duration_of_overseas_trips_to_usa_if_known: str = Field(
        default="",
        description=(
            "Average length of each trip to the USA, if known, e.g. in days .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    number_of_domestic_overseas_business_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of business trips classified as domestic overseas trips in "
            "the next 12 months"
        ),
    )

    number_of_domestic_overseas_leisure_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of leisure trips classified as domestic overseas trips in the "
            "next 12 months"
        ),
    )

    average_duration_of_domestic_overseas_trips: str = Field(
        default="",
        description=(
            "Average length of each domestic overseas trip, e.g. in days .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    maximum_duration_of_any_overseas_business_trip: str = Field(
        default="",
        description=(
            "Maximum expected length of any single overseas business trip, e.g. in days .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    maximum_duration_of_any_overseas_leisure_trip: str = Field(
        default="",
        description=(
            "Maximum expected length of any single overseas leisure trip, e.g. in days .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    average_duration_of_maximum_duration_of_any_overseas_trip: str = Field(
        default="",
        description=(
            "Average duration corresponding to the maximum-length overseas trips (as per "
            'form\'s average duration column) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class EstimateTravelPatternLocalTravelwithinAustralia(BaseModel):
    """Interstate and intrastate travel within Australia"""

    number_of_interstate_business_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of business trips between Australian states in the next 12 months"
        ),
    )

    number_of_interstate_leisure_trips: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of leisure trips between Australian states in the next 12 months"
        ),
    )

    average_duration_of_interstate_trips: str = Field(
        default="",
        description=(
            "Average length of each interstate trip within Australia, e.g. in days .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    number_of_intrastate_business_trips_beyond_50kms: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of business trips within the same state beyond 50km in the "
            "next 12 months"
        ),
    )

    number_of_intrastate_leisure_trips_beyond_50kms: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of leisure trips within the same state beyond 50km in the "
            "next 12 months"
        ),
    )

    average_duration_of_intrastate_trips_beyond_50kms: str = Field(
        default="",
        description=(
            "Average length of each intrastate trip beyond 50km, e.g. in days .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class NonscheduleAircraft(BaseModel):
    """Charter and helicopter flights and people travelling together"""

    will_any_insured_person_be_undertaking_charter_non_schedule_flights: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether any insured person will take charter or non-scheduled flights "
            "and provide details if yes"
        ),
    )

    number_of_overseas_charter_non_schedule_flights: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of charter or non-scheduled flights undertaken overseas in "
            "the next 12 months"
        ),
    )

    number_of_interstate_charter_non_schedule_flights: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of charter or non-scheduled flights undertaken interstate in "
            "Australia in the next 12 months"
        ),
    )

    number_of_intrastate_charter_non_schedule_flights: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of charter or non-scheduled flights undertaken intrastate in "
            "Australia in the next 12 months"
        ),
    )

    number_of_overseas_helicopter_flights: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of helicopter flights undertaken overseas in the next 12 months"
        ),
    )

    number_of_interstate_helicopter_flights: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of helicopter flights undertaken interstate in Australia in "
            "the next 12 months"
        ),
    )

    number_of_intrastate_helicopter_flights: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated number of helicopter flights undertaken intrastate in Australia in "
            "the next 12 months"
        ),
    )

    maximum_number_of_people_travelling_together_on_overseas_flights: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Maximum number of insured persons expected to travel together on any single "
            "overseas flight"
        ),
    )

    maximum_number_of_people_travelling_together_on_interstate_flights: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Maximum number of insured persons expected to travel together on any single "
            "interstate flight"
        ),
    )

    maximum_number_of_people_travelling_together_on_intrastate_flights: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Maximum number of insured persons expected to travel together on any single "
            "intrastate flight"
        ),
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
    estimate_travel_pattern___local_travel_within_australia: EstimateTravelPatternLocalTravelwithinAustralia = Field(
        ..., description="Estimate Travel Pattern - Local Travel (within Australia)"
    )
    non_schedule_aircraft: NonscheduleAircraft = Field(..., description="Non-schedule Aircraft")
    additional_comments: AdditionalComments = Field(..., description="Additional Comments")
