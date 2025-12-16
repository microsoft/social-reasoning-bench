from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OfficeUseOnly(BaseModel):
    """For police department records and licensing decisions"""

    date_received_in_records: str = Field(
        default="", description="Date the application was received in records (office use only)"
    )  # YYYY-MM-DD format

    by: str = Field(
        default="",
        description=(
            "Initials or name of records staff receiving the application (office use only) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    fee_paid: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount of fee paid (office use only)"
    )

    date_office_use_fee: str = Field(
        default="", description="Date fee was paid (office use only)"
    )  # YYYY-MM-DD format

    license_number_office_use_only: str = Field(
        default="",
        description=(
            "Assigned license number (office use only) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    approved: BooleanLike = Field(
        default="", description="Indicates the application is approved (office use only)"
    )

    denied: BooleanLike = Field(
        default="", description="Indicates the application is denied (office use only)"
    )

    date_approval_denial: str = Field(
        default="", description="Date of approval or denial decision (office use only)"
    )  # YYYY-MM-DD format

    date_of_expiration: str = Field(
        default="", description="Expiration date of the issued license (office use only)"
    )  # YYYY-MM-DD format


class ApplicationInformation(BaseModel):
    """Application type, applicant, and business details"""

    new_license: BooleanLike = Field(
        ..., description="Check if this application is for a new license"
    )

    license_renewal: BooleanLike = Field(
        ..., description="Check if this application is for a license renewal"
    )

    temporary_license: BooleanLike = Field(
        ..., description="Check if this application is for a temporary license"
    )

    present_license_number_for_license_renewal: str = Field(
        default="",
        description=(
            "Current license number, required if applying for renewal .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_license_for_license_renewal: str = Field(
        default="",
        description="Original date of the current license, required if applying for renewal",
    )  # YYYY-MM-DD format

    name_of_applicant: str = Field(
        ...,
        description=(
            'Full legal name of the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(..., description="Applicant's date of birth")  # YYYY-MM-DD format

    resident_address: str = Field(
        ...,
        description=(
            'Applicant\'s full residential address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    resident_address_address: str = Field(
        ...,
        description=(
            "Street address of the applicant's residence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    resident_address_city: str = Field(
        ...,
        description=(
            'City of the applicant\'s residence .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    resident_address_state: str = Field(..., description="State of the applicant's residence")

    resident_address_zip: str = Field(..., description="ZIP code of the applicant's residence")

    name_of_business_under_which_applicant_will_operate: str = Field(
        ...,
        description=(
            "Legal or trade name of the business under which the applicant will operate .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address_at_which_applicant_will_operate_place_of_business_and_maintain_records: str = Field(
        ...,
        description=(
            "Full address of the business location where operations and records are "
            'maintained .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    place_of_business_address: str = Field(
        ...,
        description=(
            "Street address of the business location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    place_of_business_city: str = Field(
        ...,
        description=(
            'City of the business location .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    place_of_business_state: str = Field(..., description="State of the business location")

    place_of_business_zip: str = Field(..., description="ZIP code of the business location")

    business_phone: str = Field(
        ...,
        description=(
            'Primary business telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    alternate_phone: str = Field(
        default="",
        description=(
            'Alternate contact telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    hours_of_operation: str = Field(
        ...,
        description=(
            "Days and hours during which the business operates .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class BackgroundInformation(BaseModel):
    """Criminal history and related details"""

    have_you_ever_been_convicted_of_a_felony_or_misdemeanor_yes: BooleanLike = Field(
        ..., description="Check YES if you have ever been convicted of a felony or misdemeanor"
    )

    have_you_ever_been_convicted_of_a_felony_or_misdemeanor_no: BooleanLike = Field(
        ..., description="Check NO if you have never been convicted of a felony or misdemeanor"
    )

    if_yes_list_charges_location_of_offense_court_and_penalty_imposed: str = Field(
        default="",
        description=(
            "If you answered YES, provide details of each conviction including charge, "
            'location, court, and penalty .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    charges_row_1: str = Field(
        default="",
        description=(
            'Charge for the first listed offense .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    location_row_1: str = Field(
        default="",
        description=(
            'Location of the first listed offense .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    court_row_1: str = Field(
        default="",
        description=(
            'Court for the first listed offense .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    penalty_row_1: str = Field(
        default="",
        description=(
            "Penalty imposed for the first listed offense .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    charges_row_2: str = Field(
        default="",
        description=(
            'Charge for the second listed offense .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    location_row_2: str = Field(
        default="",
        description=(
            'Location of the second listed offense .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    court_row_2: str = Field(
        default="",
        description=(
            'Court for the second listed offense .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    penalty_row_2: str = Field(
        default="",
        description=(
            "Penalty imposed for the second listed offense .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    charges_row_3: str = Field(
        default="",
        description=(
            'Charge for the third listed offense .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    location_row_3: str = Field(
        default="",
        description=(
            'Location of the third listed offense .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    court_row_3: str = Field(
        default="",
        description=(
            'Court for the third listed offense .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    penalty_row_3: str = Field(
        default="",
        description=(
            "Penalty imposed for the third listed offense .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    charges_row_4: str = Field(
        default="",
        description=(
            'Charge for the fourth listed offense .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    location_row_4: str = Field(
        default="",
        description=(
            'Location of the fourth listed offense .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    court_row_4: str = Field(
        default="",
        description=(
            'Court for the fourth listed offense .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    penalty_row_4: str = Field(
        default="",
        description=(
            "Penalty imposed for the fourth listed offense .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class pythonPreciousMetalGemsDealerLicenseLongviewOrdinance76(BaseModel):
    """
        APPLICATION FOR
    PRECIOUS METAL AND GEMS DEALER LICENSE
    LONGVIEW CITY ORDINANCE CHAPTER 76

        ''
    """

    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
    application_information: ApplicationInformation = Field(
        ..., description="Application Information"
    )
    background_information: BackgroundInformation = Field(..., description="Background Information")
