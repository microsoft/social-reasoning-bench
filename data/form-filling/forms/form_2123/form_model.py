from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class NameRow(BaseModel):
    """Single row in Name"""

    name: str = Field(default="", description="Name")
    type: str = Field(default="", description="Type")
    skill: str = Field(default="", description="Skill")
    effective_level: str = Field(default="", description="Effective_Level")
    reliability: str = Field(default="", description="Reliability")
    base_point_cost: str = Field(default="", description="Base_Point_Cost")


class CampaignBasics(BaseModel):
    """Overall point budget and template guidance for character creation"""

    starting_points: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total character points available at character creation"
    )

    disadvantage_limit: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Maximum total points that may be gained from disadvantages"
    )

    suggested_character_concepts: str = Field(
        default="",
        description=(
            "Brief descriptions of character concepts appropriate for this campaign .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    character_racial_templates_point_total: str = Field(
        default="",
        description=(
            "List of allowed character or racial templates and their point totals .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Attributes(BaseModel):
    """Primary attributes and their allowed ranges/house rules"""

    st_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum Strength score allowed for characters"
    )

    st_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum Strength score allowed for characters"
    )

    st_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Strength .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dx_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum Dexterity score allowed for characters"
    )

    dx_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum Dexterity score allowed for characters"
    )

    dx_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Dexterity .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    iq_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum Intelligence score allowed for characters"
    )

    iq_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum Intelligence score allowed for characters"
    )

    iq_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Intelligence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ht_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum Health score allowed for characters"
    )

    ht_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum Health score allowed for characters"
    )

    ht_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Health .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class SecondaryCharacteristics(BaseModel):
    """Secondary stats relative to base attributes, with ranges and house rules"""

    hp_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum Hit Points relative to base allowed"
    )

    hp_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum Hit Points relative to base allowed"
    )

    hp_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Hit Points .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    will_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum Will score relative to base allowed"
    )

    will_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum Will score relative to base allowed"
    )

    will_house_rules: str = Field(
        default="",
        description=(
            'House rules or notes specific to Will .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    per_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum Perception score relative to base allowed"
    )

    per_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum Perception score relative to base allowed"
    )

    per_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Perception .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    fp_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum Fatigue Points relative to base allowed"
    )

    fp_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum Fatigue Points relative to base allowed"
    )

    fp_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Fatigue Points .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    basic_speed_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum Basic Speed relative to base allowed"
    )

    basic_speed_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum Basic Speed relative to base allowed"
    )

    basic_speed_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Basic Speed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    basic_move_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum Basic Move relative to base allowed"
    )

    basic_move_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum Basic Move relative to base allowed"
    )

    basic_move_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Basic Move .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class SocialTraits(BaseModel):
    """Tech level, wealth, status, culture, language, and rank-related traits"""

    low_tl: str = Field(
        default="",
        description=(
            "Lowest Technology Level allowed or typical for the campaign .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    high_tl: str = Field(
        default="",
        description=(
            "Highest Technology Level allowed or typical for the campaign .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    status_levels_min_max: str = Field(
        default="",
        description=(
            "Minimum and maximum social Status levels allowed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    pc_starting_wealth: str = Field(
        default="",
        description=(
            "Standard starting wealth for player characters .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    wealth_levels_min_max: str = Field(
        default="",
        description=(
            "Minimum and maximum Wealth advantage levels allowed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cultures_for_cultural_familiarity: str = Field(
        default="",
        description=(
            "List of cultures relevant for Cultural Familiarity advantages .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    languages: str = Field(
        default="",
        description=(
            "List of languages commonly known or available in the campaign .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    social_stigma: str = Field(
        default="",
        description=(
            "Common or campaign-specific Social Stigma traits .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    social_regard: str = Field(
        default="",
        description=(
            "Common or campaign-specific Social Regard traits .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other: str = Field(
        default="",
        description=(
            "Other notable social traits or modifiers .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    rank_type_1: str = Field(
        default="",
        description=(
            "Type of Rank advantage (e.g., Military, Religious) for the first rank entry "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    number_of_levels_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of levels in the first Rank type"
    )

    notes_1: str = Field(
        default="",
        description=(
            "Notes or restrictions for the first Rank entry .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    rank_type_2: str = Field(
        default="",
        description=(
            "Type of Rank advantage for the second rank entry .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    number_of_levels_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of levels in the second Rank type"
    )

    notes_2: str = Field(
        default="",
        description=(
            "Notes or restrictions for the second Rank entry .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Advantages(BaseModel):
    """Required, allowed, and prohibited advantages for the campaign"""

    required_advantages: str = Field(
        default="",
        description=(
            "List of advantages that all characters must take .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    allowed_special_advantages: str = Field(
        default="",
        description=(
            "List of unusual or special advantages that are permitted .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    prohibited_mundane_advantages: str = Field(
        default="",
        description=(
            "List of ordinary advantages that are not allowed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Disadvantages(BaseModel):
    """Required, allowed, and prohibited disadvantages for the campaign"""

    required_disadvantages: str = Field(
        default="",
        description=(
            "List of disadvantages that all characters must take .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    allowed_special_disadvantages: str = Field(
        default="",
        description=(
            "List of unusual or special disadvantages that are permitted .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    prohibited_mundane_disadvantages: str = Field(
        default="",
        description=(
            "List of ordinary disadvantages that are not allowed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AppropriateContacts(BaseModel):
    """Contacts available in the campaign and their stats"""

    name: List[NameRow] = Field(
        default_factory=list,
        description=(
            "Table of appropriate contacts including name, type, skill, level, reliability, "
            "and point cost"
        ),
    )  # List of table rows

    type: str = Field(
        default="",
        description=(
            "Contact type (e.g., police, criminal, merchant) when not using the table "
            'structure .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    skill: str = Field(
        default="",
        description=(
            "Primary skill or area of expertise of the contact when not using the table "
            'structure .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    effective_level: str = Field(
        default="",
        description=(
            "Effective skill level of the contact when not using the table structure .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reliability: str = Field(
        default="",
        description=(
            "Reliability rating of the contact when not using the table structure .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    base_point_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Base point cost of the contact when not using the table structure"
    )


class GurpsCharacterCreationGuidePart1(BaseModel):
    """
    GURPS Character Creation Guide, Part 1

    ''
    """

    campaign_basics: CampaignBasics = Field(..., description="Campaign Basics")
    attributes: Attributes = Field(..., description="Attributes")
    secondary_characteristics: SecondaryCharacteristics = Field(
        ..., description="Secondary Characteristics"
    )
    social_traits: SocialTraits = Field(..., description="Social Traits")
    advantages: Advantages = Field(..., description="Advantages")
    disadvantages: Disadvantages = Field(..., description="Disadvantages")
    appropriate_contacts: AppropriateContacts = Field(..., description="Appropriate Contacts")
