from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EntrantDetails(BaseModel):
    """Details of the Food & Drink Hero entrant"""

    full_name_of_hero_applying: str = Field(
        ...,
        description=(
            "Full name of the person being nominated as the Food & Drink Hero .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    current_place_of_employment: str = Field(
        ...,
        description=(
            "Name of the organisation or business where the hero currently works .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    current_position: str = Field(
        ...,
        description=(
            "Job title or role of the hero at their current place of employment .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    length_of_employment_in_above_position: str = Field(
        default="",
        description=(
            "How long the hero has been in their current position (e.g. in years or months) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    contact_telephone: str = Field(
        ...,
        description=(
            "Primary contact telephone number for the hero .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mobile: str = Field(
        default="",
        description=(
            'Mobile phone number for the hero .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Email address for contacting the hero .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    website_if_applicable: str = Field(
        default="",
        description=(
            "Website URL for the hero or their business, if they have one .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    social_media_links_facebook: str = Field(
        default="",
        description=(
            "Link or handle for the hero’s Facebook presence .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    social_media_links_instagram: str = Field(
        default="",
        description=(
            "Link or handle for the hero’s Instagram presence .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    social_media_links_twitter: str = Field(
        default="",
        description=(
            "Link or handle for the hero’s Twitter presence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    social_media_links_trip_advisor: str = Field(
        default="",
        description=(
            "Link or listing URL for the hero’s TripAdvisor presence .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AuthorityandDeclaration(BaseModel):
    """Consent and confirmation of details"""

    authority_consent: BooleanLike = Field(
        ...,
        description=(
            "Confirmation that the details provided are correct and consent is given to "
            "enter them into the awards"
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of the person giving consent .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    print_name: str = Field(
        ...,
        description=(
            "Printed name of the person signing the form .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date on which the form is signed")  # YYYY-MM-DD format


class FoodDrinkHeroQuestion(BaseModel):
    """Main application narrative and supporting information"""

    box_1_details_food_drink_hero_question_600_words_max: str = Field(
        ...,
        description=(
            "Main narrative answering the Food & Drink Hero question, up to 600 words .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    box_2_supporting_information: str = Field(
        default="",
        description=(
            "Additional supporting information such as qualifications, awards, press or "
            'social media references .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class MadesNorthNottsFoodDrinkAwards(BaseModel):
    """
    Made’s North Notts Food & Drink Awards

    We are looking for those who possess the greatest of qualities and the best working practices. The most outstanding, the most ethical, the most food fanatical or just simply those who are thought of as the best. Is it because they source the best ingredients, use the most responsible sources or are they the heart and soul of the community, maybe a person or a business that has done/created something that is out of the ordinary.
    """

    entrant_details: EntrantDetails = Field(..., description="Entrant Details")
    authority_and_declaration: AuthorityandDeclaration = Field(
        ..., description="Authority and Declaration"
    )
    food__drink_hero_question: FoodDrinkHeroQuestion = Field(
        ..., description="Food & Drink Hero Question"
    )
