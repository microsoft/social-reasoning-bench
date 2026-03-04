from typing import List, Literal, Optional, Union

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

    which_certificate_are_you_applying_for_torrens_title: BooleanLike = Field(
        ...,
        description=(
            "Select if the subdivision certificate application is for a Torrens Title subdivision"
        ),
    )

    which_certificate_are_you_applying_for_boundary_adjustment: BooleanLike = Field(
        ...,
        description="Select if the subdivision certificate application is for a Boundary Adjustment",
    )

    which_certificate_are_you_applying_for_consolidation: BooleanLike = Field(
        ..., description="Select if the subdivision certificate application is for a Consolidation"
    )

    which_certificate_are_you_applying_for_road_easement_dedication: BooleanLike = Field(
        ...,
        description=(
            "Select if the subdivision certificate application is for a Road & Easement Dedication"
        ),
    )

    which_certificate_are_you_applying_for_strata: BooleanLike = Field(
        ...,
        description="Select if the subdivision certificate application is for a Strata subdivision",
    )

    which_certificate_are_you_applying_for_stratum: BooleanLike = Field(
        ...,
        description="Select if the subdivision certificate application is for a Stratum subdivision",
    )


class Part1SiteDetails(BaseModel):
    """Location and legal description of the property"""

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
            'Suburb or town of the property .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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


class SubdivisionDetails(BaseModel):
    """Description of the subdivision certificate and proposed lots"""

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
    subdivision_details: SubdivisionDetails = Field(..., description="Subdivision Details")
