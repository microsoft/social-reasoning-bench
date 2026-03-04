from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CampaignOverview(BaseModel):
    """Basic information and high-level description of the campaign"""

    campaign_name: str = Field(
        ...,
        description=(
            'Name of the GURPS campaign .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    gm: str = Field(
        ...,
        description=(
            "Name of the Game Master running the campaign .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    creation_date: str = Field(
        default="", description="Date this campaign prospectus was created"
    )  # YYYY-MM-DD format

    genre: str = Field(
        ...,
        description=(
            "Primary genre of the campaign (e.g., fantasy, sci-fi, horror) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    tech_level_tl: str = Field(
        ...,
        description=(
            "Overall technology level of the setting (GURPS TL value) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tl_exceptions: str = Field(
        default="",
        description=(
            "Notable exceptions to the general tech level (e.g., advanced medicine, "
            'primitive weapons) .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    power_level: str = Field(
        ...,
        description=(
            "Overall power level of characters (e.g., point total or descriptive level) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    realism_level: Literal[
        "Grittly Realistic", "Realistic", "Cinematic", "Over-the-Top", "N/A", ""
    ] = Field(..., description="Tone of realism for the campaign")

    campaign_synopsis_and_recent_events: str = Field(
        ...,
        description=(
            "Summary of the campaign premise and any recent or ongoing events .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    timeline_of_significant_historical_events: str = Field(
        default="",
        description=(
            "Chronological list of important historical events in the setting .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Economy(BaseModel):
    """Currency and economic basics of the setting"""

    currency_value_1: str = Field(
        default="",
        description=(
            "Description or name of a currency and its value relative to a baseline .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    currency_value_2: str = Field(
        default="",
        description=(
            "Description or name of a second currency and its value .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    currency_value_3: str = Field(
        default="",
        description=(
            "Description or name of a third currency and its value .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    precious_metals: BooleanLike = Field(
        default="",
        description="Indicate whether precious metals are used as currency or store of value",
    )

    paper_money: BooleanLike = Field(
        default="", description="Indicate whether paper money is used in the setting"
    )

    e_money: BooleanLike = Field(
        default="", description="Indicate whether electronic money is used in the setting"
    )

    is_slavery_legal: BooleanLike = Field(
        default="", description="Indicate whether slavery is legally permitted in the setting"
    )


class MajorNations(BaseModel):
    """Details for major nations in the campaign world"""

    major_nation_1_name: str = Field(
        default="",
        description=(
            'Name of the major nation .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_capital: str = Field(
        default="",
        description=(
            'Capital city of the major nation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_ruler: str = Field(
        default="",
        description=(
            "Primary ruler or head of state of the nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_population: str = Field(
        default="",
        description=(
            'Approximate population of the nation .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_search_bonus: str = Field(
        default="",
        description=(
            "Search bonus modifier associated with this nation .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_terrain: str = Field(
        default="",
        description=(
            "Dominant terrain types within the nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_appearance: str = Field(
        default="",
        description=(
            "General appearance modifier or description for inhabitants .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_hygiene: str = Field(
        default="",
        description=(
            "Hygiene level or modifier for the nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_mana: str = Field(
        default="",
        description=(
            "Mana level or magical energy availability in the nation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_enchantment: str = Field(
        default="",
        description=(
            "Enchantment level or prevalence of magical items .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_cultural_familiarity: str = Field(
        default="",
        description=(
            "Relevant cultural familiarities for this nation .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_languages: str = Field(
        default="",
        description=(
            "Languages commonly spoken in the nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_literacy: str = Field(
        default="",
        description=(
            "General literacy level or rules for literacy in the nation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_tl: str = Field(
        default="",
        description=(
            'Tech level specific to this nation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_wealth: str = Field(
        default="",
        description=(
            "Typical wealth level or economic status in the nation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_status_range: str = Field(
        default="",
        description=(
            "Range of social Status levels common in the nation .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_society_government: str = Field(
        default="",
        description=(
            "Type of society and form of government .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_control_rating_cr: str = Field(
        default="",
        description=(
            "Control Rating value representing governmental control .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_corruption_modifier: str = Field(
        default="",
        description=(
            "Modifier representing the level of corruption .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_military_resources: str = Field(
        default="",
        description=(
            "Summary of the nation's military resources and capabilities .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    major_nation_1_defense_bonus: str = Field(
        default="",
        description=(
            "Defense bonus value associated with the nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_notes: str = Field(
        default="",
        description=(
            "Additional notes or details about the nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_name: str = Field(
        default="",
        description=(
            'Name of the second major nation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_capital: str = Field(
        default="",
        description=(
            "Capital city of the second major nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_ruler: str = Field(
        default="",
        description=(
            "Primary ruler or head of state of the second nation .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_population: str = Field(
        default="",
        description=(
            "Approximate population of the second nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_search_bonus: str = Field(
        default="",
        description=(
            "Search bonus modifier for the second nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_terrain: str = Field(
        default="",
        description=(
            "Dominant terrain types within the second nation .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_appearance: str = Field(
        default="",
        description=(
            "General appearance modifier or description for inhabitants of the second "
            'nation .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    major_nation_2_hygiene: str = Field(
        default="",
        description=(
            "Hygiene level or modifier for the second nation .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_mana: str = Field(
        default="",
        description=(
            "Mana level or magical energy availability in the second nation .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    major_nation_2_enchantment: str = Field(
        default="",
        description=(
            "Enchantment level or prevalence of magical items in the second nation .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    major_nation_2_cultural_familiarity: str = Field(
        default="",
        description=(
            "Relevant cultural familiarities for the second nation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_languages: str = Field(
        default="",
        description=(
            "Languages commonly spoken in the second nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_literacy: str = Field(
        default="",
        description=(
            "General literacy level or rules for literacy in the second nation .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    major_nation_2_tl: str = Field(
        default="",
        description=(
            "Tech level specific to the second nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_wealth: str = Field(
        default="",
        description=(
            "Typical wealth level or economic status in the second nation .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    major_nation_2_status_range: str = Field(
        default="",
        description=(
            "Range of social Status levels common in the second nation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_society_government: str = Field(
        default="",
        description=(
            "Type of society and form of government in the second nation .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    major_nation_2_control_rating_cr: str = Field(
        default="",
        description=(
            "Control Rating value representing governmental control in the second nation "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    major_nation_2_corruption_modifier: str = Field(
        default="",
        description=(
            "Modifier representing the level of corruption in the second nation .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    major_nation_2_military_resources: str = Field(
        default="",
        description=(
            "Summary of the second nation's military resources and capabilities .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    major_nation_2_defense_bonus: str = Field(
        default="",
        description=(
            "Defense bonus value associated with the second nation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_notes: str = Field(
        default="",
        description=(
            "Additional notes or details about the second nation .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class OtherMajorPlanesofExistence(BaseModel):
    """Information about other planes relevant to the campaign"""

    plane_1_name: str = Field(
        default="",
        description=(
            "Name of the other major plane of existence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    plane_1_type: str = Field(
        default="",
        description=(
            "Type or category of this plane (e.g., astral, elemental) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    plane_1_description: str = Field(
        default="",
        description=(
            "Brief description of the plane of existence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    plane_2_name: str = Field(
        default="",
        description=(
            "Name of the second major plane of existence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    plane_2_type: str = Field(
        default="",
        description=(
            'Type or category of the second plane .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    plane_2_description: str = Field(
        default="",
        description=(
            "Brief description of the second plane of existence .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Rules(BaseModel):
    """GURPS books used, optional rules, and house rules for the campaign"""

    book_1_title: str = Field(
        default="",
        description=(
            "Title of a GURPS book used in this campaign .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    book_1_notes: str = Field(
        default="",
        description=(
            'Notes on how this GURPS book is used .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    book_2_title: str = Field(
        default="",
        description=(
            'Title of a second GURPS book used .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    book_2_notes: str = Field(
        default="",
        description=(
            "Notes on how the second GURPS book is used .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    book_3_title: str = Field(
        default="",
        description=(
            'Title of a third GURPS book used .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    book_3_notes: str = Field(
        default="",
        description=(
            "Notes on how the third GURPS book is used .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    optional_rule_1_rule: str = Field(
        default="",
        description=(
            "Name or description of an optional rule used .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    optional_rule_1_book: str = Field(
        default="",
        description=(
            "Book where this optional rule is found .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    optional_rule_1_page: str = Field(
        default="",
        description=(
            "Page number of the optional rule in the book .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    optional_rule_2_rule: str = Field(
        default="",
        description=(
            "Name or description of a second optional rule used .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    optional_rule_2_book: str = Field(
        default="",
        description=(
            "Book where the second optional rule is found .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    optional_rule_2_page: str = Field(
        default="",
        description=(
            "Page number of the second optional rule in the book .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    optional_rule_3_rule: str = Field(
        default="",
        description=(
            "Name or description of a third optional rule used .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    optional_rule_3_book: str = Field(
        default="",
        description=(
            "Book where the third optional rule is found .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    optional_rule_3_page: str = Field(
        default="",
        description=(
            "Page number of the third optional rule in the book .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    house_rules: str = Field(
        default="",
        description=(
            "Custom house rules used in this campaign .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ExpandedCampaignPlanningForm(BaseModel):
    """
    EXPANDED CAMPAIGN PLANNING FORM

    ''
    """

    campaign_overview: CampaignOverview = Field(..., description="Campaign Overview")
    economy: Economy = Field(..., description="Economy")
    major_nations: MajorNations = Field(..., description="Major Nations")
    other_major_planes_of_existence: OtherMajorPlanesofExistence = Field(
        ..., description="Other Major Planes of Existence"
    )
    rules: Rules = Field(..., description="Rules")
