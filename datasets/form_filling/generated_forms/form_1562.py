from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CaseCaption(BaseModel):
    """Basic case information identifying the parties and case number"""

    plaintiff: str = Field(
        ...,
        description=(
            'Name of the plaintiff in this case .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    case_no: str = Field(
        ...,
        description=(
            'Court-assigned case number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    defendant: str = Field(
        ...,
        description=(
            'Name of the defendant in this case .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class MotionforContinuance(BaseModel):
    """Movant’s identity and stated reasons for requesting a continuance"""

    print_name_here: str = Field(
        ...,
        description=(
            "Printed name of the person filing the motion .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reason_for_continuance_line_1: str = Field(
        ...,
        description=(
            "First line explaining the reason for requesting a continuance .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    reason_for_continuance_line_2: str = Field(
        default="",
        description=(
            "Second line explaining the reason for requesting a continuance .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    reason_for_continuance_line_3: str = Field(
        default="",
        description=(
            "Third line explaining the reason for requesting a continuance .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    reason_for_continuance_line_4: str = Field(
        default="",
        description=(
            "Fourth line explaining the reason for requesting a continuance .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    reason_for_continuance_line_5: str = Field(
        default="",
        description=(
            "Fifth line explaining the reason for requesting a continuance .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class AdditionalInformation(BaseModel):
    """Contact information and signature of the party filing the motion"""

    street: str = Field(
        ...,
        description=(
            "Street address of the person filing the motion .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code of the person filing the motion .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        ...,
        description=(
            "Phone number of the person filing the motion .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        default="",
        description=(
            "Email address of the person filing the motion .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of the person filing the motion .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class JudgmentEntry(BaseModel):
    """Court’s ruling on the motion and related notes"""

    granted: BooleanLike = Field(
        default="", description="Indicates that the motion for continuance is granted"
    )

    denied: BooleanLike = Field(
        default="", description="Indicates that the motion for continuance is denied"
    )

    judgment_entry_explanation_line_1: str = Field(
        default="",
        description=(
            "First line for the judge's explanation or notes regarding the ruling .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    judgment_entry_explanation_line_2: str = Field(
        default="",
        description=(
            "Second line for the judge's explanation or notes regarding the ruling .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    judgment_entry_explanation_line_3: str = Field(
        default="",
        description=(
            "Third line for the judge's explanation or notes regarding the ruling .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(
        ..., description="Date the judge signs the judgment entry"
    )  # YYYY-MM-DD format


class ServiceCopiescc(BaseModel):
    """Recipients to receive copies of the judgment entry"""

    cc_line_1: str = Field(
        default="",
        description=(
            "First line for listing parties or attorneys to receive a copy (cc) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    cc_line_2: str = Field(
        default="",
        description=(
            "Second line for listing parties or attorneys to receive a copy (cc) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PainesvilleMunicipalCourtLakeCountyOhioMotionForContinuance(BaseModel):
    """PAINESVILLE MUNICIPAL COURT
    LAKE COUNTY, OHIO

    MOTION FOR CONTINUANCE"""

    case_caption: CaseCaption = Field(..., description="Case Caption")
    motion_for_continuance: MotionforContinuance = Field(..., description="Motion for Continuance")
    additional_information: AdditionalInformation = Field(..., description="Additional Information")
    judgment_entry: JudgmentEntry = Field(..., description="Judgment Entry")
    service__copies_cc: ServiceCopiescc = Field(..., description="Service / Copies (cc)")
