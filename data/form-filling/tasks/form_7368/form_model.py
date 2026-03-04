from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PropertyDescription(BaseModel):
    """Location and position of the proposed advertisement/sign"""

    description_of_property_on_which_advertisement_is_to_be_displayed_including_full_details_of_its_proposed_position_within_the_property: str = Field(
        ...,
        description=(
            "Describe the property and the exact proposed position of the advertisement "
            'within the property. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class DetailsofProposedSign(BaseModel):
    """Physical characteristics, materials, and illumination details of the proposed sign"""

    type_of_structure_on_which_advertisement_is_to_be_erected_ie_freestanding_wall_mounted_other: str = Field(
        ...,
        description=(
            "Specify the type of structure on which the advertisement will be erected (e.g. "
            'freestanding, wall mounted, other). .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    height: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Overall height of the proposed sign structure (include units)."
    )

    width: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Overall width of the proposed sign structure (include units)."
    )

    depth: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Overall depth or thickness of the proposed sign structure (include units).",
    )

    colours_to_be_used: str = Field(
        ...,
        description=(
            "List the colours to be used on the sign and its structure. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    height_above_ground_level_to_top_of_advertisement: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Height from ground level to the top of the advertisement (include units)."
    )

    height_above_ground_level_to_underside: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Height from ground level to the underside of the advertisement (include units).",
    )

    materials_to_be_used: str = Field(
        ...,
        description=(
            "Describe the materials to be used in the construction of the sign and its "
            'support. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    illuminated_yes: BooleanLike = Field(
        ..., description="Select if the advertisement will be illuminated."
    )

    illuminated_no: BooleanLike = Field(
        ..., description="Select if the advertisement will not be illuminated."
    )

    illumination_type_steady: BooleanLike = Field(
        default="", description="Tick if the illumination will be steady."
    )

    illumination_type_moving: BooleanLike = Field(
        default="", description="Tick if the illumination will be moving."
    )

    illumination_type_flashing: BooleanLike = Field(
        default="", description="Tick if the illumination will be flashing."
    )

    illumination_type_alternating: BooleanLike = Field(
        default="", description="Tick if the illumination will be alternating."
    )

    illumination_type_digital: BooleanLike = Field(
        default="", description="Tick if the illumination will be digital."
    )

    illumination_type_animated: BooleanLike = Field(
        default="", description="Tick if the illumination will be animated."
    )

    illumination_type_scintillating: BooleanLike = Field(
        default="", description="Tick if the illumination will be scintillating."
    )

    state_the_intensity_of_the_light_source: str = Field(
        default="",
        description=(
            "Provide the intensity of the light source (e.g. lumens or wattage). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AdvertisingPeriod(BaseModel):
    """Duration for which the advertisement is required"""

    period_of_time_for_which_advertisement_is_required: str = Field(
        ...,
        description=(
            "Specify the duration for which approval for the advertisement is sought. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ExistingSignstobeRemoved(BaseModel):
    """Details of any existing signs that will be removed if this application is approved"""

    details_of_signs_if_any_to_be_removed_if_this_application_is_approved: str = Field(
        default="",
        description=(
            "Describe any existing signs that will be removed if this application is "
            'approved. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class Declaration(BaseModel):
    """Signature and date of advertiser(s)"""

    signature_of_advertisers: str = Field(
        ...,
        description=(
            'Signature of the advertiser(s). .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Date the form is signed by the advertiser(s)."
    )  # YYYY-MM-DD format


class ShireOfEastPilbaraDevelopmentApprovalAdvertisementInfo(BaseModel):
    """
        SHIRE OF EAST PILBARA
    ADDITIONAL INFORMATION FOR DEVELOPMENT
    APPROVAL FOR ADVERTISEMENTS / SIGNS

        NOTE: THIS FORM IS TO BE COMPLETED IN ADDITION TO THE APPLICATION FOR DEVELOPMENT APPROVAL FORM WHERE AN ADVERTISEMENT / SIGN IS PROPOSED
    """

    property_description: PropertyDescription = Field(..., description="Property Description")
    details_of_proposed_sign: DetailsofProposedSign = Field(
        ..., description="Details of Proposed Sign"
    )
    advertising_period: AdvertisingPeriod = Field(..., description="Advertising Period")
    existing_signs_to_be_removed: ExistingSignstobeRemoved = Field(
        ..., description="Existing Signs to be Removed"
    )
    declaration: Declaration = Field(..., description="Declaration")
