from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicationDetails(BaseModel):
    """Basic information about this scholarship application and amount requested"""

    date_of_application: str = Field(
        ..., description="Date when this scholarship application is completed"
    )  # YYYY-MM-DD format

    amount_requested_3000_max: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Dollar amount of scholarship funds requested, up to $3,000"
    )


class ApplicantInformation(BaseModel):
    """Personal details about the applicant"""

    last_name: str = Field(
        ...,
        description=(
            'Applicant\'s last name (family name) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Applicant\'s first name (given name) .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    month_of_birth: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month of birth (1–12)"
    )

    day_of_birth: Union[float, Literal["N/A", ""]] = Field(..., description="Day of birth (1–31)")

    year_of_birth: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year of birth (four digits)"
    )

    graduation_year: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Year the applicant graduated from Beverly Hills High School or relevant institution"
        ),
    )

    yes_related_to_bhaaa_board_or_staff: BooleanLike = Field(
        ...,
        description=(
            "Check if the applicant is related to any BHAAA Board of Directors member or staff"
        ),
    )

    no_not_related_to_bhaaa_board_or_staff: BooleanLike = Field(
        ...,
        description=(
            "Check if the applicant is not related to any BHAAA Board of Directors member or staff"
        ),
    )


class ContactInformation(BaseModel):
    """Mailing and contact details for the applicant"""

    street: str = Field(
        ...,
        description=(
            "Street address for mailing (house number and street name) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City for the mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(
        ..., description="State for the mailing address (two-letter abbreviation if in the U.S.)"
    )

    zip: str = Field(..., description="ZIP or postal code for the mailing address")

    daytime_telephone_number: str = Field(
        ...,
        description=(
            "Primary daytime phone number where the applicant can be reached .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    e_mail_address: str = Field(
        ...,
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class AthleticProgramInformation(BaseModel):
    """Details about the applicant’s participation in sports or athletic programs"""

    sports_played_or_athletic_program: str = Field(
        ...,
        description=(
            "Sport(s) or athletic program(s) in which the applicant participated .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class FinancialNeedandMedicalDetails(BaseModel):
    """Explanation of financial need and any related medical circumstances"""

    description_of_need_for_financial_assistance: str = Field(
        ...,
        description=(
            "Explain why financial assistance is needed and how the scholarship funds will "
            'be used .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    details_if_funds_related_to_medical_bills_or_condition: str = Field(
        default="",
        description=(
            "If applicable, provide brief details about medical bills or conditions related "
            'to the requested funds .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class BhaaaJoeSuttonScholarshipFundApplication(BaseModel):
    """
        Beverly Hills Athletic Alumni Association
    BHAAA Assist Joe Sutton Scholarship Fund Application

        ''
    """

    application_details: ApplicationDetails = Field(..., description="Application Details")
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    contact_information: ContactInformation = Field(..., description="Contact Information")
    athletic_program_information: AthleticProgramInformation = Field(
        ..., description="Athletic Program Information"
    )
    financial_need_and_medical_details: FinancialNeedandMedicalDetails = Field(
        ..., description="Financial Need and Medical Details"
    )
