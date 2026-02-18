from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ArtistInformation(BaseModel):
    """Contact details for the submitting artist"""

    name: str = Field(
        ...,
        description=(
            'Artist\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street address .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of residence .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State abbreviation")

    zip: str = Field(..., description="Zip or postal code")

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Primary contact email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class ArtworkEntry1(BaseModel):
    """Details for the first artwork submitted"""

    item1_title: str = Field(
        ...,
        description=(
            'Title of first artwork entry .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    item1_medium: str = Field(
        ...,
        description=(
            "Medium and recycled materials used for first artwork .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    item1_price: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Sale price for first artwork (leave blank if not for sale)"
    )

    item1_nfs: BooleanLike = Field(
        default="", description="Indicate if first artwork is not for sale (NFS)"
    )


class ArtworkEntry2(BaseModel):
    """Details for the second artwork submitted"""

    item2_title: str = Field(
        default="",
        description=(
            'Title of second artwork entry .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    item2_medium: str = Field(
        default="",
        description=(
            "Medium and recycled materials used for second artwork .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    item2_price: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Sale price for second artwork (leave blank if not for sale)"
    )

    item2_nfs: BooleanLike = Field(
        default="", description="Indicate if second artwork is not for sale (NFS)"
    )


class AgreementandSpecialRequirements(BaseModel):
    """Signature, date, and any special installation requirements"""

    signature: str = Field(
        ...,
        description=(
            "Artist's signature agreeing to the terms .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the form is signed")  # YYYY-MM-DD format

    special_requirements_installation_line_1: str = Field(
        default="",
        description=(
            "First line of any special installation requirements .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    special_requirements_installation_line_2: str = Field(
        default="",
        description=(
            "Second line of any special installation requirements .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LemontCenterForTheArts(BaseModel):
    """
        Lemont
    Center for the ARTS

        In keeping with the show theme, artists are asked to be clear about the types of the recycled media used (e.g., “found photography; reclaimed barn wood”, etc.) and even specify their origins (e.g., “Grandma Helen’s broken china”, thrift shop find, etc.).
    """

    artist_information: ArtistInformation = Field(..., description="Artist Information")
    artwork_entry_1: ArtworkEntry1 = Field(..., description="Artwork Entry 1")
    artwork_entry_2: ArtworkEntry2 = Field(..., description="Artwork Entry 2")
    agreement_and_special_requirements: AgreementandSpecialRequirements = Field(
        ..., description="Agreement and Special Requirements"
    )
