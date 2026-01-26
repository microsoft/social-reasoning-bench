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
            "Primary genre of the campaign (e.g., fantasy, sci‑fi, horror) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    tech_level_tl: str = Field(
        ...,
        description=(
            "Overall technology level of the setting .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    tl_exceptions: str = Field(
        default="",
        description=(
            "Notable exceptions to the general tech level .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    power_level: str = Field(
        ...,
        description=(
            "Overall power level of characters and threats in the campaign .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    realism_level: Literal[
        "Grittily Realistic", "Realistic", "Cinematic", "Over-the-Top", "N/A", ""
    ] = Field(..., description="How realistic or cinematic the campaign tone is")

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
            "Key historical events relevant to the campaign world .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class EconomyandCurrency(BaseModel):
    """Monetary system and economic details of the setting"""

    currency_value_1: str = Field(
        default="",
        description=(
            "Name and relative value of a currency used in the setting .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    currency_value_2: str = Field(
        default="",
        description=(
            "Name and relative value of a second currency used in the setting .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    currency_value_3: str = Field(
        default="",
        description=(
            "Name and relative value of a third currency used in the setting .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    precious_metals: BooleanLike = Field(
        default="", description="Whether precious metals are used as currency or store of value"
    )

    paper_money: BooleanLike = Field(
        default="", description="Whether paper money is used in the setting"
    )

    e_money: BooleanLike = Field(
        default="", description="Whether electronic or digital money is used in the setting"
    )

    is_slavery_legal: BooleanLike = Field(
        default="", description="Indicate if slavery is legally permitted in the setting"
    )


class MajorNations(BaseModel):
    """Key nations and their political, social, and military details"""

    name_1: str = Field(
        default="",
        description=(
            'Name of the major nation .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    capital_1: str = Field(
        default="",
        description=(
            'Capital city of the nation .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    ruler_1: str = Field(
        default="",
        description=(
            "Primary ruler or governing body of the nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    population_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Approximate population of the nation"
    )

    search_bonus_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Search bonus modifier for this nation or region"
    )

    terrain_1: str = Field(
        default="",
        description=(
            'Dominant terrain types in the nation .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    appearance_1: str = Field(
        default="",
        description=(
            "General appearance or aesthetic of the nation or its people .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    hygiene_1: str = Field(
        default="",
        description=(
            'Typical hygiene level or modifier .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mana_1: str = Field(
        default="",
        description=(
            'Mana level in this nation or region .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    enchantment_1: str = Field(
        default="",
        description=(
            'Enchantment level or availability .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    cultural_familiarity_1: str = Field(
        default="",
        description=(
            "Relevant cultural familiarity traits for this nation .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    languages_1: str = Field(
        default="",
        description=(
            "Languages commonly spoken in this nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    literacy_1: str = Field(
        default="",
        description=(
            'General literacy level or rate .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    tl_1: str = Field(
        default="",
        description=(
            'Tech level specific to this nation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    wealth_1: str = Field(
        default="",
        description=(
            'Typical wealth level or modifier .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    status_range_1: str = Field(
        default="",
        description=(
            "Common social status range in this nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    society_government_1: str = Field(
        default="",
        description=(
            "Type of society and government structure .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    control_rating_cr_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Control Rating (CR) for this nation"
    )

    corruption_modifier_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Corruption modifier for this nation"
    )

    military_resources_1: str = Field(
        default="",
        description=(
            "Summary of the nation's military resources .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    defense_bonus_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Defense bonus value for this nation"
    )

    notes_1: str = Field(
        default="",
        description=(
            'Additional notes about this nation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_2: str = Field(
        default="",
        description=(
            'Name of the second major nation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    capital_2: str = Field(
        default="",
        description=(
            'Capital city of the second nation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    ruler_2: str = Field(
        default="",
        description=(
            "Primary ruler or governing body of the second nation .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    population_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Approximate population of the second nation"
    )

    search_bonus_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Search bonus modifier for the second nation or region"
    )

    terrain_2: str = Field(
        default="",
        description=(
            "Dominant terrain types in the second nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    appearance_2: str = Field(
        default="",
        description=(
            "General appearance or aesthetic of the second nation or its people .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    hygiene_2: str = Field(
        default="",
        description=(
            "Typical hygiene level or modifier in the second nation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    mana_2: str = Field(
        default="",
        description=(
            "Mana level in the second nation or region .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    enchantment_2: str = Field(
        default="",
        description=(
            "Enchantment level or availability in the second nation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cultural_familiarity_2: str = Field(
        default="",
        description=(
            "Relevant cultural familiarity traits for the second nation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    languages_2: str = Field(
        default="",
        description=(
            "Languages commonly spoken in the second nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    literacy_2: str = Field(
        default="",
        description=(
            "General literacy level or rate in the second nation .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tl_2: str = Field(
        default="",
        description=(
            "Tech level specific to the second nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    wealth_2: str = Field(
        default="",
        description=(
            "Typical wealth level or modifier in the second nation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    status_range_2: str = Field(
        default="",
        description=(
            "Common social status range in the second nation .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    society_government_2: str = Field(
        default="",
        description=(
            "Type of society and government structure in the second nation .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    control_rating_cr_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Control Rating (CR) for the second nation"
    )

    corruption_modifier_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Corruption modifier for the second nation"
    )

    military_resources_2: str = Field(
        default="",
        description=(
            "Summary of the second nation's military resources .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    defense_bonus_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Defense bonus value for the second nation"
    )

    notes_2: str = Field(
        default="",
        description=(
            "Additional notes about the second nation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class OtherMajorPlanesofExistence(BaseModel):
    """Information about additional planes or dimensions in the setting"""

    name_plane_1: str = Field(
        default="",
        description=(
            "Name of the other major plane of existence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    type_plane_1: str = Field(
        default="",
        description=(
            "Type or category of this plane (e.g., astral, elemental) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    description_plane_1: str = Field(
        default="",
        description=(
            "Brief description of this plane of existence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_plane_2: str = Field(
        default="",
        description=(
            "Name of another major plane of existence .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    type_plane_2: str = Field(
        default="",
        description=(
            'Type or category of the second plane .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    description_plane_2: str = Field(
        default="",
        description=(
            "Brief description of the second plane of existence .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class GURPSBooksUsed(BaseModel):
    """Sourcebooks and references used for this campaign"""

    title_1: str = Field(
        default="",
        description=(
            "Title of a GURPS book used in this campaign .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    notes_book_1: str = Field(
        default="",
        description=(
            'Notes on how this GURPS book is used .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    title_2: str = Field(
        default="",
        description=(
            'Title of a second GURPS book used .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    notes_book_2: str = Field(
        default="",
        description=(
            "Notes on how the second GURPS book is used .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    title_3: str = Field(
        default="",
        description=(
            'Title of a third GURPS book used .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    notes_book_3: str = Field(
        default="",
        description=(
            "Notes on how the third GURPS book is used .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class OptionalRules(BaseModel):
    """Specific optional rules and where they are found"""

    rule_1: str = Field(
        default="",
        description=(
            "Name or description of an optional rule used .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    book_1: str = Field(
        default="",
        description=(
            "Book where this optional rule is found .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    page_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Page number of the optional rule"
    )

    rule_2: str = Field(
        default="",
        description=(
            "Name or description of a second optional rule used .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    book_2: str = Field(
        default="",
        description=(
            "Book where the second optional rule is found .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    page_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Page number of the second optional rule"
    )

    rule_3: str = Field(
        default="",
        description=(
            "Name or description of a third optional rule used .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    book_3: str = Field(
        default="",
        description=(
            "Book where the third optional rule is found .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    page_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Page number of the third optional rule"
    )


class HouseRules(BaseModel):
    """Custom rules defined by the GM for this campaign"""

    house_rules: str = Field(
        default="",
        description=(
            "Custom house rules used in this campaign .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ExpandedCampaignPlanningForm(BaseModel):
    """EXPANDED CAMPAIGN PLANNING FORM"""

    campaign_overview: CampaignOverview = Field(..., description="Campaign Overview")
    economy_and_currency: EconomyandCurrency = Field(..., description="Economy and Currency")
    major_nations: MajorNations = Field(..., description="Major Nations")
    other_major_planes_of_existence: OtherMajorPlanesofExistence = Field(
        ..., description="Other Major Planes of Existence"
    )
    gurps_books_used: GURPSBooksUsed = Field(..., description="GURPS Books Used")
    optional_rules: OptionalRules = Field(..., description="Optional Rules")
    house_rules: HouseRules = Field(..., description="House Rules")
