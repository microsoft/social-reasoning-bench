from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantDetails(BaseModel):
    """Primary artist or group contact information"""

    artist_or_group_name: str = Field(
        ...,
        description=(
            "Name of the individual artist or the group applying for the exhibition .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    contact_person: str = Field(
        ...,
        description=(
            "Name of the primary contact person for this application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Postal or street address for the artist or group .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            "Primary landline or contact telephone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Email address for correspondence about the exhibition application .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mobile: str = Field(
        default="",
        description=(
            "Mobile phone number for the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    website: str = Field(
        default="",
        description=(
            "Artist or group website URL, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalArtistsGroupExhibitions(BaseModel):
    """Details of additional artists for group exhibitions"""

    additional_artist_2_name_and_address: str = Field(
        default="",
        description=(
            "Name and address of the second additional artist in a group exhibition .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    additional_artist_3_name_and_address: str = Field(
        default="",
        description=(
            "Name and address of the third additional artist in a group exhibition .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    additional_artist_4_name_and_address: str = Field(
        default="",
        description=(
            "Name and address of the fourth additional artist in a group exhibition .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ExhibitionDetails(BaseModel):
    """Information about the proposed exhibition"""

    proposed_exhibition_title: str = Field(
        ...,
        description=(
            'Title of the proposed exhibition .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    exhibition_rationale: str = Field(
        ...,
        description=(
            "Brief rationale or concept statement for the proposed exhibition .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    fundraiser_not_for_profit_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if the proposed exhibition is a fundraiser for a not-for-profit organisation"
        ),
    )

    fundraiser_not_for_profit_no: BooleanLike = Field(
        default="",
        description=(
            "Select if the proposed exhibition is not a fundraiser for a not-for-profit "
            "organisation"
        ),
    )

    gallery_number: str = Field(
        default="",
        description=(
            "Identifier or number of the preferred gallery space .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    preferred_gallery_space: str = Field(
        default="",
        description=(
            "Description or name of the preferred gallery space .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class GalleryExhibitionApplicationForm(BaseModel):
    """
    Gallery Exhibition Application Form

    For group exhibitions please nominate a contact person to fill in and sign this application.
    """

    applicant_details: ApplicantDetails = Field(..., description="Applicant Details")
    additional_artists_group_exhibitions: AdditionalArtistsGroupExhibitions = Field(
        ..., description="Additional Artists (Group Exhibitions)"
    )
    exhibition_details: ExhibitionDetails = Field(..., description="Exhibition Details")
