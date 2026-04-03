from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Payment(BaseModel):
    """Membership payment information"""

    my_45_00_check_or_money_order_is_enclosed: BooleanLike = Field(
        default="",
        description=(
            "Check this box if you are enclosing a $45.00 check or money order with the application"
        ),
    )


class ServiceInformation(BaseModel):
    """Dates and branch of military service"""

    aug_2_1990_present_persian_gulf: BooleanLike = Field(
        default="",
        description="Check if your active military service includes this Persian Gulf era",
    )

    dec_20_1989_jan_31_1990_panama: BooleanLike = Field(
        default="", description="Check if your active military service includes this Panama era"
    )

    aug_24_1982_jul_31_1984_lebanon_grenada: BooleanLike = Field(
        default="",
        description="Check if your active military service includes this Lebanon/Grenada era",
    )

    feb_28_1961_may_7_1975_vietnam_war: BooleanLike = Field(
        default="",
        description="Check if your active military service includes this Vietnam War era",
    )

    jun_25_1950_jan_31_1955_korean_war: BooleanLike = Field(
        default="", description="Check if your active military service includes this Korean War era"
    )

    dec_7_1941_dec_31_1946_wwii: BooleanLike = Field(
        default="",
        description="Check if your active military service includes this World War II era",
    )

    apr_6_1917_nov_11_1918_wwi: BooleanLike = Field(
        default="",
        description="Check if your active military service includes this World War I era",
    )

    dec_7_1941_present_other_eras: BooleanLike = Field(
        default="",
        description=(
            "Check if your active military service falls in other qualifying eras from Dec "
            "7, 1941 to present"
        ),
    )

    us_army: BooleanLike = Field(
        default="", description="Check if your branch of service is the US Army"
    )

    us_navy: BooleanLike = Field(
        default="", description="Check if your branch of service is the US Navy"
    )

    us_air_force: BooleanLike = Field(
        default="", description="Check if your branch of service is the US Air Force"
    )

    us_marines: BooleanLike = Field(
        default="", description="Check if your branch of service is the US Marine Corps"
    )

    us_coast_guard: BooleanLike = Field(
        default="", description="Check if your branch of service is the US Coast Guard"
    )

    us_merchant_marine_wwii_only: BooleanLike = Field(
        default="", description="Check if you served in the US Merchant Marine during World War II"
    )


class ApplicantInformation(BaseModel):
    """Personal and contact details of the applicant"""

    name: str = Field(
        ...,
        description=(
            'Applicant’s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street mailing address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            'City, state, and ZIP code .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        default="",
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            'Email address for correspondence .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    birth_date: str = Field(..., description="Applicant’s date of birth")  # YYYY-MM-DD format

    signature: str = Field(
        ...,
        description=(
            "Applicant’s signature certifying eligibility and application information .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ReferralandQuestions(BaseModel):
    """How you heard about The American Legion and any questions"""

    how_where_you_heard_about_the_american_legion_and_questions: str = Field(
        default="",
        description=(
            "Explain how or where you heard about The American Legion and list any "
            'questions you have .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class OfficeUse(BaseModel):
    """Bottom signature or initials for internal/office use"""

    bottom_signature_or_initials: str = Field(
        default="",
        description=(
            "Signature or initials at the bottom of the form, if required by processing "
            'office .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class TheAmericanLegionDepartmentOfNewYorkMembershipApplication(BaseModel):
    """
        THE AMERICAN LEGION DEPARTMENT OF NEW YORK
    MEMBERSHIP APPLICATION

        YES!  I’ll help my fellow veterans by becoming a member of The American Legion.  I certify that I served at least one day of active military duty during the dates marked below and was honorably discharged or am still serving honorably.
    """

    payment: Payment = Field(..., description="Payment")
    service_information: ServiceInformation = Field(..., description="Service Information")
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    referral_and_questions: ReferralandQuestions = Field(..., description="Referral and Questions")
    office_use: OfficeUse = Field(..., description="Office Use")
