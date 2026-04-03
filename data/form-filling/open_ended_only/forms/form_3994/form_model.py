from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CertificateType(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Select the type of subdivision certificate you are applying for."""

    which_certificate_are_you_applying_for_torrens_title: BooleanLike = Field(
        ...,
        description="Select if you are applying for a Torrens Title certificate"
    )

    which_certificate_are_you_applying_for_boundary_adjustment: BooleanLike = Field(
        ...,
        description="Select if you are applying for a Boundary Adjustment certificate"
    )

    which_certificate_are_you_applying_for_consolidation: BooleanLike = Field(
        ...,
        description="Select if you are applying for a Consolidation certificate"
    )

    which_certificate_are_you_applying_for_road_easement_dedication: BooleanLike = Field(
        ...,
        description="Select if you are applying for a Road & Easement Dedication certificate"
    )

    which_certificate_are_you_applying_for_strata: BooleanLike = Field(
        ...,
        description="Select if you are applying for a Strata certificate"
    )

    which_certificate_are_you_applying_for_stratum: BooleanLike = Field(
        ...,
        description="Select if you are applying for a Stratum certificate"
    )


class Part1SiteDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details to identify the property and describe the subdivision certificate."""

    unit_house_number: str = Field(
        ...,
        description=(
            "Unit or house number of the property .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    street: str = Field(
        ...,
        description=(
            "Street name of the property .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    suburb: str = Field(
        ...,
        description=(
            "Suburb where the property is located .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    postcode: str = Field(
        ...,
        description=(
            "Postcode of the property .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    lot_number: str = Field(
        ...,
        description=(
            "Legal lot number of the property .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    section: str = Field(
        ...,
        description=(
            "Section number (if applicable) .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    dp_sp: str = Field(
        ...,
        description=(
            "Deposited Plan (DP) or Strata Plan (SP) number .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    description_of_subdivision_certificate: str = Field(
        ...,
        description=(
            "Brief description of everything you want approved by the Council .If you "
            "cannot fill this, write \"N/A\". If this field should not be filled by you "
            "(for example, it belongs to another person or office), leave it blank (empty "
            "string \"\")."
        )
    )

    lots_to_be_created: str = Field(
        ...,
        description=(
            "Number or description of lots to be created (if applicable) .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )


class NorthernBeachesCouncilSubdivisionCertificateApplication2122(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    northern beaches council

Subdivision Certificate Application 21/22

    Purpose of collection: For Council to provide services to the community
    This form is used to apply for a Subdivision Certificate with Northern Beaches Council. Applicants must provide site details and describe the subdivision or related works they seek approval for. The information collected will be used by Council staff to process the application and provide the requested services. If personal information is not supplied, Council may be unable to provide the services sought.
    """

    certificate_type: CertificateType = Field(
        ...,
        description="Certificate Type"
    )
    part_1_site_details: Part1SiteDetails = Field(
        ...,
        description="Part 1: Site Details"
    )