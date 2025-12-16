from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ReferralInformation(BaseModel):
    """Who referred the applicant and when"""

    referred_by_name_org: str = Field(
        ...,
        description=(
            "Name of the person and organization that referred the applicant .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    title: str = Field(
        ...,
        description=(
            "Title or role of the person making the referral .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    referral_date: str = Field(..., description="Date the referral was made")  # YYYY-MM-DD format


class ApplicantInformation(BaseModel):
    """Basic personal and contact details for the applicant"""

    print_client_name: str = Field(
        ...,
        description=(
            'Printed full name of the client .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    age: Union[float, Literal["N/A", ""]] = Field(..., description="Client's age in years")

    home_address: str = Field(
        ...,
        description=(
            "Street address of the client's residence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    apt: str = Field(
        default="",
        description=(
            "Apartment or unit number, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the client\'s residence .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zip_code: str = Field(..., description="ZIP code of the client's residence")

    language_spoken_at_home: str = Field(
        default="",
        description=(
            "Primary language spoken in the client's home .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Primary home or contact phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        default="",
        description=(
            'Client\'s mobile phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class IncomeandEmployment(BaseModel):
    """Applicant and partner income and employment duration"""

    income: str = Field(
        ...,
        description=(
            "Total income from wages, SSI, Social Security, and other sources for the "
            'applicant .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    years_on_job_applicant: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years the applicant has been at their current job"
    )

    partners_income: str = Field(
        default="",
        description=(
            "Total income from wages, SSI, Social Security, and other sources for the "
            'partner .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    years_on_job_partner: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years the partner has been at their current job"
    )


class MonthlyExpensesandDebts(BaseModel):
    """Housing, medical, credit, and other recurring expenses"""

    mortgage_or_rent: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly mortgage or rent payment amount"
    )

    medical_expense: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly medical expense amount"
    )

    dental: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly dental expense amount"
    )

    finance_co: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly payment amount to finance companies"
    )

    credit_cards: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly credit card payment total"
    )

    medications: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly cost of medications"
    )

    other_debts: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly payments for other debts not listed elsewhere"
    )

    hospitals: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly payments or expenses related to hospital bills"
    )

    car1_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Model year of the first car"
    )

    car1_make: str = Field(
        default="",
        description=(
            'Make or brand of the first car .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    car1_monthly_payment: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly payment amount for the first car"
    )

    car2_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Model year of the second car"
    )

    car2_make: str = Field(
        default="",
        description=(
            'Make or brand of the second car .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    car2_monthly_payment: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly payment amount for the second car"
    )


class ApplicantCertification(BaseModel):
    """Applicant signature and date"""

    applicant_signature: str = Field(
        ...,
        description=(
            'Signature of the applicant .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    applicant_signature_date: str = Field(
        ..., description="Date the applicant signed the form"
    )  # YYYY-MM-DD format


class HistoryandProblemDescription(BaseModel):
    """Brief history and nature of the problem"""

    brief_history_nature_of_problem_line_1: str = Field(
        ...,
        description=(
            "First line of description of the history and nature of the problem .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    brief_history_nature_of_problem_line_2: str = Field(
        ...,
        description=(
            "Second line of description of the history and nature of the problem .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    brief_history_nature_of_problem_line_3: str = Field(
        ...,
        description=(
            "Third line of description of the history and nature of the problem .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class RequestedServiceandProvider(BaseModel):
    """Details of the service needed and provider information"""

    service_needed: str = Field(
        ...,
        description=(
            'Description of the service requested .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    provider: str = Field(
        ...,
        description=(
            'Name of the service provider .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    provider_contact: str = Field(
        default="",
        description=(
            "Contact person at the provider organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    provider_hours: str = Field(
        default="",
        description=(
            "Hours of service or availability for the provider .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    provider_address: str = Field(
        ...,
        description=(
            'Street address of the provider .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    provider_city: str = Field(
        ...,
        description=(
            'City where the provider is located .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    provider_zip_code: str = Field(..., description="ZIP code for the provider's address")

    email: str = Field(
        default="",
        description=(
            "Email address for contacting the applicant or provider .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            "Fax number for sending or receiving documents .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    cost_of_service_with_discount: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total cost of the service after any discounts are applied"
    )


class InternalReviewandBoardAction(BaseModel):
    """Staff investigation and board presentation details"""

    investigated_by_signature: str = Field(
        ...,
        description=(
            "Signature of the person who investigated the application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    investigated_by_date: str = Field(
        ..., description="Date the investigation was completed"
    )  # YYYY-MM-DD format

    presented_to_board_date: str = Field(
        ..., description="Date the application was presented to the Board of Directors"
    )  # YYYY-MM-DD format

    presented_to_board_by_signature: str = Field(
        ...,
        description=(
            "Signature of the person who presented the application to the Board of "
            'Directors .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class CrippledChildrensReliefAssociationOfOrangeCountyAdultApplication(BaseModel):
    """
        CRIPPLED CHILDREN'S RELIEF ASSOCIATION OF ORANGE COUNTY
    ADULT APPLICATION

        ''
    """

    referral_information: ReferralInformation = Field(..., description="Referral Information")
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    income_and_employment: IncomeandEmployment = Field(..., description="Income and Employment")
    monthly_expenses_and_debts: MonthlyExpensesandDebts = Field(
        ..., description="Monthly Expenses and Debts"
    )
    applicant_certification: ApplicantCertification = Field(
        ..., description="Applicant Certification"
    )
    history_and_problem_description: HistoryandProblemDescription = Field(
        ..., description="History and Problem Description"
    )
    requested_service_and_provider: RequestedServiceandProvider = Field(
        ..., description="Requested Service and Provider"
    )
    internal_review_and_board_action: InternalReviewandBoardAction = Field(
        ..., description="Internal Review and Board Action"
    )
