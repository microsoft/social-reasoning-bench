from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FoodTruckApplication(BaseModel):
    """Applicant and food truck details for permit consideration"""

    food_truck_name: str = Field(
        ...,
        description=(
            "Registered or operating name of the food truck .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_name: str = Field(
        ...,
        description=(
            "Full name of the person submitting the application .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Email address for the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    dates_requested: str = Field(
        ...,
        description=(
            "Requested operating date(s) for the food truck .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    completed_agreement_form_with_certificate_of_insurance_naming_the_village_of_lions_bay_as_additional_insured_attached: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether the completed agreement form and certificate of insurance "
            "naming the Village of Lions Bay as additional insured are attached"
        ),
    )

    photos_of_the_food_vending_unit_showing_all_sides_attached: BooleanLike = Field(
        ...,
        description="Indicate whether photos of the food vending unit showing all sides are attached",
    )

    list_of_food_and_beverages_to_be_sold: str = Field(
        ...,
        description=(
            "Detailed list of all food and beverage items that will be sold .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    dimensions_of_food_vending_unit_length: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Length of the food vending unit (specify units if applicable)"
    )

    dimensions_of_food_vending_unit_width: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Width of the food vending unit (specify units if applicable)"
    )

    dimensions_of_food_vending_unit_height: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Height of the food vending unit (specify units if applicable)"
    )

    location_and_description_of_cooking_and_or_food_preparation_facilities_if_applicable: str = (
        Field(
            default="",
            description=(
                "Describe where and how cooking and food preparation will occur, if applicable "
                '.If you cannot fill this, write "N/A". If this field should not be filled by '
                "you (for example, it belongs to another person or office), leave it blank "
                '(empty string "").'
            ),
        )
    )

    number_of_employees: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of employees who will be working at the food truck"
    )

    health_authority_approval_attached: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether the required Health Authority approval documentation is attached"
        ),
    )

    any_other_required_approvals_please_list_i_e_fire_inspection_etc: str = Field(
        default="",
        description=(
            "List any additional required approvals, such as fire inspection or other "
            'regulatory approvals .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    strategies_to_mitigate_impact_on_surrounding_land_uses_due_to_noise_litter_dust_odor_smoke_or_other_issues_and_covid_19_strategies: str = Field(
        ...,
        description=(
            "Describe strategies to reduce impacts such as noise, litter, dust, odor, "
            "smoke, and measures related to COVID-19 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Approval(BaseModel):
    """Internal approval decision and sign-off"""

    approved: BooleanLike = Field(
        default="", description="Indicates that the application has been approved"
    )

    declined: BooleanLike = Field(
        default="", description="Indicates that the application has been declined"
    )

    approved_by: str = Field(
        default="",
        description=(
            "Name or signature of the approving official .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_approval: str = Field(
        default="", description="Date on which the application was approved or declined"
    )  # YYYY-MM-DD format


class FoodTruckApplication(BaseModel):
    """
    FOOD TRUCK APPLICATION

    Please submit applications and all accompanying documents to office@lionsbay.ca for approval.
    """

    food_truck_application: FoodTruckApplication = Field(..., description="Food Truck Application")
    approval: Approval = Field(..., description="Approval")
