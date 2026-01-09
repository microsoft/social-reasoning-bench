from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Mind(BaseModel):
    """Team status and actions related to mental focus, clarity, and mindset"""

    mind_where_are_you_right_now_as_a_team_list_your_strengths_and_weaknesses: str = Field(
        default="",
        description=(
            "Describe the team’s current mental or cognitive strengths and weaknesses "
            '(focus, clarity, learning, mindset). .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mind_what_can_you_do_as_a_leader_list_two_action_items_per_section: str = Field(
        default="",
        description=(
            "List two concrete leadership actions to support the team’s mental or cognitive "
            'needs. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    mind_what_can_you_do_as_a_team_list_two_action_items_per_section: str = Field(
        default="",
        description=(
            "List two concrete team actions to support shared mental or cognitive "
            'effectiveness. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class Body(BaseModel):
    """Team status and actions related to physical energy, stamina, and workload"""

    body_where_are_you_right_now_as_a_team_list_your_strengths_and_weaknesses: str = Field(
        default="",
        description=(
            "Describe the team’s current physical or practical strengths and weaknesses "
            "(energy, workload, capacity, processes). .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    body_what_can_you_do_as_a_leader_list_two_action_items_per_section: str = Field(
        default="",
        description=(
            "List two concrete leadership actions to support the team’s physical or "
            'practical work needs. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    body_what_can_you_do_as_a_team_list_two_action_items_per_section: str = Field(
        default="",
        description=(
            "List two concrete team actions to support physical or practical work and "
            'capacity. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class Heart(BaseModel):
    """Team status and actions related to motivation, emotions, and relationships"""

    heart_where_are_you_right_now_as_a_team_list_your_strengths_and_weaknesses: str = Field(
        default="",
        description=(
            "Describe the team’s emotional and relational strengths and weaknesses (trust, "
            'motivation, connection). .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    heart_what_can_you_do_as_a_leader_list_two_action_items_per_section: str = Field(
        default="",
        description=(
            "List two concrete leadership actions to support the team’s emotional and "
            'relational needs. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    heart_what_can_you_do_as_a_team_list_two_action_items_per_section: str = Field(
        default="",
        description=(
            "List two concrete team actions to strengthen emotional connection, trust, and "
            'motivation. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class Environment(BaseModel):
    """Team status and actions related to surroundings, tools, and organizational context"""

    environment_where_are_you_right_now_as_a_team_list_your_strengths_and_weaknesses: str = Field(
        default="",
        description=(
            "Describe environmental or contextual strengths and weaknesses (workspace, "
            'tools, culture, external conditions). .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    environment_what_can_you_do_as_a_leader_list_two_action_items_per_section: str = Field(
        default="",
        description=(
            "List two concrete leadership actions to improve the team’s environment or "
            'context. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    environment_what_can_you_do_as_a_team_list_two_action_items_per_section: str = Field(
        default="",
        description=(
            "List two concrete team actions to improve the shared environment or working "
            'conditions. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class Exercise(BaseModel):
    """
    EXERCISE

    Refer to the guiding questions set out in the framework above to fill in the table below. As the team leader, revisit this activity periodically and make sure it is up to date.
    When you hit a bottleneck, consider revisiting this exercise to identify what kind of support can help to keep you and your team going.
    WHY IS THIS IMPORTANT?
    In this final activity, you will pull together the different components from all the previous frameworks to put in place the systems that will help your change initiative achieve results. We often put more emphasis on and effort into building teams and getting the initiative off the ground. As a result, it is very common in organizations to overlook what is needed to maintain and support efforts over time. Operational strategies provide a simple checklist to understand the needs of your team and ensure that you have the right conditions to achieve your goals.
    """

    mind: Mind = Field(..., description="Mind")
    body: Body = Field(..., description="Body")
    heart: Heart = Field(..., description="Heart")
    environment: Environment = Field(..., description="Environment")
