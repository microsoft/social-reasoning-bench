from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CoreAttributesIdentity(BaseModel):
    """Primary stats and basic character identity"""

    str: Union[float, Literal["N/A", ""]] = Field(..., description="Strength ability score")

    dex: Union[float, Literal["N/A", ""]] = Field(..., description="Dexterity ability score")

    con: Union[float, Literal["N/A", ""]] = Field(..., description="Constitution ability score")

    int: Union[float, Literal["N/A", ""]] = Field(..., description="Intelligence ability score")

    wis: Union[float, Literal["N/A", ""]] = Field(..., description="Wisdom ability score")

    cha: Union[float, Literal["N/A", ""]] = Field(..., description="Charisma ability score")

    name: str = Field(
        ...,
        description=(
            'Character name .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    hp_current_maximum: str = Field(
        ...,
        description=(
            "Current and maximum hit points, e.g. 7/12 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    level: Union[float, Literal["N/A", ""]] = Field(..., description="Current character level")

    class_: str = Field(
        ...,
        description=(
            'Character class .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    background: str = Field(
        default="",
        description=(
            "Brief description of character background .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    homeworld: str = Field(
        default="",
        description=(
            'Character\'s planet or place of origin .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    employer: str = Field(
        default="",
        description=(
            'Current employer or patron .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    species: str = Field(
        ...,
        description=(
            'Character species .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    weapon: str = Field(
        default="",
        description=(
            'Primary weapon or armament .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    initiative: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Initiative modifier (DEX + level and other bonuses)"
    )

    base_attack_bonus: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Base attack bonus value"
    )


class SkillsPsychicAbilities(BaseModel):
    """Skill levels and psychic disciplines"""

    work: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Work skill rating (0–3)"
    )

    biopsionics: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Biopsionics psychic skill rating (0–3)"
    )

    telekinesis: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Telekinesis psychic skill rating (0–3)"
    )

    telepathy: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Telepathy psychic skill rating (0–3)"
    )

    teletransport: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Teletransport psychic skill rating (0–3)"
    )

    perception: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Perception skill rating (0–3)"
    )

    reputation: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Reputation or social standing rating (0–3)"
    )

    pilot: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Pilot skill rating (0–3)"
    )

    program: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Program (computers) skill rating (0–3)"
    )

    connect: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Connect (contacts and networking) skill rating (0–3)"
    )

    exert: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Exert (physical effort) skill rating (0–3)"
    )

    fix: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Fix (repair and engineering) skill rating (0–3)"
    )

    heal: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Heal (medical) skill rating (0–3)"
    )

    know: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Know (general knowledge) skill rating (0–3)"
    )

    lead: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Lead (leadership) skill rating (0–3)"
    )

    notice: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Notice (awareness) skill rating (0–3)"
    )

    perform: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Perform (artistic performance) skill rating (0–3)"
    )

    shoot: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Shoot (ranged combat) skill rating (0–3)"
    )

    sneak: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Sneak (stealth) skill rating (0–3)"
    )

    stab: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Stab (melee combat) skill rating (0–3)"
    )

    survive: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Survive (wilderness survival) skill rating (0–3)"
    )

    talk: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Talk (social interaction) skill rating (0–3)"
    )

    trade: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Trade (commerce and bargaining) skill rating (0–3)"
    )

    proficient_technique: str = Field(
        default="",
        description=(
            "Name or description of the proficient technique .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class GoalsExperience(BaseModel):
    """Character goals, XP, and advancement notes"""

    goals_experience_one_sentence_description_of_current_character_professional_personal_narrative_ambitions: str = Field(
        default="",
        description=(
            "One-sentence description of the character's current goals or narrative "
            'ambitions .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    xp: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current experience points"
    )


class HealthStatusAffiliations(BaseModel):
    """Long-term conditions, strain, status tracks, and affiliations"""

    permanent: str = Field(
        default="",
        description=(
            "Permanent conditions or effects affecting the character .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    system_strain: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current system strain value"
    )

    status_physical: str = Field(
        default="",
        description=(
            'Physical status or condition notes .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    status_mental: str = Field(
        default="",
        description=(
            'Mental status or condition notes .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    status_fatigue: str = Field(
        default="",
        description=(
            'Fatigue status or condition notes .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    status_emotion: str = Field(
        default="",
        description=(
            'Emotional status or condition notes .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    status_morale: str = Field(
        default="",
        description=(
            'Morale status or condition notes .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    professional_faction_affiliations: str = Field(
        default="",
        description=(
            "List of professional, organizational, or faction affiliations .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    notes_cons_pros: str = Field(
        default="",
        description=(
            "Notes on pros and cons related to affiliations or character .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    use_call_a_level: str = Field(
        default="",
        description=(
            "Usage notes for calling a level or related mechanic .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    notable_details_and_page_level: str = Field(
        default="",
        description=(
            "Notable details with references to rulebook page and level .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class GearEquipment(BaseModel):
    """Carried gear, armor, weapons, ammo, and credits"""

    gear: str = Field(
        default="",
        description=(
            "General gear list (total encumbrance per highest stat, high-tech may restrict "
            'low CON) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    food: str = Field(
        default="",
        description=(
            'Food supplies and related items .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    tools_aid_misc: str = Field(
        default="",
        description=(
            "Tools, aid items, and miscellaneous equipment .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    range_ammo: str = Field(
        default="",
        description=(
            'Ranged weapons and ammunition summary .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    range_ammo_name_info: str = Field(
        default="",
        description=(
            "Names and details for ranged weapons and ammunition .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    armor: str = Field(
        default="",
        description=(
            'Armor summary .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    armor_name_info: str = Field(
        default="",
        description=(
            'Names and details for armor pieces .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    credits: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total available credits"
    )

    credits_detailed_items: str = Field(
        default="",
        description=(
            "Detailed list of items purchased or owned with credits .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class NotesMeta(BaseModel):
    """General notes, portrait, and record-keeping info"""

    notes: str = Field(
        default="",
        description=(
            "Long-form notes, thoughts, achievements, and other details .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    portrait_icon: str = Field(
        default="",
        description=(
            "Reference or description for the character's portrait or icon .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date: str = Field(
        default="", description="Date this character sheet was completed or updated"
    )  # YYYY-MM-DD format


class CharacterSheet(BaseModel):
    """
    Character Sheet

    ''
    """

    core_attributes__identity: CoreAttributesIdentity = Field(
        ..., description="Core Attributes & Identity"
    )
    skills__psychic_abilities: SkillsPsychicAbilities = Field(
        ..., description="Skills & Psychic Abilities"
    )
    goals__experience: GoalsExperience = Field(..., description="Goals & Experience")
    health_status__affiliations: HealthStatusAffiliations = Field(
        ..., description="Health, Status & Affiliations"
    )
    gear__equipment: GearEquipment = Field(..., description="Gear & Equipment")
    notes__meta: NotesMeta = Field(..., description="Notes & Meta")
