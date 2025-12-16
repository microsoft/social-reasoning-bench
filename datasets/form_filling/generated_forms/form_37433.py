from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AgentInformation(BaseModel):
    """Details about the agency and quote timing"""

    date_received: str = Field(
        ..., description="Date the application was received by the agency"
    )  # YYYY-MM-DD format

    agency: str = Field(
        ...,
        description=(
            "Name of the insurance agency submitting the application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    effective_date: str = Field(
        ..., description="Requested effective date of coverage"
    )  # YYYY-MM-DD format

    producer: str = Field(
        ...,
        description=(
            "Name of the producer or agent handling this account .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    requested_quote_date: str = Field(
        default="", description="Date by which the quote is requested"
    )  # YYYY-MM-DD format


class GeneralInformation(BaseModel):
    """Basic insured and contact information"""

    named_insured: str = Field(
        ...,
        description=(
            "Legal name of the primary insured entity .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dba: str = Field(
        default="",
        description=(
            "Doing Business As name, if different from the legal name .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    street_address: str = Field(
        ...,
        description=(
            'Street address of the named insured .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the insured\'s primary address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of the insured's primary address")

    zip: str = Field(..., description="ZIP or postal code of the insured's primary address")

    phone: str = Field(
        ...,
        description=(
            'Primary business phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            'Business fax number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    additional_named_insureds: str = Field(
        default="",
        description=(
            "Names of any additional named insureds .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    affiliated_companies: str = Field(
        default="",
        description=(
            'Names of any affiliated companies .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class Personnel(BaseModel):
    """Key personnel and ownership details"""

    president_name: str = Field(
        default="",
        description=(
            'Name of the company president .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    president_years: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of years the president has been in this position or with the company",
    )

    president_percent_of_ownership: Union[float, Literal["N/A", ""]] = Field(
        default="", description="President's percentage of ownership in the company"
    )

    operations_manager_name: str = Field(
        default="",
        description=(
            'Name of the operations manager .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    operations_manager_years: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Number of years the operations manager has been in this position or with the company"
        ),
    )

    operations_manager_percent_of_ownership: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Operations manager's percentage of ownership in the company"
    )

    safety_director_name: str = Field(
        default="",
        description=(
            'Name of the safety director .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    safety_director_years: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Number of years the safety director has been in this position or with the company"
        ),
    )

    safety_director_percent_of_ownership: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Safety director's percentage of ownership in the company, if any"
    )

    loss_control_contact_name: str = Field(
        default="",
        description=(
            "Name of the primary loss control contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    loss_control_contact_years: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Number of years the loss control contact has been in this position or with the company"
        ),
    )

    loss_control_contact_percent_of_ownership: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Loss control contact's percentage of ownership in the company, if any",
    )

    insurance_contact_name: str = Field(
        default="",
        description=(
            'Name of the primary insurance contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    insurance_contact_years: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Number of years the insurance contact has been in this position or with the company"
        ),
    )

    insurance_contact_percent_of_ownership: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Insurance contact's percentage of ownership in the company, if any"
    )


class Operations(BaseModel):
    """Operational identifiers, business and carrier type, and related details"""

    fein: str = Field(
        ...,
        description=(
            "Federal Employer Identification Number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mc_number: str = Field(
        default="",
        description=(
            'Motor Carrier (MC) number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    dot_number: str = Field(
        ...,
        description=(
            'U.S. DOT number .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    business_type_sole_proprietor: BooleanLike = Field(
        default="", description="Check if the business type is Sole Proprietor"
    )

    business_type_corporation: BooleanLike = Field(
        default="", description="Check if the business type is Corporation"
    )

    business_type_partnership: BooleanLike = Field(
        default="", description="Check if the business type is Partnership"
    )

    business_type_other: BooleanLike = Field(
        default="", description="Check if the business type is Other"
    )

    carrier_type_common: BooleanLike = Field(
        default="", description="Check if the carrier type is Common carrier"
    )

    carrier_type_contract: BooleanLike = Field(
        default="", description="Check if the carrier type is Contract carrier"
    )

    carrier_type_private: BooleanLike = Field(
        default="", description="Check if the carrier type is Private carrier"
    )

    carrier_type_other: BooleanLike = Field(
        default="", description="Check if the carrier type is Other"
    )

    years_in_business: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years the business has been operating"
    )

    years_under_current_management: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years under current management"
    )

    if_other_business_type_please_explain: str = Field(
        default="",
        description=(
            "Explanation if an 'Other' business type is selected .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    if_other_carrier_type_please_explain: str = Field(
        default="",
        description=(
            "Explanation if an 'Other' carrier type is selected .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    are_you_a_subsidiary_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the applicant is a subsidiary"
    )

    are_you_a_subsidiary_no: BooleanLike = Field(
        default="", description="Indicate No if the applicant is not a subsidiary"
    )

    if_yes_please_explain_subsidiary: str = Field(
        default="",
        description=(
            "Explanation of subsidiary relationship if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    do_you_operate_as_a_broker_yes: BooleanLike = Field(
        default="", description="Indicate Yes if the applicant operates as a broker"
    )

    do_you_operate_as_a_broker_no: BooleanLike = Field(
        default="", description="Indicate No if the applicant does not operate as a broker"
    )

    if_yes_what_is_the_mc_number: str = Field(
        default="",
        description=(
            "MC number used when operating as a broker .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    do_you_travel_into_canada_yes: BooleanLike = Field(
        default="", description="Indicate Yes if operations include travel into Canada"
    )

    do_you_travel_into_canada_no: BooleanLike = Field(
        default="", description="Indicate No if operations do not include travel into Canada"
    )

    if_yes_please_list_provinces_and_mileage: str = Field(
        default="",
        description=(
            "List Canadian provinces traveled to and approximate mileage in each .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Filings(BaseModel):
    """Requested filings and applicable states"""

    filings_requested_bmc91x: BooleanLike = Field(
        default="", description="Check if BMC91X filing is requested"
    )

    filings_requested_form_e: BooleanLike = Field(
        default="", description="Check if Form E filing is requested"
    )

    filings_requested_os32: BooleanLike = Field(
        default="", description="Check if OS32 filing is requested"
    )

    filings_requested_uiia: BooleanLike = Field(
        default="", description="Check if UIIA filing is requested"
    )

    all_needed_state_filings: str = Field(
        default="",
        description=(
            "Describe or list all state filings needed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    applicable_states: str = Field(
        default="",
        description=(
            "List all applicable states for filings or operations .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class TruckTransportationApplication(BaseModel):
    """
    Truck Transportation Application

    Truck Transportation Application
    """

    agent_information: AgentInformation = Field(..., description="Agent Information")
    general_information: GeneralInformation = Field(..., description="General Information")
    personnel: Personnel = Field(..., description="Personnel")
    operations: Operations = Field(..., description="Operations")
    filings: Filings = Field(..., description="Filings")
