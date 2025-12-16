from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class HelpingAHeroorg(BaseModel):
    """Questions about your connection to Helping A Hero"""

    how_did_you_hear_about_helping_a_hero: str = Field(
        default="",
        description=(
            "Describe how you first learned about Helping A Hero (e.g., friend, event, "
            'social media, TV, etc.) .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    do_you_know_any_veteran_who_has_received_a_helping_a_hero_home_or_home_grant_if_so_who: str = (
        Field(
            default="",
            description=(
                "List any veterans you know who have received a Helping A Hero home or home "
                "grant, including their names and any relevant details .If you cannot fill "
                'this, write "N/A". If this field should not be filled by you (for example, '
                'it belongs to another person or office), leave it blank (empty string "").'
            ),
        )
    )


class SupportFromOtherOrganizations(BaseModel):
    """Post-injury support received from other organizations"""

    have_you_received_any_post_injury_support_in_any_category_from_other_not_for_profit_organizations_veteran_related_or_otherwise_if_so_what_type_and_from_whom: str = Field(
        default="",
        description=(
            "Describe any post-injury support you have received from other nonprofit or "
            "veteran-related organizations, including the type of support and the "
            'organization names .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class CurrentHomeOwnershipRental(BaseModel):
    """Current housing situation including home ownership and rental details"""

    are_you_currently_a_homeowner_if_yes_address: str = Field(
        default="",
        description=(
            "If you are a homeowner, provide the full address of your current home .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    are_you_currently_a_homeowner_if_yes_current_value_of_home: Union[float, Literal["N/A", ""]] = (
        Field(default="", description="Estimated current market value of your home in dollars")
    )

    are_you_currently_a_homeowner_if_yes_remaining_amount_owed: Union[float, Literal["N/A", ""]] = (
        Field(
            default="", description="Approximate remaining balance owed on your mortgage in dollars"
        )
    )

    are_you_currently_a_homeowner_if_yes_monthly_insurance: Union[float, Literal["N/A", ""]] = (
        Field(default="", description="Monthly amount you pay for homeowners insurance in dollars")
    )

    are_you_currently_a_homeowner_if_yes_annual_taxes: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total annual property taxes you pay on your home in dollars"
    )

    are_you_currently_in_a_rental_or_lease_agreement: BooleanLike = Field(
        default="", description="Indicate whether you are currently in a rental or lease agreement"
    )

    if_yes_what_is_the_monthly_rental: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly rent amount in dollars"
    )

    if_yes_what_day_month_year_does_the_rent_lease_contract_expire: str = Field(
        default="", description="Expiration date of your current rental or lease contract"
    )  # YYYY-MM-DD format


class HelpingAHeroorg(BaseModel):
    """HELPING A HERO.ORG"""

    helping_a_heroorg: HelpingAHeroorg = Field(..., description="Helping A Hero.org")
    support_from_other_organizations: SupportFromOtherOrganizations = Field(
        ..., description="Support From Other Organizations"
    )
    current_home_ownershiprental: CurrentHomeOwnershipRental = Field(
        ..., description="Current Home Ownership/Rental"
    )
