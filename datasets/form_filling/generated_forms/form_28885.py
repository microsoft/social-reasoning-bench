from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class LossHistoryTableRow(BaseModel):
    """Single row in POLICY TERM"""

    policy_term: str = Field(default="", description="Policy_Term")
    number_of_claims: str = Field(default="", description="Number_Of_Claims")
    amount_paid: str = Field(default="", description="Amount_Paid")
    open_reserve: str = Field(default="", description="Open_Reserve")
    total_incurred: str = Field(default="", description="Total_Incurred")


class SubmissionSummary(BaseModel):
    """Basic submission, insured, and coverage details"""

    insured_name: str = Field(
        ...,
        description=(
            'Legal name of the insured entity .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    submitting_agent: str = Field(
        ...,
        description=(
            "Name of the agent submitting this application .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Mailing address of the insured .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Email address for primary contact .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    website: str = Field(
        default="",
        description=(
            'Company website URL, if any .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    proposed_effective_date: str = Field(
        ..., description="Requested policy effective date"
    )  # YYYY-MM-DD format

    date: str = Field(
        ..., description="Date this submission summary is completed"
    )  # YYYY-MM-DD format

    quote_needed_date: str = Field(
        default="", description="Date by which the quote is needed"
    )  # YYYY-MM-DD format

    coverage_requested: str = Field(
        ...,
        description=(
            "Type(s) of insurance coverage being requested .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    description_of_operations: str = Field(
        ...,
        description=(
            "Detailed description of the insured's operations and activities .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    exposures_line_1: str = Field(
        default="",
        description=(
            'First line describing key exposures .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    exposures_line_2: str = Field(
        default="",
        description=(
            'Second line describing key exposures .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    exposures_line_3: str = Field(
        default="",
        description=(
            'Third line describing key exposures .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    target_expiring_premium: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Target or current expiring premium amount"
    )

    target_expiring_sir: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Target or current expiring self-insured retention (SIR) amount"
    )

    iso_benchmark_rating: str = Field(
        default="",
        description=(
            "Applicable ISO or benchmark rating information .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class LossHistory(BaseModel):
    """Historical loss information and large claim details"""

    loss_history_table: List[LossHistoryTableRow] = Field(
        ...,
        description=(
            "Loss history by policy term including number of claims, amounts paid, open "
            "reserves, and total incurred"
        ),
    )  # List of table rows

    number_of_claims_header: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Header label for number of claims column in loss history table"
    )

    amount_paid_header: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Header label for amount paid column in loss history table"
    )

    open_reserve_header: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Header label for open reserve column in loss history table"
    )

    total_incurred_header: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Header label for total incurred column in loss history table"
    )

    y2018_19_number_of_claims: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of claims for policy term 2018-19"
    )

    y2018_19_amount_paid: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total amount paid for claims in policy term 2018-19"
    )

    y2018_19_open_reserve: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Open reserve amount for policy term 2018-19"
    )

    y2018_19_total_incurred: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total incurred losses for policy term 2018-19"
    )

    y2017_18_number_of_claims: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of claims for policy term 2017-18"
    )

    y2017_18_amount_paid: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total amount paid for claims in policy term 2017-18"
    )

    y2017_18_open_reserve: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Open reserve amount for policy term 2017-18"
    )

    y2017_18_total_incurred: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total incurred losses for policy term 2017-18"
    )

    y2016_17_number_of_claims: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of claims for policy term 2016-17"
    )

    y2016_17_amount_paid: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total amount paid for claims in policy term 2016-17"
    )

    y2016_17_open_reserve: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Open reserve amount for policy term 2016-17"
    )

    y2016_17_total_incurred: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total incurred losses for policy term 2016-17"
    )

    y2015_16_number_of_claims: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of claims for policy term 2015-16"
    )

    y2015_16_amount_paid: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total amount paid for claims in policy term 2015-16"
    )

    y2015_16_open_reserve: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Open reserve amount for policy term 2015-16"
    )

    y2015_16_total_incurred: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total incurred losses for policy term 2015-16"
    )

    y2014_15_number_of_claims: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of claims for policy term 2014-15"
    )

    y2014_15_amount_paid: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total amount paid for claims in policy term 2014-15"
    )

    y2014_15_open_reserve: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Open reserve amount for policy term 2014-15"
    )

    y2014_15_total_incurred: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total incurred losses for policy term 2014-15"
    )

    details_on_claims_over_25k: str = Field(
        default="",
        description=(
            "Narrative details for any individual claim with incurred amount over $25,000 "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class DocumentsIncludedforReview(BaseModel):
    """Checklist of documents submitted with this summary"""

    acord_application_125_126: BooleanLike = Field(
        default="", description="Check if ACORD application forms 125/126 are included"
    )

    loss_runs: BooleanLike = Field(
        default="", description="Check if current loss runs are included"
    )

    supplemental_application_includes_historical_payroll_receipts: BooleanLike = Field(
        default="",
        description=(
            "Check if supplemental application with historical payroll and receipts is included"
        ),
    )

    resume_new_ventures: BooleanLike = Field(
        default="", description="Check if resume for new ventures is included"
    )

    safety_manual_program: BooleanLike = Field(
        default="", description="Check if safety manual or safety program documentation is included"
    )


class UnderwriterNotes(BaseModel):
    """Additional notes and comments from the underwriter"""

    underwriter_notes: str = Field(
        default="",
        description=(
            "Additional notes or comments from the underwriter .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SubmissionSummary(BaseModel):
    """SUBMISSION SUMMARY"""

    submission_summary: SubmissionSummary = Field(..., description="Submission Summary")
    loss_history: LossHistory = Field(..., description="Loss History")
    documents_included_for_review: DocumentsIncludedforReview = Field(
        ..., description="Documents Included for Review"
    )
    underwriter_notes: UnderwriterNotes = Field(..., description="Underwriter Notes")
