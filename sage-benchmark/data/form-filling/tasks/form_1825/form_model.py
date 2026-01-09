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
    """Performer and act details, including contact and background information"""

    performer_duo_name: str = Field(
        ...,
        description=(
            'Name of the solo performer or duo .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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
            "Performer or group's website URL, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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
            "Brief description of musical experience and background .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    together_since: str = Field(
        default="",
        description=(
            "Year or date the act started performing together .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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


class PerformancePaymentDetails(BaseModel):
    """Performance type selection and payment information"""

    solo_75_00: BooleanLike = Field(
        default="", description="Check if the performance is a solo act with a $75.00 fee"
    )

    duo_100_00: BooleanLike = Field(
        default="", description="Check if the performance is a duo act with a $100.00 fee"
    )

    remuneration_payable_to: str = Field(
        ...,
        description=(
            "Name of the individual or organization to whom the cheque should be made "
            'payable .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class Authorization(BaseModel):
    """Sign-off and internal use"""

    signature: str = Field(
        ...,
        description=(
            "Signature of the applicant or authorized signing officer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the application is signed")  # YYYY-MM-DD format

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
    JAMMIN’ AT THE MARKET APPLICATION

    Solos and duets are invited to make a submission for consideration to perform during Jammin’ at the Market summer concert series. This series will run June to September at the Welland Farmers’ Market, 70 Young Street, with all performances from 10am-11am. Demo required-please include a CD, audio/YouTube/social media link for reference. Performers are required to provide their own sound equipment. A tent and chair(s) will be provided. Performances are rain or shine (in the case of inclement weather, performances will be moved indoors).
    """

    entertainer_information: EntertainerInformation = Field(
        ..., description="Entertainer Information"
    )
    performance__payment_details: PerformancePaymentDetails = Field(
        ..., description="Performance & Payment Details"
    )
    authorization: Authorization = Field(..., description="Authorization")
