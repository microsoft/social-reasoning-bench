from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicationDetails(BaseModel):
    """Reference numbers and type of subdivision certificate being applied for"""

    application_no: str = Field(
        ...,
        description=(
            "Council-issued subdivision application number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    receipt_no: str = Field(
        default="",
        description=(
            "Payment receipt number for this application .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    torrens_title: BooleanLike = Field(
        ..., description="Select if applying for a Torrens Title subdivision certificate"
    )

    boundary_adjustment: BooleanLike = Field(
        ..., description="Select if the application is for a boundary adjustment"
    )

    consolidation: BooleanLike = Field(
        ..., description="Select if the application is for consolidation of lots"
    )

    road_easement_dedication: BooleanLike = Field(
        ..., description="Select if the application is for road and/or easement dedication"
    )

    strata: BooleanLike = Field(
        ..., description="Select if applying for a Strata subdivision certificate"
    )

    stratum: BooleanLike = Field(
        ..., description="Select if applying for a Stratum subdivision certificate"
    )


class Part1SiteDetails(BaseModel):
    """Location of property and description of the subdivision certificate"""

    unit_house_number: str = Field(
        ...,
        description=(
            'Unit or house number of the property .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    street: str = Field(
        ...,
        description=(
            'Street name of the property address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    suburb: str = Field(
        ...,
        description=(
            'Suburb of the property address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    postcode: str = Field(..., description="Postcode of the property address")

    lot_number: str = Field(
        ...,
        description=(
            "Lot number from the legal property description .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    section: str = Field(
        default="",
        description=(
            "Section number from the legal property description, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    dp_sp: str = Field(
        ...,
        description=(
            "Deposited Plan (DP) or Strata Plan (SP) number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    description_of_subdivision_certificate: str = Field(
        ...,
        description=(
            "Brief description of everything to be approved, including use, subdivision, "
            'demolition, etc. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    lots_to_be_created_if_applicable: str = Field(
        default="",
        description=(
            "Number or identifiers of lots to be created, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class NorthernBeachesCouncilSubdivisionCertificateApplication2122(BaseModel):
    """
        northern beaches council
    Subdivision Certificate Application 21/22

        ''
    """

    application_details: ApplicationDetails = Field(..., description="Application Details")
    part_1_site_details: Part1SiteDetails = Field(..., description="Part 1: Site Details")
