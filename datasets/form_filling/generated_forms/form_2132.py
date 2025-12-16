from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class WhoDiscriminatedAgainstYou(BaseModel):
    """Type of person or entity that discriminated against you"""

    builder: BooleanLike = Field(
        default="",
        description="Check if the person or entity who discriminated against you was a builder.",
    )

    bank_or_other_lender: BooleanLike = Field(
        default="",
        description=(
            "Check if the person or entity who discriminated against you was a bank or "
            "other lender."
        ),
    )

    manager_superintendent: BooleanLike = Field(
        default="",
        description=(
            "Check if the person or entity who discriminated against you was a manager or "
            "superintendent."
        ),
    )

    owner_landlord: BooleanLike = Field(
        default="",
        description=(
            "Check if the person or entity who discriminated against you was the owner or landlord."
        ),
    )

    salesperson: BooleanLike = Field(
        default="",
        description="Check if the person or entity who discriminated against you was a salesperson.",
    )

    other_who_discriminated_against_you: str = Field(
        default="",
        description=(
            "If the person or entity who discriminated against you is not listed, describe "
            'who it was. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    co_op_board: BooleanLike = Field(
        default="",
        description="Check if the person or entity who discriminated against you was a co-op board.",
    )

    condo_association: BooleanLike = Field(
        default="",
        description=(
            "Check if the person or entity who discriminated against you was a condo association."
        ),
    )


class PropertyInformation(BaseModel):
    """Details about the property involved in the discrimination"""

    single_family_house: BooleanLike = Field(
        default="", description="Check if the property involved was a single-family house."
    )

    mobile_home: BooleanLike = Field(
        default="", description="Check if the property involved was a mobile home."
    )

    building_with_2_4_apartments: BooleanLike = Field(
        default="", description="Check if the property involved was a building with 2–4 apartments."
    )

    two_family_house: BooleanLike = Field(
        default="", description="Check if the property involved was a two-family house."
    )

    commercial_space: BooleanLike = Field(
        default="", description="Check if the property involved was commercial space."
    )

    building_with_5_or_more_apartments: BooleanLike = Field(
        default="",
        description="Check if the property involved was a building with 5 or more apartments.",
    )

    other_kind_of_property: str = Field(
        default="",
        description=(
            "If the kind of property is not listed, describe it here. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    does_the_owner_live_on_the_property_yes: BooleanLike = Field(
        default="", description="Select if the owner lives on the property."
    )

    does_the_owner_live_on_the_property_no: BooleanLike = Field(
        default="", description="Select if the owner does not live on the property."
    )

    was_this_property_being_sold_being_sold: BooleanLike = Field(
        default="", description="Select if the property was being sold."
    )

    was_this_property_being_rented_being_rented: BooleanLike = Field(
        default="", description="Select if the property was being rented."
    )

    address: str = Field(
        ...,
        description=(
            "Street address of the property involved. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    apt_or_floor_number: str = Field(
        default="",
        description=(
            "Apartment number or floor number of the property. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City where the property is located. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State where the property is located.")

    zip: str = Field(..., description="ZIP code of the property location.")

    are_you_currently_living_there_yes: BooleanLike = Field(
        default="", description="Select if you are currently living at this property."
    )

    are_you_currently_living_there_no: BooleanLike = Field(
        default="", description="Select if you are not currently living at this property."
    )


class ActsofDiscrimination(BaseModel):
    """What the person or entity did that was discriminatory"""

    refused_to_rent_or_sell_to_me: BooleanLike = Field(
        default="", description="Check if the person refused to rent or sell the property to you."
    )

    evicted_me_threatened_to_evict_me: BooleanLike = Field(
        default="", description="Check if the person evicted you or threatened to evict you."
    )

    denied_me_access_for_my_disability: BooleanLike = Field(
        default="",
        description="Check if you were denied access or accommodations because of your disability.",
    )

    denied_me_equal_terms_privileges_or_facilities_that_other_tenants_were_given: BooleanLike = (
        Field(
            default="",
            description=(
                "Check if you were denied the same terms, privileges, or facilities that other "
                "tenants received."
            ),
        )
    )

    discriminated_against_me_in_lending_or_financing: BooleanLike = Field(
        default="",
        description=(
            "Check if you experienced discrimination in lending or financing related to "
            "this property."
        ),
    )

    advertised_in_a_discriminatory_way: BooleanLike = Field(
        default="", description="Check if the property was advertised in a discriminatory manner."
    )

    harassed_me_based_on_my_sex_national_origin_race_disability_etc: BooleanLike = Field(
        default="",
        description=(
            "Check if you were harassed because of your sex, national origin, race, "
            "disability, or another protected characteristic."
        ),
    )

    other_acts_of_discrimination: str = Field(
        default="",
        description=(
            "Describe any other discriminatory acts that are not listed above. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class HousingDiscrimination(BaseModel):
    """
    HOUSING DISCRIMINATION

    Please answer the questions on this page only if you were discriminated against in the area of housing.
    """

    who_discriminated_against_you: WhoDiscriminatedAgainstYou = Field(
        ..., description="Who Discriminated Against You"
    )
    property_information: PropertyInformation = Field(..., description="Property Information")
    acts_of_discrimination: ActsofDiscrimination = Field(..., description="Acts of Discrimination")
