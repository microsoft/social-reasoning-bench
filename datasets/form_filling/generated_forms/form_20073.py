from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AwardInformation(BaseModel):
    """Details about the award and show"""

    date: str = Field(
        ..., description="Date the award application is completed and submitted"
    )  # YYYY-MM-DD format

    award_name_and_number: str = Field(
        ...,
        description=(
            "Official name and number of the award being applied for .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title_of_show: str = Field(
        ...,
        description=(
            "Official title of the flower show for which the award application is submitted "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class ClubInformation(BaseModel):
    """Information about the submitting club and district"""

    submitted_by_club_name: str = Field(
        ...,
        description=(
            "Exact name of the club submitting the application, as it should appear on the "
            'certificate .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    district: str = Field(
        ...,
        description=(
            'District of the submitting club .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ContactInformation(BaseModel):
    """Contact details for the individual sending the application"""

    individual_sending_application: str = Field(
        ...,
        description=(
            "Name of the person submitting or mailing the application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing address of the individual sending the application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    zip: str = Field(..., description="ZIP code for the mailing address")

    email: str = Field(
        ...,
        description=(
            "Email address of the individual sending the application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Phone number of the individual sending the application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class pythonGardenClubPAFlowerShowAwardApplication(BaseModel):
    """
        THE GARDEN CLUB FERDERATION OF
    PENNSYLVANIA AWARD APPLICATION FORM
    FOR FLOWER SHOWS

        ''
    """

    award_information: AwardInformation = Field(..., description="Award Information")
    club_information: ClubInformation = Field(..., description="Club Information")
    contact_information: ContactInformation = Field(..., description="Contact Information")
