from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class HonoreeInformation(BaseModel):
    """Information about the individual being honored"""

    donation_in_the_name_of: str = Field(
        ...,
        description=(
            "Name of the individual being honored with the $100 donation (up to 24 "
            "characters including spaces for the physical Wall of Honor) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    birth_date: str = Field(
        default="", description="Birth date of the individual being honored"
    )  # YYYY-MM-DD format

    birth_date_month: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month of birth (if collected separately)"
    )

    birth_date_day: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day of birth (if collected separately)"
    )

    birth_date_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year of birth (if collected separately)"
    )

    birth_date_location: str = Field(
        default="",
        description=(
            "Place of birth (city, state, or other location details) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    father: str = Field(
        default="",
        description=(
            'Name of the individual\'s father .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mother: str = Field(
        default="",
        description=(
            'Name of the individual\'s mother .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    death_date: str = Field(
        default="", description="Death date of the individual (if applicable)"
    )  # YYYY-MM-DD format

    death_date_month: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month of death (if collected separately)"
    )

    death_date_day: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day of death (if collected separately)"
    )

    death_date_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year of death (if collected separately)"
    )

    death_date_location: str = Field(
        default="",
        description=(
            "Place of death (city, state, or other location details) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    burial_location: str = Field(
        default="",
        description=(
            'Burial location of the individual .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    chenango_county_affiliation: str = Field(
        default="",
        description=(
            "Description (250–500 words) of the individual's affiliation with Chenango "
            'County for the virtual Wall of Honor .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    activity_accomplishment_occupation: str = Field(
        default="",
        description=(
            "Primary activity, accomplishment, or occupation to appear on the physical Wall "
            "of Honor (up to 24 characters including spaces) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_information: str = Field(
        default="",
        description=(
            "Any additional information about the individual .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class DonorInformation(BaseModel):
    """Contact information for the person making the donation"""

    donor_name_and_address: str = Field(
        ...,
        description=(
            "Full name and mailing address of the donor .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Donor\'s phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            'Donor\'s email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    relationship: str = Field(
        default="",
        description=(
            "Donor's relationship to the individual being honored .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ChenangosHeritageWallOfHonorRegistrationForm(BaseModel):
    """
        Chenango’s Heritage
    Wall of Honor Registration Form

        Each tax-deductible $100 donation can be made for any individual affiliated with Chenango County. The name, primary occupation and/or activity, birth year and death year (if applicable) will be displayed on the “Chenango’s Heritage” Wall of Honor located in the Ward School No. 2 main entrance. Please include a high resolution image (300 dpi) of the individual for the virtual Wall of Honor as well.
    """

    honoree_information: HonoreeInformation = Field(..., description="Honoree Information")
    donor_information: DonorInformation = Field(..., description="Donor Information")
