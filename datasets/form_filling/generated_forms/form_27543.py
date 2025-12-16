from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class GeneralHealthBackground(BaseModel):
    """Background, sleep, pain, digestion, and allergies"""

    what_is_your_ancestry: str = Field(
        default="",
        description=(
            "Describe your ancestry or ethnic background. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    what_blood_type_are_you: str = Field(
        default="",
        description=(
            "Indicate your blood type (e.g., A+, O-, B+). .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    how_is_your_sleep: str = Field(
        default="",
        description=(
            "Briefly describe the quality of your sleep. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    how_many_hours: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Average number of hours you sleep per night."
    )

    do_you_wake_up_at_night: BooleanLike = Field(
        default="", description="Indicate whether you typically wake up during the night."
    )

    why: str = Field(
        default="",
        description=(
            "If you wake up at night, explain why or what you notice. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    any_pain_stiffness_or_swelling: str = Field(
        default="",
        description=(
            "Describe any pain, stiffness, or swelling you experience. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    constipation_diarrhea_gas: str = Field(
        default="",
        description=(
            "Note any issues with constipation, diarrhea, or gas. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    allergies_or_sensitivities_please_explain: str = Field(
        default="",
        description=(
            "List any allergies or sensitivities and provide details. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class MedicalInformation(BaseModel):
    """Medications, supplements, therapies, and exercise"""

    do_you_take_any_supplements_or_medications_please_list: str = Field(
        default="",
        description=(
            "List all supplements and medications you currently take. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    any_healers_helpers_or_therapies_with_which_you_are_involved_please_list: str = Field(
        default="",
        description=(
            "List any healers, helpers, or therapies you are currently involved with. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    what_role_do_sports_and_exercise_play_in_your_life: str = Field(
        default="",
        description=(
            "Describe how often and in what ways you engage in sports or exercise. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class FoodInformation(BaseModel):
    """Eating patterns in childhood and currently"""

    what_foods_did_you_eat_often_as_a_child_breakfast: str = Field(
        default="",
        description=(
            "Foods you commonly ate for breakfast as a child. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    what_foods_did_you_eat_often_as_a_child_lunch: str = Field(
        default="",
        description=(
            "Foods you commonly ate for lunch as a child. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    what_foods_did_you_eat_often_as_a_child_dinner: str = Field(
        default="",
        description=(
            "Foods you commonly ate for dinner as a child. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    what_foods_did_you_eat_often_as_a_child_snacks: str = Field(
        default="",
        description=(
            'Snacks you commonly ate as a child. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    what_foods_did_you_eat_often_as_a_child_liquids: str = Field(
        default="",
        description=(
            "Drinks and other liquids you commonly consumed as a child. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    what_is_your_food_like_these_days_breakfast: str = Field(
        default="",
        description=(
            "What you typically eat for breakfast these days. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    what_is_your_food_like_these_days_lunch: str = Field(
        default="",
        description=(
            "What you typically eat for lunch these days. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    what_is_your_food_like_these_days_dinner: str = Field(
        default="",
        description=(
            "What you typically eat for dinner these days. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    what_is_your_food_like_these_days_snacks: str = Field(
        default="",
        description=(
            'Snacks you typically eat these days. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    what_is_your_food_like_these_days_liquids: str = Field(
        default="",
        description=(
            "Drinks and other liquids you typically consume these days. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IcraveCoaching(BaseModel):
    """iCrave COACHING"""

    general_health__background: GeneralHealthBackground = Field(
        ..., description="General Health & Background"
    )
    medical_information: MedicalInformation = Field(..., description="Medical Information")
    food_information: FoodInformation = Field(..., description="Food Information")
