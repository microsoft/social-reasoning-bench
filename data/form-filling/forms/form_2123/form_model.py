from pydantic import BaseModel, ConfigDict, Field


class GurpsCharacterCreationGuidePart1(BaseModel):
    """GURPS Character Creation Guide, Part 1

    The Game Master (or campaign organizer) uses this guide to set the character
    creation rules for a GURPS campaign—starting point totals, attribute and
    secondary characteristic ranges, allowed/prohibited traits, and social
    parameters. Players may reference it while building characters, and the GM
    reviews it to decide what character options are permitted and whether PCs
    comply with campaign limits.
    """

    model_config = ConfigDict(extra="forbid")

    starting_points: str = Field(
        ...,
        description='Starting points. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    suggested_character_concepts: str = Field(
        ...,
        description='Suggested character concepts. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    attributes_st_min: str = Field(
        ...,
        description='ST minimum. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    attributes_st_max: str = Field(
        ...,
        description='ST maximum. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    attributes_st_house_rules: str = Field(
        ...,
        description='ST house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    attributes_dx_house_rules: str = Field(
        ...,
        description='DX house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    attributes_iq_house_rules: str = Field(
        ...,
        description='IQ house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    attributes_ht_house_rules: str = Field(
        ...,
        description='HT house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    secondary_hp_max: str = Field(
        ...,
        description='HP maximum. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    secondary_hp_house_rules: str = Field(
        ...,
        description='HP house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    secondary_will_min: str = Field(
        ...,
        description='Will minimum. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    secondary_will_house_rules: str = Field(
        ...,
        description='Will house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    secondary_per_house_rules: str = Field(
        ...,
        description='Per house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    secondary_fp_house_rules: str = Field(
        ...,
        description='FP house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    secondary_basic_speed_house_rules: str = Field(
        ...,
        description='Basic Speed house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    secondary_basic_move_house_rules: str = Field(
        ...,
        description='Basic Move house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    social_traits_other: str = Field(
        ...,
        description='Other social traits. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    social_traits_rank_1_notes: str = Field(
        ...,
        description='Rank 1 notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    social_traits_rank_2_notes: str = Field(
        ...,
        description='Rank 2 notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    advantages_required_advantages: str = Field(
        ...,
        description='Required advantages. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    disadvantages_required_disadvantages: str = Field(
        ...,
        description='Required disadvantages. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
