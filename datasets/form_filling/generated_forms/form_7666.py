from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AdditionalInformation(BaseModel):
    """Additional regulatory and relationship information about the account and its owners"""

    will_this_account_be_used_for_hedging_purposes_yes: BooleanLike = Field(
        default="",
        description="Select if the account will be used for hedging purposes (Yes option).",
    )

    will_this_account_be_used_for_hedging_purposes_no: BooleanLike = Field(
        default="",
        description="Select if the account will not be used for hedging purposes (No option).",
    )

    do_any_owners_control_trading_in_other_admis_account_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if any owner controls trading in another ADMIS commodity account (Yes option)."
        ),
    )

    do_any_owners_control_trading_in_other_admis_account_no: BooleanLike = Field(
        default="",
        description=(
            "Select if no owner controls trading in another ADMIS commodity account (No option)."
        ),
    )

    if_yes_provide_names_and_account_numbers_line_1: str = Field(
        default="",
        description=(
            "Enter the names and account numbers of other ADMIS commodity accounts "
            "controlled by the owners (first line). .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    if_yes_provide_names_and_account_numbers_line_2: str = Field(
        default="",
        description=(
            "Additional space for names and account numbers of other ADMIS commodity "
            'accounts (second line). .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    will_this_account_be_traded_or_managed_by_anyone_else_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if someone other than the owner will trade or manage this account (Yes option)."
        ),
    )

    will_this_account_be_traded_or_managed_by_anyone_else_no: BooleanLike = Field(
        default="",
        description="Select if no one else will trade or manage this account (No option).",
    )

    if_yes_identify_trader_and_attach_poa_line_1: str = Field(
        default="",
        description=(
            "Provide the name and details of the trader and note that a power of attorney "
            'must be attached (first line). .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    if_yes_identify_trader_and_attach_poa_line_2: str = Field(
        default="",
        description=(
            "Additional space for trader identification and related information (second "
            'line). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    does_any_other_person_have_financial_interest_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if another person or entity has a financial interest in this account "
            "(Yes option)."
        ),
    )

    does_any_other_person_have_financial_interest_no: BooleanLike = Field(
        default="",
        description=(
            "Select if no other person or entity has a financial interest in this account "
            "(No option)."
        ),
    )

    if_yes_identify_person_and_type_of_interest_line_1: str = Field(
        default="",
        description=(
            "List the persons or entities with a financial interest and describe the type "
            'of interest (first line). .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    if_yes_identify_person_and_type_of_interest_line_2: str = Field(
        default="",
        description=(
            "Additional space to describe persons and types of financial interest (second "
            'line). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    are_any_owners_presently_member_on_any_exchange_yes: BooleanLike = Field(
        default="",
        description="Select if any owner is currently a member of any exchange (Yes option).",
    )

    are_any_owners_presently_member_on_any_exchange_no: BooleanLike = Field(
        default="",
        description="Select if no owner is currently a member of any exchange (No option).",
    )

    if_yes_exchange_membership_details_line_1: str = Field(
        default="",
        description=(
            "Provide the exchange name, membership type, and approximate effective date "
            '(first line). .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    if_yes_exchange_membership_details_line_2: str = Field(
        default="",
        description=(
            "Additional space for exchange membership details (second line). .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    are_any_owners_presently_ap_of_cftc_registrant_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if any owner is currently an Associated Person (AP) of a CFTC "
            "registrant (Yes option)."
        ),
    )

    are_any_owners_presently_ap_of_cftc_registrant_no: BooleanLike = Field(
        default="",
        description=(
            "Select if no owner is currently an Associated Person (AP) of a CFTC registrant "
            "(No option)."
        ),
    )

    if_yes_list_registrant_name_and_nfa_id: str = Field(
        default="",
        description=(
            "Provide the name of the CFTC registrant and its NFA ID number. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    is_owner_fcm_or_introducing_broker_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if the account owner is a Futures Commission Merchant or Introducing "
            "Broker (Yes option)."
        ),
    )

    is_owner_fcm_or_introducing_broker_no: BooleanLike = Field(
        default="",
        description=(
            "Select if the account owner is not a Futures Commission Merchant or "
            "Introducing Broker (No option)."
        ),
    )

    if_yes_please_explain_line_1: str = Field(
        default="",
        description=(
            "Explain the nature of the owner's status as a Futures Commission Merchant or "
            'Introducing Broker (first line). .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    if_yes_please_explain_line_2: str = Field(
        default="",
        description=(
            "Additional space to explain the owner's status as a Futures Commission "
            "Merchant or Introducing Broker (second line). .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class DuplicateStatementsandMailingInformation(BaseModel):
    """Instructions for duplicate statements, mailing address, and signatures"""

    transmit_duplicate_statements_to_name: str = Field(
        default="",
        description=(
            "Name of the person or entity to receive duplicate account statements. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    transmit_duplicate_statements_to_email_address: str = Field(
        default="",
        description=(
            "Email address for receiving duplicate account statements. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        default="",
        description=(
            "Street mailing address for duplicate statements (no P.O. Boxes except rural). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    city: str = Field(
        default="",
        description=(
            'City for the mailing address. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(default="", description="State or province for the mailing address.")

    country: str = Field(
        default="",
        description=(
            'Country for the mailing address. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    postal_code: str = Field(default="", description="Postal or ZIP code for the mailing address.")

    signature_first: str = Field(
        default="",
        description=(
            "First signature authorizing the information provided. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_first: str = Field(
        default="", description="Date of the first signature."
    )  # YYYY-MM-DD format

    signature_second: str = Field(
        default="",
        description=(
            "Second signature authorizing the information provided. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_second: str = Field(
        default="", description="Date of the second signature."
    )  # YYYY-MM-DD format


class InvestorServicesCustomerAccountInfo(BaseModel):
    """ADM INVESTOR SERVICES INC. CUSTOMER ACCOUNT APPLICATION
    ADDITIONAL INFORMATION"""

    additional_information: AdditionalInformation = Field(..., description="Additional Information")
    duplicate_statements_and_mailing_information: DuplicateStatementsandMailingInformation = Field(
        ..., description="Duplicate Statements and Mailing Information"
    )
