from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Section1PatientInformation(BaseModel):
    """Patient contact and identifying information"""

    last_name: str = Field(
        ...,
        description=(
            'Patient\'s legal last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Patient\'s legal first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    mi: str = Field(
        default="",
        description=(
            'Patient\'s middle initial .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Patient's date of birth")  # YYYY-MM-DD format

    account_from_statement_leave_blank_if_unavailable: str = Field(
        default="",
        description=(
            "Account number from the OmniSeq statement, if available .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            'Patient\'s email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    home_address: str = Field(
        ...,
        description=(
            'Patient\'s street address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City for patient\'s home address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for patient's home address")

    zip: str = Field(..., description="ZIP code for patient's home address")

    home_phone_number: str = Field(
        default="",
        description=(
            'Patient\'s home phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    cell_phone_number: str = Field(
        default="",
        description=(
            'Patient\'s mobile/cell phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    ordering_physician_practice: str = Field(
        default="",
        description=(
            "Name of the ordering physician or practice .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Section2ResponsiblePartyInformation(BaseModel):
    """Responsible party contact and billing information"""

    last_name_responsible_party: str = Field(
        default="",
        description=(
            "Responsible party's last name, if different from patient .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    first_name_responsible_party: str = Field(
        default="",
        description=(
            "Responsible party's first name, if different from patient .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mi_responsible_party: str = Field(
        default="",
        description=(
            'Responsible party\'s middle initial .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    billing_address: str = Field(
        default="",
        description=(
            "Responsible party's billing street address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    relationship: str = Field(
        default="",
        description=(
            "Relationship of responsible party to the patient .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_responsible_party: str = Field(
        default="",
        description=(
            'City for responsible party\'s address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state_responsible_party: str = Field(
        default="", description="State for responsible party's address"
    )

    zip_responsible_party: str = Field(
        default="", description="ZIP code for responsible party's address"
    )

    home_phone_number_responsible_party: str = Field(
        default="",
        description=(
            'Responsible party\'s home phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    cell_phone_number_responsible_party: str = Field(
        default="",
        description=(
            "Responsible party's mobile/cell phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_responsible_party: str = Field(
        default="",
        description=(
            'Responsible party\'s email address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class Section3FinancialInformation(BaseModel):
    """Household income, employment, and health care expenses"""

    total_earned_annual_gross_household_income_income_before_taxes_and_deductions: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Total earned annual gross household income before taxes and deductions",
    )

    unemployment_income: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total unemployment income received"
    )

    social_security_income: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total Social Security income received"
    )

    additional_income_please_specify: str = Field(
        default="",
        description=(
            "Description and amount of any additional income .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    number_of_persons_in_household_supported_by_above_income: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Total number of people in the household supported by the listed income",
        )
    )

    are_you_currently_employed: BooleanLike = Field(
        default="", description="Indicates whether the patient is currently employed"
    )

    are_you_currently_employed_no: BooleanLike = Field(
        default="", description="Indicates whether the patient is not currently employed"
    )

    other_health_care_expenses: str = Field(
        default="",
        description=(
            "Description of other health care expenses .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_health_care_expenses_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount associated with the other health care expenses"
    )

    other_health_care_expenses_frequency: str = Field(
        default="",
        description=(
            "How often the other health care expense occurs (e.g., monthly, yearly) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class OmniseqCaresFinancialSupportApplication(BaseModel):
    """
    OmniSeq CARES – Financial Support Application

    Application for patients who are invoiced by OmniSeq, Inc. • OmniSeq CARES representatives are available to answer any questions Monday through Friday 8:00 AM – 5:00 PM EST. • For timely processing of your application, please complete all fields. • Return completed to PO Box 8000, Dept 815, Buffalo, NY 14267-0002, by fax 888-770-4931 or secured email to CARES@omniseq.com.
    """

    section_1___patient_information: Section1PatientInformation = Field(
        ..., description="Section 1 - Patient Information"
    )
    section_2___responsible_party_information: Section2ResponsiblePartyInformation = Field(
        ..., description="Section 2 - Responsible Party Information"
    )
    section_3___financial_information: Section3FinancialInformation = Field(
        ..., description="Section 3 - Financial Information"
    )
