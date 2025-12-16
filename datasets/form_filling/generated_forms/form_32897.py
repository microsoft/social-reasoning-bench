from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Details(BaseModel):
    """Artist personal and contact details"""

    first_name: str = Field(
        ...,
        description=(
            'Artist\'s given name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Artist\'s family name or surname .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Artist's date of birth")  # YYYY-MM-DD format

    address_line_1: str = Field(
        ...,
        description=(
            'Street address, first line .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address_line_2: str = Field(
        default="",
        description=(
            "Additional address information, second line (optional) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State or territory of residence")

    postcode: str = Field(..., description="Postcode for the address")

    email: str = Field(
        ...,
        description=(
            'Artist\'s email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Artist\'s primary contact phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    gallery_dealer_contact_details_if_applicable: str = Field(
        default="",
        description=(
            "Contact details for the artist's gallery or dealer, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class DetailsofProposedArtwork(BaseModel):
    """Information about the proposed artwork"""

    western_australian_flora_botanical_names: str = Field(
        ...,
        description=(
            "Botanical name or names of the Western Australian flora depicted .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    medium: str = Field(
        ...,
        description=(
            "Art medium used (e.g. oil, acrylic, watercolor, sculpture) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    approximate_size: str = Field(
        ...,
        description=(
            'Approximate dimensions of the artwork .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    description: str = Field(
        ...,
        description=(
            "Brief description of the proposed artwork .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ArtistExpressionOfInterest(BaseModel):
    """
    Artist Expression of Interest

    ''
    """

    details: Details = Field(..., description="Details")
    details_of_proposed_artwork: DetailsofProposedArtwork = Field(
        ..., description="Details of Proposed Artwork"
    )
