from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ViolationHistory(BaseModel):
    """Applicant violation and probation history"""

    convicted_felony: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you have ever been convicted of a felony as a juvenile or adult."
        ),
    )

    convicted_felony_no: BooleanLike = Field(
        ...,
        description="Indicate that you have not been convicted of a felony as a juvenile or adult.",
    )

    scheduled_court_dates: BooleanLike = Field(
        ..., description="Indicate whether you are scheduled for any upcoming court dates."
    )

    scheduled_court_dates_no: BooleanLike = Field(
        ..., description="Indicate that you are not scheduled for any upcoming court dates."
    )

    pending_charges: BooleanLike = Field(
        ..., description="Indicate whether you currently have any pending criminal charges."
    )

    pending_charges_no: BooleanLike = Field(
        ..., description="Indicate that you do not currently have any pending criminal charges."
    )

    currently_on_probation: BooleanLike = Field(
        ..., description="Indicate whether you are currently on juvenile or adult probation."
    )

    currently_on_probation_no: BooleanLike = Field(
        ..., description="Indicate that you are not currently on juvenile or adult probation."
    )

    probation_until_when: str = Field(
        default="",
        description=(
            "Date or time period when your current probation is scheduled to end. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    probation_officer_name: str = Field(
        default="",
        description=(
            "Full name of your current probation officer, if applicable. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    probation_officer_phone: str = Field(
        default="",
        description=(
            "Phone number of your probation officer, including area code. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class OffenseDetails(BaseModel):
    """List of all offenses on record"""

    offense_1_offense: str = Field(
        default="",
        description=(
            "Description or name of your first listed offense. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    offense_1_location_county: str = Field(
        default="",
        description=(
            "City, location, or county where the first offense occurred or was processed. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    offense_1_mm_yyyy: str = Field(
        default="",
        description=(
            "Month and year (MM/YYYY) of the first offense. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    offense_1_adjudication_outcome_of_charge_ex_misd: str = Field(
        default="",
        description=(
            "Outcome or adjudication of the first offense (e.g., misdemeanor, dismissed, "
            'probation). .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    offense_2_offense: str = Field(
        default="",
        description=(
            "Description or name of your second listed offense. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    offense_2_location_county: str = Field(
        default="",
        description=(
            "City, location, or county where the second offense occurred or was processed. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    offense_2_mm_yyyy: str = Field(
        default="",
        description=(
            "Month and year (MM/YYYY) of the second offense. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    offense_2_adjudication_outcome_of_charge_ex_misd: str = Field(
        default="",
        description=(
            "Outcome or adjudication of the second offense (e.g., misdemeanor, dismissed, "
            'probation). .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    offense_3_offense: str = Field(
        default="",
        description=(
            "Description or name of your third listed offense. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    offense_3_location_county: str = Field(
        default="",
        description=(
            "City, location, or county where the third offense occurred or was processed. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    offense_3_mm_yyyy: str = Field(
        default="",
        description=(
            "Month and year (MM/YYYY) of the third offense. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    offense_3_adjudication_outcome_of_charge_ex_misd: str = Field(
        default="",
        description=(
            "Outcome or adjudication of the third offense (e.g., misdemeanor, dismissed, "
            'probation). .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    offense_4_offense: str = Field(
        default="",
        description=(
            "Description or name of your fourth listed offense. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    offense_4_location_county: str = Field(
        default="",
        description=(
            "City, location, or county where the fourth offense occurred or was processed. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    offense_4_mm_yyyy: str = Field(
        default="",
        description=(
            "Month and year (MM/YYYY) of the fourth offense. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    offense_4_adjudication_outcome_of_charge_ex_misd: str = Field(
        default="",
        description=(
            "Outcome or adjudication of the fourth offense (e.g., misdemeanor, dismissed, "
            'probation). .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class Signatures(BaseModel):
    """Applicant and parent/guardian authorization"""

    applicant_signature: str = Field(
        ...,
        description=(
            "Signature of the applicant certifying that the information provided is true "
            'and complete. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    applicant_signature_date: str = Field(
        ..., description="Date the applicant signed this form."
    )  # YYYY-MM-DD format

    parent_guardian_signature: str = Field(
        ...,
        description=(
            "Signature of a parent or legal guardian, if the applicant is a minor. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    parent_guardian_signature_date: str = Field(
        ..., description="Date the parent or guardian signed this form."
    )  # YYYY-MM-DD format


class ViolationHistory(BaseModel):
    """
    Violation History

    Application for acceptance to the Arkansas National Guard Youth ChalleNGe Program requires disclosure of past law violations that are on your record. Please list all offenses on your record. If you have no offenses, you must write NONE below.
    """

    violation_history: ViolationHistory = Field(..., description="Violation History")
    offense_details: OffenseDetails = Field(..., description="Offense Details")
    signatures: Signatures = Field(..., description="Signatures")
