from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CaseInformation(BaseModel):
    """Basic case caption details"""

    plaintiff: str = Field(
        ...,
        description=(
            'Name of the plaintiff in this case .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    case_number: str = Field(
        ...,
        description=(
            "Court-assigned case number for this matter .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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


class EffortstoObtainCounsel(BaseModel):
    """Description of attempts to secure legal representation"""

    other_material_if_any: str = Field(
        default="",
        description=(
            "Description of any additional materials attached in support of this motion .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    efforts_to_obtain_counsel_line_1: str = Field(
        ...,
        description=(
            "First line describing efforts made to obtain counsel without payment or on a "
            'contingent fee basis .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    efforts_to_obtain_counsel_line_2: str = Field(
        ...,
        description=(
            "Second line describing efforts made to obtain counsel .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    efforts_to_obtain_counsel_line_3: str = Field(
        ...,
        description=(
            "Third line describing efforts made to obtain counsel .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    efforts_to_obtain_counsel_line_4: str = Field(
        ...,
        description=(
            "Fourth line describing efforts made to obtain counsel .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    efforts_to_obtain_counsel_line_5: str = Field(
        ...,
        description=(
            "Fifth line describing efforts made to obtain counsel .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SignatureandContactInformation(BaseModel):
    """Certification, signature, and contact details of the movant"""

    date: str = Field(..., description="Date the motion is signed")  # YYYY-MM-DD format

    signature: str = Field(
        ...,
        description=(
            "Signature of the party requesting appointment of counsel .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    print_name: str = Field(
        ...,
        description=(
            "Printed name of the person signing the motion .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing address of the person requesting appointment of counsel .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code corresponding to the address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            "Telephone number where the party can be reached .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class MotionForTheAppointmentOfCounsel(BaseModel):
    """
    MOTION FOR THE APPOINTMENT OF COUNSEL

    I request that the Court appoint an attorney to represent me in the matter cited above.
    """

    case_information: CaseInformation = Field(..., description="Case Information")
    efforts_to_obtain_counsel: EffortstoObtainCounsel = Field(
        ..., description="Efforts to Obtain Counsel"
    )
    signature_and_contact_information: SignatureandContactInformation = Field(
        ..., description="Signature and Contact Information"
    )
