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
    """Basic contact information for the applicant"""

    name: str = Field(
        ...,
        description=(
            'Applicant\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_incl_street_city_state_zip: str = Field(
        ...,
        description=(
            "Complete mailing address including street, city, state, and zip code .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Primary phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Primary email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class RegionRankings(BaseModel):
    """Rankings for each region to which the applicant is willing to be placed"""

    region_1_a_massachusetts_worcester_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 1A Massachusetts "
            "Worcester, or leave blank if not applying"
        ),
    )

    region_1_b_new_york_elmira_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 1B New York Elmira, or "
            "leave blank if not applying"
        ),
    )

    region_2_rhode_island_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 2 Rhode Island, or leave "
            "blank if not applying"
        ),
    )

    region_3_nyc_bronxville_near_yonkers_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 3 NYC Bronxville (near "
            "Yonkers), or leave blank if not applying"
        ),
    )

    region_4_pennsylvania_new_jersey_philadelphia_and_surrounding_areas_ranking: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 4 Pennsylvania & New "
            "Jersey Philadelphia and surrounding areas, or leave blank if not applying"
        ),
    )

    region_4_lehigh_valley_harrisburg_northern_new_jersey_west_virginia_ranking: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 4 Lehigh Valley, "
            "Harrisburg, Northern New Jersey, West Virginia, or leave blank if not applying"
        ),
    )

    region_4_martinsburg_ranson_parkersburg_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 4 Martinsburg/Ranson, "
            "Parkersburg, or leave blank if not applying"
        ),
    )

    region_6_a_north_carolina_elkin_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 6A North Carolina Elkin, "
            "or leave blank if not applying"
        ),
    )

    region_6_b_georgia_thomaston_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 6B Georgia Thomaston, or "
            "leave blank if not applying"
        ),
    )

    region_7_florida_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 7 Florida, or leave blank "
            "if not applying"
        ),
    )

    region_8_a_ohio_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 8A Ohio, or leave blank "
            "if not applying"
        ),
    )

    region_8_b_indiana_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 8B Indiana, or leave "
            "blank if not applying"
        ),
    )

    region_8_a_illinois_chicago_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 8A Illinois Chicago, or "
            "leave blank if not applying"
        ),
    )

    region_9_b_minnesota_minneapolis_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 9B Minnesota Minneapolis, "
            "or leave blank if not applying"
        ),
    )

    region_9_c_missouri_kansas_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 9C Missouri, Kansas, or "
            "leave blank if not applying"
        ),
    )

    region_10_texas_greater_houston_area_corpus_christi_ranking: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 10 Texas Greater Houston "
            "area, Corpus Christi, or leave blank if not applying"
        ),
    )

    region_10_a_colorado_denver_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 10A Colorado Denver, or "
            "leave blank if not applying"
        ),
    )

    region_11_b_colorado_colorado_springs_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 11B Colorado Colorado "
            "Springs, or leave blank if not applying"
        ),
    )

    region_11_c_colorado_grand_junction_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 11C Colorado Grand "
            "Junction, or leave blank if not applying"
        ),
    )

    region_11_d_montana_billings_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 11D Montana Billings, or "
            "leave blank if not applying"
        ),
    )

    region_12_a_california_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 12A California, or leave "
            "blank if not applying"
        ),
    )

    region_12_b_hawaii_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 12B Hawaii, or leave "
            "blank if not applying"
        ),
    )

    region_12_c_nevada_arizona_ranking: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Enter your ranking number (1, 2, 3, etc.) for Region 12C Nevada & Arizona, or "
            "leave blank if not applying"
        ),
    )


class AdditionalGeographicInformation(BaseModel):
    """Optional notes about geographic preferences or placement information"""

    additional_geographic_placement_information: str = Field(
        default="",
        description=(
            "Optional: provide any additional geographic preferences or information about "
            'locations .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class ApplicationCoverSheetFall2021Match(BaseModel):
    """
    Application Cover Sheet Fall 2021 Match

    Complete this form, save it, and upload it to the supplemental materials section of DICAS and to our Sodexo Smartsheet online document.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    region_rankings: RegionRankings = Field(..., description="Region Rankings")
    additional_geographic_information: AdditionalGeographicInformation = Field(
        ..., description="Additional Geographic Information"
    )
