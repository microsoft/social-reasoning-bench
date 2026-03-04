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
    """Contact information for the company and responsible person"""

    fax_phone: str = Field(
        default="",
        description=(
            'Fax phone number including area code .If you cannot fill this, write "N/A". '
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
            'Mailing address of the company .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            "Primary telephone number including area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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

    name_title_phone_person_responsible_on_location: str = Field(
        ...,
        description=(
            "Name, title, and phone number of the person in charge on location .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class LocationInformation(BaseModel):
    """Details about the site and specific areas to be used"""

    location_of_site_desired: str = Field(
        ...,
        description=(
            "General description of the desired site location .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    specific_locations_to_be_used: str = Field(
        ...,
        description=(
            "Specific parts of the area to be used (e.g., which part of lake bed, dunes, "
            'etc.) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class TypeandPurposeofUse(BaseModel):
    """Type of production and purpose of use"""

    commercial_production: BooleanLike = Field(
        default="", description="Check if the type of use is commercial production"
    )

    nonprofit_production: BooleanLike = Field(
        default="", description="Check if the type of use is nonprofit production"
    )

    community_service_production: BooleanLike = Field(
        default="", description="Check if the type of use is community service production"
    )

    educational_production: BooleanLike = Field(
        default="", description="Check if the type of use is educational production"
    )

    feature_film: BooleanLike = Field(
        default="", description="Check if the purpose of use is a feature film"
    )

    advertisement: BooleanLike = Field(
        default="", description="Check if the purpose of use is an advertisement"
    )

    documentary: BooleanLike = Field(
        default="", description="Check if the purpose of use is a documentary"
    )

    still_photograph: BooleanLike = Field(
        default="", description="Check if the purpose of use is still photography"
    )

    video: BooleanLike = Field(default="", description="Check if the purpose of use is video")

    other_state: str = Field(
        default="",
        description=(
            "Describe other purpose of use if not listed above .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    state_name_of_feature_film_tv_series_commercial_product_music_video_group_other: str = Field(
        ...,
        description=(
            "Title or name of the feature film, TV series, commercial product, music video "
            'group, or other project .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class UseScheduleandPersonnel(BaseModel):
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
            "Planned hours of use for the site on the specified dates .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    number_of_personnel_involved_include_production_cast_and_crew: Union[
        float, Literal["N/A", ""]
    ] = Field(
        ...,
        description="Total number of people involved, including production staff, cast, and crew",
    )


class ActivityandAnimals(BaseModel):
    """Description of activities and animals to be used on location"""

    statement_of_activity_to_take_place_in_detail: str = Field(
        ...,
        description=(
            "Detailed description of all activities that will take place on location .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    animals_to_be_used_on_location_how_many: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of animals that will be used on location"
    )

    what_kind: str = Field(
        default="",
        description=(
            "Types or species of animals to be used on location .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    none: BooleanLike = Field(
        default="", description="Check if no animals will be used on location"
    )


class UsDeptInteriorBLMCommercialUseApplication(BaseModel):
    """UNITED STATES DEPARTMENT OF THE INTERIOR
    BUREAU OF LAND MANAGEMENT

    COMMERCIAL USE APPLICATION (revised 8/13/98)"""

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    location_information: LocationInformation = Field(..., description="Location Information")
    type_and_purpose_of_use: TypeandPurposeofUse = Field(..., description="Type and Purpose of Use")
    use_schedule_and_personnel: UseScheduleandPersonnel = Field(
        ..., description="Use Schedule and Personnel"
    )
    activity_and_animals: ActivityandAnimals = Field(..., description="Activity and Animals")
