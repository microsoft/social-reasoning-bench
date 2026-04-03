from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AppropriateContactsRow(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Single row in Appropriate Contacts"""

    name: str = Field(
        ...,
        description="Name"
    )
    type: str = Field(
        ...,
        description="Type"
    )
    skill: str = Field(
        ...,
        description="Skill"
    )
    effective_level: str = Field(
        ...,
        description="Effective_Level"
    )
    reliability: str = Field(
        ...,
        description="Reliability"
    )
    base_point_cost: str = Field(
        ...,
        description="Base_Point_Cost"
    )


class CharacterBasics(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Core character concept and template information"""

    starting_points: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Total points available for character creation"
    )

    disadvantage_limit: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Maximum points allowed for disadvantages"
    )

    suggested_character_concepts: str = Field(
        ...,
        description=(
            "Ideas or themes for your character .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    character_racial_templates_point_total: str = Field(
        ...,
        description=(
            "Template name and total points for character or race .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )


class Attributes(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Primary character attributes and house rules"""

    st_min: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Minimum Strength value"
    )

    st_max: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Maximum Strength value"
    )

    st_house_rules: str = Field(
        ...,
        description=(
            "House rules or notes for Strength .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    dx_min: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Minimum Dexterity value"
    )

    dx_max: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Maximum Dexterity value"
    )

    dx_house_rules: str = Field(
        ...,
        description=(
            "House rules or notes for Dexterity .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    iq_min: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Minimum Intelligence value"
    )

    iq_max: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Maximum Intelligence value"
    )

    iq_house_rules: str = Field(
        ...,
        description=(
            "House rules or notes for Intelligence .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    ht_min: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Minimum Health value"
    )

    ht_max: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Maximum Health value"
    )

    ht_house_rules: str = Field(
        ...,
        description=(
            "House rules or notes for Health .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class SecondaryCharacteristics(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Secondary stats derived from attributes"""

    hp_min: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Minimum Hit Points value"
    )

    hp_max: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Maximum Hit Points value"
    )

    hp_house_rules: str = Field(
        ...,
        description=(
            "House rules or notes for Hit Points .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    will_min: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Minimum Will value"
    )

    will_max: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Maximum Will value"
    )

    will_house_rules: str = Field(
        ...,
        description=(
            "House rules or notes for Will .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    per_min: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Minimum Perception value"
    )

    per_max: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Maximum Perception value"
    )

    per_house_rules: str = Field(
        ...,
        description=(
            "House rules or notes for Perception .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    fp_min: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Minimum Fatigue Points value"
    )

    fp_max: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Maximum Fatigue Points value"
    )

    fp_house_rules: str = Field(
        ...,
        description=(
            "House rules or notes for Fatigue Points .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    basic_speed_min: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Minimum Basic Speed value"
    )

    basic_speed_max: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Maximum Basic Speed value"
    )

    basic_speed_house_rules: str = Field(
        ...,
        description=(
            "House rules or notes for Basic Speed .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    basic_move_min: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Minimum Basic Move value"
    )

    basic_move_max: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Maximum Basic Move value"
    )

    basic_move_house_rules: str = Field(
        ...,
        description=(
            "House rules or notes for Basic Move .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class SocialTraits(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Social standing, wealth, culture, and ranks"""

    low_tl: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Lowest Tech Level for character"
    )

    high_tl: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Highest Tech Level for character"
    )

    status_levels_min_max: str = Field(
        ...,
        description=(
            "Minimum and maximum status levels .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    pc_starting_wealth: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Starting wealth for player character"
    )

    wealth_levels_min_max: str = Field(
        ...,
        description=(
            "Minimum and maximum wealth levels .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    cultures_for_cultural_familiarity: str = Field(
        ...,
        description=(
            "Cultures the character is familiar with .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    languages: str = Field(
        ...,
        description=(
            "Languages known by the character .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    social_stigma: str = Field(
        ...,
        description=(
            "Any social stigma affecting the character .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    social_regard: str = Field(
        ...,
        description=(
            "Any social regard affecting the character .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    other: str = Field(
        ...,
        description=(
            "Other social traits .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    rank_type_1: str = Field(
        ...,
        description=(
            "Type of rank (first entry) .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    number_of_levels_1: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of levels for rank (first entry)"
    )

    notes_1: str = Field(
        ...,
        description=(
            "Notes for rank (first entry) .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    rank_type_2: str = Field(
        ...,
        description=(
            "Type of rank (second entry) .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    number_of_levels_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Number of levels for rank (second entry)"
    )

    notes_2: str = Field(
        ...,
        description=(
            "Notes for rank (second entry) .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )


class Advantages(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Advantages allowed or required for the character"""

    required_advantages: str = Field(
        ...,
        description=(
            "Advantages that must be taken .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    allowed_special_advantages: str = Field(
        ...,
        description=(
            "Special advantages allowed for the character .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    prohibited_mundane_advantages: str = Field(
        ...,
        description=(
            "Mundane advantages not allowed .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class Disadvantages(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Disadvantages allowed or required for the character"""

    required_disadvantages: str = Field(
        ...,
        description=(
            "Disadvantages that must be taken .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    allowed_special_disadvantages: str = Field(
        ...,
        description=(
            "Special disadvantages allowed for the character .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    prohibited_mundane_disadvantages: str = Field(
        ...,
        description=(
            "Mundane disadvantages not allowed .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class AppropriateContacts(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Contacts relevant to the character"""

    appropriate_contacts: List[AppropriateContactsRow] = Field(
        ...,
        description=(
            "Table for listing contacts, their type, skill, effective level, reliability, "
            "and base point cost"
        )
    )  # List of table rows


class GurpsCharacterCreationGuidePart1(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    GURPS Character Creation Guide, Part 1

    ''
    """

    character_basics: CharacterBasics = Field(
        ...,
        description="Character Basics"
    )
    attributes: Attributes = Field(
        ...,
        description="Attributes"
    )
    secondary_characteristics: SecondaryCharacteristics = Field(
        ...,
        description="Secondary Characteristics"
    )
    social_traits: SocialTraits = Field(
        ...,
        description="Social Traits"
    )
    advantages: Advantages = Field(
        ...,
        description="Advantages"
    )
    disadvantages: Disadvantages = Field(
        ...,
        description="Disadvantages"
    )
    appropriate_contacts: AppropriateContacts = Field(
        ...,
        description="Appropriate Contacts"
    )