from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FairInformation(BaseModel):
    """Basic information about the fair and division"""

    fair_name: str = Field(
        ...,
        description=(
            'Official name of the fair .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    fair_state_province: str = Field(
        ...,
        description=(
            "State or province where the fair is located .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    division: str = Field(
        ...,
        description=(
            "Division based on attendance (see rules) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    theme_if_applicable: str = Field(
        default="",
        description=(
            'Fair theme, if one was used .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class Category3NewDisplayMethodandorProp(BaseModel):
    """Details about the new display method or prop used for competitive exhibits"""

    method: BooleanLike = Field(..., description="Check if the new display is a method")

    prop: BooleanLike = Field(..., description="Check if the new display is a prop")

    why_was_this_one_method_of_display_and_or_prop_created_or_chosen: str = Field(
        ...,
        description=(
            "Explain the reason for creating or choosing this display method or prop .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    on_what_class_or_division_of_entries_was_the_display_method_and_or_prop_used: str = Field(
        ...,
        description=(
            "Describe the class or division of entries where this display method or prop "
            'was used .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    height: str = Field(
        ...,
        description=(
            "Overall height of the prop, including units .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    width: str = Field(
        ...,
        description=(
            "Overall width of the prop, including units .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    depth: str = Field(
        ...,
        description=(
            "Overall depth of the prop, including units .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    how_much_did_this_cost_to_create_cost_of_material_labor_etc: str = Field(
        ...,
        description=(
            "Total cost to create the method or prop, including materials and labor .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class IafeCompetitiveExhibitsAwardsProgramCategory3Form2021(BaseModel):
    """
        IAFE COMPETITIVE EXHIBITS AWARDS PROGRAM
    CATEGORY 3 FORM (2021)

        Please provide all information requested on this form in the space allocated (no additional lines and or pages of explanation).
    """

    fair_information: FairInformation = Field(..., description="Fair Information")
    category_3___new_display_method_andor_prop: Category3NewDisplayMethodandorProp = Field(
        ..., description="Category 3 – New Display Method and/or Prop"
    )
