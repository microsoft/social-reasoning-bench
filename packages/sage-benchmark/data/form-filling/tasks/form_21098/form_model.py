from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class OrderVehicleInformation(BaseModel):
    """Basic order details and vehicle identification for the recycled parts request"""

    date: str = Field(
        ..., description="Date this work order form is completed"
    )  # YYYY-MM-DD format

    work_order_number: str = Field(
        ...,
        description=(
            "Internal work order or job reference number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    to: str = Field(
        ...,
        description=(
            "Name or department the form is being sent to .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    from_: str = Field(
        ...,
        description=(
            "Name of the person or company sending the form .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    year: Union[float, Literal["N/A", ""]] = Field(..., description="Model year of the vehicle")

    make: str = Field(
        ...,
        description=(
            "Vehicle manufacturer (e.g., Ford, Chevrolet, Dodge) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    model: str = Field(
        ...,
        description=(
            "Vehicle model (e.g., F-150, Silverado, Ram 1500) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ContactInformation(BaseModel):
    """Contact details for communication regarding this work order"""

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            "Fax number for contact or document return .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            "Email address for contact or confirmation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CutInstructions(BaseModel):
    """Detailed instructions for where and how the body cut should be made"""

    please_use_this_area_to_explain_your_cut_instructions_in_detail: str = Field(
        ...,
        description=(
            "Detailed description of where and how the body cut should be made .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class WaterlooAutoPartsRecycledPartsQuadCabTruck(BaseModel):
    """
    Waterloo Auto Parts Recycled Parts: Quad Cab Truck

    After downloading this form and filling it out, go to Tools > Comment. Then click on the draw free form tool in the tool bar, and draw on an image where the body cut should be. Please use this area to explain your cut instructions in detail.
    """

    order__vehicle_information: OrderVehicleInformation = Field(
        ..., description="Order & Vehicle Information"
    )
    contact_information: ContactInformation = Field(..., description="Contact Information")
    cut_instructions: CutInstructions = Field(..., description="Cut Instructions")
