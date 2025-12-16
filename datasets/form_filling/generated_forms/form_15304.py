from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class WhatICanDoToday(BaseModel):
    """Immediate actions to start the weight-management plan"""

    understand_the_bodys_natural_reaction_to_weight_loss: BooleanLike = Field(
        default="", description="Check if this is a goal or action you plan to take today."
    )

    fill_my_prescription: BooleanLike = Field(
        default="",
        description="Check if filling your prescription is a goal or action you plan to take today.",
    )

    discuss_how_weight_related_health_conditions_may_affect_me: BooleanLike = Field(
        default="",
        description=(
            "Check if you plan to discuss weight-related health conditions with your health "
            "care professional."
        ),
    )


class HealthyEating(BaseModel):
    """Daily nutrition goals and eating habits"""

    eat_3_meals_a_day_including_breakfast: BooleanLike = Field(
        default="",
        description="Check if eating 3 meals a day including breakfast is part of your plan.",
    )

    drink_8_glasses_of_water_a_day: BooleanLike = Field(
        default="", description="Check if drinking 8 glasses of water daily is part of your plan."
    )

    reduce_portions: BooleanLike = Field(
        default="", description="Check if reducing portion sizes is part of your plan."
    )

    increase_protein: BooleanLike = Field(
        default="", description="Check if increasing protein intake is part of your plan."
    )

    increase_fiber: BooleanLike = Field(
        default="", description="Check if increasing fiber intake is part of your plan."
    )

    reduce_sugar: BooleanLike = Field(
        default="", description="Check if reducing sugar intake is part of your plan."
    )

    reduce_sodium: BooleanLike = Field(
        default="", description="Check if reducing sodium intake is part of your plan."
    )

    reduce_carbohydrates: BooleanLike = Field(
        default="", description="Check if reducing carbohydrate intake is part of your plan."
    )

    limit_saturated_and_trans_fats: BooleanLike = Field(
        default="", description="Check if limiting saturated and trans fats is part of your plan."
    )

    find_a_healthy_go_to_snack_low_in_carbs_sugar_and_fat: BooleanLike = Field(
        default="",
        description=(
            "Check if finding a healthy low-carb, low-sugar, low-fat snack is part of your plan."
        ),
    )

    increase_servings_of_fruit: BooleanLike = Field(
        default="", description="Check if increasing fruit servings is part of your plan."
    )

    increase_servings_of_vegetables: BooleanLike = Field(
        default="", description="Check if increasing vegetable servings is part of your plan."
    )

    reduce_soda: BooleanLike = Field(
        default="", description="Check if reducing soda intake is part of your plan."
    )

    limit_processed_foods: BooleanLike = Field(
        default="", description="Check if limiting processed foods is part of your plan."
    )

    consult_a_dietitian_about: str = Field(
        default="",
        description=(
            "Describe what you plan to consult a dietitian about. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    daily_goal_calories: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Enter your daily calorie goal."
    )

    notes: str = Field(
        default="",
        description=(
            "Use this space for any additional notes about your weight-management plan. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PhysicalActivity(BaseModel):
    """Exercise and movement goals"""

    walk_brisktly: BooleanLike = Field(
        default="", description="Check if walking briskly is part of your physical activity plan."
    )

    play_golf: BooleanLike = Field(
        default="", description="Check if playing golf is part of your physical activity plan."
    )

    bike: BooleanLike = Field(
        default="", description="Check if biking is part of your physical activity plan."
    )

    do_yoga_or_pilates: BooleanLike = Field(
        default="",
        description="Check if doing yoga or pilates is part of your physical activity plan.",
    )

    swim: BooleanLike = Field(
        default="", description="Check if swimming is part of your physical activity plan."
    )

    lift_weights: BooleanLike = Field(
        default="", description="Check if lifting weights is part of your physical activity plan."
    )

    dance: BooleanLike = Field(
        default="", description="Check if dancing is part of your physical activity plan."
    )

    do_housework_or_yardwork: BooleanLike = Field(
        default="",
        description="Check if doing housework or yardwork is part of your physical activity plan.",
    )

    hike: BooleanLike = Field(
        default="", description="Check if hiking is part of your physical activity plan."
    )

    other_activity: str = Field(
        default="",
        description=(
            "Specify another physical activity you plan to do. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    add_new_activity_goals_to_your_plan_over_time: BooleanLike = Field(
        default="", description="Check if you plan to add new activity goals over time."
    )


class BehaviorandMindset(BaseModel):
    """Habits, thoughts, and behaviors that support weight management"""

    keep_a_food_journal: BooleanLike = Field(
        default="", description="Check if keeping a food journal is part of your behavior plan."
    )

    keep_an_activity_journal: BooleanLike = Field(
        default="",
        description="Check if keeping an activity journal is part of your behavior plan.",
    )

    identify_triggers_that_lead_to_emotional_eating: BooleanLike = Field(
        default="",
        description="Check if identifying triggers for emotional eating is part of your plan.",
    )

    identify_challenging_social_eating_situations: BooleanLike = Field(
        default="",
        description="Check if identifying challenging social eating situations is part of your plan.",
    )

    learn_about_eating_mindfully: BooleanLike = Field(
        default="", description="Check if learning about mindful eating is part of your plan."
    )

    prepare_for_how_to_handle_setbacks: BooleanLike = Field(
        default="",
        description="Check if preparing for how to handle setbacks is part of your plan.",
    )

    get_a_full_nights_sleep_7_8_hours: BooleanLike = Field(
        default="", description="Check if getting 7–8 hours of sleep nightly is part of your plan."
    )

    focus_on_small_changes_like: str = Field(
        default="",
        description=(
            "Describe specific small changes you want to focus on. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class MyWeightmanagementPlan(BaseModel):
    """
    My Weight-Management Plan

    Obesity is a disease that can become more severe over time. Even with the help of a prescription treatment for chronic weight management, a successful, long-term plan includes healthy eating, increased physical activity, and behavior changes that fit your lifestyle. Please use the following ideas as a guide for discussing your weight-management plan with your health care professional.
    """

    what_i_can_do_today: WhatICanDoToday = Field(..., description="What I Can Do Today")
    healthy_eating: HealthyEating = Field(..., description="Healthy Eating")
    physical_activity: PhysicalActivity = Field(..., description="Physical Activity")
    behavior_and_mindset: BehaviorandMindset = Field(..., description="Behavior and Mindset")
