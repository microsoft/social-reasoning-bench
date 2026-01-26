from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantContactInformation(BaseModel):
    """Company and primary contact details for the application"""

    fax_phone: str = Field(
        default="",
        description=(
            'Fax phone number, including area code .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_of_company: str = Field(
        ...,
        description=(
            "Legal name of the company applying for the permit .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street mailing address of the company .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            "Primary telephone number for the company, including area code .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for the company address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    person_responsible_on_location: str = Field(
        ...,
        description=(
            "Name, job title, and phone number of the person in charge at the location .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class LocationInformation(BaseModel):
    """Details about the site and specific areas to be used"""

    location_of_site_desired: str = Field(
        ...,
        description=(
            "General description of the site or area requested, referencing the enclosed "
            'map .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    specific_locations_to_be_used: str = Field(
        ...,
        description=(
            "Detailed description of specific parts of the site to be used and "
            'corresponding markings on the map .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class TypePurposeofUse(BaseModel):
    """Type of production and purpose of the commercial use"""

    type_of_use_commercial_production: BooleanLike = Field(
        ..., description="Check if the use is a commercial production"
    )

    type_of_use_nonprofit_production: BooleanLike = Field(
        ..., description="Check if the use is a nonprofit production"
    )

    type_of_use_community_service_production: BooleanLike = Field(
        ..., description="Check if the use is a community service production"
    )

    type_of_use_educational_production: BooleanLike = Field(
        ..., description="Check if the use is an educational production"
    )

    purpose_feature_film: BooleanLike = Field(
        ..., description="Check if the purpose of use is a feature film"
    )

    purpose_advertisement: BooleanLike = Field(
        ..., description="Check if the purpose of use is an advertisement"
    )

    purpose_documentary: BooleanLike = Field(
        ..., description="Check if the purpose of use is a documentary"
    )

    purpose_still_photograph: BooleanLike = Field(
        ..., description="Check if the purpose of use is still photography"
    )

    purpose_video: BooleanLike = Field(..., description="Check if the purpose of use is video")

    purpose_other_state: str = Field(
        default="",
        description=(
            "If the purpose is other than the listed options, describe it here .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    name_of_feature_film_tv_series_commercial_product_music_video_group_other: str = Field(
        ...,
        description=(
            "Title or name of the feature film, TV series, product, music video group, or "
            'other project .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class SchedulePersonnel(BaseModel):
    """Timing of use and number of people involved"""

    dates_of_use: str = Field(
        ...,
        description=(
            "Planned dates during which the site will be used .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hours_of_use: str = Field(
        ...,
        description=(
            'Planned hours of use for each day .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    number_of_personnel_involved: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Total number of people on site, including production staff, cast, and crew",
    )


class ActivityAnimals(BaseModel):
    """Description of planned activities and any animals used"""

    statement_of_activity: str = Field(
        ...,
        description=(
            "Detailed description of all activities that will occur on location .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    animals_how_many: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of animals that will be used on location"
    )

    animals_what_kind: str = Field(
        default="",
        description=(
            "Species or type of animals that will be used on location .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    animals_none: BooleanLike = Field(
        default="", description="Check if no animals will be used on location"
    )


class BLMCommercialUseApplication(BaseModel):
    """UNITED STATES DEPARTMENT OF THE INTERIOR
    BUREAU OF LAND MANAGEMENT

    COMMERCIAL USE APPLICATION"""

    applicant__contact_information: ApplicantContactInformation = Field(
        ..., description="Applicant & Contact Information"
    )
    location_information: LocationInformation = Field(..., description="Location Information")
    type__purpose_of_use: TypePurposeofUse = Field(..., description="Type & Purpose of Use")
    schedule__personnel: SchedulePersonnel = Field(..., description="Schedule & Personnel")
    activity__animals: ActivityAnimals = Field(..., description="Activity & Animals")
