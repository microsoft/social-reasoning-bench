from pydantic import BaseModel, ConfigDict, Field


class OlivioGrandeRgbwUniversalMountOrderForm(BaseModel):
    """Olivio Grande RGBW Universal Mount

    Customers or sales staff use this form to specify and order an Olivio Grande RGBW Universal Mount
    lighting fixture (and optional pole) by selecting optics, mounting, finish, voltage, quantity, and
    any factory modifications. Selux sales/order processing and factory/production teams review the
    selections, confirm approvals/compliance needs, and decide what configuration will be manufactured
    and shipped for the project.
    """

    model_config = ConfigDict(extra="forbid")

    header_date: str = Field(
        ...,
        description='Form date (YYYY-MM-DD).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    fixture_order_code_segment_1: str = Field(
        ...,
        description='Fixture code segment 1 (after OLGR).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    fixture_order_code_segment_2: str = Field(
        ...,
        description='Fixture code segment 2.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    fixture_order_code_segment_4: str = Field(
        ...,
        description='Fixture code segment 4.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    pole_order_code_options: str = Field(
        ...,
        description='Pole options code segment.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    product_modifications: str = Field(
        ...,
        description='Factory modification requirements.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    approvals_box: str = Field(
        ...,
        description='Approvals notes/markings in box.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
