from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RequestDetails(BaseModel):
    """Information about the funds request and payee"""

    date_of_request: str = Field(
        ..., description="Date this funds request form is being submitted"
    )  # YYYY-MM-DD format

    reimbursement: BooleanLike = Field(
        ..., description="Check if this request is for reimbursement"
    )

    invoice: BooleanLike = Field(..., description="Check if this request is to pay an invoice")

    group_sport_funds_to_be_charged: str = Field(
        ...,
        description=(
            "Name of the group or sport account that should be charged .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    coach_advised: str = Field(
        default="",
        description=(
            "Name of the coach or advisor who was informed of this request .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            "Email address of the person submitting the request .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Phone number of the person submitting the request .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    general_purpose_of_request_attach_receipts_invoice: str = Field(
        ...,
        description=(
            "Describe the purpose of the funds request and reference attached receipts or "
            'invoice .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    total_amount_requested: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total dollar amount being requested"
    )

    make_check_payable_to: str = Field(
        ...,
        description=(
            "Name of the person or organization the check should be made out to .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mail_check_to_address: str = Field(
        default="",
        description=(
            "Mailing address where the check should be sent .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AccountingUseOnly(BaseModel):
    """Internal accounting and approval information"""

    check_number: str = Field(
        default="",
        description=(
            'Check number assigned by accounting .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_issued: str = Field(
        default="", description="Date the check was issued"
    )  # YYYY-MM-DD format

    account_paid_from: str = Field(
        default="",
        description=(
            "Accounting account or fund from which the payment was made .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    approver_1: str = Field(
        ...,
        description=(
            "Name or signature of the first approver authorizing payment .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    approver_2: str = Field(
        default="",
        description=(
            "Name or signature of the second approver authorizing payment, if required .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    check_was_given_to_provide_name: str = Field(
        default="",
        description=(
            "Name of the person to whom the check was physically given .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    check_was_mailed_to_payee_at_address_above: BooleanLike = Field(
        default="",
        description="Indicate that the check was mailed to the payee at the address listed above",
    )

    different_address: str = Field(
        default="",
        description=(
            "Alternate mailing address if different from the address above .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    entered_in_general_ledger: BooleanLike = Field(
        default="",
        description="Indicate that this transaction has been entered in the general ledger",
    )

    date: str = Field(
        default="", description="Date the transaction was entered in the general ledger"
    )  # YYYY-MM-DD format


class MthsBoostersFundsRequestForm(BaseModel):
    """
        MTHS Boosters
    Funds Request Form

        Checks are issued 2x a month. Complete this form and either mail to MTHS Boosters or scan documentation and email to MTHSBCBoard@Edmonds.Wednet.edu to request funds (reimbursement or invoice payment) from MTHS Boosters.
    """

    request_details: RequestDetails = Field(..., description="Request Details")
    accounting_use_only: AccountingUseOnly = Field(..., description="Accounting Use Only")
