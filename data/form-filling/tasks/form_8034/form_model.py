from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OtherSchoolBasedWellnessActivities(BaseModel):
    """Assessment of other school-based wellness activities and related goals"""

    included_in_the_written_policy_yes: BooleanLike = Field(
        default="",
        description=(
            "Indicate that this wellness activity or guideline is explicitly included in "
            "the written policy."
        ),
    )

    included_in_the_written_policy_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate that this wellness activity or guideline is not included in the "
            "written policy."
        ),
    )

    implemented_in_the_school_buildings_fully_in_place: BooleanLike = Field(
        default="",
        description=(
            "Indicate that this wellness activity or guideline is fully implemented in the "
            "school building(s)."
        ),
    )

    implemented_in_the_school_buildings_partially_in_place: BooleanLike = Field(
        default="",
        description=(
            "Indicate that this wellness activity or guideline is partially implemented in "
            "the school building(s)."
        ),
    )

    implemented_in_the_school_buildings_not_in_place: BooleanLike = Field(
        default="",
        description=(
            "Indicate that this wellness activity or guideline is not implemented in the "
            "school building(s)."
        ),
    )

    free_drinking_water_is_available_and_accessible_to_students_during_meal_periods_and_throughout_the_school_day: BooleanLike = Field(
        default="",
        description=(
            "Specify whether free drinking water is available and accessible to students "
            "during meal periods and throughout the school day."
        ),
    )

    school_nutrition_staff_meet_local_hiring_criteria_and_in_compliance_with_federal_regulations: BooleanLike = Field(
        default="",
        description=(
            "Specify whether school nutrition staff meet local hiring criteria and comply "
            "with federal regulations."
        ),
    )

    we_provide_continuing_education_to_school_nutrition_staff_as_required_by_federal_regulations: BooleanLike = Field(
        default="",
        description=(
            "Specify whether continuing education is provided to school nutrition staff as "
            "required by federal regulations."
        ),
    )

    we_provide_adequate_space_for_eating_and_serving_school_meals: BooleanLike = Field(
        default="",
        description="Specify whether adequate space is provided for eating and serving school meals.",
    )

    we_provide_a_safe_and_clean_meal_environment_for_students: BooleanLike = Field(
        default="",
        description="Specify whether the meal environment for students is safe and clean.",
    )

    we_offer_students_enough_time_to_eat_and_schedule_meal_periods_at_appropriate_hours: BooleanLike = Field(
        default="",
        description=(
            "Specify whether students have sufficient sit-down time for meals and meal "
            "periods are scheduled at appropriate hours."
        ),
    )

    we_implement_alternate_school_breakfast_service_models_to_increase_participation: BooleanLike = Field(
        default="",
        description=(
            "Specify whether alternate breakfast service models (e.g., grab & go, "
            "in-classroom, after first period) are implemented to increase participation."
        ),
    )

    students_have_access_to_hand_washing_or_sanitizing_before_meals: BooleanLike = Field(
        default="",
        description=(
            "Specify whether students have access to hand washing or sanitizing before meals."
        ),
    )

    only_authorized_staff_have_access_to_the_food_service_operation: BooleanLike = Field(
        default="",
        description=(
            "Specify whether access to the food service operation is limited to authorized staff."
        ),
    )

    we_provide_the_nutrition_content_of_school_meals_to_the_school_community: BooleanLike = Field(
        default="",
        description=(
            "Specify whether nutrition content information for school meals is shared with "
            "the school community."
        ),
    )

    we_include_students_parents_in_menu_selections_through_taste_testing_and_surveys: BooleanLike = Field(
        default="",
        description=(
            "Specify whether students and parents are involved in menu selections via "
            "taste-testing and surveys."
        ),
    )

    we_utilize_outside_funding_and_programs_to_enhance_school_wellness: BooleanLike = Field(
        default="",
        description=(
            "Specify whether outside funding and programs are used to enhance school wellness."
        ),
    )

    we_train_all_staff_on_the_components_of_the_school_wellness_policy: BooleanLike = Field(
        default="",
        description=(
            "Specify whether all staff receive training on the components of the school "
            "wellness policy."
        ),
    )

    school_based_activities_are_planned_with_wellness_policy_goals_in_mind: BooleanLike = Field(
        default="",
        description=(
            "Specify whether school-based activities are planned to align with wellness "
            "policy goals."
        ),
    )

    fundraising_projects_submitted_for_approval_are_supportive_of_healthy_eating_and_student_wellness: BooleanLike = Field(
        default="",
        description=(
            "Specify whether fundraising projects support healthy eating and student wellness."
        ),
    )

    we_encourage_stakeholders_to_serve_as_positive_role_models: BooleanLike = Field(
        default="",
        description=(
            "Specify whether key stakeholders are encouraged to serve as positive role "
            "models through district programs, communications, and outreach."
        ),
    )

    we_communicate_information_to_parents_to_support_healthy_diet_and_physical_activity: BooleanLike = Field(
        default="",
        description=(
            "Specify whether information is communicated to parents/guardians to support "
            "healthy diet and daily physical activity for their children."
        ),
    )

    indoor_air_quality_is_in_accordance_with_healthy_learning_environment_program_and_laws: BooleanLike = Field(
        default="",
        description=(
            "Specify whether indoor air quality meets the healthy learning environment "
            "program and applicable laws and regulations."
        ),
    )

    other_goal_describe: str = Field(
        default="",
        description=(
            "Describe any additional school-based wellness goal not listed above. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    notes_on_goals_for_other_school_based_activities: str = Field(
        default="",
        description=(
            "Provide notes or details about goals for other school-based wellness "
            'activities. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class NutritionGuidelinesforAllFoodsandBeveragesatSchool(BaseModel):
    """Assessment of nutrition standards and practices for all foods and beverages at school"""

    we_consider_promoting_student_health_and_reducing_obesity_when_offering_foods_and_beverages: BooleanLike = Field(
        default="",
        description=(
            "Specify whether student health and obesity prevention are considered when "
            "offering foods and beverages at school."
        ),
    )

    foods_and_beverages_provided_through_nslp_and_sbp_comply_with_federal_meal_standards: BooleanLike = Field(
        default="",
        description=(
            "Specify whether foods and beverages in the National School Lunch and School "
            "Breakfast Programs comply with federal meal standards."
        ),
    )

    we_offer_healthy_food_and_beverage_options_at_school_sponsored_events: BooleanLike = Field(
        default="",
        description=(
            "Specify whether healthy food and beverage options are offered at "
            "school-sponsored events (e.g., dances, sporting events)."
        ),
    )

    foods_and_beverages_outside_of_the_school_meal_meet_or_exceed_competitive_food_standards: BooleanLike = Field(
        default="",
        description=(
            "Specify whether all foods and beverages sold to students outside of school "
            "meals during the school day meet or exceed federal competitive food standards "
            "(USDA Smart Snacks in School)."
        ),
    )


class WellnessPolicyAssessmentToolAndReportTemplate(BaseModel):
    """
    Wellness Policy Assessment Tool and Report Template

    ''
    """

    other_school_based_wellness_activities: OtherSchoolBasedWellnessActivities = Field(
        ..., description="Other School-Based Wellness Activities"
    )
    nutrition_guidelines_for_all_foods_and_beverages_at_school: NutritionGuidelinesforAllFoodsandBeveragesatSchool = Field(
        ..., description="Nutrition Guidelines for All Foods and Beverages at School"
    )
