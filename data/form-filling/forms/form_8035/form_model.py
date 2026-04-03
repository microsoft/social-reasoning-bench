from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PolicyStatus(BaseModel):
    """Whether the wellness policy elements are written and implemented"""

    included_in_the_written_policy_yes: BooleanLike = Field(
        default="", description="Indicate that the item is included in the written wellness policy."
    )

    included_in_the_written_policy_no: BooleanLike = Field(
        default="",
        description="Indicate that the item is not included in the written wellness policy.",
    )

    implemented_in_the_school_buildings_fully_in_place: BooleanLike = Field(
        default="",
        description="Indicate that the item is fully implemented in the school building(s).",
    )

    implemented_in_the_school_buildings_partially_in_place: BooleanLike = Field(
        default="",
        description="Indicate that the item is partially implemented in the school building(s).",
    )

    implemented_in_the_school_buildings_not_in_place: BooleanLike = Field(
        default="",
        description="Indicate that the item is not implemented in the school building(s).",
    )


class NutritionGuidelinesforFoodsandBeveragesatSchool(BaseModel):
    """Specific wellness policy goals and practices related to foods and beverages"""

    we_limit_the_number_of_food_fundraisers_at_school_and_have_procedures_in_place_for_requesting_a_fundraiser_exemption: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the school limits food fundraisers and has procedures for "
            "fundraiser exemptions."
        ),
    )

    we_have_local_standards_in_our_written_policy_for_foods_and_beverages_offered_for_free_to_students_at_school_including_food_rewards_items_offered_at_classroom_parties_and_celebrations_and_foods_beverages_provided_to_the_class_as_shared_classroom_snacks: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether local standards for free foods and beverages (rewards, "
            "parties, shared snacks) are included in the written policy."
        ),
    )

    we_provide_a_list_of_nonfood_ideas_and_healthy_food_beverage_alternatives_to_staff_and_parents_guardians: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether a list of nonfood ideas and healthy food/beverage "
            "alternatives is provided to staff and parents/guardians."
        ),
    )

    only_foods_and_beverages_that_meet_or_exceed_federal_nutrition_standards_are_permitted_to_be_marketed_or_promoted_to_students_during_the_school_day: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether only foods and beverages meeting federal nutrition standards "
            "may be marketed or promoted to students during the school day."
        ),
    )

    notes_on_nutrition_guidelines_for_foods_and_beverages_at_school: str = Field(
        default="",
        description=(
            "Provide any additional notes or comments on nutrition guidelines for foods and "
            'beverages at school. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class WellnessPolicyProgressReport(BaseModel):
    """Required reporting on progress toward wellness policy goals"""

    report_on_the_progress_made_in_attaining_the_goals_of_the_wellness_policy: str = Field(
        ...,
        description=(
            "Describe the progress made in attaining the goals of the wellness policy. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class WellnessPolicyAssessmentToolAndReportTemplate(BaseModel):
    """
    Wellness Policy Assessment Tool and Report Template

    ''
    """

    policy_status: PolicyStatus = Field(..., description="Policy Status")
    nutrition_guidelines_for_foods_and_beverages_at_school: NutritionGuidelinesforFoodsandBeveragesatSchool = Field(
        ..., description="Nutrition Guidelines for Foods and Beverages at School"
    )
    wellness_policy_progress_report: WellnessPolicyProgressReport = Field(
        ..., description="Wellness Policy Progress Report"
    )
