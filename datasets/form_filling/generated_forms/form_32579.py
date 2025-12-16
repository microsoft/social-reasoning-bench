from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ClientInformation(BaseModel):
    """Client details and situation overview"""

    date: str = Field(..., description="Date this form is completed")  # YYYY-MM-DD format

    family_individual_name: str = Field(
        ...,
        description=(
            "Full name of the family or individual requesting assistance .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    story_highlights_briefly_what_you_need_help_with_and_why: str = Field(
        ...,
        description=(
            "Brief description of your situation, what assistance you need, why, and "
            'approximate dollar amounts .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    have_you_filed_your_2019_tax_return_yet: BooleanLike = Field(
        default="", description="Indicate whether you have filed your 2019 tax return"
    )

    have_you_filed_your_2019_tax_return_yet_no: BooleanLike = Field(
        default="", description="Indicate whether you have NOT filed your 2019 tax return"
    )

    do_you_have_an_eviction_notice: BooleanLike = Field(
        default="", description="Indicate whether you currently have an eviction notice"
    )

    do_you_have_an_eviction_notice_no: BooleanLike = Field(
        default="", description="Indicate whether you do NOT have an eviction notice"
    )

    other_resources_to_help_you_out_family_friends_landlord: str = Field(
        default="",
        description=(
            "List any other people or resources helping you, such as family, friends, or "
            'landlord .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    are_you_receiving_or_have_you_applied_for_unemployment: BooleanLike = Field(
        default="",
        description="Indicate whether you are receiving or have applied for unemployment benefits",
    )

    are_you_receiving_or_have_you_applied_for_unemployment_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether you are NOT receiving and have NOT applied for unemployment benefits"
        ),
    )

    other_agencies_helping_you_salvation_army_food_share_human_services_social_workers_etc: str = (
        Field(
            default="",
            description=(
                "List any agencies or organizations currently helping you .If you cannot fill "
                'this, write "N/A". If this field should not be filled by you (for example, '
                'it belongs to another person or office), leave it blank (empty string "").'
            ),
        )
    )

    do_you_have_health_insurance_coverage: BooleanLike = Field(
        default="", description="Indicate whether you currently have health insurance coverage"
    )

    do_you_have_health_insurance_coverage_no: BooleanLike = Field(
        default="", description="Indicate whether you do NOT have health insurance coverage"
    )

    are_you_a_veteran: BooleanLike = Field(
        default="", description="Indicate whether you have veteran status"
    )

    are_you_a_veteran_no: BooleanLike = Field(
        default="", description="Indicate whether you are NOT a veteran"
    )

    are_you_using_the_food_pantries: BooleanLike = Field(
        default="", description="Indicate whether you are currently using food pantries"
    )

    are_you_using_the_food_pantries_no: BooleanLike = Field(
        default="", description="Indicate whether you are NOT using food pantries"
    )

    have_you_applied_for_energy_assistance: BooleanLike = Field(
        default="", description="Indicate whether you have applied for Energy Assistance"
    )

    have_you_applied_for_energy_assistance_no: BooleanLike = Field(
        default="", description="Indicate whether you have NOT applied for Energy Assistance"
    )


class HousingandUtilities(BaseModel):
    """Landlord/mortgage and utility account information"""

    landlord_mortgage_holder_name: str = Field(
        ...,
        description=(
            "Full name of the landlord or mortgage holder .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    landlord_mortgage_holder_address: str = Field(
        ...,
        description=(
            "Mailing address of the landlord or mortgage holder .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    landlord_mortgage_holder_phone_number: str = Field(
        ...,
        description=(
            "Phone number for the landlord or mortgage holder .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    alliant_account_holder_name: str = Field(
        default="",
        description=(
            'Name on the Alliant utility account .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    alliant_amount_owed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount currently owed to Alliant"
    )

    alliant_account_number: str = Field(
        default="",
        description=(
            'Alliant utility account number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    we_energy_account_holder_name: str = Field(
        default="",
        description=(
            'Name on the We Energy utility account .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    we_energy_amount_owed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount currently owed to We Energy"
    )

    we_energy_account_number: str = Field(
        default="",
        description=(
            'We Energy utility account number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    water_dept_account_holder_name: str = Field(
        default="",
        description=(
            "Name on the Water Department utility account .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    water_dept_amount_owed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount currently owed to the Water Department"
    )

    water_dept_account_number: str = Field(
        default="",
        description=(
            "Water Department utility account number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class SidebySideInternalUse(BaseModel):
    """To be completed by Side by Side member"""

    volunteer_name: str = Field(
        default="",
        description=(
            "Name of the Side by Side volunteer completing this section .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_called: str = Field(
        default="", description="Date the client was called by the volunteer"
    )  # YYYY-MM-DD format

    recommendation: str = Field(
        default="",
        description=(
            "Volunteer’s recommendation regarding assistance .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_information: str = Field(
        default="",
        description=(
            "Any additional notes or information from the volunteer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SideBySideIncClientInformation(BaseModel):
    """
        Side by Side, Inc.
    Client Information

        Side by Side can only offer assistance to those who live in the Badger High School District.
    """

    client_information: ClientInformation = Field(..., description="Client Information")
    housing_and_utilities: HousingandUtilities = Field(..., description="Housing and Utilities")
    side_by_side_internal_use: SidebySideInternalUse = Field(
        ..., description="Side by Side Internal Use"
    )
