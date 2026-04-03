from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CertificateType(BaseModel):
    """Type of subdivision certificate being applied for"""

    torrens_title: BooleanLike = Field(
        ..., description="Tick if applying for a Torrens Title subdivision certificate"
    )

    boundary_adjustment: BooleanLike = Field(
        ..., description="Tick if applying for a Boundary Adjustment subdivision certificate"
    )

    consolidation: BooleanLike = Field(
        ..., description="Tick if applying for a Consolidation subdivision certificate"
    )

    road_easement_dedication: BooleanLike = Field(
        ...,
        description="Tick if applying for a Road and Easement Dedication subdivision certificate",
    )

    strata: BooleanLike = Field(
        ..., description="Tick if applying for a Strata subdivision certificate"
    )

    stratum: BooleanLike = Field(
        ..., description="Tick if applying for a Stratum subdivision certificate"
    )


class Part1SiteDetails(BaseModel):
    """Location and legal description of the property and subdivision details"""

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
            'Street name of the property .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    suburb: str = Field(
        ...,
        description=(
            'Suburb of the property .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    postcode: str = Field(..., description="Postcode of the property")

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
            "Details of any new lots to be created by the subdivision, if applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class NorthernBeachesCouncilSubdivisionCertificateApplication2122(BaseModel):
    """
        northern
    beaches
    council

    Subdivision Certificate
    Application 21/22

        For Council to provide services to the community
    """

    certificate_type: CertificateType = Field(..., description="Certificate Type")
    part_1_site_details: Part1SiteDetails = Field(..., description="Part 1: Site Details")
