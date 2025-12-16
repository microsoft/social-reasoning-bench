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
            'Name of the campaign .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    gm: str = Field(
        ...,
        description=(
            'Name of the Game Master .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
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
            "Notable exceptions to the stated tech level .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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

    realism_level_grittily_realistic_realistic_cinematic_over_the_top: Literal[
        "Grittily Realistic", "Realistic", "Cinematic", "Over-the-Top", "N/A", ""
    ] = Field(..., description="Chosen realism level for the campaign tone")

    campaign_synopsis_and_recent_events: str = Field(
        ...,
        description=(
            "Brief overview of the campaign and any recent events .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    timeline_of_significant_historical_events: str = Field(
        default="",
        description=(
            "Key historical events relevant to the campaign, in chronological order .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class EconomyandCurrency(BaseModel):
    """Monetary system and related societal details"""

    currency_value_1: str = Field(
        default="",
        description=(
            "Description or name of a currency and its value .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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
        default="", description="Indicate if precious metals are used as currency"
    )

    paper_money: BooleanLike = Field(
        default="", description="Indicate if paper money is used as currency"
    )

    e_money: BooleanLike = Field(
        default="", description="Indicate if electronic money is used as currency"
    )

    is_slavery_legal: BooleanLike = Field(
        default="", description="Indicate whether slavery is legal in the setting"
    )


class MajorNations(BaseModel):
    """Key nations and their characteristics (see also City Stats)"""

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
            'Capital city of the nation .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_ruler: str = Field(
        default="",
        description=(
            "Primary ruler or governing body of the nation .If you cannot fill this, write "
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
            "Search bonus value for this nation (per City Stats rules) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_terrain: str = Field(
        default="",
        description=(
            'Dominant terrain types in the nation .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_appearance: str = Field(
        default="",
        description=(
            "General appearance modifier or description .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
            "Mana level in the nation (e.g., low, normal, high) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_enchantment: str = Field(
        default="",
        description=(
            "Enchantment level or availability in the nation .If you cannot fill this, "
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
            "General literacy level or notes on literacy .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
            'Typical wealth level in the nation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_status_range: str = Field(
        default="",
        description=(
            "Typical range of Status levels in the nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_society_government: str = Field(
        default="",
        description=(
            "Type of society and government structure .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_control_rating_cr: str = Field(
        default="",
        description=(
            'Control Rating value for the nation .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_corruption_modifier: str = Field(
        default="",
        description=(
            'Corruption modifier for the nation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_military_resources: str = Field(
        default="",
        description=(
            "Summary of the nation's military resources .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_defense_bonus: str = Field(
        default="",
        description=(
            'Defense bonus value for the nation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_1_notes: str = Field(
        default="",
        description=(
            'Additional notes about the nation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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
            'Capital city of the second nation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_ruler: str = Field(
        default="",
        description=(
            "Primary ruler or governing body of the second nation .If you cannot fill this, "
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
            "Search bonus value for the second nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_terrain: str = Field(
        default="",
        description=(
            "Dominant terrain types in the second nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_appearance: str = Field(
        default="",
        description=(
            "General appearance modifier or description for the second nation .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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
            'Mana level in the second nation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_enchantment: str = Field(
        default="",
        description=(
            "Enchantment level or availability in the second nation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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
            "General literacy level or notes on literacy in the second nation .If you "
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
            "Typical wealth level in the second nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_status_range: str = Field(
        default="",
        description=(
            "Typical range of Status levels in the second nation .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_society_government: str = Field(
        default="",
        description=(
            "Type of society and government structure in the second nation .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    major_nation_2_control_rating_cr: str = Field(
        default="",
        description=(
            "Control Rating value for the second nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_corruption_modifier: str = Field(
        default="",
        description=(
            "Corruption modifier for the second nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_military_resources: str = Field(
        default="",
        description=(
            "Summary of the second nation's military resources .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_defense_bonus: str = Field(
        default="",
        description=(
            "Defense bonus value for the second nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    major_nation_2_notes: str = Field(
        default="",
        description=(
            "Additional notes about the second nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class OtherMajorPlanesofExistence(BaseModel):
    """Additional planes and their basic properties"""

    plane_1_name: str = Field(
        default="",
        description=(
            'Name of the other plane of existence .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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
            "Brief description of this plane of existence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    plane_2_name: str = Field(
        default="",
        description=(
            'Name of a second plane of existence .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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


class GURPSBooksUsed(BaseModel):
    """Sourcebooks referenced for this campaign"""

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


class OptionalRules(BaseModel):
    """Optional rules in use and their sources"""

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
            'Page number of the optional rule .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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
            "Page number of the second optional rule .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
            "Page number of the third optional rule .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class HouseRules(BaseModel):
    """Custom rules defined by the GM"""

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
    economy_and_currency: EconomyandCurrency = Field(..., description="Economy and Currency")
    major_nations: MajorNations = Field(..., description="Major Nations")
    other_major_planes_of_existence: OtherMajorPlanesofExistence = Field(
        ..., description="Other Major Planes of Existence"
    )
    gurps_books_used: GURPSBooksUsed = Field(..., description="GURPS Books Used")
    optional_rules: OptionalRules = Field(..., description="Optional Rules")
    house_rules: HouseRules = Field(..., description="House Rules")
