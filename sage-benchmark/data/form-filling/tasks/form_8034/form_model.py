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
    """Assessment of policy inclusion and implementation for other school-based wellness activities"""

    included_in_the_written_policy_free_drinking_water_is_available_and_accessible_to_students_during_meal_periods_and_throughout_the_school_day: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Indicate whether the policy about free drinking water availability is "
            "explicitly included in the written wellness policy."
        ),
    )

    implemented_in_the_school_buildings_free_drinking_water_is_available_and_accessible_to_students_during_meal_periods_and_throughout_the_school_day: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Rate the level of implementation of free drinking water availability in the "
            "school building(s)."
        ),
    )

    included_in_the_written_policy_school_nutrition_staff_meet_local_hiring_criteria_and_in_compliance_with_federal_regulations: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Indicate if meeting local hiring criteria and federal regulations for school "
            "nutrition staff is written into the policy."
        ),
    )

    implemented_in_the_school_buildings_school_nutrition_staff_meet_local_hiring_criteria_and_in_compliance_with_federal_regulations: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Rate how fully the hiring criteria and federal regulation requirements for "
            "school nutrition staff are implemented."
        ),
    )

    included_in_the_written_policy_we_provide_continuing_education_to_school_nutrition_staff_as_required_by_federal_regulations: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Specify whether continuing education for school nutrition staff is included in "
            "the written policy."
        ),
    )

    implemented_in_the_school_buildings_we_provide_continuing_education_to_school_nutrition_staff_as_required_by_federal_regulations: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Indicate the extent to which continuing education for school nutrition staff "
            "is implemented."
        ),
    )

    included_in_the_written_policy_we_provide_adequate_space_for_eating_and_serving_school_meals: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "State whether providing adequate space for eating and serving meals is written "
            "into the policy."
        ),
    )

    implemented_in_the_school_buildings_we_provide_adequate_space_for_eating_and_serving_school_meals: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Rate how fully adequate space for eating and serving meals is provided in practice."
        ),
    )

    included_in_the_written_policy_we_provide_a_safe_and_clean_meal_environment_for_students: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Indicate if a safe and clean meal environment is specified in the written policy."
        ),
    )

    implemented_in_the_school_buildings_we_provide_a_safe_and_clean_meal_environment_for_students: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description="Assess the level of implementation of a safe and clean meal environment.",
    )

    included_in_the_written_policy_we_offer_students_enough_time_to_eat_and_schedule_meal_periods_at_appropriate_hours: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Specify whether adequate sit-down time and appropriate scheduling of meal "
            "periods are written into the policy."
        ),
    )

    implemented_in_the_school_buildings_we_offer_students_enough_time_to_eat_and_schedule_meal_periods_at_appropriate_hours: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description="Rate how fully adequate meal time and appropriate scheduling are implemented.",
    )

    included_in_the_written_policy_we_implement_alternate_school_breakfast_service_models_to_increase_participation: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Indicate whether alternate breakfast service models are included in the "
            "written policy."
        ),
    )

    implemented_in_the_school_buildings_we_implement_alternate_school_breakfast_service_models_to_increase_participation: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description="Assess the extent to which alternate breakfast service models are implemented.",
    )

    included_in_the_written_policy_students_have_access_to_hand_washing_or_sanitizing_before_meals: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "State whether student access to hand washing or sanitizing before meals is "
            "written into the policy."
        ),
    )

    implemented_in_the_school_buildings_students_have_access_to_hand_washing_or_sanitizing_before_meals: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Rate how fully access to hand washing or sanitizing before meals is implemented."
        ),
    )

    included_in_the_written_policy_only_authorized_staff_have_access_to_the_food_service_operation: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Indicate if restricted access to the food service operation is specified in "
            "the written policy."
        ),
    )

    implemented_in_the_school_buildings_only_authorized_staff_have_access_to_the_food_service_operation: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Assess how fully access to the food service operation is limited to authorized staff."
        ),
    )

    included_in_the_written_policy_we_provide_the_nutrition_content_of_school_meals_to_the_school_community: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Specify whether sharing nutrition content of school meals is written into the policy."
        ),
    )

    implemented_in_the_school_buildings_we_provide_the_nutrition_content_of_school_meals_to_the_school_community: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Rate the implementation of providing nutrition content information to the "
            "school community."
        ),
    )

    included_in_the_written_policy_we_include_students_parents_in_menu_selections_through_taste_testing_and_surveys: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Indicate whether involving students and parents in menu selection is written "
            "into the policy."
        ),
    )

    implemented_in_the_school_buildings_we_include_students_parents_in_menu_selections_through_taste_testing_and_surveys: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Assess how fully students and parents are involved in menu selections in practice."
        ),
    )

    included_in_the_written_policy_we_utilize_outside_funding_and_programs_to_enhance_school_wellness: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "State whether using outside funding and programs for wellness is written into "
            "the policy."
        ),
    )

    implemented_in_the_school_buildings_we_utilize_outside_funding_and_programs_to_enhance_school_wellness: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Rate the extent to which outside funding and programs are used to enhance wellness."
        ),
    )

    included_in_the_written_policy_we_train_all_staff_on_the_components_of_the_school_wellness_policy: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Indicate whether staff training on the wellness policy is included in the "
            "written policy."
        ),
    )

    implemented_in_the_school_buildings_we_train_all_staff_on_the_components_of_the_school_wellness_policy: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description="Assess how fully staff training on the wellness policy is implemented.",
    )

    included_in_the_written_policy_school_based_activities_are_planned_with_wellness_policy_goals_in_mind: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Specify whether planning school-based activities with wellness goals is "
            "written into the policy."
        ),
    )

    implemented_in_the_school_buildings_school_based_activities_are_planned_with_wellness_policy_goals_in_mind: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Rate how consistently school-based activities are planned with wellness goals "
            "in practice."
        ),
    )

    included_in_the_written_policy_fundraising_projects_submitted_for_approval_are_supportive_of_healthy_eating_and_student_wellness: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Indicate whether healthy, wellness-supportive fundraising is specified in the "
            "written policy."
        ),
    )

    implemented_in_the_school_buildings_fundraising_projects_submitted_for_approval_are_supportive_of_healthy_eating_and_student_wellness: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Assess how fully fundraising projects support healthy eating and wellness in practice."
        ),
    )

    included_in_the_written_policy_we_encourage_administrators_teachers_school_nutrition_professionals_students_parents_guardians_and_community_members_to_serve_as_positive_role_models: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "State whether encouraging key stakeholders to serve as positive role models is "
            "written into the policy."
        ),
    )

    implemented_in_the_school_buildings_we_encourage_administrators_teachers_school_nutrition_professionals_students_parents_guardians_and_community_members_to_serve_as_positive_role_models: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Rate how fully stakeholders are encouraged and supported to act as positive "
            "role models."
        ),
    )

    included_in_the_written_policy_we_communicate_information_to_parents_guardians_to_support_their_efforts_to_provide_a_healthy_diet_and_daily_physical_activity: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Indicate whether communication to parents/guardians about healthy diet and "
            "activity is written into the policy."
        ),
    )

    implemented_in_the_school_buildings_we_communicate_information_to_parents_guardians_to_support_their_efforts_to_provide_a_healthy_diet_and_daily_physical_activity: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description="Assess how fully this communication to parents/guardians is implemented.",
    )

    included_in_the_written_policy_indoor_air_quality_is_in_accordance_with_our_healthy_learning_environment_program_and_applicable_laws_and_regulations: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Specify whether indoor air quality standards are written into the wellness or "
            "related policy."
        ),
    )

    implemented_in_the_school_buildings_indoor_air_quality_is_in_accordance_with_our_healthy_learning_environment_program_and_applicable_laws_and_regulations: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="", description="Rate how fully indoor air quality standards are met in practice."
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
            "Provide notes or details about the other school-based wellness goals and their "
            'implementation. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class NutritionGuidelinesforAllFoodsandBeveragesatSchool(BaseModel):
    """Assessment of policy inclusion and implementation for nutrition guidelines for all foods and beverages at school"""

    included_in_the_written_policy_we_consider_promoting_student_health_and_reducing_obesity_when_offering_foods_and_beverages_to_students_at_school: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Indicate whether considering student health and obesity prevention in food and "
            "beverage offerings is written into the policy."
        ),
    )

    implemented_in_the_school_buildings_we_consider_promoting_student_health_and_reducing_obesity_when_offering_foods_and_beverages_to_students_at_school: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Rate how fully student health and obesity prevention are considered in actual "
            "food and beverage offerings."
        ),
    )

    included_in_the_written_policy_foods_and_beverages_provided_through_the_national_school_lunch_and_school_breakfast_programs_comply_with_federal_meal_standards: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Specify whether compliance with federal meal standards for NSLP and SBP is "
            "written into the policy."
        ),
    )

    implemented_in_the_school_buildings_foods_and_beverages_provided_through_the_national_school_lunch_and_school_breakfast_programs_comply_with_federal_meal_standards: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Assess how fully NSLP and SBP offerings comply with federal meal standards in "
            "practice."
        ),
    )

    included_in_the_written_policy_we_offer_healthy_food_and_beverage_options_at_school_sponsored_events: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Indicate whether providing healthy options at school-sponsored events is "
            "written into the policy."
        ),
    )

    implemented_in_the_school_buildings_we_offer_healthy_food_and_beverage_options_at_school_sponsored_events: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description="Rate how consistently healthy options are offered at school-sponsored events.",
    )

    included_in_the_written_policy_foods_and_beverages_outside_of_the_school_meal_meet_or_exceed_federal_competitive_food_standards: Literal[
        "Yes", "No", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Specify whether compliance with USDA Smart Snacks standards for all "
            "competitive foods is written into the policy."
        ),
    )

    implemented_in_the_school_buildings_foods_and_beverages_outside_of_the_school_meal_meet_or_exceed_federal_competitive_food_standards: Literal[
        "Fully in Place", "Partially in Place", "Not in Place", "N/A", ""
    ] = Field(
        default="",
        description=(
            "Assess how fully all competitive foods sold during the school day meet USDA "
            "Smart Snacks standards."
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
