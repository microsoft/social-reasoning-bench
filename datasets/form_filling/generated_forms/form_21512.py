from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantCompanyInformation(BaseModel):
    """Contact details for the applying company and responsible person"""

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
            "Legal name of the company submitting the application .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Mailing street address of the company .If you cannot fill this, write "N/A". '
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

    name_title_phone_person_responsible_on_location: str = Field(
        ...,
        description=(
            "Name, job title, and phone number of the person in charge on location .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class LocationInformation(BaseModel):
    """Details about the desired site and map reference"""

    location_of_site_desired: str = Field(
        ...,
        description=(
            "General description of the site location requested .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    see_enclosed_map: BooleanLike = Field(
        default="",
        description=(
            "Indicates that the enclosed map has been reviewed and marked with the desired area"
        ),
    )


class UseTypeandPurpose(BaseModel):
    """Type of production and purpose of use"""

    type_of_use_commercial_production: BooleanLike = Field(
        ..., description="Check if the use is for a commercial production"
    )

    type_of_use_nonprofit_production: BooleanLike = Field(
        ..., description="Check if the use is for a nonprofit production"
    )

    type_of_use_community_service_production: BooleanLike = Field(
        ..., description="Check if the use is for a community service production"
    )

    type_of_use_educational_production: BooleanLike = Field(
        ..., description="Check if the use is for an educational production"
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
            "Describe any other purpose of use not listed above .If you cannot fill this, "
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


class ScheduleandPersonnel(BaseModel):
    """Dates, hours, and number of people involved"""

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
        description="Total number of people involved, including production staff, cast, and crew",
    )


class ActivityandAnimals(BaseModel):
    """Description of activities and any animals used on location"""

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
            "Type or species of animals to be used on location .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    none: BooleanLike = Field(
        default="", description="Check if no animals will be used on location"
    )


class BLMCommercialUseApplication(BaseModel):
    """UNITED STATES DEPARTMENT OF THE INTERIOR
    BUREAU OF LAND MANAGEMENT

    COMMERCIAL USE APPLICATION (revised 8/13/98)"""

    applicant__company_information: ApplicantCompanyInformation = Field(
        ..., description="Applicant / Company Information"
    )
    location_information: LocationInformation = Field(..., description="Location Information")
    use_type_and_purpose: UseTypeandPurpose = Field(..., description="Use Type and Purpose")
    schedule_and_personnel: ScheduleandPersonnel = Field(..., description="Schedule and Personnel")
    activity_and_animals: ActivityandAnimals = Field(..., description="Activity and Animals")
