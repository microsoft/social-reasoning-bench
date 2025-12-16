from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FoodAllergy(BaseModel):
    """Specific food allergens and other dietary restrictions"""

    dairy: BooleanLike = Field(
        default="",
        description="Check if the participant has a dairy allergy or dietary restriction.",
    )

    soy: BooleanLike = Field(
        default="", description="Check if the participant has a soy allergy or dietary restriction."
    )

    eggs: BooleanLike = Field(
        default="",
        description="Check if the participant has an egg allergy or dietary restriction.",
    )

    peanuts: BooleanLike = Field(
        default="",
        description="Check if the participant has a peanut allergy or dietary restriction.",
    )

    tree_nuts: BooleanLike = Field(
        default="",
        description="Check if the participant has a tree nut allergy or dietary restriction.",
    )

    shellfish: BooleanLike = Field(
        default="",
        description="Check if the participant has a shellfish allergy or dietary restriction.",
    )

    sesame: BooleanLike = Field(
        default="",
        description="Check if the participant has a sesame allergy or dietary restriction.",
    )

    fish: BooleanLike = Field(
        default="",
        description="Check if the participant has a fish allergy or dietary restriction.",
    )

    wheat: BooleanLike = Field(
        default="",
        description=(
            "Check if the participant has a wheat or gluten-related allergy or dietary restriction."
        ),
    )

    other_please_list: str = Field(
        default="",
        description=(
            "List any other food allergies or dietary restrictions not covered above. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_special_diet_needs_or_restrictions: str = Field(
        default="",
        description=(
            "Describe any additional special diet needs or restrictions. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class DietaryNeedsQuestionnaire(BaseModel):
    """Details about substitutions, reactions, and participant understanding"""

    what_are_the_preferred_food_substitutions_if_any: str = Field(
        default="",
        description=(
            "Describe preferred food substitutions (e.g., soy butter for peanut butter, "
            'gluten-free breads, soy milk). .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    airborne: BooleanLike = Field(
        default="", description="Check if airborne exposure to the allergen can cause a reaction."
    )

    trace_cross_contact: BooleanLike = Field(
        default="",
        description="Check if trace cross-contact with the allergen can cause a reaction.",
    )

    actual_ingestion_of_food: BooleanLike = Field(
        default="",
        description="Check if actual ingestion of the allergen is required to cause a reaction.",
    )

    please_explain: str = Field(
        default="",
        description=(
            "Explain the types of contact that cause a reaction and any relevant details. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    does_the_participant_understand_the_food_allergy_and_what_needs_to_be_done_to_manage_it: str = (
        Field(
            default="",
            description=(
                "Describe the participant’s understanding of their food allergy and how to "
                'manage it. .If you cannot fill this, write "N/A". If this field should not '
                "be filled by you (for example, it belongs to another person or office), leave "
                'it blank (empty string "").'
            ),
        )
    )

    has_the_participant_ever_attended_camp_or_eaten_meals_outside_the_home: str = Field(
        default="",
        description=(
            "Indicate whether the participant has attended camp or eaten meals outside the "
            'home. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    if_yes_how_were_the_meals_handled: str = Field(
        default="",
        description=(
            "If the participant has eaten meals outside the home, describe how those meals "
            'were handled. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class FoodAllergydietaryNeeds(BaseModel):
    """
    Food Allergy/Dietary Needs

    Please attach medical documentation describing the dietary restrictions due to the food allergy and/or intolerance, from the Participant’s Physician.
    """

    food_allergy: FoodAllergy = Field(..., description="Food Allergy")
    dietary_needs_questionnaire: DietaryNeedsQuestionnaire = Field(
        ..., description="Dietary Needs Questionnaire"
    )
