from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CityOfMuskegonPlanningZoningApplication(BaseModel):
    """
    City of Muskegon Planning & Zoning Application

    These questions are ONLY for Zoning Board of Appeals requests
    """

    why_should_your_property_be_unique_compared_to_others_in_the_neighborhood: str = Field(
        ...,
        description=(
            "Explain what makes your property unique compared to other nearby properties. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    what_property_rights_do_your_neighbors_enjoy_that_you_cant_because_of_the_nature_of_your_property: str = Field(
        ...,
        description=(
            "Describe the property rights or uses your neighbors have that you cannot "
            "exercise due to your property’s characteristics. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    will_granting_a_variance_to_you_negatively_affect_your_neighbors_or_the_public: str = Field(
        ...,
        description=(
            "Explain any potential negative impacts of the requested variance on neighbors "
            'or the general public. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    who_or_what_is_the_cause_of_the_difficulty_with_the_current_ordinance: str = Field(
        ...,
        description=(
            "Describe the source or cause of the hardship or difficulty created by the "
            'current zoning ordinance. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    do_you_have_reasons_other_than_financial_gain_for_asking_for_the_variance: str = Field(
        ...,
        description=(
            "Provide non-financial reasons or justifications for requesting the variance. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    could_you_get_by_with_less_of_a_variance_from_the_ordinance_requirements: str = Field(
        ...,
        description=(
            "Explain whether a smaller or more limited variance could reasonably address "
            'your situation. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    will_this_variance_alter_the_essential_character_of_the_area: str = Field(
        ...,
        description=(
            "Describe whether and how the variance would change the overall character of "
            'the surrounding area. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    is_your_preferred_property_use_specifically_mentioned_in_the_ordinance_as_not_being_allowed_in_your_zoning_district: str = Field(
        ...,
        description=(
            "Indicate whether the use you are requesting is explicitly listed as not "
            "permitted in your zoning district and explain. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )
