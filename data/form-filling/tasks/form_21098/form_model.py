from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class JobContactInformation(BaseModel):
    """Basic job details and contact information for the work order"""

    date: str = Field(
        ..., description="Date this work order form is completed"
    )  # YYYY-MM-DD format

    work_order_number: str = Field(
        ...,
        description=(
            "Internal work order or job number for this request .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    to: str = Field(
        ...,
        description=(
            "Name or department this form is being sent to .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    from_: str = Field(
        ...,
        description=(
            "Name of the person or company sending this form .If you cannot fill this, "
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

    fax: str = Field(
        default="",
        description=(
            'Fax number for contact, if applicable .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Contact email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class VehicleInformation(BaseModel):
    """Details about the vehicle for the recycled parts request"""

    year: Union[float, Literal["N/A", ""]] = Field(..., description="Model year of the vehicle")

    make: str = Field(
        ...,
        description=(
            "Vehicle manufacturer (e.g., Ford, Chevrolet, Toyota) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    model: str = Field(
        ...,
        description=(
            "Vehicle model (e.g., F-150, Silverado, Camry) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CutInstructions(BaseModel):
    """Detailed instructions for the body cut"""

    please_use_this_area_to_explain_your_cut_instructions_in_detail: str = Field(
        ...,
        description=(
            "Detailed description of the required body cut, including measurements and "
            'specific instructions .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class WaterlooAutoPartsSalvageCenter(BaseModel):
    """
        Waterloo
    Auto Parts
    SALVAGE CENTER

        After downloading this form and filling it out, go to Tools > Comment. Then click on the draw free form tool in the tool bar, and draw on an image where the body cut should be. Please use this area to explain your cut instructions in detail.
    """

    job__contact_information: JobContactInformation = Field(
        ..., description="Job & Contact Information"
    )
    vehicle_information: VehicleInformation = Field(..., description="Vehicle Information")
    cut_instructions: CutInstructions = Field(..., description="Cut Instructions")
