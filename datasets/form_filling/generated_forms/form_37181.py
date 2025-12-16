from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PersonalInformation(BaseModel):
    """Applicant's personal and contact details, and prior internship history"""

    first_name: str = Field(
        ...,
        description=(
            'Applicant\'s legal first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    middle: str = Field(
        default="",
        description=(
            'Applicant\'s middle name or initial .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    last: str = Field(
        ...,
        description=(
            'Applicant\'s legal last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    street_address: str = Field(
        ...,
        description=(
            'Street address for mailing purposes .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    apt_unit: str = Field(
        default="",
        description=(
            "Apartment, unit, or suite number (if applicable) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of residence .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(
        ..., description="State of residence (two-letter abbreviation if applicable)"
    )

    zip_code: str = Field(..., description="5-digit ZIP code (plus 4 if known)")

    phone_number: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    cell_phone_number: str = Field(
        default="",
        description=(
            'Mobile or cell phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        ...,
        description=(
            'Primary email address for contact .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    internship_applied_before_yes: BooleanLike = Field(
        ...,
        description=(
            "Select if you have previously applied for or held an internship with Montgomery County"
        ),
    )

    internship_applied_before_no: BooleanLike = Field(
        ...,
        description=(
            "Select if you have not previously applied for or held an internship with "
            "Montgomery County"
        ),
    )

    prior_internship_department_and_dates: str = Field(
        default="",
        description=(
            "If you answered yes, list the department and the dates of your prior "
            'internship or application .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class Availability(BaseModel):
    """Applicant's weekly availability and desired hours"""

    hours_per_week: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Approximate number of hours per week you are seeking to work"
    )

    monday_morning_approx_8_30_1: BooleanLike = Field(
        default="",
        description="Check if you are generally available Monday mornings (approximately 8:30–1)",
    )

    tuesday_morning_approx_8_30_1: BooleanLike = Field(
        default="",
        description="Check if you are generally available Tuesday mornings (approximately 8:30–1)",
    )

    wednesday_morning_approx_8_30_1: BooleanLike = Field(
        default="",
        description="Check if you are generally available Wednesday mornings (approximately 8:30–1)",
    )

    thursday_morning_approx_8_30_1: BooleanLike = Field(
        default="",
        description="Check if you are generally available Thursday mornings (approximately 8:30–1)",
    )

    friday_morning_approx_8_30_1: BooleanLike = Field(
        default="",
        description="Check if you are generally available Friday mornings (approximately 8:30–1)",
    )

    monday_afternoon_approx_12_30_4_15: BooleanLike = Field(
        default="",
        description=(
            "Check if you are generally available Monday afternoons (approximately 12:30–4:15)"
        ),
    )

    tuesday_afternoon_approx_12_30_4_15: BooleanLike = Field(
        default="",
        description=(
            "Check if you are generally available Tuesday afternoons (approximately 12:30–4:15)"
        ),
    )

    wednesday_afternoon_approx_12_30_4_15: BooleanLike = Field(
        default="",
        description=(
            "Check if you are generally available Wednesday afternoons (approximately 12:30–4:15)"
        ),
    )

    thursday_afternoon_approx_12_30_4_15: BooleanLike = Field(
        default="",
        description=(
            "Check if you are generally available Thursday afternoons (approximately 12:30–4:15)"
        ),
    )

    friday_afternoon_approx_12_30_4_15: BooleanLike = Field(
        default="",
        description=(
            "Check if you are generally available Friday afternoons (approximately 12:30–4:15)"
        ),
    )

    monday_all_day_approx_8_30_4_15: BooleanLike = Field(
        default="",
        description="Check if you are generally available all day Monday (approximately 8:30–4:15)",
    )

    tuesday_all_day_approx_8_30_4_15: BooleanLike = Field(
        default="",
        description="Check if you are generally available all day Tuesday (approximately 8:30–4:15)",
    )

    wednesday_all_day_approx_8_30_4_15: BooleanLike = Field(
        default="",
        description=(
            "Check if you are generally available all day Wednesday (approximately 8:30–4:15)"
        ),
    )

    thursday_all_day_approx_8_30_4_15: BooleanLike = Field(
        default="",
        description="Check if you are generally available all day Thursday (approximately 8:30–4:15)",
    )

    friday_all_day_approx_8_30_4_15: BooleanLike = Field(
        default="",
        description="Check if you are generally available all day Friday (approximately 8:30–4:15)",
    )


class MontgomeryCountyInternshipApplication(BaseModel):
    """
    Montgomery County Internship Application

    ''
    """

    personal_information: PersonalInformation = Field(..., description="Personal Information")
    availability: Availability = Field(..., description="Availability")
