from pydantic import BaseModel, ConfigDict, Field


class MthsBoostersFundsRequestForm(BaseModel):
    """MTHS Boosters Funds Request Form

    Coaches, advisors, or other authorized requesters submit this form to ask MTHS Boosters
    to disburse funds either as a reimbursement for expenses already paid or as payment of
    an invoice. The Boosters treasurer/accounting team uses it to issue checks, record the
    transaction, and confirm delivery details, while designated approvers review the request
    and authorize payment from the specified group/sport account.
    """

    model_config = ConfigDict(extra="forbid")

    date_of_request: str = Field(
        ...,
        description='Date of request (YYYY-MM-DD).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    group_sport_funds_to_be_charged: str = Field(
        ...,
        description='Group/sport funds to be charged.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    phone: str = Field(
        ...,
        description='Requester phone number.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    general_purpose_of_request: str = Field(
        ...,
        description='General purpose of request.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    total_amount_requested: float | None = Field(
        ...,
        description="Total amount requested (USD)",
    )


    authorization_approver_1: str = Field(
        ...,
        description='Approver #1 name/signature.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

