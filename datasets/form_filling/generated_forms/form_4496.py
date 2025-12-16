from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class GeneralInformation(BaseModel):
    """Basic information about the company and its operations"""

    company_name: str = Field(
        ...,
        description=(
            'Legal name of the company .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street address of the company .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City where the company is located .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    year_company_established: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year the company was founded"
    )

    country: str = Field(
        ...,
        description=(
            'Country where the company is located .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    number_of_employees: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of employees in the company"
    )

    telephone: str = Field(
        ...,
        description=(
            "Primary company telephone number including country and area code .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Primary company email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            "Company fax number including country and area code .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    web_site: str = Field(
        default="",
        description=(
            'Company website URL .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    company_registration_number: str = Field(
        ...,
        description=(
            "Official company registration or license number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    number_of_students_sent_abroad_per_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Approximate number of students the company sends abroad each year"
    )

    name_of_your_main_bank: str = Field(
        ...,
        description=(
            "Name of the primary banking institution used by the company .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    bank_routing: str = Field(
        ...,
        description=(
            "Bank routing number for the main bank account .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    bank_account: str = Field(
        ...,
        description=(
            "Bank account number for the main bank account .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    bank_address: str = Field(
        ...,
        description=(
            "Street address of the main bank branch .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    bank_phone: str = Field(
        default="",
        description=(
            "Telephone number of the main bank branch .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    summary_of_changes_in_company_ownership_last_5_years: str = Field(
        default="",
        description=(
            "Brief description of any ownership changes in the past five years .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ChiefExecutiveOfficer(BaseModel):
    """Contact and address details for the Chief Executive Officer"""

    chief_executive_officer_name: str = Field(
        ...,
        description=(
            "Full name of the Chief Executive Officer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    chief_executive_officer_title: str = Field(
        ...,
        description=(
            "Job title of the Chief Executive Officer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    chief_executive_officer_address: str = Field(
        default="",
        description=(
            "Mailing address of the Chief Executive Officer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    chief_executive_officer_city: str = Field(
        default="",
        description=(
            "City of the Chief Executive Officer's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    chief_executive_officer_telephone: str = Field(
        default="",
        description=(
            "Telephone number for the Chief Executive Officer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    chief_executive_officer_country: str = Field(
        default="",
        description=(
            "Country of the Chief Executive Officer's address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    chief_executive_officer_fax: str = Field(
        default="",
        description=(
            "Fax number for the Chief Executive Officer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    chief_executive_officer_cell: str = Field(
        default="",
        description=(
            "Mobile phone number for the Chief Executive Officer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    chief_executive_officer_email: str = Field(
        default="",
        description=(
            "Email address of the Chief Executive Officer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ChiefFinancialOfficer(BaseModel):
    """Contact and address details for the Chief Financial Officer"""

    chief_financial_officer_name: str = Field(
        ...,
        description=(
            "Full name of the Chief Financial Officer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    chief_financial_officer_title: str = Field(
        ...,
        description=(
            "Job title of the Chief Financial Officer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    chief_financial_officer_address: str = Field(
        default="",
        description=(
            "Mailing address of the Chief Financial Officer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    chief_financial_officer_city: str = Field(
        default="",
        description=(
            "City of the Chief Financial Officer's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    chief_financial_officer_telephone: str = Field(
        default="",
        description=(
            "Telephone number for the Chief Financial Officer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    chief_financial_officer_country: str = Field(
        default="",
        description=(
            "Country of the Chief Financial Officer's address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    chief_financial_officer_fax: str = Field(
        default="",
        description=(
            "Fax number for the Chief Financial Officer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    chief_financial_officer_cell: str = Field(
        default="",
        description=(
            "Mobile phone number for the Chief Financial Officer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    chief_financial_officer_email: str = Field(
        default="",
        description=(
            "Email address of the Chief Financial Officer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class USMarketManager(BaseModel):
    """Contact and address details for the US Market Manager"""

    us_market_manager_name: str = Field(
        ...,
        description=(
            'Full name of the US Market Manager .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    us_market_manager_title: str = Field(
        ...,
        description=(
            'Job title of the US Market Manager .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    us_market_manager_address: str = Field(
        default="",
        description=(
            "Mailing address of the US Market Manager .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    us_market_manager_city: str = Field(
        default="",
        description=(
            "City of the US Market Manager's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    us_market_manager_telephone: str = Field(
        default="",
        description=(
            "Telephone number for the US Market Manager .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class UTChattanoogaAgentProfileFormForIntlStudentRecruitment(BaseModel):
    """
        The University of Tennessee at Chattanooga
    AGENT PROFILE FORM (APF)   FOR INTERNATIONAL STUDENT RECRUITMENT

        1. GENERAL INFORMATION: Please complete clearly. Use additional paper if required.
    """

    general_information: GeneralInformation = Field(..., description="General Information")
    chief_executive_officer: ChiefExecutiveOfficer = Field(
        ..., description="Chief Executive Officer"
    )
    chief_financial_officer: ChiefFinancialOfficer = Field(
        ..., description="Chief Financial Officer"
    )
    us_market_manager: USMarketManager = Field(..., description="US Market Manager")
