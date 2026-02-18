from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class BuyerDetails(BaseModel):
    """Contact information for the buyer"""

    name: str = Field(
        ...,
        description=(
            'Full name of the prospective buyer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            "Email address for property updates and communication .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PropertyPreferences(BaseModel):
    """Details of the type of property the buyer is looking for"""

    suburbs: str = Field(
        ...,
        description=(
            "Preferred suburbs or areas to search in .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    property_type: str = Field(
        ...,
        description=(
            "Type of property (e.g. house, apartment, townhouse) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    number_of_bedrooms: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Preferred number of bedrooms"
    )

    number_of_bathrooms: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Preferred number of bathrooms"
    )

    preferred_land_size: str = Field(
        default="",
        description=(
            "Preferred land size (include units, e.g. m², hectares) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    price_range_from: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Minimum price in your preferred price range"
    )

    price_range_to: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Maximum price in your preferred price range"
    )

    other_requirements_line_1: str = Field(
        default="",
        description=(
            "Additional property requirements or preferences (line 1) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_requirements_line_2: str = Field(
        default="",
        description=(
            "Additional property requirements or preferences (line 2) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_requirements_line_3: str = Field(
        default="",
        description=(
            "Additional property requirements or preferences (line 3) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ConsentandSignature(BaseModel):
    """Agreement to privacy terms and confirmation by signature"""

    signed: str = Field(
        ...,
        description=(
            "Signature of the person providing the information .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_day: Union[float, Literal["N/A", ""]] = Field(..., description="Day of signing")

    date_month: Union[float, Literal["N/A", ""]] = Field(..., description="Month of signing")

    date_year: Union[float, Literal["N/A", ""]] = Field(..., description="Year of signing")


class LetUsHelpYouFindYourNewHome(BaseModel):
    """
    Let us help you find your new home

    Let us help you find your new home
    """

    buyer_details: BuyerDetails = Field(..., description="Buyer Details")
    property_preferences: PropertyPreferences = Field(..., description="Property Preferences")
    consent_and_signature: ConsentandSignature = Field(..., description="Consent and Signature")
