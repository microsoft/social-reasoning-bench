from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AppropriateContactsNameRow(BaseModel):
    """Single row in Appropriate Contacts Name"""

    name: str = Field(default="", description="Name")
    type: str = Field(default="", description="Type")
    skill: str = Field(default="", description="Skill")
    effective_level: str = Field(default="", description="Effective_Level")
    reliability: str = Field(default="", description="Reliability")
    base_point_cost: str = Field(default="", description="Base_Point_Cost")


class AppropriateContactsTypeRow(BaseModel):
    """Single row in Appropriate Contacts Type"""

    name: str = Field(default="", description="Name")
    type: str = Field(default="", description="Type")
    skill: str = Field(default="", description="Skill")
    effective_level: str = Field(default="", description="Effective_Level")
    reliability: str = Field(default="", description="Reliability")
    base_point_cost: str = Field(default="", description="Base_Point_Cost")


class AppropriateContactsSkillRow(BaseModel):
    """Single row in Appropriate Contacts Skill"""

    name: str = Field(default="", description="Name")
    type: str = Field(default="", description="Type")
    skill: str = Field(default="", description="Skill")
    effective_level: str = Field(default="", description="Effective_Level")
    reliability: str = Field(default="", description="Reliability")
    base_point_cost: str = Field(default="", description="Base_Point_Cost")


class AppropriateContactsEffectiveLevelRow(BaseModel):
    """Single row in Appropriate Contacts Effective Level"""

    name: str = Field(default="", description="Name")
    type: str = Field(default="", description="Type")
    skill: str = Field(default="", description="Skill")
    effective_level: str = Field(default="", description="Effective_Level")
    reliability: str = Field(default="", description="Reliability")
    base_point_cost: str = Field(default="", description="Base_Point_Cost")


class AppropriateContactsReliabilityRow(BaseModel):
    """Single row in Appropriate Contacts Reliability"""

    name: str = Field(default="", description="Name")
    type: str = Field(default="", description="Type")
    skill: str = Field(default="", description="Skill")
    effective_level: str = Field(default="", description="Effective_Level")
    reliability: str = Field(default="", description="Reliability")
    base_point_cost: str = Field(default="", description="Base_Point_Cost")


class AppropriateContactsBasePointCostRow(BaseModel):
    """Single row in Appropriate Contacts Base Point Cost"""

    name: str = Field(default="", description="Name")
    type: str = Field(default="", description="Type")
    skill: str = Field(default="", description="Skill")
    effective_level: str = Field(default="", description="Effective_Level")
    reliability: str = Field(default="", description="Reliability")
    base_point_cost: str = Field(default="", description="Base_Point_Cost")


