from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EntertainerInformation(BaseModel):
    """Performer and act details for Jammin' at the Market"""

    performer_duo_name: str = Field(
        ...,
        description=(
            "Name of the solo performer or duo applying to perform .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_name: str = Field(
        ...,
        description=(
            'Primary contact person\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_number: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing address for the performer or contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    website: str = Field(
        default="",
        description=(
            "Performer or group's website URL, if available .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Email address for the primary contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    music_background: str = Field(
        ...,
        description=(
            "Brief description of the performer or duo's musical background and experience "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    together_since: str = Field(
        default="",
        description=(
            "Year or date the performer or duo started performing together .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    genre_style: str = Field(
        ...,
        description=(
            "Primary musical genre or style performed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PerformanceFees(BaseModel):
    """Selection of solo or duo performance fee"""

    solo_75_00: BooleanLike = Field(
        default="", description="Check if applying as a solo performer for the $75.00 fee"
    )

    duo_100_00: BooleanLike = Field(
        default="", description="Check if applying as a duo for the $100.00 fee"
    )


class PaymentAuthorization(BaseModel):
    """Payee information and applicant authorization"""

    organization_signing_officer: str = Field(
        default="",
        description=(
            "Name of the organization signing officer to whom the cheque should be made "
            'payable .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of the applicant or authorized signing officer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the application is signed")  # YYYY-MM-DD format


class OfficeUseOnly(BaseModel):
    """For City of Welland staff completion"""

    csc_initial: str = Field(
        default="",
        description=(
            "Initials of CSC staff receiving or processing the application .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class JamminAtTheMarketApplication(BaseModel):
    """
    JAMMIN' AT THE MARKET APPLICATION

    Solos and duets are invited to make a submission for consideration to perform during Jammin' at the Market summer concert series. This series will run June to September at the Welland Farmers' Market, 70 Young Street, with all performances from 10am-11am. Demo required-please include a CD, audio/YouTube/social media link for reference. Performers are required to provide their own sound equipment. A tent and chair(s) will be provided. Performances are rain or shine (in the case of inclement weather, performances will be moved indoors).
    """

    entertainer_information: EntertainerInformation = Field(
        ..., description="Entertainer Information"
    )
    performance_fees: PerformanceFees = Field(..., description="Performance Fees")
    payment__authorization: PaymentAuthorization = Field(..., description="Payment & Authorization")
    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
