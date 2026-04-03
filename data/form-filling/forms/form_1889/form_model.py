from typing import Literal, Optional, List, Union
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
        ..., description="Select if this request is for reimbursement"
    )

    invoice: BooleanLike = Field(..., description="Select if this request is to pay an invoice")

    group_sport_funds_to_be_charged: str = Field(
        ...,
        description=(
            "Name of the group or sport whose funds will be charged .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    coach_advised: str = Field(
        default="",
        description=(
            "Name of the coach who has been advised or approved this request .If you cannot "
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
            "Description of the purpose of the funds request; attach receipts or invoice "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    total_amount_requested: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total dollar amount being requested"
    )

    make_check_payable_to: str = Field(
        ...,
        description=(
            "Name of the person or organization to whom the check should be made payable "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
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
    """Internal accounting processing information"""

    accounting_use_only_check_number: str = Field(
        default="",
        description=(
            'Check number assigned by accounting .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    accounting_use_only_date_issued: str = Field(
        default="", description="Date the check was issued by accounting"
    )  # YYYY-MM-DD format

    account_paid_from: str = Field(
        default="",
        description=(
            "Accounting code or description of the account from which payment is made .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    approver_1: str = Field(
        default="",
        description=(
            "Name or signature of first approver authorizing payment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    approver_2: str = Field(
        default="",
        description=(
            "Name or signature of second approver authorizing payment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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
        description="Indicate if the check was mailed to the payee at the main address listed above",
    )

    different_address_line_1: str = Field(
        default="",
        description=(
            "First line of alternate mailing address if different from the main address .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    different_address_line_2: str = Field(
        default="",
        description=(
            "Second line of alternate mailing address if different from the main address "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    entered_in_general_ledger: BooleanLike = Field(
        default="",
        description="Indicate that this transaction has been entered in the general ledger",
    )

    entered_in_general_ledger_date: str = Field(
        default="", description="Date the transaction was entered in the general ledger"
    )  # YYYY-MM-DD format


class MthsBoostersFundsRequestForm(BaseModel):
    """
        MTHS Boosters
    Funds Request Form

        Checks are issued 2x a month. Complete this form and either mail to: MTHS Boosters, 21801 44th Ave W, Mountlake Terrace, WA 98043 or scan documentation and email to MTHSBCBoard@Edmonds.Wednet.edu.
    """

    request_details: RequestDetails = Field(..., description="Request Details")
    accounting_use_only: AccountingUseOnly = Field(..., description="Accounting Use Only")
