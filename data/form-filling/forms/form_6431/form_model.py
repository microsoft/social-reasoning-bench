from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectInformation(BaseModel):
    """Basic project and customer details"""

    date: str = Field(..., description="Date the order form is completed")  # YYYY-MM-DD format

    customer: str = Field(
        ...,
        description=(
            "Customer name or company placing the order .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
            "Type or category of the order or project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    qty: Union[float, Literal["N/A", ""]] = Field(..., description="Quantity of fixtures ordered")


class FixtureOrderCode(BaseModel):
    """Configuration of the Olivio Grande RGBW fixture"""

    fixture_order_code_segment_1: Literal["OLGR", "N/A", ""] = Field(
        ..., description="First segment of fixture order code (series)"
    )

    fixture_order_code_segment_2: Literal["OLGR", "N/A", ""] = Field(
        ..., description="Second segment of fixture order code (series OLGR Olivio Grande RGBW)"
    )

    fixture_order_code_segment_3: Literal["N13", "M50", "W80", "N/A", ""] = Field(
        ..., description="Third segment of fixture order code (optics selection)"
    )

    fixture_order_code_segment_4: Literal["U", "T1", "N/A", ""] = Field(
        ..., description="Fourth segment of fixture order code (mounting type)"
    )

    fixture_order_code_segment_5: Literal["L50", "N/A", ""] = Field(
        ..., description="Fifth segment of fixture order code (light engine)"
    )

    fixture_order_code_segment_6: Literal["RGBW", "N/A", ""] = Field(
        ..., description="Sixth segment of fixture order code (CCT / color configuration)"
    )

    fixture_order_code_segment_7: Literal["WH", "BK", "BL", "BZ", "SV", "SP", "N/A", ""] = Field(
        ..., description="Seventh segment of fixture order code (finish color)"
    )

    optics: Literal["N13", "M50", "W80", "N/A", ""] = Field(
        ..., description="Optical distribution for the fixture"
    )

    mounting: Literal["U", "T1", "N/A", ""] = Field(
        ..., description="Mounting configuration for the fixture"
    )

    light_engine: Literal["L50", "N/A", ""] = Field(
        ..., description="Light engine specification for the fixture"
    )

    cct: Literal["RGBW", "N/A", ""] = Field(
        ..., description="Correlated color temperature / color configuration"
    )

    finish: Literal["WH", "BK", "BL", "BZ", "SV", "SP", "N/A", ""] = Field(
        ..., description="Fixture finish color"
    )

    voltage: Literal["UNV", "N/A", ""] = Field(..., description="Input voltage selection")


class PoleOrderCode(BaseModel):
    """Pole series, height, finish, and options"""

    pole_order_code_series: str = Field(
        default="",
        description=(
            'Series portion of the pole order code .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    pole_order_code_height: str = Field(
        default="",
        description=(
            'Height portion of the pole order code .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    pole_order_code_finish: str = Field(
        default="",
        description=(
            'Finish portion of the pole order code .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    pole_order_code_options: str = Field(
        default="",
        description=(
            "Options portion of the pole order code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProductModifications(BaseModel):
    """Requested product modifications for factory review"""

    product_modifications_line_1: str = Field(
        default="",
        description=(
            "First line of product modification requirements .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    product_modifications_line_2: str = Field(
        default="",
        description=(
            "Second line of product modification requirements .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    product_modifications_line_3: str = Field(
        default="",
        description=(
            "Third line of product modification requirements .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    product_modifications_line_4: str = Field(
        default="",
        description=(
            "Fourth line of product modification requirements .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Approvals(BaseModel):
    """Approval signatures and date"""

    approvals_line_1: str = Field(
        default="",
        description=(
            "First approval signature or initials line .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    approvals_line_2: str = Field(
        default="",
        description=(
            "Second approval signature or initials line .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    approvals_line_3: str = Field(
        default="",
        description=(
            "Third approval signature or initials line .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    approvals_line_4: str = Field(
        default="",
        description=(
            "Fourth approval signature or initials line .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    approvals_date: str = Field(
        default="", description="Date of final approval"
    )  # YYYY-MM-DD format


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
