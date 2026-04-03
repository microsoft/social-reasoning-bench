from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CampaignOverview(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Basic information about the campaign and its setting."""

    campaign_name: str = Field(
        ...,
        description=(
            "Name of the campaign .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    gm: str = Field(
        ...,
        description=(
            "Game Master's name .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    creation_date: str = Field(
        ...,
        description="Date the campaign was created"
    )  # YYYY-MM-DD format

    genre: str = Field(
        ...,
        description=(
            "Genre of the campaign (e.g., Fantasy, Sci-Fi) .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    tech_level_tl: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Overall technology level for the campaign"
    )

    tl_exceptions: str = Field(
        ...,
        description=(
            "Any exceptions to the general tech level .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    power_level: str = Field(
        ...,
        description=(
            "General power level of characters or setting .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    realism_level: Literal["Grittily Realistic", "Realistic", "Cinematic", "Over-the-Top", "N/A", ""] = Field(
        ...,
        description="Level of realism in the campaign"
    )

    campaign_synopsis_and_recent_events: str = Field(
        ...,
        description=(
            "Summary of the campaign and recent events .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    timeline_of_significant_historical_events: str = Field(
        ...,
        description=(
            "Timeline of important events in the campaign world .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )


class Economy(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details about currency and economic features of the campaign."""

    currency_value_1: str = Field(
        ...,
        description=(
            "First type of currency and its value .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    currency_value_2: str = Field(
        ...,
        description=(
            "Second type of currency and its value .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    currency_value_3: str = Field(
        ...,
        description=(
            "Third type of currency and its value .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    precious_metals: BooleanLike = Field(
        ...,
        description="Are precious metals used as currency?"
    )

    paper_money: BooleanLike = Field(
        ...,
        description="Is paper money used?"
    )

    e_money: BooleanLike = Field(
        ...,
        description="Is electronic money used?"
    )

    is_slavery_legal: BooleanLike = Field(
        ...,
        description="Is slavery legal in the campaign?"
    )


class MajorNations(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the major nations in the campaign world."""

    major_nation_name_1: str = Field(
        ...,
        description=(
            "Name of the first major nation .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_capital_1: str = Field(
        ...,
        description=(
            "Capital city of the first major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_ruler_1: str = Field(
        ...,
        description=(
            "Ruler of the first major nation .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_population_1: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Population of the first major nation"
    )

    major_nation_search_bonus_1: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Search bonus for the first major nation"
    )

    major_nation_terrain_1: str = Field(
        ...,
        description=(
            "Terrain of the first major nation .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_appearance_1: str = Field(
        ...,
        description=(
            "Appearance of the first major nation .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_hygiene_1: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Hygiene rating of the first major nation"
    )

    major_nation_mana_1: str = Field(
        ...,
        description=(
            "Mana level of the first major nation .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_enchantment_1: str = Field(
        ...,
        description=(
            "Enchantment level of the first major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_cultural_familiarity_1: str = Field(
        ...,
        description=(
            "Cultural familiarity of the first major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_language_s_1: str = Field(
        ...,
        description=(
            "Languages spoken in the first major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_literacy_1: str = Field(
        ...,
        description=(
            "Literacy level in the first major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_tl_1: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Tech level of the first major nation"
    )

    major_nation_wealth_1: str = Field(
        ...,
        description=(
            "Wealth level of the first major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_status_range_1: str = Field(
        ...,
        description=(
            "Status range in the first major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_society_government_1: str = Field(
        ...,
        description=(
            "Society or government type of the first major nation .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_control_rating_cr_1: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Control rating of the first major nation"
    )

    major_nation_corruption_modifier_1: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Corruption modifier for the first major nation"
    )

    major_nation_military_resources_1: str = Field(
        ...,
        description=(
            "Military resources of the first major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_defense_bonus_1: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Defense bonus for the first major nation"
    )

    major_nation_notes_1: str = Field(
        ...,
        description=(
            "Additional notes for the first major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_name_2: str = Field(
        ...,
        description=(
            "Name of the second major nation .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_capital_2: str = Field(
        ...,
        description=(
            "Capital city of the second major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_ruler_2: str = Field(
        ...,
        description=(
            "Ruler of the second major nation .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_population_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Population of the second major nation"
    )

    major_nation_search_bonus_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Search bonus for the second major nation"
    )

    major_nation_terrain_2: str = Field(
        ...,
        description=(
            "Terrain of the second major nation .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_appearance_2: str = Field(
        ...,
        description=(
            "Appearance of the second major nation .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_hygiene_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Hygiene rating of the second major nation"
    )

    major_nation_mana_2: str = Field(
        ...,
        description=(
            "Mana level of the second major nation .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_enchantment_2: str = Field(
        ...,
        description=(
            "Enchantment level of the second major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_cultural_familiarity_2: str = Field(
        ...,
        description=(
            "Cultural familiarity of the second major nation .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_language_s_2: str = Field(
        ...,
        description=(
            "Languages spoken in the second major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_literacy_2: str = Field(
        ...,
        description=(
            "Literacy level in the second major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_tl_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Tech level of the second major nation"
    )

    major_nation_wealth_2: str = Field(
        ...,
        description=(
            "Wealth level of the second major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_status_range_2: str = Field(
        ...,
        description=(
            "Status range in the second major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_society_government_2: str = Field(
        ...,
        description=(
            "Society or government type of the second major nation .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_control_rating_cr_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Control rating of the second major nation"
    )

    major_nation_corruption_modifier_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Corruption modifier for the second major nation"
    )

    major_nation_military_resources_2: str = Field(
        ...,
        description=(
            "Military resources of the second major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    major_nation_defense_bonus_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Defense bonus for the second major nation"
    )

    major_nation_notes_2: str = Field(
        ...,
        description=(
            "Additional notes for the second major nation .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )


class OtherMajorPlanesofExistence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details about other planes or dimensions in the campaign."""

    other_plane_name_1: str = Field(
        ...,
        description=(
            "Name of the first other plane of existence .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    other_plane_type_1: str = Field(
        ...,
        description=(
            "Type of the first other plane of existence .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    other_plane_description_1: str = Field(
        ...,
        description=(
            "Description of the first other plane of existence .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    other_plane_name_2: str = Field(
        ...,
        description=(
            "Name of the second other plane of existence .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    other_plane_type_2: str = Field(
        ...,
        description=(
            "Type of the second other plane of existence .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    other_plane_description_2: str = Field(
        ...,
        description=(
            "Description of the second other plane of existence .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )


class Rules(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Rules, books used, optional and house rules for the campaign."""

    gurps_book_title_1: str = Field(
        ...,
        description=(
            "Title of the first GURPS book used .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    gurps_book_notes_1: str = Field(
        ...,
        description=(
            "Notes for the first GURPS book used .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    gurps_book_title_2: str = Field(
        ...,
        description=(
            "Title of the second GURPS book used .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    gurps_book_notes_2: str = Field(
        ...,
        description=(
            "Notes for the second GURPS book used .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    gurps_book_title_3: str = Field(
        ...,
        description=(
            "Title of the third GURPS book used .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    gurps_book_notes_3: str = Field(
        ...,
        description=(
            "Notes for the third GURPS book used .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    optional_rule_1: str = Field(
        ...,
        description=(
            "First optional rule used .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    optional_rule_book_1: str = Field(
        ...,
        description=(
            "Book for the first optional rule .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    optional_rule_page_1: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Page number for the first optional rule"
    )

    optional_rule_2: str = Field(
        ...,
        description=(
            "Second optional rule used .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    optional_rule_book_2: str = Field(
        ...,
        description=(
            "Book for the second optional rule .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    optional_rule_page_2: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Page number for the second optional rule"
    )

    optional_rule_3: str = Field(
        ...,
        description=(
            "Third optional rule used .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    optional_rule_book_3: str = Field(
        ...,
        description=(
            "Book for the third optional rule .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    optional_rule_page_3: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Page number for the third optional rule"
    )

    house_rules: str = Field(
        ...,
        description=(
            "Any house rules for the campaign .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class ExpandedCampaignPlanningFormGurpsCampaignProspectus(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    EXPANDED CAMPAIGN PLANNING FORM

GURPS Campaign Prospectus

    ''
    """

    campaign_overview: CampaignOverview = Field(
        ...,
        description="Campaign Overview"
    )
    economy: Economy = Field(
        ...,
        description="Economy"
    )
    major_nations: MajorNations = Field(
        ...,
        description="Major Nations"
    )
    other_major_planes_of_existence: OtherMajorPlanesofExistence = Field(
        ...,
        description="Other Major Planes of Existence"
    )
    rules: Rules = Field(
        ...,
        description="Rules"
    )