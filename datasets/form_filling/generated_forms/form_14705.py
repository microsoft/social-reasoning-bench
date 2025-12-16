from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CompanyContactInformation(BaseModel):
    """Basic company and contact details"""

    company_name: str = Field(
        ...,
        description=(
            'Legal or common name of your company .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    your_name: str = Field(
        ...,
        description=(
            'Your full name .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    install_city_state: str = Field(
        ...,
        description=(
            "City and state where the CASI-IBOD will be installed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    todays_date: str = Field(
        ..., description="Date this questionnaire is completed"
    )  # YYYY-MM-DD format

    email: str = Field(
        ...,
        description=(
            'Contact email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class BoxCharacteristicsHandlingRequirements(BaseModel):
    """Box sizes, weights, handling rate, and packing details"""

    at_what_rate_do_boxes_need_to_be_cut_open: str = Field(
        ...,
        description=(
            "Required throughput rate for cutting boxes (e.g., boxes per minute or hour) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    smallest_box_size_l_x_w_x_h: str = Field(
        ...,
        description=(
            "Dimensions of the smallest box (length x width x height) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    largest_box_size_l_x_w_x_h: str = Field(
        ...,
        description=(
            "Dimensions of the largest box (length x width x height) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    growth_expectations_affecting_future_rate_requirements: str = Field(
        default="",
        description=(
            "Describe anticipated growth that could change required processing rates .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    helpful_to_see_product_inside_box: BooleanLike = Field(
        default="",
        description="Indicate if you will include photos showing the product inside the box",
    )

    helpful_to_see_product_yes: BooleanLike = Field(
        default="", description="Check if you will include photos of the product inside the box"
    )

    helpful_to_see_product_no: BooleanLike = Field(
        default="", description="Check if you will not include photos of the product inside the box"
    )

    how_is_product_packed_within_box: Literal[
        "VERY TIGHTLY", "LOOSE PRODUCT", "WRAPPED IN PLASTIC", "OTHER", "N/A", ""
    ] = Field(default="", description="Select how the product is typically packed inside the box")

    packed_very_tightly: BooleanLike = Field(
        default="", description="Check if product is usually packed very tightly"
    )

    packed_loose_product: BooleanLike = Field(
        default="", description="Check if product is usually loose inside the box"
    )

    packed_wrapped_in_plastic: BooleanLike = Field(
        default="", description="Check if product is usually wrapped in plastic"
    )

    packed_other: str = Field(
        default="",
        description=(
            "Describe any other packing method used .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    minimum_box_weight: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Weight of the lightest box (include units, e.g., lbs)"
    )

    maximum_box_weight: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Weight of the heaviest box (include units, e.g., lbs)"
    )

    percentage_of_boxes_over_50_lbs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Approximate percentage of boxes that weigh more than 50 lbs"
    )

    types_of_cut_needed: Literal[
        "4-SIDED TOP CUT", "3-SIDED TOP CUT", "TAPE CUT", "WINDOW CUT", "N/A", ""
    ] = Field(default="", description="Select all cut types required for your boxes")

    cut_4_sided_top: BooleanLike = Field(
        default="", description="Check if a 4-sided top cut is needed"
    )

    cut_3_sided_top: BooleanLike = Field(
        default="", description="Check if a 3-sided top cut is needed"
    )

    cut_tape: BooleanLike = Field(default="", description="Check if tape cuts are needed")

    cut_window: BooleanLike = Field(default="", description="Check if window cuts are needed")

    boxes_will_be: Literal[
        "MANUALLY PLACED ON CASI-IBOD INFEED CONVEYOR",
        "ROBOTICALLY DEPALLETIZED, THEN PLACED ON CASI-IBOD INFEED CONVEYOR",
        "CONVEYED TO CASI-IBOD FROM YOUR CONVEYOR",
        "N/A",
        "",
    ] = Field(default="", description="Select how boxes will be delivered to the CASI-IBOD infeed")

    boxes_manually_placed_on_infeed: BooleanLike = Field(
        default="", description="Check if boxes will be manually placed on the infeed conveyor"
    )

    boxes_robotically_depalletized: BooleanLike = Field(
        default="", description="Check if boxes will be robotically depalletized before infeed"
    )

    boxes_conveyed_from_your_conveyor: BooleanLike = Field(
        default="", description="Check if boxes will arrive via your existing conveyor"
    )

    will_boxes_include: Literal["STRAPPING", "STAPLES", "N/A", ""] = Field(
        default="", description="Indicate if boxes include strapping or staples"
    )

    boxes_include_strapping: BooleanLike = Field(
        default="", description="Check if boxes include strapping"
    )

    boxes_include_staples: BooleanLike = Field(
        default="", description="Check if boxes include staples"
    )

    product_type_within_boxes: str = Field(
        default="",
        description=(
            "Describe the types of products contained in the boxes .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PostCutProcessInstallation(BaseModel):
    """What happens after cutting and installation/site details"""

    what_happens_to_cut_boxes_after_leaving_casi_ibod: str = Field(
        default="",
        description=(
            "Explain downstream handling or processes for boxes after cutting .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    can_drawing_be_provided_for_installation_area: BooleanLike = Field(
        default="", description="Indicate if you can provide a CAD drawing of the installation area"
    )

    drawing_can_be_provided_yes: BooleanLike = Field(
        default="", description="Check if a CAD drawing can be provided"
    )

    drawing_can_be_provided_no: BooleanLike = Field(
        default="", description="Check if a CAD drawing cannot be provided"
    )

    what_type_of_corrugation: Literal[
        "SINGLE-WALL",
        "DOUBLE-WALL",
        "TRIPLE-WALL",
        "MOIST CORRUGATED",
        "FROZEN CORRUGATED",
        "N/A",
        "",
    ] = Field(default="", description="Select all corrugation types that must be cut")

    corrugation_single_wall: BooleanLike = Field(
        default="", description="Check if single-wall corrugation must be cut"
    )

    corrugation_double_wall: BooleanLike = Field(
        default="", description="Check if double-wall corrugation must be cut"
    )

    corrugation_triple_wall: BooleanLike = Field(
        default="", description="Check if triple-wall corrugation must be cut"
    )

    corrugation_moist: BooleanLike = Field(
        default="", description="Check if moist corrugated material must be cut"
    )

    corrugation_frozen: BooleanLike = Field(
        default="", description="Check if frozen corrugated material must be cut"
    )

    box_styles: Literal[
        "TYPICAL RSC WITH TAPED SEAMS",
        "TRAY WITH GLUED LID",
        "FOLD-OVER LID STYLE",
        "OTHER",
        "N/A",
        "",
    ] = Field(default="", description="Select all box styles used")

    box_style_typical_rsc_with_taped_seams: BooleanLike = Field(
        default="", description="Check if you use typical RSC boxes with taped seams"
    )

    box_style_tray_with_glued_lid: BooleanLike = Field(
        default="", description="Check if you use tray boxes with glued lids"
    )

    box_style_fold_over_lid_style: BooleanLike = Field(
        default="", description="Check if you use fold-over lid style boxes"
    )

    box_style_other: str = Field(
        default="",
        description=(
            'Describe any other box styles used .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class CurrentOperationsReceivingProcess(BaseModel):
    """Current labor allocation and how goods are received and sorted"""

    employees_unloading_trucks: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees currently unloading trucks"
    )

    employees_opening_boxes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees currently opening boxes"
    )

    employees_staging_goods_to_put_away: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees currently staging goods to put away"
    )

    employees_other: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of employees devoted to other related tasks"
    )

    goods_received: Literal["ON PALLETS IN TRUCKS", "FLOOR-LOADED IN TRUCKS", "BOTH", "N/A", ""] = (
        Field(default="", description="Indicate how goods are typically received")
    )

    goods_received_on_pallets_in_trucks: BooleanLike = Field(
        default="", description="Check if goods are received on pallets in trucks"
    )

    goods_received_floor_loaded_in_trucks: BooleanLike = Field(
        default="", description="Check if goods are received floor-loaded in trucks"
    )

    goods_received_both: BooleanLike = Field(
        default="", description="Check if goods are received both on pallets and floor-loaded"
    )

    how_sort_product_after_boxes_cut_open: str = Field(
        default="",
        description=(
            "Describe your intended product sorting process after boxes are opened .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ControlsResponsibilityAdditionalComments(BaseModel):
    """Controls ownership and any other notes"""

    who_responsible_for_controls_functionality: Literal["CASI", "YOU (THE CUSTOMER)", "N/A", ""] = (
        Field(
            default="", description="Select who will manage controls functionality for order flow"
        )
    )

    controls_responsible_casi: BooleanLike = Field(
        default="", description="Check if CASI will be responsible for controls functionality"
    )

    controls_responsible_customer: BooleanLike = Field(
        default="",
        description="Check if you (the customer) will be responsible for controls functionality",
    )

    other_comments: str = Field(
        default="",
        description=(
            "Provide any additional information or comments .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CasiibodQuestionnaire(BaseModel):
    """
    CASi-IBOD Questionnaire

    ''
    """

    company__contact_information: CompanyContactInformation = Field(
        ..., description="Company & Contact Information"
    )
    box_characteristics__handling_requirements: BoxCharacteristicsHandlingRequirements = Field(
        ..., description="Box Characteristics & Handling Requirements"
    )
    post_cut_process__installation: PostCutProcessInstallation = Field(
        ..., description="Post-Cut Process & Installation"
    )
    current_operations__receiving_process: CurrentOperationsReceivingProcess = Field(
        ..., description="Current Operations & Receiving Process"
    )
    controls_responsibility__additional_comments: ControlsResponsibilityAdditionalComments = Field(
        ..., description="Controls Responsibility & Additional Comments"
    )
