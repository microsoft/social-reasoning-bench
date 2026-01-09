from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class NomineeInformation(BaseModel):
    """Basic information about the person being nominated"""

    name_placed_in_nomination: str = Field(
        ...,
        description=(
            "Full name of the person being nominated for the award .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    position_title: str = Field(
        ...,
        description=(
            "Current position or job title of the nominee .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    jurisdiction: str = Field(
        ...,
        description=(
            "Jurisdiction or organization where the nominee serves .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class NominationDetails(BaseModel):
    """Details about the type of nomination and contact person"""

    chapter_nomination: str = Field(
        default="",
        description=(
            "Name of the chapter submitting the nomination, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    individual_nomination: str = Field(
        default="",
        description=(
            "Name of the individual submitting the nomination, if not a chapter .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    contact_person_with_phone_or_email: str = Field(
        ...,
        description=(
            "Name of the contact person and their phone number or email address .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ProfessionalOfficesHeld(BaseModel):
    """Elected offices held by the nominee in various organizations"""

    nominees_chapter: str = Field(
        default="",
        description=(
            "Chapter in which the nominee has held elected office, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    state_chapter: str = Field(
        default="",
        description=(
            "State chapter in which the nominee has held elected office, if applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    region_8: str = Field(
        default="",
        description=(
            "Region 8 position or role held by the nominee, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    icc: str = Field(
        default="",
        description=(
            "ICC position or role held by the nominee, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AchievementsandJustification(BaseModel):
    """Civic involvement, achievements, and reasons for consideration"""

    civic_involvement_if_known: str = Field(
        default="",
        description=(
            "Description of the nominee's civic or community involvement, if known .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_notable_achievements: str = Field(
        default="",
        description=(
            "Any other notable achievements or accomplishments of the nominee .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    additional_comments_on_why_the_nominee_should_be_considered_for_this_award: str = Field(
        default="",
        description=(
            "Additional comments explaining why the nominee deserves this award .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class BOAGHalCosperLifetimeAchievementAwardNomination(BaseModel):
    """
        BUILDING OFFICIALS ASSOCIATION OF

    GEORGIA

    Hal Cosper Memorial Lifetime Achievement Award Nomination

        Instructions: The nominating form must be completed and postmarked by the date indicated below. Where dates are requested, the year is sufficient. If additional attachments are used, please staple to the nomination form. Within the comment section state briefly why the person nominated is deserving of the award.
    """

    nominee_information: NomineeInformation = Field(..., description="Nominee Information")
    nomination_details: NominationDetails = Field(..., description="Nomination Details")
    professional_offices_held: ProfessionalOfficesHeld = Field(
        ..., description="Professional Offices Held"
    )
    achievements_and_justification: AchievementsandJustification = Field(
        ..., description="Achievements and Justification"
    )
