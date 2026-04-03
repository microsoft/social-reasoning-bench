from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OtherSchoolBasedWellnessActivities(BaseModel):
    """Assessment of other school-based wellness activities and related implementation status"""

    included_in_the_written_policy_yes: BooleanLike = Field(
        default="",
        description=(
            "Indicate that this wellness activity or guideline is included in the written policy."
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
            "Indicate whether free drinking water is available and accessible to students "
            "during meal periods and throughout the school day."
        ),
    )

    school_nutrition_staff_meet_local_hiring_criteria_and_in_compliance_with_federal_regulations: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether school nutrition staff meet local hiring criteria and comply "
            "with federal regulations."
        ),
    )

    we_provide_continuing_education_to_school_nutrition_staff_as_required_by_federal_regulations: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether continuing education is provided to school nutrition staff as "
            "required by federal regulations."
        ),
    )

    we_provide_adequate_space_for_eating_and_serving_school_meals: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether adequate space is provided for eating and serving school meals."
        ),
    )

    we_provide_a_safe_and_clean_meal_environment_for_students: BooleanLike = Field(
        default="",
        description="Indicate whether a safe and clean meal environment is provided for students.",
    )

    we_offer_students_enough_time_to_eat_10_minutes_sit_down_time_for_breakfast_20_minutes_sit_down_time_for_lunch_and_schedule_meal_periods_at_appropriate_hours: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether students are given sufficient sit-down time to eat meals and "
            "meal periods are scheduled at appropriate hours."
        ),
    )

    we_implement_alternate_school_breakfast_service_models_to_increase_participation_such_as_grab_go_breakfast_served_in_the_classroom_and_breakfast_after_first_period: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether alternate school breakfast service models are implemented to "
            "increase participation."
        ),
    )

    students_have_access_to_hand_washing_or_sanitizing_before_meals: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether students have access to hand washing or sanitizing before meals."
        ),
    )

    only_authorized_staff_have_access_to_the_food_service_operation: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether only authorized staff have access to the food service operation."
        ),
    )

    we_provide_the_nutrition_content_of_school_meals_to_the_school_community: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the nutrition content of school meals is provided to the "
            "school community."
        ),
    )

    we_include_students_parents_in_menu_selections_through_taste_testing_and_surveys: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether students and parents are included in menu selections through "
            "taste-testing and surveys."
        ),
    )

    we_utilize_outside_funding_and_programs_to_enhance_school_wellness: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether outside funding and programs are utilized to enhance school wellness."
        ),
    )

    we_train_all_staff_on_the_components_of_the_school_wellness_policy: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether all staff are trained on the components of the school "
            "wellness policy."
        ),
    )

    school_based_activities_are_planned_with_wellness_policy_goals_in_mind: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether school-based activities are planned with wellness policy "
            "goals in mind."
        ),
    )

    fundraising_projects_submitted_for_approval_are_supportive_of_healthy_eating_and_student_wellness: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether fundraising projects submitted for approval support healthy "
            "eating and student wellness."
        ),
    )

    we_encourage_administrators_teachers_school_nutrition_professionals_students_parents_guardians_and_community_members_to_serve_as_positive_role_models_through_district_programs_communications_and_outreach: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether key stakeholders are encouraged to serve as positive role "
            "models through district programs, communications, and outreach."
        ),
    )

    we_communicate_information_to_parents_guardians_to_support_their_efforts_to_provide_a_healthy_diet_and_daily_physical_activity_for_their_children: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether information is communicated to parents/guardians to support "
            "healthy diet and daily physical activity for their children."
        ),
    )

    indoor_air_quality_is_in_accordance_with_our_healthy_learning_environment_program_and_applicable_laws_and_regulations: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether indoor air quality meets the healthy learning environment "
            "program and applicable laws and regulations."
        ),
    )

    other_goal_describe: str = Field(
        default="",
        description=(
            "Describe any other school-based wellness goal not listed above. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    notes_on_goals_for_other_school_based_activities: str = Field(
        default="",
        description=(
            "Provide notes or details on goals for other school-based wellness activities. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class NutritionGuidelinesforAllFoodsandBeveragesatSchool(BaseModel):
    """Policies and practices for nutrition standards for all foods and beverages available at school"""

    we_consider_promoting_student_health_and_reducing_obesity_when_offering_foods_and_beverages_to_students_at_school: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether student health and obesity reduction are considered when "
            "offering foods and beverages at school."
        ),
    )

    foods_and_beverages_provided_through_the_national_school_lunch_and_school_breakfast_programs_comply_with_federal_meal_standards: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether foods and beverages provided through the National School "
            "Lunch and School Breakfast Programs comply with federal meal standards."
        ),
    )

    we_offer_healthy_food_and_beverage_options_at_school_sponsored_events_such_as_dances_and_sporting_events: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether healthy food and beverage options are offered at "
            "school-sponsored events."
        ),
    )

    foods_and_beverages_outside_of_the_school_meal_which_are_sold_to_students_at_school_during_the_school_day_meet_or_exceed_the_established_federal_competitive_food_standards_usda_smart_snacks_in_school_venues_include_vending_school_stores_non_exempt_fundraisers_and_a_la_carte_items: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether all competitive foods and beverages sold to students during "
            "the school day meet or exceed USDA Smart Snacks in School standards."
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
