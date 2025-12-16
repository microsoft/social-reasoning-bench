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
    """Basic personal and contact details of the applicant"""

    name: str = Field(
        ...,
        description=(
            'Applicant\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this application is completed")  # YYYY-MM-DD format

    address: str = Field(
        ...,
        description=(
            "Street address, including apartment or unit number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of current residence .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of current residence")

    zip: str = Field(..., description="ZIP or postal code of current residence")

    home_phone: str = Field(
        default="",
        description=(
            "Home telephone number, including area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        ...,
        description=(
            "Primary mobile/cell phone number, including area code .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Primary email address for contact .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_available: str = Field(
        ..., description="Date you are available to begin work"
    )  # YYYY-MM-DD format

    social_security: str = Field(..., description="Social Security Number")

    desired_salary: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Desired rate of pay (hourly or annual, as applicable)"
    )

    position_applied_for: str = Field(
        ...,
        description=(
            "Job title or position you are applying for .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class EmploymentEligibilityBackground(BaseModel):
    """Eligibility to work, prior relationship with the company, and background information"""

    citizen_of_united_states: BooleanLike = Field(
        ..., description="Indicate whether you are a citizen of the United States"
    )

    citizen_of_united_states_no: BooleanLike = Field(
        ..., description="Indicate whether you are not a citizen of the United States"
    )

    prior_employment_with_company: BooleanLike = Field(
        ...,
        description=(
            "Indicate if you have previously applied for employment or worked for this company"
        ),
    )

    prior_employment_with_company_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate if you have not previously applied for employment or worked for this company"
        ),
    )

    prior_employment_details: str = Field(
        default="",
        description=(
            "Details of prior applications or employment with this company, including dates "
            'and positions .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    friends_or_relatives_employed: BooleanLike = Field(
        ...,
        description="Indicate if you have friends or relatives currently working for this company",
    )

    friends_or_relatives_employed_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate if you do not have friends or relatives currently working for this company"
        ),
    )

    friends_or_relatives_details: str = Field(
        default="",
        description=(
            "Names and relationships of friends or relatives who work for this company .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reliable_transportation: BooleanLike = Field(
        ..., description="Indicate if you have reliable transportation to and from work"
    )

    reliable_transportation_no: BooleanLike = Field(
        ..., description="Indicate if you do not have reliable transportation to and from work"
    )

    convicted_crime_other_than_minor_traffic: BooleanLike = Field(
        ...,
        description=(
            "Indicate if you have been convicted of any crime other than minor traffic violations"
        ),
    )

    convicted_crime_other_than_minor_traffic_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate if you have not been convicted of any crime other than minor traffic "
            "violations"
        ),
    )

    convicted_felony: BooleanLike = Field(
        ..., description="Indicate if you have ever been convicted of a felony"
    )

    convicted_felony_no: BooleanLike = Field(
        ..., description="Indicate if you have not been convicted of a felony"
    )

    valid_drivers_license: BooleanLike = Field(
        ..., description="Indicate if you currently hold a valid driver's license"
    )

    valid_drivers_license_no: BooleanLike = Field(
        ..., description="Indicate if you do not currently hold a valid driver's license"
    )


class MountJoyWireCorporationJobApplicationForm(BaseModel):
    """
        MOUNT JOY WIRE CORPORATION

    JOB APPLICATION FORM

        Our team is always seeking dedicated individuals interested in a career with Mount Joy Wire. The company success over the past 20 Year's can be credited to the quality and dedication of our employees. We are a smoke and drug free environment with a zero tolerance policy.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    employment_eligibility__background: EmploymentEligibilityBackground = Field(
        ..., description="Employment Eligibility & Background"
    )
