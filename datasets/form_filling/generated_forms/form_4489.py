from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RespondentInformation(BaseModel):
    """Contact information for the person submitting the survey"""

    name: str = Field(
        ...,
        description=(
            'Your full name .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    town_of_residence: str = Field(
        ...,
        description=(
            'Town or city where you currently live .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        default="",
        description=(
            'Your email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    telephone_number: str = Field(
        default="",
        description=(
            'Your telephone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class QuailLocationandHistory(BaseModel):
    """Details about the historic quail location and sightings"""

    quail_once_lived_here: str = Field(
        default="",
        description=(
            "General information about the location where quail once lived .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    valley_quail: BooleanLike = Field(
        default="", description="Check if Valley Quail once lived at this location"
    )

    gambels_quail: BooleanLike = Field(
        default="", description="Check if Gambel's Quail once lived at this location"
    )

    mountain_quail: BooleanLike = Field(
        default="", description="Check if Mountain Quail once lived at this location"
    )

    county: str = Field(
        default="",
        description=(
            "County where the historic quail location is found .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    nearest_city_or_landmark: str = Field(
        default="",
        description=(
            "Name of the nearest city or recognizable landmark to the location .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    general_description_of_area: str = Field(
        default="",
        description=(
            "Brief description of the terrain, vegetation, and surroundings of the area .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    last_years_birds_were_seen: str = Field(
        default="",
        description=(
            "Most recent year or range of years when quail were last observed at this "
            'location .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    last_year_area_was_checked_for_birds: str = Field(
        default="",
        description=(
            "Most recent year when you or others checked this area for quail, even if none "
            'were seen .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    gps_coordinates: str = Field(
        default="",
        description=(
            "GPS coordinates of the historic quail location, if available .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    usgs_7_1_2_minute_map_name: str = Field(
        default="",
        description=(
            "Name of the USGS 7 1/2-minute topographic map covering this location, if known "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class NearestHistoricWaterSource(BaseModel):
    """Information about nearby historic water sources related to the quail location"""

    at_the_location_above_was_there_a_nearby_water_source: Literal[
        "Yes", "No", "Unknown", "N/A", ""
    ] = Field(
        default="", description="Indicate whether there was a water source near the quail location"
    )

    yes_nearby_water_source: BooleanLike = Field(
        default="", description="Check if there was a nearby water source at the location"
    )

    no_nearby_water_source: BooleanLike = Field(
        default="", description="Check if there was no nearby water source at the location"
    )

    unknown_nearby_water_source: BooleanLike = Field(
        default="", description="Check if it is unknown whether there was a nearby water source"
    )

    type_of_water: Literal[
        "Spring", "Stock Tank", "Windmill/Well", "Guzzler", "Mine Shaft", "Other", "N/A", ""
    ] = Field(default="", description="Type of water source near the quail location")

    spring: BooleanLike = Field(default="", description="Check if the water source was a spring")

    stock_tank: BooleanLike = Field(
        default="", description="Check if the water source was a stock tank"
    )

    windmill_well: BooleanLike = Field(
        default="", description="Check if the water source was a windmill or well"
    )

    guzzler: BooleanLike = Field(default="", description="Check if the water source was a guzzler")

    mine_shaft: BooleanLike = Field(
        default="", description="Check if the water source was a mine shaft"
    )

    other_type_of_water: str = Field(
        default="",
        description=(
            "Describe the water source if it is of another type .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_water_source: str = Field(
        default="",
        description=(
            "Name of the water source, if it has one .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_description_and_or_gps_coordinates: str = Field(
        default="",
        description=(
            "Description and/or GPS coordinates of the water source location .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    approximate_distance_from_quail: str = Field(
        default="",
        description=(
            "Approximate distance between the water source and the quail location (include "
            'units) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    is_this_source_still_available: Literal["Yes", "No", "N/A", ""] = Field(
        default="", description="Indicate whether this water source is still available"
    )

    yes_source_still_available: BooleanLike = Field(
        default="", description="Check if the water source is still available"
    )

    no_source_still_available: BooleanLike = Field(
        default="", description="Check if the water source is no longer available"
    )

    if_no_what_was_the_last_year_it_was_known_to_have_water: str = Field(
        default="",
        description=(
            "Last year in which this water source was known to contain water .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class QuailDeclineHabitatSurveyNewsletter(BaseModel):
    """
        Western Birds
    The Newsletter's Newsletter

    Quail Decline: Habitat and Historic Range Loss Survey

        The number and distribution of the three quail species that live in California has declined over the past 50 years, but the state Department of Fish and Wildlife has little data about short-term or long-term declines, and no comprehensive program to restore or increase bird numbers and distribution. Hunters across the state are being asked to help determine areas where quail no longer exist. This survey is also seeking to define loss of historic water sources that are critical to desert and foothill quail in late spring, summer, and fall. This information can come from you, parents, grandparents, or old hunting buddies. We are hoping to put together a comprehensive database of lost water sources and lost historic quail range.
    """

    respondent_information: RespondentInformation = Field(..., description="Respondent Information")
    quail_location_and_history: QuailLocationandHistory = Field(
        ..., description="Quail Location and History"
    )
    nearest_historic_water_source: NearestHistoricWaterSource = Field(
        ..., description="Nearest Historic Water Source"
    )
