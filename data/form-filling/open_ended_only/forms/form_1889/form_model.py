from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FundsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Requester and payment information for funds request"""

    date_of_request: str = Field(
        ...,
        description="Date this funds request is being submitted"
    )  # YYYY-MM-DD format

    reimbursement: BooleanLike = Field(
        ...,
        description="Check if this request is for reimbursement"
    )

    invoice: BooleanLike = Field(
        ...,
        description="Check if this request is for an invoice"
    )

    group_sport_funds_to_be_charged: str = Field(
        ...,
        description=(
            "Name of the group or sport account to be charged .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    coach_advised: str = Field(
        ...,
        description=(
            "Name of coach or advisor who was notified .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    e_mail: str = Field(
        ...,
        description=(
            "Contact email address .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    phone: str = Field(
        ...,
        description=(
            "Contact phone number .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    general_purpose_of_request_attach_receipts_invoice: str = Field(
        ...,
        description=(
            "Describe the purpose of the funds request and attach receipts or invoice .If "
            "you cannot fill this, write \"N/A\". If this field should not be filled by you "
            "(for example, it belongs to another person or office), leave it blank (empty "
            "string \"\")."
        )
    )

    total_amount_requested: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Total dollar amount being requested"
    )

    make_check_payable_to: str = Field(
        ...,
        description=(
            "Name to appear on the check .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    mail_check_to_address: str = Field(
        ...,
        description=(
            "Address where the check should be mailed .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )


class AccountingUseOnly(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Internal accounting and authorization details"""

    check_number: str = Field(
        ...,
        description=(
            "Check number (for accounting use only) .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    date_issued: str = Field(
        ...,
        description="Date the check was issued (for accounting use only)"
    )  # YYYY-MM-DD format

    account_paid_from: str = Field(
        ...,
        description=(
            "Account from which payment was made (for accounting use only) .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )

    approver_1: str = Field(
        ...,
        description=(
            "Signature or name of first approver .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    approver_2: str = Field(
        ...,
        description=(
            "Signature or name of second approver .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    check_was_given_to_provide_name: str = Field(
        ...,
        description=(
            "Name of person who received the check .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    check_was_mailed_to_payee_at_address_above: BooleanLike = Field(
        ...,
        description="Check if the check was mailed to the payee at the address above"
    )

    different_address: str = Field(
        ...,
        description=(
            "Alternate address for mailing the check .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    entered_in_general_ledger: BooleanLike = Field(
        ...,
        description="Check if this transaction was entered in the general ledger"
    )

    date: str = Field(
        ...,
        description="Date entered in the general ledger"
    )  # YYYY-MM-DD format


class MthsBoostersFundsRequestForm(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    MTHS Boosters
Funds Request Form

    Checks are issued 2x a month. Complete this form and either mail to: MTHS Boosters, 21801 44th Ave W, Mountlake Terrace, WA 98043 or scan documentation and email to MTHSBBoard@Edmonds.Wednet.edu. This form is used to request funds or reimbursement from the MTHS Boosters, specifying the group or sport, purpose of the request, and payment details. Receipts or invoices must be attached.
    """

    funds_request: FundsRequest = Field(
        ...,
        description="Funds Request"
    )
    accounting_use_only: AccountingUseOnly = Field(
        ...,
        description="Accounting Use Only"
    )