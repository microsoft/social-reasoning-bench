from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EntrantDetails(BaseModel):
    """Basic details of the Food & Drink Hero entrant"""

    full_name_of_hero_applying: str = Field(
        ...,
        description=(
            "Full name of the person being nominated as the 'hero' .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    current_place_of_employment: str = Field(
        ...,
        description=(
            "Name of the hero’s current employer or business .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    current_position: str = Field(
        ...,
        description=(
            'Current job title or role of the hero .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    length_of_employment_in_above_position: str = Field(
        ...,
        description=(
            "How long the hero has been in their current position (e.g. years, months) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    contact_telephone: str = Field(
        ...,
        description=(
            'Primary contact telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mobile: str = Field(
        default="",
        description=(
            'Mobile phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Main email address for contacting the hero .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
            "Link or handle for the hero’s Instagram account .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    social_media_links_twitter: str = Field(
        default="",
        description=(
            "Link or handle for the hero’s Twitter account .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    social_media_links_trip_advisor: str = Field(
        default="",
        description=(
            "Link to the hero’s or business’s TripAdvisor page .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Declaration(BaseModel):
    """Authority, signature and date confirming the information provided"""

    authority_consent: BooleanLike = Field(
        ...,
        description=(
            "Confirmation that the details are correct and consent is given to enter the awards"
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
            "Printed full name of the person signing .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the form is signed")  # YYYY-MM-DD format


class FoodDrinkHeroApplication(BaseModel):
    """Main application questions and supporting information"""

    box_1_the_food_drink_hero_question_600_words_max: str = Field(
        ...,
        description=(
            "Main narrative explaining why the nominee is the North Notts Food & Drink Hero "
            '(up to 600 words) .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    box_2_supporting_information: str = Field(
        default="",
        description=(
            "Additional supporting information such as qualifications, awards, press or "
            "social media coverage relevant to the application .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class MadesNorthNottsFoodDrinkAwards(BaseModel):
    """
    Made’s North Notts Food & Drink Awards

    We are looking for those who possess the greatest of qualities and the best working practices. The most outstanding, the most ethical, the most food fanatical or just simply those who are thought of as the best. Is it because they source the best ingredients, use the most responsible sources or are they the heart and soul of the community, maybe a person or a business that has done/created something that is out of the ordinary.
    """

    entrant_details: EntrantDetails = Field(..., description="Entrant Details")
    declaration: Declaration = Field(..., description="Declaration")
    food__drink_hero_application: FoodDrinkHeroApplication = Field(
        ..., description="Food & Drink Hero Application"
    )
