from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RentalInformation(BaseModel):
    """Property being applied for and basic applicant personal details"""

    rental_address: str = Field(
        ...,
        description=(
            "Full address of the rental unit being applied for .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name: str = Field(
        ...,
        description=(
            'Applicant\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    birthdate: str = Field(..., description="Applicant's date of birth")  # YYYY-MM-DD format

    social_security: str = Field(..., description="Applicant's Social Security number")

    cell_phone: str = Field(
        ...,
        description=(
            'Applicant\'s primary cell phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    work_phone: str = Field(
        default="",
        description=(
            'Applicant\'s work phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    nearest_living_relative_name: str = Field(
        ...,
        description=(
            "Full name of applicant's nearest living relative .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    nearest_living_relative_phone: str = Field(
        ...,
        description=(
            "Phone number of applicant's nearest living relative .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    number_of_occupants: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of people who will occupy the rental unit"
    )

    relationships_to_self: str = Field(
        ...,
        description=(
            "Describe how each occupant is related to the applicant (e.g., spouse, child, "
            'roommate) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    list_any_pets: str = Field(
        default="",
        description=(
            "List all pets that will live in the rental (names, types, sizes, etc.) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    breeds: str = Field(
        default="",
        description=(
            'Breed or breeds of the listed pets .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    maiden_name_or_alias_if_divorced_previous_name: str = Field(
        default="",
        description=(
            "Any maiden name, alias, or previous legal name if divorced .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ResidenceHistory(BaseModel):
    """Current and previous residence and landlord information"""

    present_address: str = Field(
        ...,
        description=(
            "Applicant's current residential address (street, city, state) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    present_address_zip: str = Field(..., description="ZIP code for the present address")

    present_address_phone: str = Field(
        default="",
        description=(
            "Phone number associated with the present address (if different from cell/work) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    how_long_at_present_address: str = Field(
        ...,
        description=(
            "Length of time the applicant has lived at the present address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    reason_for_moving: str = Field(
        ...,
        description=(
            "Brief explanation of why the applicant is moving .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    current_rent: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Monthly rent amount currently being paid at present address"
    )

    current_landlord_name: str = Field(
        ...,
        description=(
            "Name of the current landlord or property manager .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    current_landlord_phone: str = Field(
        ...,
        description=(
            "Phone number of the current landlord or property manager .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    previous_address: str = Field(
        default="",
        description=(
            "Applicant's prior residential address before the present one .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    previous_address_zip: str = Field(default="", description="ZIP code for the previous address")

    previous_rent: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly rent amount paid at the previous address"
    )

    previous_landlord_name: str = Field(
        default="",
        description=(
            "Name of the previous landlord or property manager .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    previous_landlord_phone: str = Field(
        default="",
        description=(
            "Phone number of the previous landlord or property manager .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class VehicleInformation(BaseModel):
    """Vehicles associated with the applicant"""

    car_1_make: str = Field(
        default="",
        description=(
            "Make of the first vehicle (e.g., Ford, Toyota) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    car_1_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Model year of the first vehicle"
    )

    car_1_model: str = Field(
        default="",
        description=(
            'Model of the first vehicle .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    car_1_color: str = Field(
        default="",
        description=(
            'Color of the first vehicle .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    car_1_lic_plate: str = Field(
        default="",
        description=(
            "License plate number of the first vehicle .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    car_2_make: str = Field(
        default="",
        description=(
            "Make of the second vehicle (e.g., Ford, Toyota) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    car_2_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Model year of the second vehicle"
    )

    car_2_model: str = Field(
        default="",
        description=(
            'Model of the second vehicle .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    car_2_color: str = Field(
        default="",
        description=(
            'Color of the second vehicle .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    car_2_lic_plate: str = Field(
        default="",
        description=(
            "License plate number of the second vehicle .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class OfficeUseOnly(BaseModel):
    """For management/office processing and decision"""

    payment_cash: BooleanLike = Field(
        default="", description="Indicates if payment was made in cash"
    )

    payment_check_number: str = Field(
        default="",
        description=(
            "Check number if payment was made by check .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    payment_money_order: BooleanLike = Field(
        default="", description="Indicates if payment was made by money order"
    )

    fica_negative: BooleanLike = Field(
        default="", description="Indicates if the FICA/credit report returned negative information"
    )

    eviction: BooleanLike = Field(
        default="", description="Indicates if the applicant has an eviction record"
    )

    criminal: BooleanLike = Field(
        default="", description="Indicates if the applicant has a criminal record"
    )

    denied: BooleanLike = Field(default="", description="Indicates if the application was denied")

    approved: BooleanLike = Field(
        default="", description="Indicates if the application was approved"
    )

    init: str = Field(
        default="",
        description=(
            "Initials of the staff member processing the application decision .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    adverse_action_letter_sent: BooleanLike = Field(
        default="", description="Indicates if an adverse action letter was sent to the applicant"
    )

    lease_signing_date: str = Field(
        default="", description="Date on which the lease was signed"
    )  # YYYY-MM-DD format

    move_in_date: str = Field(default="", description="Scheduled move-in date")  # YYYY-MM-DD format

    move_out_date: str = Field(
        default="", description="Scheduled move-out date"
    )  # YYYY-MM-DD format


class ApplicationToRentTenantsPersonalAndCreditInformation(BaseModel):
    """
        APPLICATION TO RENT
    TENANT'S PERSONAL AND CREDIT INFORMATION

        APPLICATION TO RENT TENANT'S PERSONAL AND CREDIT INFORMATION MUST BE FILLED OUT COMPLETELY TO BE PROCESSED
    """

    rental_information: RentalInformation = Field(..., description="Rental Information")
    residence_history: ResidenceHistory = Field(..., description="Residence History")
    vehicle_information: VehicleInformation = Field(..., description="Vehicle Information")
    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
