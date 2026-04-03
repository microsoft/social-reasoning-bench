from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EntertainerInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details about the performer or duo and their contact information"""

    performer_duo_name: str = Field(
        ...,
        description=(
            "Name of the solo performer or duo .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    contact_name: str = Field(
        ...,
        description=(
            "Name of the main contact person .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    contact_number: str = Field(
        ...,
        description=(
            "Phone number for contact .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    address: str = Field(
        ...,
        description=(
            "Mailing address of the performer or duo .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    website: str = Field(
        ...,
        description=(
            "Website URL for the performer or duo (if available) .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    email_address: str = Field(
        ...,
        description=(
            "Email address for contact .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    music_background: str = Field(
        ...,
        description=(
            "Brief description of music background .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    together_since: str = Field(
        ...,
        description=(
            "Year or date the performer/duo started performing together .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    genre_style: str = Field(
        ...,
        description=(
            "Musical genre or style .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )


class PerformanceFees(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Selection of performance type and fee"""

    solo_75_00: BooleanLike = Field(
        ...,
        description="Select if applying as a solo performer ($75.00 fee)"
    )

    duo_100_00: BooleanLike = Field(
        ...,
        description="Select if applying as a duo ($100.00 fee)"
    )


class Remuneration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Payment details and authorization"""

    organization_signing_officer: str = Field(
        ...,
        description=(
            "Name of the organization signing officer for cheque payment .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of applicant .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    date: str = Field(
        ...,
        description="Date of signing"
    )  # YYYY-MM-DD format


class AdministrativeUse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """For office use only"""

    csc_initial: str = Field(
        ...,
        description=(
            "Initials of City staff for processing .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class JamminAtTheMarketApplication(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    Jammin’ 
AT THE MARKET APPLICATION

    Solos and duets are invited to make a submission for consideration to perform during Jammin' at the Market summer concert series. This series will run June to September at the Welland Farmers' Market, 70 Young Street, with all performances from 10am-11am. Demo required - please include a CD, audio/YouTube/social media link for reference. Performers are required to provide their own sound equipment. A tent and chair(s) will be provided. Performances are rain or shine (in the case of inclement weather, performances will be moved indoors).
    """

    entertainer_information: EntertainerInformation = Field(
        ...,
        description="Entertainer Information"
    )
    performance_fees: PerformanceFees = Field(
        ...,
        description="Performance Fees"
    )
    remuneration: Remuneration = Field(
        ...,
        description="Remuneration"
    )
    administrative_use: AdministrativeUse = Field(
        ...,
        description="Administrative Use"
    )