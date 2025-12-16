from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class DriverInformation(BaseModel):
    """Student driver details and contact information"""

    student_name: str = Field(
        ...,
        description=(
            'Full legal name of the student driver .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    grade: str = Field(
        ...,
        description=(
            "Current school grade level of the student (e.g., 9, 10, 11, 12) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Street address of the student’s residence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_zip: str = Field(
        ...,
        description=(
            "City and ZIP code for the student’s address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    valid_class_e_dl_number: str = Field(
        ...,
        description=(
            "Driver’s license number for a valid Class E license .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    state_driver_license: str = Field(..., description="State that issued the driver’s license")

    driver_contact_number: str = Field(
        ...,
        description=(
            "Primary contact phone number for the student driver .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PermitVehicleInformation(BaseModel):
    """Information about the vehicle being registered for a parking permit"""

    year: Union[float, Literal["N/A", ""]] = Field(..., description="Model year of the vehicle")

    make: str = Field(
        ...,
        description=(
            "Manufacturer of the vehicle (e.g., Ford, Toyota) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    model: str = Field(
        ...,
        description=(
            "Model of the vehicle (e.g., Camry, F-150) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    color: str = Field(
        ...,
        description=(
            'Primary exterior color of the vehicle .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    tag_number: str = Field(
        ...,
        description=(
            "License plate (tag) number of the vehicle .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_tag: str = Field(
        ..., description="State where the vehicle is registered (license plate state)"
    )

    vehicle_vin_number: str = Field(
        ...,
        description=(
            'Vehicle Identification Number (VIN) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    insurance_company_and_policy_number: str = Field(
        ...,
        description=(
            "Name of the insurance company and the policy number covering the vehicle .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    registered_owner_name: str = Field(
        ...,
        description=(
            "Full name of the person listed as the registered owner of the vehicle .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    registered_owner_address: str = Field(
        ...,
        description=(
            "Mailing address of the registered owner of the vehicle .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class OtherInformation(BaseModel):
    """Student programs, activities, and club participation"""

    off_campus_dual_enrollment_student_yes: BooleanLike = Field(
        default="", description="Check YES if the student is an off-campus dual enrollment student"
    )

    off_campus_dual_enrollment_student_no: BooleanLike = Field(
        default="",
        description="Check NO if the student is not an off-campus dual enrollment student",
    )

    dct_student_yes: BooleanLike = Field(
        default="", description="Check YES if the student is enrolled in DCT"
    )

    dct_student_no: BooleanLike = Field(
        default="", description="Check NO if the student is not enrolled in DCT"
    )

    attend_locklin_tech_yes: BooleanLike = Field(
        default="",
        description="Check YES if the student attends Locklin Tech during the school day",
    )

    attend_locklin_tech_no: BooleanLike = Field(
        default="",
        description="Check NO if the student does not attend Locklin Tech during the school day",
    )

    marine_science_beach_yes: BooleanLike = Field(
        default="",
        description="Check YES if the student is enrolled in Marine Science at the beach",
    )

    marine_science_beach_no: BooleanLike = Field(
        default="",
        description="Check NO if the student is not enrolled in Marine Science at the beach",
    )

    njrotc_member_yes: BooleanLike = Field(
        default="", description="Check YES if the student is a member of NJROTC"
    )

    njrotc_member_no: BooleanLike = Field(
        default="", description="Check NO if the student is not a member of NJROTC"
    )

    band_or_color_guard_yes: BooleanLike = Field(
        default="", description="Check YES if the student participates in Band or Color Guard"
    )

    band_or_color_guard_no: BooleanLike = Field(
        default="",
        description="Check NO if the student does not participate in Band or Color Guard",
    )

    participate_in_sport_yes: BooleanLike = Field(
        default="", description="Check YES if the student participates in any sport"
    )

    participate_in_sport_no: BooleanLike = Field(
        default="", description="Check NO if the student does not participate in any sport"
    )

    if_yes_what_sports: str = Field(
        default="",
        description=(
            "List the sports the student participates in, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    participate_in_any_clubs_yes: BooleanLike = Field(
        default="", description="Check YES if the student participates in any school clubs"
    )

    participate_in_any_clubs_no: BooleanLike = Field(
        default="", description="Check NO if the student does not participate in any school clubs"
    )

    if_yes_what_clubs: str = Field(
        default="",
        description=(
            "List the clubs the student participates in, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Signatures(BaseModel):
    """Student and parent signatures with dates"""

    student_signature: str = Field(
        ...,
        description=(
            "Signature of the student acknowledging the information provided .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    student_signature_date: str = Field(
        ..., description="Date the student signed the application"
    )  # YYYY-MM-DD format

    parent_signature: str = Field(
        ...,
        description=(
            "Signature of a parent or guardian as required for the application .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    parent_signature_date: str = Field(
        ..., description="Date the parent or guardian signed the application"
    )  # YYYY-MM-DD format


class OfficeUseOnly(BaseModel):
    """School/administrative completion of permit details"""

    decal_number: str = Field(
        default="",
        description=(
            "Assigned parking decal number (office use) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    permit_number: str = Field(
        default="",
        description=(
            "Assigned parking permit number (office use) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    amount_paid: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total amount paid for the parking permit (office use)"
    )

    approval: str = Field(
        default="",
        description=(
            "Signature, initials, or name of the approving school official .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class NavarreHighSchoolParkingPermitApplication20212022(BaseModel):
    """
        Navarre High School
    Parking Permit
    Application 2021-2022

        ''
    """

    driver_information: DriverInformation = Field(..., description="Driver Information")
    permit_vehicle_information: PermitVehicleInformation = Field(
        ..., description="Permit Vehicle Information"
    )
    other_information: OtherInformation = Field(..., description="Other Information")
    signatures: Signatures = Field(..., description="Signatures")
    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
