from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectInformation(BaseModel):
    """General project and customer details"""

    date: str = Field(..., description="Date this form is completed")  # YYYY-MM-DD format

    customer: str = Field(
        ...,
        description=(
            'Customer name or company .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    project: str = Field(
        ...,
        description=(
            'Project name or identifier .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    type: str = Field(
        default="",
        description=(
            "Type or description of the order or project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    qty: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Quantity of fixtures or items requested"
    )


class FixtureOrderCode(BaseModel):
    """Configuration for the Olivio Grande RGBW fixture"""

    fixture_order_code_position_1: Literal["OLGR", "N/A", ""] = Field(
        ..., description="First segment of fixture order code (series)"
    )

    fixture_order_code_position_2: Literal["N13", "M50", "W80", "N/A", ""] = Field(
        ...,
        description="Second segment of fixture order code (optics: narrow, medium, or wide beam)",
    )

    fixture_order_code_position_3: Literal["U", "T1", "N/A", ""] = Field(
        ..., description="Third segment of fixture order code (mounting type)"
    )

    fixture_order_code_position_4: Literal["L50", "N/A", ""] = Field(
        ..., description="Fourth segment of fixture order code (light engine / wattage)"
    )

    fixture_order_code_position_5: Literal["RGBW", "N/A", ""] = Field(
        ..., description="Fifth segment of fixture order code (CCT / color configuration)"
    )


class PoleOrderCode(BaseModel):
    """Configuration for the pole (series, height, finish, options)"""

    pole_order_code_series: str = Field(
        default="",
        description=(
            "Pole series identifier (first segment of pole order code) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    pole_order_code_height: str = Field(
        default="",
        description=(
            "Pole height (second segment of pole order code) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    pole_order_code_finish: Literal["WH", "BK", "BL", "BZ", "SV", "SP", "N/A", ""] = Field(
        default="", description="Pole finish (third segment of pole order code)"
    )

    pole_order_code_options: str = Field(
        default="",
        description=(
            "Additional pole options (fourth segment of pole order code) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ProductModifications(BaseModel):
    """Requested product modifications for factory review"""

    product_modifications_line_1: str = Field(
        default="",
        description=(
            "First line of requested product modifications .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    product_modifications_line_2: str = Field(
        default="",
        description=(
            "Second line of requested product modifications .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    product_modifications_line_3: str = Field(
        default="",
        description=(
            "Third line of requested product modifications .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    product_modifications_line_4: str = Field(
        default="",
        description=(
            "Fourth line of requested product modifications .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Approvals(BaseModel):
    """Approval checkbox and date"""

    approvals: BooleanLike = Field(
        default="",
        description=(
            "Indicates whether the product modifications or order have been approved "
            "(checkbox in blank box)"
        ),
    )

    approvals_date: str = Field(default="", description="Date of approval")  # YYYY-MM-DD format


class OlivioGrandeRgbwUniversalMount(BaseModel):
    """
        Olivio Grande RGBW
    Universal Mount

        ''
    """

    project_information: ProjectInformation = Field(..., description="Project Information")
    fixture_order_code: FixtureOrderCode = Field(..., description="Fixture Order Code")
    pole_order_code: PoleOrderCode = Field(..., description="Pole Order Code")
    product_modifications: ProductModifications = Field(..., description="Product Modifications")
    approvals: Approvals = Field(..., description="Approvals")
