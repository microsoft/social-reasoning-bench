from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CulturalAwarenessScales(BaseModel):
    """Your and your culture's positions on the cultural awareness framework scales"""

    low_power_distance_to_high_power_distance_scale_your_position: Literal[
        "Far toward low power distance",
        "Somewhat toward low power distance",
        "Middle",
        "Somewhat toward high power distance",
        "Far toward high power distance",
        "N/A",
        "",
    ] = Field(
        default="",
        description=(
            "Your own position on the authority scale from low power distance to high power "
            "distance."
        ),
    )

    low_power_distance_to_high_power_distance_scale_your_cultures_position: Literal[
        "Far toward low power distance",
        "Somewhat toward low power distance",
        "Middle",
        "Somewhat toward high power distance",
        "Far toward high power distance",
        "N/A",
        "",
    ] = Field(
        default="",
        description=(
            "Where you think the culture you were raised in falls on the authority scale "
            "from low to high power distance."
        ),
    )

    monochronic_to_polychronic_scale_your_position: Literal[
        "Far toward monochronic",
        "Somewhat toward monochronic",
        "Middle",
        "Somewhat toward polychronic",
        "Far toward polychronic",
        "N/A",
        "",
    ] = Field(
        default="",
        description=(
            "Your own position on the time orientation scale from monochronic to polychronic."
        ),
    )

    monochronic_to_polychronic_scale_your_cultures_position: Literal[
        "Far toward monochronic",
        "Somewhat toward monochronic",
        "Middle",
        "Somewhat toward polychronic",
        "Far toward polychronic",
        "N/A",
        "",
    ] = Field(
        default="",
        description=(
            "Where you think the culture you were raised in falls on the time orientation "
            "scale from monochronic to polychronic."
        ),
    )

    low_context_to_high_context_scale_your_position: Literal[
        "Far toward low context",
        "Somewhat toward low context",
        "Middle",
        "Somewhat toward high context",
        "Far toward high context",
        "N/A",
        "",
    ] = Field(
        default="",
        description=(
            "Your own position on the communication style scale from low context to high context."
        ),
    )

    low_context_to_high_context_scale_your_cultures_position: Literal[
        "Far toward low context",
        "Somewhat toward low context",
        "Middle",
        "Somewhat toward high context",
        "Far toward high context",
        "N/A",
        "",
    ] = Field(
        default="",
        description=(
            "Where you think the culture you were raised in falls on the communication "
            "style scale from low context to high context."
        ),
    )

    competitive_to_cooperative_scale_your_position: Literal[
        "Far toward competitive",
        "Somewhat toward competitive",
        "Middle",
        "Somewhat toward cooperative",
        "Far toward cooperative",
        "N/A",
        "",
    ] = Field(
        default="",
        description="Your own position on the achievement scale from competitive to cooperative.",
    )

    competitive_to_cooperative_scale_your_cultures_position: Literal[
        "Far toward competitive",
        "Somewhat toward competitive",
        "Middle",
        "Somewhat toward cooperative",
        "Far toward cooperative",
        "N/A",
        "",
    ] = Field(
        default="",
        description=(
            "Where you think the culture you were raised in falls on the achievement scale "
            "from competitive to cooperative."
        ),
    )


class CulturalDifferenceExamples(BaseModel):
    """Examples of colleagues or collaborators acting in culturally different ways and your reactions"""

    authority_example: str = Field(
        default="",
        description=(
            "Describe an example where a colleague or collaborator acted in a culturally "
            "different way related to authority, and how you reacted. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    time_example: str = Field(
        default="",
        description=(
            "Describe an example where a colleague or collaborator acted in a culturally "
            "different way related to time, and how you reacted. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    communication_example: str = Field(
        default="",
        description=(
            "Describe an example where a colleague or collaborator acted in a culturally "
            "different way related to communication, and how you reacted. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    achievement_example: str = Field(
        default="",
        description=(
            "Describe an example where a colleague or collaborator acted in a culturally "
            "different way related to achievement, and how you reacted. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Exercise(BaseModel):
    """
    EXERCISE

    Let's start by gaining an understanding of your own cultural profile and tendencies. On the diagram below, which shows the cultural awareness framework as a set of scales, mark where you stand on the scales. If your personal positions are different from those of the culture you were raised in, you can also reflect on these differences and mark what you think your culture's positions are on the scales.
    If you can think of an example of a time when you worked in a different cultural context or interacted with someone with a different cultural background, mark where you think the person or organization fell on the scales.
    Think of an example for each dimension of a time when one of your colleagues or collaborators acted in a culturally different way. How did you react? In light of what you have learned, would you react differently now? How?
    WHY IS THIS IMPORTANT?
    It is important to be aware of different dimensions of culture. This will deepen your ability to understand yourself, as well as those around you. In a work environment, cultural awareness can make collaboration smoother and more effective.
    Cultural awareness is the foundation of effective communication. People see, interpret and evaluate things in different ways. What is considered appropriate behaviour in one culture is frequently inappropriate in another. Misunderstandings can arise when we make sense of other people's reality through assumptions based on our own culture.
    Cultural awareness is essential for your advocacy, especially in international contexts. Your advocacy efforts may be fruitless unless you are able to adjust your communication style and behaviour to the culture that you are in.
    Having a good understanding of how your cultural identity may be perceived in different contexts is crucial. Based on your age and gender, you are likely to face certain cultural norms that may not always work in your favour. This is especially likely to happen in advocacy work where there is interaction with powerful individuals and organizations. Being smart about navigating these situations can help you in your efforts to achieve social change.
    """

    cultural_awareness_scales: CulturalAwarenessScales = Field(
        ..., description="Cultural Awareness Scales"
    )
    cultural_difference_examples: CulturalDifferenceExamples = Field(
        ..., description="Cultural Difference Examples"
    )
