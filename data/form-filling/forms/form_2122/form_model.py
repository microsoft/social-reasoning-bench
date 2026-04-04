from pydantic import BaseModel, ConfigDict, Field


class GurpsCampaignProspectus(BaseModel):
    """EXPANDED CAMPAIGN PLANNING FORM — GURPS Campaign Prospectus

    The Game Master fills out this worksheet to define a GURPS campaign’s core
    premise, tone, rules assumptions, and key world details (like nations,
    currency, and planes of existence). The GM and player group use it to align
    expectations, decide what books and optional rules are in play, and provide
    a shared reference for character creation and ongoing play.
    """

    model_config = ConfigDict(extra="forbid")

    creation_date: str = Field(
        ...,
        description='Creation date (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    genre: str = Field(
        ...,
        description='Genre. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    power_level: str = Field(
        ...,
        description='Power level. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    campaign_synopsis_and_recent_events: str = Field(
        ...,
        description='Synopsis and recent events. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    timeline_of_significant_historical_events: str = Field(
        ...,
        description='Timeline of significant events. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    currency_value_1: str = Field(
        ...,
        description='Currency/$ value entry 1. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    currency_value_2: str = Field(
        ...,
        description='Currency/$ value entry 2. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    currency_value_3: str = Field(
        ...,
        description='Currency/$ value entry 3. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    major_nation_1_capital: str = Field(
        ...,
        description='Nation 1 capital. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    major_nation_1_appearance: str = Field(
        ...,
        description='Nation 1 appearance. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    major_nation_1_enchantment: str = Field(
        ...,
        description='Nation 1 enchantment. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    major_nation_1_cultural_familiarity: str = Field(
        ...,
        description='Nation 1 cultural familiarity. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    major_nation_1_society_government: str = Field(
        ...,
        description='Nation 1 society/government. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    major_nation_1_military_resources: str = Field(
        ...,
        description='Nation 1 military resources. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    major_nation_2_appearance: str = Field(
        ...,
        description='Nation 2 appearance. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    major_nation_2_enchantment: str = Field(
        ...,
        description='Nation 2 enchantment. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    major_nation_2_cultural_familiarity: str = Field(
        ...,
        description='Nation 2 cultural familiarity. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    major_nation_2_status_range: str = Field(
        ...,
        description='Nation 2 status (range). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    major_nation_2_society_government: str = Field(
        ...,
        description='Nation 2 society/government. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    major_nation_2_military_resources: str = Field(
        ...,
        description='Nation 2 military resources. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    other_plane_1_type: str = Field(
        ...,
        description='Plane 1 type. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    other_plane_1_description: str = Field(
        ...,
        description='Plane 1 description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    other_plane_2_type: str = Field(
        ...,
        description='Plane 2 type. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    other_plane_2_description: str = Field(
        ...,
        description='Plane 2 description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    gurps_books_used_1_notes: str = Field(
        ...,
        description='GURPS book used 1 notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    gurps_books_used_2_notes: str = Field(
        ...,
        description='GURPS book used 2 notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    gurps_books_used_3_notes: str = Field(
        ...,
        description='GURPS book used 3 notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    optional_rule_1_rule: str = Field(
        ...,
        description='Optional rule 1. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    optional_rule_1_book: str = Field(
        ...,
        description='Optional rule 1 book. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    house_rules: str = Field(
        ...,
        description='House rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )