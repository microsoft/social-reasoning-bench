from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EmployeeApplicantInformation(BaseModel):
    """Employer, applicant, and residence details"""

    name_of_employer: str = Field(
        ...,
        description=(
            'Legal name of the employer .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_hired: str = Field(
        ..., description="Date the applicant was hired by the employer"
    )  # YYYY-MM-DD format

    name_of_applicant: str = Field(
        ...,
        description=(
            "Full legal name of the applicant/employee .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(..., description="Applicant's date of birth")  # YYYY-MM-DD format

    resident_address: str = Field(
        ...,
        description=(
            "Full residential street address of the applicant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Street address line (number, street, apartment/suite if applicable) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the residential address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of the residential address")

    zip: str = Field(..., description="ZIP code of the residential address")


class CriminalBackgroundInformation(BaseModel):
    """Felony/misdemeanor conviction history and details"""

    felony_misdemeanor_conviction: BooleanLike = Field(
        ..., description="Indicate whether you have ever been convicted of a felony or misdemeanor"
    )

    charges_location_court_penalty_explanation: str = Field(
        default="",
        description=(
            "If you answered YES, provide details of each conviction including charge, "
            'location, court, and penalty .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    charges_1: str = Field(
        default="",
        description=(
            'First listed criminal charge .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    location_1: str = Field(
        default="",
        description=(
            "Location (city/county/state) of the first listed offense .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    court_1: str = Field(
        default="",
        description=(
            "Court where the first listed case was heard .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    penalty_1: str = Field(
        default="",
        description=(
            "Penalty imposed for the first listed conviction .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    charges_2: str = Field(
        default="",
        description=(
            'Second listed criminal charge .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    location_2: str = Field(
        default="",
        description=(
            "Location (city/county/state) of the second listed offense .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    court_2: str = Field(
        default="",
        description=(
            "Court where the second listed case was heard .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    penalty_2: str = Field(
        default="",
        description=(
            "Penalty imposed for the second listed conviction .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    charges_3: str = Field(
        default="",
        description=(
            'Third listed criminal charge .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    location_3: str = Field(
        default="",
        description=(
            "Location (city/county/state) of the third listed offense .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    court_3: str = Field(
        default="",
        description=(
            "Court where the third listed case was heard .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    penalty_3: str = Field(
        default="",
        description=(
            "Penalty imposed for the third listed conviction .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    charges_4: str = Field(
        default="",
        description=(
            'Fourth listed criminal charge .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    location_4: str = Field(
        default="",
        description=(
            "Location (city/county/state) of the fourth listed offense .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    court_4: str = Field(
        default="",
        description=(
            "Court where the fourth listed case was heard .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    penalty_4: str = Field(
        default="",
        description=(
            "Penalty imposed for the fourth listed conviction .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CivilLitigationHistory(BaseModel):
    """Civil litigation related to sales or purchases of goods or services"""

    civil_litigation_involvement: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you have ever been or are currently a party to civil "
            "litigation related to sales or purchases of goods or services"
        ),
    )

    if_yes_court: str = Field(
        default="",
        description=(
            "If you answered YES, name of the court for the referenced civil litigation .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    if_yes_date: str = Field(
        default="",
        description="If you answered YES, date associated with the referenced civil litigation",
    )  # YYYY-MM-DD format

    civil_court_1: str = Field(
        default="",
        description=(
            "First listed court for civil litigation matter .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_1_civil_litigation: str = Field(
        default="",
        description=(
            "Location (city/county/state) of the first listed civil litigation court .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    status_outcome_1: str = Field(
        default="",
        description=(
            "Status or outcome of the first listed civil litigation case .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    involved_parties_1: str = Field(
        default="",
        description=(
            "Names of parties involved in the first listed civil litigation case .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    civil_court_2: str = Field(
        default="",
        description=(
            "Second listed court for civil litigation matter .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    location_2_civil_litigation: str = Field(
        default="",
        description=(
            "Location (city/county/state) of the second listed civil litigation court .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    status_outcome_2: str = Field(
        default="",
        description=(
            "Status or outcome of the second listed civil litigation case .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    involved_parties_2: str = Field(
        default="",
        description=(
            "Names of parties involved in the second listed civil litigation case .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    civil_court_3: str = Field(
        default="",
        description=(
            "Third listed court for civil litigation matter .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_3_civil_litigation: str = Field(
        default="",
        description=(
            "Location (city/county/state) of the third listed civil litigation court .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    status_outcome_3: str = Field(
        default="",
        description=(
            "Status or outcome of the third listed civil litigation case .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    involved_parties_3: str = Field(
        default="",
        description=(
            "Names of parties involved in the third listed civil litigation case .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ApplicantCertificationNotarization(BaseModel):
    """Applicant signature and notary information"""

    applicant_signature: str = Field(
        ...,
        description=(
            "Signature of the applicant attesting to the truth and completeness of the "
            'information .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    applicant_signature_date: str = Field(
        ..., description="Date the applicant signed this form"
    )  # YYYY-MM-DD format

    notary_day: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day of the month when the notary witnessed the signature"
    )

    notary_month: str = Field(
        ...,
        description=(
            "Month when the notary witnessed the signature .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    notary_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year (last two digits) when the notary witnessed the signature"
    )

    notary_public: str = Field(
        ...,
        description=(
            'Signature of the notary public .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    my_commission_expires: str = Field(
        ..., description="Expiration date of the notary public's commission"
    )  # YYYY-MM-DD format


class EmployeeAddendum(BaseModel):
    """
    EMPLOYEE ADDENDUM

    EACH CURRENT EMPLOYEE MUST HAVE THIS DOCUMENT ON FILE WITH POLICE RECORDS
    """

    employee__applicant_information: EmployeeApplicantInformation = Field(
        ..., description="Employee & Applicant Information"
    )
    criminal_background_information: CriminalBackgroundInformation = Field(
        ..., description="Criminal Background Information"
    )
    civil_litigation_history: CivilLitigationHistory = Field(
        ..., description="Civil Litigation History"
    )
    applicant_certification__notarization: ApplicantCertificationNotarization = Field(
        ..., description="Applicant Certification & Notarization"
    )