class CampaignBasics(BaseModel):
    """Overall character creation parameters and templates"""

    starting_points: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total character points each player character starts with"
    )

    disadvantage_limit: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Maximum total points that may be gained from disadvantages"
    )

    suggested_character_concepts: str = Field(
        default="",
        description=(
            "Suggested archetypes or concepts appropriate for this campaign .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
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
    """Primary attributes and any house rules for them"""

    st_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum allowed Strength (ST) score"
    )

    st_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum allowed Strength (ST) score"
    )

    st_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Strength (ST) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dx_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum allowed Dexterity (DX) score"
    )

    dx_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum allowed Dexterity (DX) score"
    )

    dx_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Dexterity (DX) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    iq_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum allowed Intelligence (IQ) score"
    )

    iq_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum allowed Intelligence (IQ) score"
    )

    iq_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Intelligence (IQ) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    ht_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum allowed Health (HT) score"
    )

    ht_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum allowed Health (HT) score"
    )

    ht_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Health (HT) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class SecondaryCharacteristics(BaseModel):
    """Secondary stats derived from attributes, with limits and house rules"""

    hp_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum allowed Hit Points (HP) relative to base"
    )

    hp_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum allowed Hit Points (HP) relative to base"
    )

    hp_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Hit Points (HP) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    will_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum allowed Will score relative to base"
    )

    will_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum allowed Will score relative to base"
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
        default="", description="Minimum allowed Perception (Per) score relative to base"
    )

    per_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum allowed Perception (Per) score relative to base"
    )

    per_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Perception (Per) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    fp_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum allowed Fatigue Points (FP) relative to base"
    )

    fp_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum allowed Fatigue Points (FP) relative to base"
    )

    fp_house_rules: str = Field(
        default="",
        description=(
            "House rules or notes specific to Fatigue Points (FP) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    basic_speed_min: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum allowed Basic Speed relative to base"
    )

    basic_speed_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum allowed Basic Speed relative to base"
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
        default="", description="Minimum allowed Basic Move relative to base"
    )

    basic_move_max: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Maximum allowed Basic Move relative to base"
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
    """Tech level, wealth, culture, language, status, and rank-related traits"""

    low_tl: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Lowest allowed Tech Level (TL) for characters"
    )

    high_tl: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Highest allowed Tech Level (TL) for characters"
    )

    status_levels_min_max: str = Field(
        default="",
        description=(
            "Minimum and maximum allowed Status levels .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    pc_starting_wealth: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Starting wealth for player characters, usually in campaign currency",
    )

    wealth_levels_min_max: str = Field(
        default="",
        description=(
            "Minimum and maximum allowed Wealth advantage levels .If you cannot fill this, "
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
            "Languages commonly known or available in the campaign .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    social_stigma: str = Field(
        default="",
        description=(
            "Common or campaign-specific Social Stigma disadvantages .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    social_regard: str = Field(
        default="",
        description=(
            "Common or campaign-specific Social Regard advantages .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other: str = Field(
        default="",
        description=(
            "Any other notable social traits or modifiers .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    rank_type_1: str = Field(
        default="",
        description=(
            "Type of Rank (e.g., Military, Religious) for the first rank entry .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    number_of_levels_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of levels in the first Rank entry"
    )

    notes_1: str = Field(
        default="",
        description=(
            'Notes for the first Rank entry .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    rank_type_2: str = Field(
        default="",
        description=(
            "Type of Rank for the second rank entry .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    number_of_levels_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of levels in the second Rank entry"
    )

    notes_2: str = Field(
        default="",
        description=(
            'Notes for the second Rank entry .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class Advantages(BaseModel):
    """Allowed, required, and prohibited advantages"""

    required_advantages: str = Field(
        default="",
        description=(
            "Advantages that all or certain characters must take .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    allowed_special_advantages: str = Field(
        default="",
        description=(
            "Special or unusual advantages that are permitted in this campaign .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    prohibited_mundane_advantages: str = Field(
        default="",
        description=(
            "Ordinary advantages that are not allowed in this campaign .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Disadvantages(BaseModel):
    """Allowed, required, and prohibited disadvantages"""

    required_disadvantages: str = Field(
        default="",
        description=(
            "Disadvantages that all or certain characters must take .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    allowed_special_disadvantages: str = Field(
        default="",
        description=(
            "Special or unusual disadvantages that are permitted in this campaign .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    prohibited_mundane_disadvantages: str = Field(
        default="",
        description=(
            "Ordinary disadvantages that are not allowed in this campaign .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class AppropriateContacts(BaseModel):
    """Details for contacts appropriate to the campaign"""

    appropriate_contacts_name: List[AppropriateContactsNameRow] = Field(
        default="",
        description=(
            "Table of appropriate Contacts, including name, type, skill, effective level, "
            "reliability, and base point cost"
        ),
    )  # List of table rows

    appropriate_contacts_type: List[AppropriateContactsTypeRow] = Field(
        default="", description="Same contacts table; see 'Appropriate Contacts Name'"
    )  # List of table rows

    appropriate_contacts_skill: List[AppropriateContactsSkillRow] = Field(
        default="", description="Same contacts table; see 'Appropriate Contacts Name'"
    )  # List of table rows

    appropriate_contacts_effective_level: List[AppropriateContactsEffectiveLevelRow] = Field(
        default="", description="Same contacts table; see 'Appropriate Contacts Name'"
    )  # List of table rows

    appropriate_contacts_reliability: List[AppropriateContactsReliabilityRow] = Field(
        default="", description="Same contacts table; see 'Appropriate Contacts Name'"
    )  # List of table rows

    appropriate_contacts_base_point_cost: List[AppropriateContactsBasePointCostRow] = Field(
        default="", description="Same contacts table; see 'Appropriate Contacts Name'"
    )  # List of table rows


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
