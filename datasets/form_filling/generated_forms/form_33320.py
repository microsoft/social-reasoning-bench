from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PatientInformation(BaseModel):
    """Basic identifying and contact details for the patient"""

    patient_name: str = Field(
        ...,
        description=(
            'Full legal name of the patient .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    ohip: str = Field(
        ...,
        description=(
            "Patient's OHIP (Ontario Health Insurance Plan) number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(
        ..., description="Patient's date of birth (DD/MM/YYYY)"
    )  # YYYY-MM-DD format

    telephone: str = Field(
        ...,
        description=(
            "Primary telephone contact number(s) for the patient .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    h: BooleanLike = Field(
        default="", description="Indicates that the listed telephone number is a home number"
    )

    w: BooleanLike = Field(
        default="", description="Indicates that the listed telephone number is a work number"
    )

    c: BooleanLike = Field(
        default="", description="Indicates that the listed telephone number is a cell/mobile number"
    )


class ReferralDetails(BaseModel):
    """Reason for referral and requested services"""

    referral: str = Field(
        ...,
        description=(
            "Details of the referral, including reason and relevant clinical information "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    physiotherapy: BooleanLike = Field(
        default="", description="Check if the referral is for physiotherapy services"
    )

    massage_therapy: BooleanLike = Field(
        default="", description="Check if the referral is for massage therapy services"
    )

    wound_care: BooleanLike = Field(
        default="", description="Check if the referral is for wound care services"
    )

    comments: str = Field(
        default="",
        description=(
            "Additional comments or relevant information about the referral .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class PhysicianInformation(BaseModel):
    """Referring physician’s details and authorization"""

    physicians_name: str = Field(
        ...,
        description=(
            'Full name of the referring physician .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    physicians_signature: str = Field(
        ...,
        description=(
            'Signature of the referring physician .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_dd_mm_yyyy: str = Field(
        ..., description="Date the referral form is completed (DD/MM/YYYY)"
    )  # YYYY-MM-DD format


class BreastRehabReferralForm(BaseModel):
    """
        breast rehab
    referral form

        ''
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    referral_details: ReferralDetails = Field(..., description="Referral Details")
    physician_information: PhysicianInformation = Field(..., description="Physician Information")
