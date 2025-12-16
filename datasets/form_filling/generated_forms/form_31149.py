from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantPropertyInformation(BaseModel):
    """Owner details, address, ownership, legal description, and zoning of the property"""

    property_owner_last: str = Field(
        ...,
        description=(
            "Last name of the primary property owner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_first: str = Field(
        ...,
        description=(
            "First name of the primary property owner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    property_owner_middle_int: str = Field(
        default="",
        description=(
            "Middle initial of the primary property owner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    co_owner_last: str = Field(
        default="",
        description=(
            'Last name of the co-owner, if any .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    co_owner_first: str = Field(
        default="",
        description=(
            'First name of the co-owner, if any .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    co_owner_middle_int: str = Field(
        default="",
        description=(
            "Middle initial of the co-owner, if any .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_street: str = Field(
        ...,
        description=(
            'Street address of the property owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_city: str = Field(
        ...,
        description=(
            'City for the property owner\'s address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_zip: str = Field(..., description="ZIP code for the property owner's address")

    address_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the property owner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    ownership_deed_holder: BooleanLike = Field(
        ..., description="Indicate if ownership is held by deed"
    )

    ownership_land_contract: BooleanLike = Field(
        ..., description="Indicate if ownership is held by land contract"
    )

    legal_description_line_1: str = Field(
        ...,
        description=(
            "First line of the legal description of the property being appealed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    legal_description_line_2: str = Field(
        default="",
        description=(
            "Second line of the legal description of the property being appealed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    legal_description_line_3: str = Field(
        default="",
        description=(
            "Third line of the legal description of the property being appealed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    zoning_of_property: str = Field(
        ...,
        description=(
            "Current zoning classification of the property .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    parcel_number: str = Field(
        ...,
        description=(
            "Parcel identification number of the property .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class SectionAInterpretation(BaseModel):
    """Request for interpretation of the zoning ordinance and map"""

    article: str = Field(
        default="",
        description=(
            "Article number of the Zoning Ordinance for which interpretation is requested "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    section: str = Field(
        default="",
        description=(
            "Section number of the Zoning Ordinance for which interpretation is requested "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    interpretation_reason_line_1: str = Field(
        ...,
        description=(
            "First line explaining the reason an interpretation is requested .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    interpretation_reason_line_2: str = Field(
        default="",
        description=(
            "Second line explaining the reason an interpretation is requested .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    interpretation_reason_line_3: str = Field(
        default="",
        description=(
            "Third line explaining the reason an interpretation is requested .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    interpretation_reason_line_4: str = Field(
        default="",
        description=(
            "Fourth line explaining the reason an interpretation is requested .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    interpretation_reason_line_5: str = Field(
        default="",
        description=(
            "Fifth line explaining the reason an interpretation is requested .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    interpretation_reason_line_6: str = Field(
        default="",
        description=(
            "Sixth line explaining the reason an interpretation is requested .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class SectionBSpecialException(BaseModel):
    """Request for special exception and description of proposed use"""

    special_exception_description_line_1: str = Field(
        ...,
        description=(
            "First line describing the requested special exception and proposed use of the "
            'property .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    special_exception_description_line_2: str = Field(
        default="",
        description=(
            "Second line describing the requested special exception and proposed use of the "
            'property .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    special_exception_description_line_3: str = Field(
        default="",
        description=(
            "Third line describing the requested special exception and proposed use of the "
            'property .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    special_exception_description_line_4: str = Field(
        default="",
        description=(
            "Fourth line describing the requested special exception and proposed use of the "
            'property .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    special_exception_description_line_5: str = Field(
        default="",
        description=(
            "Fifth line describing the requested special exception and proposed use of the "
            'property .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    special_exception_description_line_6: str = Field(
        default="",
        description=(
            "Sixth line describing the requested special exception and proposed use of the "
            'property .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class OrchardLakeZoningBoardAppealsSpecialExceptionApp(BaseModel):
    """
        CITY OF ORCHARD LAKE VILLAGE
    ZONING BOARD OF APPEALS APPLICATION
    FOR INTERPRETATION & SPECIAL EXCEPTION ONLY

        I (We) the undersigned do hereby make application to the Zoning Board of Appeals of the City of Orchard Lake Village for a hearing on the following described matter:
    """

    applicant__property_information: ApplicantPropertyInformation = Field(
        ..., description="Applicant & Property Information"
    )
    section_a___interpretation: SectionAInterpretation = Field(
        ..., description="Section A - Interpretation"
    )
    section_b___special_exception: SectionBSpecialException = Field(
        ..., description="Section B - Special Exception"
    )
