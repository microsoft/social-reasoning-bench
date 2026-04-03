from pydantic import BaseModel, ConfigDict, Field


class GurpsCharacterCreationGuidePart1(BaseModel):
    """GURPS Character Creation Guide, Part 1"""

    model_config = ConfigDict(extra="forbid")

    starting_points: str = Field(
        ..., description='Starting points. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    suggested_character_concepts: str = Field(
        ..., description='Suggested character concepts. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )

    attributes_st_min: str = Field(
        ..., description='Attributes ST min. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    attributes_st_house_rules: str = Field(
        ..., description='Attributes ST house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    attributes_dx_house_rules: str = Field(
        ..., description='Attributes DX house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    attributes_iq_min: str = Field(
        ..., description='Attributes IQ min. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    attributes_iq_house_rules: str = Field(
        ..., description='Attributes IQ house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    attributes_ht_min: str = Field(
        ..., description='Attributes HT min. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    attributes_ht_house_rules: str = Field(
        ..., description='Attributes HT house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )

    secondary_hp_house_rules: str = Field(
        ..., description='Secondary HP house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    secondary_will_house_rules: str = Field(
        ..., description='Secondary Will house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    secondary_per_house_rules: str = Field(
        ..., description='Secondary Per house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    secondary_fp_house_rules: str = Field(
        ..., description='Secondary FP house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    secondary_basic_speed_house_rules: str = Field(
        ..., description='Secondary Basic Speed house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    secondary_basic_move_house_rules: str = Field(
        ..., description='Secondary Basic Move house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )

    social_social_regard: str = Field(
        ..., description='Social Regard. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    social_other: str = Field(
        ..., description='Other social traits. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    social_rank1_notes: str = Field(
        ..., description='Rank 1 notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    social_rank2_notes: str = Field(
        ..., description='Rank 2 notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )


