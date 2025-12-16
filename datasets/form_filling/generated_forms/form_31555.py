from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class BusinessOwnershipTableRow(BaseModel):
    """Single row in Owner Name"""

    owner_name: str = Field(default="", description="Owner_Name")
    title: str = Field(default="", description="Title")
    ownership_percent: str = Field(default="", description="Ownership_Percent")
    address: str = Field(default="", description="Address")


class ApplicationDetails(BaseModel):
    """Program selection, terms, and basic application info"""

    received_date_of_application: str = Field(
        ..., description="Date the credit application was received"
    )  # YYYY-MM-DD format

    geda_loan_program_gdfa: BooleanLike = Field(
        ..., description="Check if applying under the GDFA loan program"
    )

    geda_loan_program_adf: BooleanLike = Field(
        ..., description="Check if applying under the ADF loan program"
    )

    terms_direct_loan: BooleanLike = Field(
        ..., description="Check if the requested credit is a direct loan"
    )

    terms_line_of_credit: BooleanLike = Field(
        ..., description="Check if the requested credit is a line of credit"
    )

    repayment_terms: str = Field(
        ...,
        description=(
            "Summary of proposed repayment terms (e.g., term length, frequency) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class BusinessInformation(BaseModel):
    """Core business identity and contact details"""

    business_legal_name: str = Field(
        ...,
        description=(
            "Full legal name of the business entity .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dba_or_registered_trade_name: str = Field(
        default="",
        description=(
            "Doing Business As (DBA) or registered trade name, if different from legal name "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    business_physical_address: str = Field(
        ...,
        description=(
            "Street address where the business is physically located .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    business_mailing_address: str = Field(
        ...,
        description=(
            "Mailing address for the business, if different from physical address .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    primary_point_of_contact: str = Field(
        ...,
        description=(
            "Name of the primary contact person for this application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    position_title: str = Field(
        ...,
        description=(
            "Job title or position of the primary contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    primary_contact_number: str = Field(
        ...,
        description=(
            "Primary phone number for the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Email address for the primary contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    federal_tax_id_ss: str = Field(
        ...,
        description=(
            "Federal Tax Identification Number or Social Security Number, as applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    business_phone_number: str = Field(
        ...,
        description=(
            'Main business telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    business_activity_agriculture: BooleanLike = Field(
        default="", description="Check if the business activity includes agriculture"
    )

    business_activity_fishing: BooleanLike = Field(
        default="", description="Check if the business activity includes fishing"
    )

    business_activity_tourism: BooleanLike = Field(
        default="", description="Check if the business activity includes tourism"
    )

    business_activity_manufacturing: BooleanLike = Field(
        default="", description="Check if the business activity includes manufacturing"
    )

    business_activity_other: BooleanLike = Field(
        default="", description="Check if the business activity is of another type not listed"
    )

    briefly_describe_business_activity: str = Field(
        ...,
        description=(
            "Short description of the primary business activities .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class BusinessLegalStatusOwnership(BaseModel):
    """Business structure, owners, and employment"""

    business_legal_status_sole_proprietor: BooleanLike = Field(
        ..., description="Check if the business is a sole proprietorship"
    )

    business_legal_status_general_partnership: BooleanLike = Field(
        ..., description="Check if the business is a general partnership"
    )

    business_legal_status_limited_partnership: BooleanLike = Field(
        ..., description="Check if the business is a limited partnership"
    )

    business_legal_status_professional_corporation: BooleanLike = Field(
        ..., description="Check if the business is a professional corporation"
    )

    business_legal_status_c_corporation: BooleanLike = Field(
        ..., description="Check if the business is a C corporation"
    )

    business_legal_status_s_corporation: BooleanLike = Field(
        ..., description="Check if the business is an S corporation"
    )

    business_legal_status_limited_liability_partnership: BooleanLike = Field(
        ..., description="Check if the business is a limited liability partnership (LLP)"
    )

    business_legal_status_limited_liability_corporation: BooleanLike = Field(
        ..., description="Check if the business is a limited liability company (LLC)"
    )

    business_ownership_table: List[BusinessOwnershipTableRow] = Field(
        ...,
        description=(
            "List all proprietors, partners, officers, directors, and stockholders with "
            "their title, ownership percentage, and address"
        ),
    )  # List of table rows

    current_number_of_employees: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of employees currently employed by the business"
    )

    expected_number_of_employees_if_loan_is_granted: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Projected number of employees if the loan is approved"
    )


class PurposeofLoan(BaseModel):
    """Use of proceeds and total credit requested"""

    start_up_costs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of loan proceeds to be used for start-up costs"
    )

    inventory: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of loan proceeds to be used for inventory"
    )

    working_capital: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of loan proceeds to be used for working capital"
    )

    land_acquisition: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of loan proceeds to be used for land acquisition"
    )

    business_procurement: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Dollar amount of loan proceeds to be used for purchasing an existing business",
    )

    furniture_fixtures_equipment: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Dollar amount of loan proceeds to be used for furniture, fixtures, and equipment"
        ),
    )

    new_construction_expansion_renovation: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Dollar amount of loan proceeds to be used for construction, expansion, or renovation"
        ),
    )

    total_amount_of_credit_requested: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Total loan amount requested; should equal the sum of all use-of-proceeds amounts"
        ),
    )


class RepaymentInformation(BaseModel):
    """How the loan will be repaid and repayment sources"""

    repayment_manner_description: str = Field(
        ...,
        description=(
            "Describe how the loan will be repaid (e.g., payment schedule, terms) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    source_of_repayment: str = Field(
        ...,
        description=(
            "Describe the primary sources of funds that will be used to repay the loan .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ApplicationForCreditGedaForm1001(BaseModel):
    """APPLICATION FOR CREDIT
    GEDA FORM 1-001"""

    application_details: ApplicationDetails = Field(..., description="Application Details")
    business_information: BusinessInformation = Field(..., description="Business Information")
    business_legal_status__ownership: BusinessLegalStatusOwnership = Field(
        ..., description="Business Legal Status & Ownership"
    )
    purpose_of_loan: PurposeofLoan = Field(..., description="Purpose of Loan")
    repayment_information: RepaymentInformation = Field(..., description="Repayment Information")
