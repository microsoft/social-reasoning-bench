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
    """Information about the funds request and requester"""

    date_of_request: str = Field(
        ..., description="Date this funds request form is being submitted"
    )  # YYYY-MM-DD format

    reimbursement: BooleanLike = Field(
        ..., description="Check this box if the request is for reimbursement"
    )

    invoice: BooleanLike = Field(
        ..., description="Check this box if the request is to pay an invoice directly"
    )

    group_sport_funds_to_be_charged: str = Field(
        ...,
        description=(
            "Name of the group or sport whose booster funds should be charged .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    coach_advised: str = Field(
        default="",
        description=(
            "Name of the coach who has been informed or approved this request .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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
            "Brief description of what the funds are for; attach receipts or invoice as "
            'indicated .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    total_amount_requested: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total dollar amount being requested"
    )


class PayeeMailingInformation(BaseModel):
    """Details on who the check is payable to and where it should be sent"""

    make_check_payable_to: str = Field(
        ...,
        description=(
            "Name of the person or organization to whom the check should be written .If you "
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
        description="Indicates that the check was mailed to the payee at the address listed above",
    )

    different_address: str = Field(
        default="",
        description=(
            "Alternate address if the check was mailed somewhere other than the address "
            'above .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
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
            "Accounting code or description of the account from which payment was made .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    approver_1: str = Field(
        ...,
        description=(
            "Signature or printed name of the first approver authorizing payment .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    approver_2: str = Field(
        default="",
        description=(
            "Signature or printed name of the second approver authorizing payment, if "
            'required .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    entered_in_general_ledger: BooleanLike = Field(
        default="",
        description="Indicates that this transaction has been entered into the general ledger",
    )

    date: str = Field(
        default="", description="Date the transaction was entered in the general ledger"
    )  # YYYY-MM-DD format


class MthsBoostersFundsRequestForm(BaseModel):
    """
        MTHS Boosters
    Funds Request Form

        Checks are issued 2x a month. Complete this form and either mail to: MTHS Boosters, 21801 44th Ave W, Mountlake Terrace, WA 98043 or scan documentation and email to MTHSBCBoard@Edmonds.Wednet.edu.
    """

    request_details: RequestDetails = Field(..., description="Request Details")
    payee__mailing_information: PayeeMailingInformation = Field(
        ..., description="Payee & Mailing Information"
    )
    accounting_use_only: AccountingUseOnly = Field(..., description="Accounting Use Only")
