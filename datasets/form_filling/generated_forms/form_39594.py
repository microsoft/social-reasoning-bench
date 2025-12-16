from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RecordingInformation(BaseModel):
    """Information for recorder and mailing after recording"""

    recording_requested_by: str = Field(
        default="",
        description=(
            "Name of the person or entity requesting recording of this document .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    when_recorded_mail_to_name: str = Field(
        default="",
        description=(
            "Name of the person or entity to whom the recorded document should be mailed "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    when_recorded_mail_to_street: str = Field(
        default="",
        description=(
            "Street address for mailing the recorded document .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    when_recorded_mail_to_address: str = Field(
        default="",
        description=(
            "Additional address line if needed (e.g., apartment, suite, or secondary "
            'address information) .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    when_recorded_mail_to_city_state_zip_code: str = Field(
        default="",
        description=(
            "City, state, and ZIP code for mailing the recorded document .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class PrincipalandAttorneyinFact(BaseModel):
    """Identification of the principal and appointed attorney-in-fact"""

    principal_name: str = Field(
        ...,
        description=(
            "Full legal name of the principal granting the limited power of attorney .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    principal_additional_name_address_line: str = Field(
        default="",
        description=(
            "Additional line for principal information (e.g., second name or address line) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    attorney_in_fact_name: str = Field(
        ...,
        description=(
            "Name of the attorney-in-fact being appointed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PowersGranted(BaseModel):
    """Description of the limited powers granted to the attorney-in-fact"""

    powers_granted_description_line_1: str = Field(
        ...,
        description=(
            "First line describing the specific powers granted to the attorney-in-fact .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    powers_granted_description_line_2: str = Field(
        default="",
        description=(
            "Second line describing the specific powers granted to the attorney-in-fact .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    powers_granted_description_line_3: str = Field(
        default="",
        description=(
            "Third line describing the specific powers granted to the attorney-in-fact .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class TermofLimitedPowerofAttorney(BaseModel):
    """Duration, effective date, and termination date of the limited power of attorney"""

    period_of_limited_power_of_attorney: str = Field(
        ...,
        description=(
            "Overall period or duration for which this limited power of attorney is granted "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    effective_date: str = Field(
        ..., description="Date on which this limited power of attorney becomes effective"
    )  # YYYY-MM-DD format

    termination_date: str = Field(
        ..., description="Date on which this limited power of attorney terminates"
    )  # YYYY-MM-DD format


class ExecutionbyPrincipal(BaseModel):
    """Date and signatures for execution of the document by the principal"""

    day_of_execution: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Numeric day of the month when the principal signs this document"
    )

    month_and_year_of_execution: str = Field(
        ...,
        description=(
            "Month and year when the principal signs this document .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    principal_signature_line_1: str = Field(
        ...,
        description=(
            "Signature of principal (first signature line, if more than one principal) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    principal_signature_line_2: str = Field(
        default="",
        description=(
            "Signature of additional principal (second signature line, if applicable) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class NotarialAcknowledgment(BaseModel):
    """Notary jurisdiction, acknowledgment details, and notary signatures"""

    state: str = Field(..., description="State where the notarial acknowledgment is taken")

    county: str = Field(
        ...,
        description=(
            "County where the notarial acknowledgment is taken .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_notarial_acknowledgment: str = Field(
        ..., description="Date on which the notary public takes the acknowledgment"
    )  # YYYY-MM-DD format

    name_of_notary_public: str = Field(
        ...,
        description=(
            'Printed name of the notary public .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_of_persons_appearing: str = Field(
        ...,
        description=(
            "Name of the person or persons who appeared before the notary .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    notary_signature_under_seal: str = Field(
        ...,
        description=(
            "Signature of the notary public adjacent to the official seal .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    notary_signature: str = Field(
        ...,
        description=(
            "Signature of the notary public on the signature line .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LimitedPowerOfAttorney(BaseModel):
    """LIMITED POWER OF ATTORNEY"""

    recording_information: RecordingInformation = Field(..., description="Recording Information")
    principal_and_attorney_in_fact: PrincipalandAttorneyinFact = Field(
        ..., description="Principal and Attorney-in-Fact"
    )
    powers_granted: PowersGranted = Field(..., description="Powers Granted")
    term_of_limited_power_of_attorney: TermofLimitedPowerofAttorney = Field(
        ..., description="Term of Limited Power of Attorney"
    )
    execution_by_principal: ExecutionbyPrincipal = Field(..., description="Execution by Principal")
    notarial_acknowledgment: NotarialAcknowledgment = Field(
        ..., description="Notarial Acknowledgment"
    )
