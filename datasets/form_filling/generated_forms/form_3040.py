from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicationType(BaseModel):
    """Whether this is a new or renewal operator's license application"""

    renewal_50_00: BooleanLike = Field(
        default="", description="Check if this application is for a renewal operator's license"
    )

    new_50_00: BooleanLike = Field(
        default="", description="Check if this application is for a new operator's license"
    )


class ApplicantInformation(BaseModel):
    """Personal details of the applicant"""

    applicants_full_name_first: str = Field(
        ...,
        description=(
            'Applicant\'s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    applicants_full_name_middle: str = Field(
        default="",
        description=(
            'Applicant\'s middle name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    applicants_full_name_last: str = Field(
        ...,
        description=(
            'Applicant\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    home_address: str = Field(
        ...,
        description=(
            'Applicant\'s home street address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of applicant\'s home address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of applicant's home address")

    zip: str = Field(..., description="ZIP code of applicant's home address")

    age_in_years: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Applicant's age in years"
    )

    date_of_birth: str = Field(..., description="Applicant's date of birth")  # YYYY-MM-DD format

    place_of_birth: str = Field(
        ...,
        description=(
            "City and state or country where the applicant was born .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    drivers_license_number: str = Field(
        ...,
        description=(
            "Applicant's driver's license number .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    drivers_license_expiration_date: str = Field(
        ..., description="Expiration date of the applicant's driver's license"
    )  # YYYY-MM-DD format


class EstablishmentInformation(BaseModel):
    """Information about the establishment where the applicant will work"""

    name_of_establishment: str = Field(
        ...,
        description=(
            "Name of the establishment where the applicant will be employed .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    establishment_phone_number: str = Field(
        ...,
        description=(
            'Phone number of the establishment .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ResidencyInformation(BaseModel):
    """Applicant's residency history in Wisconsin and the Town of Brooklyn"""

    resident_state_wisconsin_since: str = Field(
        ..., description="Date since when the applicant has been a continuous resident of Wisconsin"
    )  # YYYY-MM-DD format

    resident_town_brooklyn_since: str = Field(
        ..., description="Date since when the applicant has been a resident of the Town of Brooklyn"
    )  # YYYY-MM-DD format


class TrainingandCourseInformation(BaseModel):
    """Alcohol awareness and responsible beverage server training details"""

    completed_alcohol_awareness_course_yes: BooleanLike = Field(
        ..., description="Check if the applicant has completed the alcohol awareness course"
    )

    completed_alcohol_awareness_course_no: BooleanLike = Field(
        ..., description="Check if the applicant has not completed the alcohol awareness course"
    )

    where_alcohol_awareness_course_completed: str = Field(
        default="",
        description=(
            "Location where the alcohol awareness course was completed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    completed_responsible_beverage_servers_training_course: BooleanLike = Field(
        default="",
        description=(
            "Indicate if the applicant has completed the Responsible Beverage Server's "
            "Training Course"
        ),
    )

    responsible_beverage_servers_training_course: BooleanLike = Field(
        default="",
        description=(
            "Indicate completion of the Responsible Beverage Server's Training Course at issuance"
        ),
    )

    responsible_beverage_servers_training_course_on_file: BooleanLike = Field(
        default="",
        description="Check if proof of the Responsible Beverage Server's Training Course is on file",
    )


class ConvictionsandViolations(BaseModel):
    """Disclosure of any prior convictions or license law violations"""

    convicted_felony_or_law_violation_yes: BooleanLike = Field(
        ..., description="Check if the applicant has been convicted of a felony or law violation"
    )

    convicted_felony_or_law_violation_no: BooleanLike = Field(
        ...,
        description="Check if the applicant has not been convicted of a felony or law violation",
    )

    date_of_such_conviction: str = Field(
        default="", description="Date of the conviction, if applicable"
    )  # YYYY-MM-DD format

    name_of_court: str = Field(
        default="",
        description=(
            "Name of the court where the conviction occurred .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    nature_of_offense_felony_or_law_violation: str = Field(
        default="",
        description=(
            "Description of the felony or law violation offense .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    convicted_violating_license_law_nature_of_offense: str = Field(
        default="",
        description=(
            "Description of any offense involving violation of license laws or ordinances "
            "regulating sale of fermented malt beverages or intoxicating liquors .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ApplicantCertification(BaseModel):
    """Applicant’s certification and signature"""

    signature_of_applicant: str = Field(
        ...,
        description=(
            "Signature of the applicant certifying the accuracy of the application .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class NotaryClerkCertification(BaseModel):
    """Sworn date before the clerk"""

    day_of_month_sworn: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day of the month on which the application was sworn"
    )

    month_sworn: str = Field(
        default="",
        description=(
            "Month in which the application was sworn .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PaymentInformation(BaseModel):
    """Application fee payment details"""

    check_payment_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid by check for the application fee"
    )

    cash_payment_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount paid in cash for the application fee"
    )


class OfficeUseOnly(BaseModel):
    """For municipal/clerical processing of the license"""

    date_issued: str = Field(
        default="", description="Date the license was issued"
    )  # YYYY-MM-DD format

    license_number: str = Field(
        default="",
        description=(
            'Assigned operator\'s license number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    disposition_of_investigative_check: str = Field(
        default="",
        description=(
            "Notes on the disposition or results of the investigative check .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ApplicationForAnOperatorsLicense(BaseModel):
    """
    Application for an Operator's License

    Application for an Operator's License
    """

    application_type: ApplicationType = Field(..., description="Application Type")
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    establishment_information: EstablishmentInformation = Field(
        ..., description="Establishment Information"
    )
    residency_information: ResidencyInformation = Field(..., description="Residency Information")
    training_and_course_information: TrainingandCourseInformation = Field(
        ..., description="Training and Course Information"
    )
    convictions_and_violations: ConvictionsandViolations = Field(
        ..., description="Convictions and Violations"
    )
    applicant_certification: ApplicantCertification = Field(
        ..., description="Applicant Certification"
    )
    notary__clerk_certification: NotaryClerkCertification = Field(
        ..., description="Notary / Clerk Certification"
    )
    payment_information: PaymentInformation = Field(..., description="Payment Information")
    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
