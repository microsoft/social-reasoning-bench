from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PolicyStatus(BaseModel):
    """Whether the wellness items are included in written policy and implemented in school buildings"""

    included_in_the_written_policy_yes: BooleanLike = Field(
        default="",
        description="Indicate that this item is included in the written wellness policy.",
    )

    included_in_the_written_policy_no: BooleanLike = Field(
        default="",
        description="Indicate that this item is not included in the written wellness policy.",
    )

    implemented_in_the_school_buildings_fully_in_place: BooleanLike = Field(
        default="",
        description="Check if the item is fully implemented in all relevant school buildings.",
    )

    implemented_in_the_school_buildings_partially_in_place: BooleanLike = Field(
        default="",
        description="Check if the item is only partially implemented in the school buildings.",
    )

    implemented_in_the_school_buildings_not_in_place: BooleanLike = Field(
        default="", description="Check if the item is not implemented in the school buildings."
    )


class NutritionGuidelinesforFoodsandBeveragesatSchool(BaseModel):
    """Specific wellness policy goals and practices related to foods, beverages, and marketing"""

    we_limit_the_number_of_food_fundraisers_at_school: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the school limits food fundraisers and has procedures for "
            "fundraiser exemptions per PDE limits."
        ),
    )

    we_have_local_standards_in_our_written_policy_for_foods_and_beverages_offered_for_free: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether local standards exist in the written policy for foods and "
            "beverages offered for free to students."
        ),
    )

    we_provide_a_list_of_nonfood_ideas_and_healthy_alternatives: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the school provides staff and parents/guardians with nonfood "
            "ideas and healthy food/beverage alternatives."
        ),
    )

    only_foods_and_beverages_meeting_federal_nutrition_standards_are_marketed: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether only foods and beverages meeting USDA Smart Snacks standards "
            "are marketed or promoted to students during the school day."
        ),
    )

    notes_on_nutrition_guidelines_for_foods_and_beverages_at_school: str = Field(
        default="",
        description=(
            "Provide any additional notes or explanations about the nutrition guidelines "
            'for foods and beverages at school. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class WellnessPolicyProgressReport(BaseModel):
    """Reporting on progress toward wellness policy goals"""

    report_on_the_progress_made_in_attaining_the_goals_of_the_wellness_policy: str = Field(
        ...,
        description=(
            "Required narrative report describing progress toward meeting the goals of the "
            'wellness policy. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class WellnessPolicyAssessmentToolAndReportTemplate(BaseModel):
    """
    Wellness Policy Assessment Tool and Report Template

    Included in the written policy? Yes  No
    Implemented in the school building(s)? Fully in Place  Partially in Place  Not in Place
    """

    policy_status: PolicyStatus = Field(..., description="Policy Status")
    nutrition_guidelines_for_foods_and_beverages_at_school: NutritionGuidelinesforFoodsandBeveragesatSchool = Field(
        ..., description="Nutrition Guidelines for Foods and Beverages at School"
    )
    wellness_policy_progress_report: WellnessPolicyProgressReport = Field(
        ..., description="Wellness Policy Progress Report"
    )
