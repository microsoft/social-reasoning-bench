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

    date: str = Field(..., description="Date the order form is completed")  # YYYY-MM-DD format

    customer: str = Field(
        ...,
        description=(
            'Customer or company name .If you cannot fill this, write "N/A". If this '
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
        ...,
        description=(
            'Fixture or order type designation .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    qty: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Quantity of fixtures or poles ordered"
    )


class OrderCodes(BaseModel):
    """Fixture and pole order coding"""

    fixture_order_code_olgr: str = Field(
        ...,
        description=(
            "Complete OLGR fixture order code including all option segments .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    pole_order_code: str = Field(
        default="",
        description=(
            "Complete pole order code including all option segments, if poles are ordered "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class FixtureConfiguration(BaseModel):
    """Technical configuration and options for the Olivio Grande RGBW fixture"""

    optics_n13_narrow_13_beam: BooleanLike = Field(
        default="", description="Select if N13 narrow 13° beam optic is required"
    )

    optics_m50_medium_50_beam: BooleanLike = Field(
        default="", description="Select if M50 medium 50° beam optic is required"
    )

    optics_w80_wide_80_beam: BooleanLike = Field(
        default="", description="Select if W80 wide 80° beam optic is required"
    )

    mounting_u_universal_surface_mount: BooleanLike = Field(
        default="", description="Select if U universal surface mount is required"
    )

    mounting_t1_single_pole_top: BooleanLike = Field(
        default="", description="Select if T1 single pole top mounting is required"
    )

    light_engine_l50_50w_max: BooleanLike = Field(
        default="", description="Select if L50 50W max light engine is required"
    )

    cct_rgbw_red_green_blue_white: BooleanLike = Field(
        default="",
        description="Select if RGBW (red, green, blue, white) color configuration is required",
    )

    finish_wh_white: BooleanLike = Field(default="", description="Select WH white finish")

    finish_bk_black: BooleanLike = Field(default="", description="Select BK black finish")

    finish_bl_semi_matte_black: BooleanLike = Field(
        default="", description="Select BL semi-matte black finish"
    )

    finish_bz_bronze: BooleanLike = Field(default="", description="Select BZ bronze finish")

    finish_sv_silver: BooleanLike = Field(default="", description="Select SV silver finish")

    finish_sp_specify_premium_color: BooleanLike = Field(
        default="", description="Select SP to specify a custom premium color finish"
    )

    voltage_unv_120v_277v: BooleanLike = Field(
        default="", description="Select UNV universal voltage (120V-277V)"
    )


class ProductModifications(BaseModel):
    """Requested product modifications for factory review"""

    product_modifications_line_1: str = Field(
        default="",
        description=(
            "First line for listing requested product modifications .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    product_modifications_line_2: str = Field(
        default="",
        description=(
            "Second line for listing requested product modifications .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    product_modifications_line_3: str = Field(
        default="",
        description=(
            "Third line for listing requested product modifications .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Approvals(BaseModel):
    """Approval sign-off and date"""

    approvals: str = Field(
        default="",
        description=(
            "Name, title, or indication of person or department providing approval .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_approvals_section: str = Field(
        default="", description="Date of approval"
    )  # YYYY-MM-DD format


class OlivioGrandeRgbwUniversalMount(BaseModel):
    """
        Olivio Grande RGBW
    Universal Mount

        ''
    """

    project_information: ProjectInformation = Field(..., description="Project Information")
    order_codes: OrderCodes = Field(..., description="Order Codes")
    fixture_configuration: FixtureConfiguration = Field(..., description="Fixture Configuration")
    product_modifications: ProductModifications = Field(..., description="Product Modifications")
    approvals: Approvals = Field(..., description="Approvals")
