from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PremiumAndLossRecordTableRow(BaseModel):
    """Single row in Policy Period"""

    policy_period: str = Field(default="", description="Policy_Period")
    carrier: str = Field(default="", description="Carrier")
    premium: str = Field(default="", description="Premium")
    loss_amount: str = Field(default="", description="Loss_Amount")
    non_renewal_or_cancel: str = Field(default="", description="Non_Renewal_Or_Cancel")


class ApplicantHistory(BaseModel):
    """Applicant’s experience and loss history information"""

    applicants_experience_with_haunted_houses_including_years_numbers_dates: str = Field(
        ...,
        description=(
            "Describe the applicant’s haunted house experience, including number of years, "
            "number of events/locations, and relevant dates. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    premium_and_loss_record_table: List[PremiumAndLossRecordTableRow] = Field(
        ...,
        description=(
            "Premium and loss record for the last five years, including policy period, "
            "carrier, premium, loss amount, and non-renewal or cancel status."
        ),
    )  # List of table rows

    carrier: str = Field(
        default="",
        description=(
            "Name of the insurance carrier for the policy period. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    premium: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Premium amount charged for the policy period."
    )

    loss_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total loss amount incurred during the policy period."
    )

    non_renewal_or_cancel: str = Field(
        default="",
        description=(
            "Indicate if the policy was non-renewed or cancelled and provide brief reason "
            'if applicable. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    details_of_losses_incidents_for_the_past_five_years: str = Field(
        ...,
        description=(
            "Provide detailed descriptions of all losses or incidents in the past five "
            "years, including dates, amounts, and circumstances. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Signatures(BaseModel):
    """Signatures confirming accuracy of the application"""

    insured_signature: str = Field(
        ...,
        description=(
            "Signature of the insured confirming the accuracy and completeness of the "
            'information provided. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    insured_signature_date: str = Field(
        ..., description="Date the insured signed the application."
    )  # YYYY-MM-DD format

    agent_signature: str = Field(
        ...,
        description=(
            "Signature of the agent submitting the application. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    agent_signature_date: str = Field(
        ..., description="Date the agent signed the application."
    )  # YYYY-MM-DD format


class ApplicantHistory(BaseModel):
    """
    APPLICANT HISTORY

    ''
    """

    applicant_history: ApplicantHistory = Field(..., description="Applicant History")
    signatures: Signatures = Field(..., description="Signatures")
