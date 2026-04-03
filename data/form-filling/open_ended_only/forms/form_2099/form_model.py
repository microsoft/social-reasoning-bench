from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PatientInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the patient applying for financial support."""

    last_name: str = Field(
        ...,
        description=(
            "Patient's last name .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    first_name: str = Field(
        ...,
        description=(
            "Patient's first name .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    mi: str = Field(
        ...,
        description=(
            "Patient's middle initial .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    date_of_birth: str = Field(
        ...,
        description="Patient's date of birth"
    )  # YYYY-MM-DD format

    account_number_from_statement: str = Field(
        ...,
        description=(
            "Account number from billing statement, if available .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    email: str = Field(
        ...,
        description=(
            "Patient's email address .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    home_address: str = Field(
        ...,
        description=(
            "Patient's home street address .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    city: str = Field(
        ...,
        description=(
            "Patient's city .If you cannot fill this, write \"N/A\". If this field should "
            "not be filled by you (for example, it belongs to another person or office), "
            "leave it blank (empty string \"\")."
        )
    )

    state: str = Field(
        ...,
        description="Patient's state"
    )

    zip: str = Field(
        ...,
        description="Patient's zip code"
    )

    home_phone_number: str = Field(
        ...,
        description=(
            "Patient's home phone number .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    cell_phone_number: str = Field(
        ...,
        description=(
            "Patient's cell phone number .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    ordering_physician_practice: str = Field(
        ...,
        description=(
            "Name of the ordering physician or practice .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )


class ResponsiblePartyInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the person responsible for the account, if different from the patient."""

    responsible_party_last_name: str = Field(
        ...,
        description=(
            "Responsible party's last name (if different from patient) .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    responsible_party_first_name: str = Field(
        ...,
        description=(
            "Responsible party's first name (if different from patient) .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    responsible_party_mi: str = Field(
        ...,
        description=(
            "Responsible party's middle initial .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    billing_address: str = Field(
        ...,
        description=(
            "Responsible party's billing address .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    relationship: str = Field(
        ...,
        description=(
            "Relationship of responsible party to patient .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    responsible_party_city: str = Field(
        ...,
        description=(
            "Responsible party's city .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    responsible_party_state: str = Field(
        ...,
        description="Responsible party's state"
    )

    responsible_party_zip: str = Field(
        ...,
        description="Responsible party's zip code"
    )

    responsible_party_home_phone_number: str = Field(
        ...,
        description=(
            "Responsible party's home phone number .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    responsible_party_cell_phone_number: str = Field(
        ...,
        description=(
            "Responsible party's cell phone number .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    responsible_party_email: str = Field(
        ...,
        description=(
            "Responsible party's email address .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class FinancialInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details about household income, employment, and health care expenses."""

    total_earned_annual_gross_household_income: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Total annual gross household income before taxes and deductions"
    )

    unemployment_income: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Annual unemployment income"
    )

    social_security_income: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Annual social security income"
    )

    additional_income_please_specify: str = Field(
        ...,
        description=(
            "Any additional income, specify source and amount .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    number_of_persons_in_household_supported_by_above_income: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of people in household supported by the listed income"
    )

    are_you_currently_employed: BooleanLike = Field(
        ...,
        description="Indicate if you are currently employed"
    )

    other_health_care_expenses_amounts_and_indicate_how_often_the_cost_occurs: str = Field(
        ...,
        description=(
            "List other health care expenses, amounts, and frequency .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )


class OmniseqCaresFinancialSupportApplicationForInvoicedPatients(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    OmniSeq CARES – Financial Support Application  
Application for patients who are invoiced by OmniSeq, Inc.

    Application for patients who are invoiced by OmniSeq, Inc. OmniSeq CARES representatives are available to answer any questions Monday through Friday 8:00 AM – 5:00 PM EST. For timely processing of your application, please complete all fields. Return completed applications to PO Box 8000, Dept 815, Buffalo, NY 14267-0002, by fax 888-770-4931 or secured email to CARES@omniseq.com.
    """

    patient_information: PatientInformation = Field(
        ...,
        description="Patient Information"
    )
    responsible_party_information: ResponsiblePartyInformation = Field(
        ...,
        description="Responsible Party Information"
    )
    financial_information: FinancialInformation = Field(
        ...,
        description="Financial Information"
    )