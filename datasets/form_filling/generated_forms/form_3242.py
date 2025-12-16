from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FromMoYrRow(BaseModel):
    """Single row in FROM (Mo/Yr)"""

    from_mo_yr: str = Field(default="", description="From_Mo_Yr")
    to_mo_yr: str = Field(default="", description="To_Mo_Yr")
    city: str = Field(default="", description="City")
    township_if_applicable: str = Field(default="", description="Township_If_Applicable")
    county: str = Field(default="", description="County")
    state: str = Field(default="", description="State")


class ApplicationType(BaseModel):
    """Type of permit to carry application being submitted"""

    new: BooleanLike = Field(
        ..., description="Check if this is an application for a new permit to carry a pistol."
    )

    renewal: BooleanLike = Field(
        ..., description="Check if this application is to renew an existing permit."
    )

    personal_data_change: BooleanLike = Field(
        ...,
        description=(
            "Check if this application is to report a personal data change on an existing permit."
        ),
    )

    replacement: BooleanLike = Field(
        ..., description="Check if this application is for a replacement permit card."
    )

    emergency: BooleanLike = Field(
        ..., description="Check if this is an emergency permit application."
    )


class DataPracticesAdvisoryAcknowledgment(BaseModel):
    """Applicant acknowledgment of the Data Practices Advisory"""

    signature: str = Field(
        ...,
        description=(
            "Applicant’s signature acknowledging the data practices advisory. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(
        ..., description="Date the applicant signs the application."
    )  # YYYY-MM-DD format


class RequiredPersonalData(BaseModel):
    """Applicant’s identifying and contact information"""

    name_last_first_middle_jr_sr: str = Field(
        ...,
        description=(
            "Full legal name including last, first, middle, and suffix (Jr/Sr) if "
            'applicable. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    birth_date: str = Field(..., description="Applicant’s date of birth.")  # YYYY-MM-DD format

    phone_no: str = Field(
        ...,
        description=(
            'Primary contact telephone number. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    maiden_name_if_applicable_or_other_names_you_have_used: str = Field(
        ...,
        description=(
            "Any maiden name or other legal names you have previously used. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    present_residence_address: str = Field(
        ...,
        description=(
            "Current street address of your primary residence. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_township_if_applicable: str = Field(
        ...,
        description=(
            "City or township of your present residence address. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    county: str = Field(
        ...,
        description=(
            "County of your present residence address. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of your present residence address.")

    zip_code: str = Field(..., description="ZIP code for your present residence address.")

    sex: str = Field(
        ...,
        description=(
            "Sex as listed on your identification document. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    height: str = Field(
        ...,
        description=(
            "Height (typically in feet and inches). .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    weight: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Weight (typically in pounds)."
    )

    eye_color: str = Field(
        ...,
        description=(
            "Eye color as listed on your identification document. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    hair_color: str = Field(
        ...,
        description=(
            "Hair color as listed on your identification document. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    state_id_issuing_state: str = Field(
        ..., description="State that issued your driver’s license, state ID, or passport."
    )

    drivers_license_state_id_or_passport_number: str = Field(
        ...,
        description=(
            "Number from your driver’s license, state identification card, or passport. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    distinguishing_physical_characteristics_including_scars_marks_tattoos_etc: str = Field(
        default="",
        description=(
            "Describe any distinguishing physical characteristics such as scars, marks, or "
            'tattoos. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class PreviousResidencesPast5Years(BaseModel):
    """Applicant’s residence history for the past five years"""

    from_mo_yr: List[FromMoYrRow] = Field(
        default="",
        description=(
            "Table of previous residences over the past 5 years, including from/to dates "
            "and locations."
        ),
    )  # List of table rows

    to_mo_yr: str = Field(
        default="",
        description=(
            "End month and year for a previous residence entry (captured within the "
            'previous residences table). .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city_previous_residence: str = Field(
        default="",
        description=(
            "City for each previous residence (captured within the previous residences "
            'table). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    township_if_applicable_previous_residence: str = Field(
        default="",
        description=(
            "Township, if applicable, for each previous residence (captured within the "
            'previous residences table). .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    county_previous_residence: str = Field(
        default="",
        description=(
            "County for each previous residence (captured within the previous residences "
            'table). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    state_previous_residence: str = Field(
        default="",
        description=(
            "State for each previous residence (captured within the previous residences table)."
        ),
    )


class MinnesotaUniformFirearmApplicationPermitToCarryAPistol(BaseModel):
    """
        MINNESOTA UNIFORM FIREARM APPLICATION
    PERMIT TO CARRY A PISTOL

        As an applicant for a permit to carry a pistol, you are being asked to provide private data about yourself that will be used to check various databases to determine your eligibility to possess a firearm.
        You may refuse to provide this data. If you refuse, the background check cannot be completed and your application will not be processed. Providing the data will permit the background check to be completed. The result of the check may be either affirmative or negative. The data you provide may be shared with other criminal justice agencies, via court order or as authorized or required by law.
    """

    application_type: ApplicationType = Field(..., description="Application Type")
    data_practices_advisory_acknowledgment: DataPracticesAdvisoryAcknowledgment = Field(
        ..., description="Data Practices Advisory Acknowledgment"
    )
    required_personal_data: RequiredPersonalData = Field(..., description="Required Personal Data")
    previous_residences_past_5_years: PreviousResidencesPast5Years = Field(
        ..., description="Previous Residences (Past 5 Years)"
    )
