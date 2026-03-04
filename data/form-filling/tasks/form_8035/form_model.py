from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PolicyItemStatus(BaseModel):
    """Indicate whether the wellness policy items are included in the written policy and implemented in school buildings"""

    included_in_the_written_policy_yes: BooleanLike = Field(
        default="",
        description="Indicate if this item is included in the written wellness policy (Yes).",
    )

    included_in_the_written_policy_no: BooleanLike = Field(
        default="",
        description="Indicate if this item is not included in the written wellness policy (No).",
    )

    implemented_in_the_school_buildings_fully_in_place: BooleanLike = Field(
        default="",
        description="Indicate if this item is fully implemented in the school building(s).",
    )

    implemented_in_the_school_buildings_partially_in_place: BooleanLike = Field(
        default="",
        description="Indicate if this item is partially implemented in the school building(s).",
    )

    implemented_in_the_school_buildings_not_in_place: BooleanLike = Field(
        default="",
        description="Indicate if this item is not implemented in the school building(s).",
    )


class NutritionGuidelinesforFoodsandBeveragesatSchool(BaseModel):
    """Specific wellness policy goals and practices related to foods and beverages at school"""

    we_limit_the_number_of_food_fundraisers_at_school_and_have_procedures_in_place_for_requesting_a_fundraiser_exemption: BooleanLike = Field(
        default="",
        description=(
            "Check if the school limits food fundraisers and has procedures for requesting "
            "exemptions for items that do not meet Smart Snacks standards."
        ),
    )

    we_have_local_standards_in_our_written_policy_for_foods_and_beverages_offered_for_free_to_students_at_school: BooleanLike = Field(
        default="",
        description=(
            "Check if the written policy includes local standards for foods and beverages "
            "offered for free (rewards, parties, celebrations, shared snacks)."
        ),
    )

    we_provide_a_list_of_nonfood_ideas_and_healthy_food_beverage_alternatives_to_staff_and_parents_guardians: BooleanLike = Field(
        default="",
        description=(
            "Check if the school provides staff and parents/guardians with a list of "
            "nonfood ideas and healthy food/beverage alternatives."
        ),
    )

    only_foods_and_beverages_that_meet_or_exceed_federal_nutrition_standards_are_permitted_to_be_marketed_or_promoted_to_students_during_the_school_day: BooleanLike = Field(
        default="",
        description=(
            "Check if only foods and beverages meeting or exceeding USDA Smart Snacks "
            "standards are marketed or promoted to students during the school day."
        ),
    )

    notes_on_nutrition_guidelines_for_foods_and_beverages_at_school: str = Field(
        default="",
        description=(
            "Additional notes or comments about nutrition guidelines for foods and "
            'beverages at school. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class WellnessPolicyProgressReport(BaseModel):
    """Report on progress made in attaining the goals of the wellness policy"""

    report_on_the_progress_made_in_attaining_the_goals_of_the_wellness_policy: str = Field(
        ...,
        description=(
            "Narrative report describing progress made toward attaining the goals of the "
            'wellness policy. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class WellnessPolicyAssessmentToolAndReportTemplate(BaseModel):
    """
    Wellness Policy Assessment Tool and Report Template

    ''
    """

    policy_item_status: PolicyItemStatus = Field(..., description="Policy Item Status")
    nutrition_guidelines_for_foods_and_beverages_at_school: NutritionGuidelinesforFoodsandBeveragesatSchool = Field(
        ..., description="Nutrition Guidelines for Foods and Beverages at School"
    )
    wellness_policy_progress_report: WellnessPolicyProgressReport = Field(
        ..., description="Wellness Policy Progress Report"
    )
