from pydantic import BaseModel, ConfigDict, Field


class GurpsCharacterCreationGuidePart1(BaseModel):
    """GURPS Character Creation Guide, Part 1

    Purpose: This form is used to guide and document the creation of a player character for a GURPS tabletop roleplaying game campaign, specifying attributes, traits, advantages, disadvantages, and other relevant details.
    Recipient: Game Masters (GMs) or campaign organizers who will review, approve, and track player character submissions for consistency with campaign rules and balance.
    """

    model_config = ConfigDict(extra="forbid")

    suggested_character_concepts: str = Field(..., description='Suggested character concepts. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    attributes_st_house_rules: str = Field(..., description='ST house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    attributes_dx_min: float | None = Field(..., description="DX minimum value")
    attributes_dx_max: float | None = Field(..., description="DX maximum value")
    attributes_dx_house_rules: str = Field(..., description='DX house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    attributes_iq_house_rules: str = Field(..., description='IQ house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    attributes_ht_house_rules: str = Field(..., description='HT house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')

    secondary_hp_house_rules: str = Field(..., description='HP house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    secondary_will_house_rules: str = Field(..., description='Will house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    secondary_per_house_rules: str = Field(..., description='Per house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    secondary_fp_house_rules: str = Field(..., description='FP house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    secondary_basic_speed_house_rules: str = Field(..., description='Basic Speed house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    secondary_basic_move_house_rules: str = Field(..., description='Basic Move house rules. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')

    social_status_levels_min_max: str = Field(..., description='Status levels (min/max). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    social_social_stigma: str = Field(..., description='Social stigma. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    social_social_regard: str = Field(..., description='Social regard. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    social_other: str = Field(..., description='Other social traits. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    social_rank1_notes: str = Field(..., description='Rank 1 notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    social_rank2_notes: str = Field(..., description='Rank 2 notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')


