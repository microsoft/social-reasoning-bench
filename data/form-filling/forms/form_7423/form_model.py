from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Basic information about the food truck and applicant"""

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


class ApplicationAttachments(BaseModel):
    """Required documents and supporting materials"""

    completed_agreement_form_with_certificate_of_insurance_naming_the_village_of_lions_bay_as_additional_insured_attached: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether the completed agreement form and certificate of insurance are "
            "attached"
        ),
    )

    photos_of_the_food_vending_unit_showing_all_sides_attached: BooleanLike = Field(
        ...,
        description="Indicate whether photos of the food vending unit from all sides are attached",
    )

    health_authority_approval_attached: BooleanLike = Field(
        ..., description="Indicate whether proof of Health Authority approval is attached"
    )

    any_other_required_approvals_please_list_i_e_fire_inspection_etc: str = Field(
        default="",
        description=(
            "List any additional required approvals obtained (e.g., fire inspection) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class FoodTruckDetails(BaseModel):
    """Details about the food truck, its offerings, and operations"""

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
        ..., description="Total number of employees working at the food truck"
    )

    strategies_to_mitigate_impact_on_surrounding_land_uses_due_to_noise_litter_dust_odor_smoke_or_other_issues_and_covid_19_strategies: str = Field(
        ...,
        description=(
            "Describe measures to reduce impacts such as noise, litter, dust, odor, smoke, "
            'and COVID-19 related risks .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class Approval(BaseModel):
    """Internal use for application decision and sign-off"""

    approved: BooleanLike = Field(default="", description="Indicate if the application is approved")

    declined: BooleanLike = Field(default="", description="Indicate if the application is declined")

    approved_by: str = Field(
        default="",
        description=(
            "Name of the official who approved or declined the application .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_of_approval: str = Field(
        default="", description="Date on which the application decision was made"
    )  # YYYY-MM-DD format


class FoodTruckApplication(BaseModel):
    """
    FOOD TRUCK APPLICATION

    Please submit applications and all accompanying documents to office@lionsbay.ca for approval.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    application_attachments: ApplicationAttachments = Field(
        ..., description="Application Attachments"
    )
    food_truck_details: FoodTruckDetails = Field(..., description="Food Truck Details")
    approval: Approval = Field(..., description="Approval")
