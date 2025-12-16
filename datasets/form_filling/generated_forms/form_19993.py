from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ClientDetails(BaseModel):
    """Client personal, contact, and physical details"""

    date: str = Field(..., description="Date this form is completed")  # YYYY-MM-DD format

    disability: str = Field(
        ...,
        description=(
            "Description of the client's disability .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name: str = Field(
        ...,
        description=(
            'Full name of the client .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    grading: str = Field(
        ...,
        description=(
            'Player grading or classification .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street address, first line .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    weight: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Client's weight (specify units if needed)"
    )

    address_second_line: str = Field(
        default="",
        description=(
            "Additional address information, second line .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    height: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Client's height (specify units if needed)"
    )

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    shoe_size: str = Field(
        ...,
        description=(
            'Client\'s shoe size .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    fax_cell: str = Field(
        default="",
        description=(
            "Fax number or mobile/cell phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    t_shirt_size: str = Field(
        ...,
        description=(
            'Client\'s T-shirt size .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            'Email address for contact .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class DeliveryDetails(BaseModel):
    """Delivery address and required delivery date"""

    delivery_details_line_1: str = Field(
        ...,
        description=(
            "Delivery address or instructions, first line .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    delivery_details_line_2: str = Field(
        default="",
        description=(
            "Delivery address or instructions, second line .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    delivery_details_line_3: str = Field(
        default="",
        description=(
            "Delivery address or instructions, third line .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    required_by: str = Field(
        default="", description="Date by which delivery is required"
    )  # YYYY-MM-DD format


class AdditionalNotes(BaseModel):
    """Extra information or special instructions"""

    additional_notes_line_1: str = Field(
        default="",
        description=(
            "Additional notes or special requirements, first line .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_notes_line_2: str = Field(
        default="",
        description=(
            "Additional notes or special requirements, second line .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_notes_line_3: str = Field(
        default="",
        description=(
            "Additional notes or special requirements, third line .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RhinoScriptFormOffensiveHighPointsuitableFor1535Player90900(BaseModel):
    """
        Rhino Script Form
    Offensive - High Point (suitable for 1.5-3.5 player)         90900

        To Order Fill in the frame dimensions and features required. For variations describe in detail on a separate page. If you have any further questions contact us at the address at the bottom of the page.
    """

    client_details: ClientDetails = Field(..., description="Client Details")
    delivery_details: DeliveryDetails = Field(..., description="Delivery Details")
    additional_notes: AdditionalNotes = Field(..., description="Additional Notes")
