from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class I1ChangesinschoolfeedingoperationsduetoCOVID19(BaseModel):
    """Overall changes in school feeding operations in the most recently completed school year"""

    number_of_students_fed_increased: BooleanLike = Field(
        default="",
        description=(
            "Indicate that the number of students fed increased compared to before the disruption."
        ),
    )

    number_of_students_fed_decreased: BooleanLike = Field(
        default="",
        description=(
            "Indicate that the number of students fed decreased compared to before the disruption."
        ),
    )

    number_of_students_fed_no_change: BooleanLike = Field(
        default="",
        description=(
            "Indicate that there was no change in the number of students fed compared to "
            "before the disruption."
        ),
    )

    frequency_of_school_feeding_increased: BooleanLike = Field(
        default="",
        description=(
            "Indicate that the frequency of school feeding increased compared to before the "
            "disruption."
        ),
    )

    frequency_of_school_feeding_decreased: BooleanLike = Field(
        default="",
        description=(
            "Indicate that the frequency of school feeding decreased compared to before the "
            "disruption."
        ),
    )

    frequency_of_school_feeding_no_change: BooleanLike = Field(
        default="",
        description=(
            "Indicate that there was no change in the frequency of school feeding compared "
            "to before the disruption."
        ),
    )

    size_of_rations_increased: BooleanLike = Field(
        default="",
        description="Indicate that the size of rations increased compared to before the disruption.",
    )

    size_of_rations_decreased: BooleanLike = Field(
        default="",
        description="Indicate that the size of rations decreased compared to before the disruption.",
    )

    size_of_rations_no_change: BooleanLike = Field(
        default="",
        description=(
            "Indicate that there was no change in the size of rations compared to before "
            "the disruption."
        ),
    )

    level_of_food_basket_variety_increased: BooleanLike = Field(
        default="",
        description=(
            "Indicate that the variety of items in the food basket increased compared to "
            "before the disruption."
        ),
    )

    level_of_food_basket_variety_decreased: BooleanLike = Field(
        default="",
        description=(
            "Indicate that the variety of items in the food basket decreased compared to "
            "before the disruption."
        ),
    )

    level_of_food_basket_variety_no_change: BooleanLike = Field(
        default="",
        description=(
            "Indicate that there was no change in the variety of items in the food basket "
            "compared to before the disruption."
        ),
    )

    amount_of_funding_increased: BooleanLike = Field(
        default="",
        description=(
            "Indicate that the amount of funding for school feeding increased compared to "
            "before the disruption."
        ),
    )

    amount_of_funding_decreased: BooleanLike = Field(
        default="",
        description=(
            "Indicate that the amount of funding for school feeding decreased compared to "
            "before the disruption."
        ),
    )

    amount_of_funding_no_change: BooleanLike = Field(
        default="",
        description=(
            "Indicate that there was no change in the amount of funding for school feeding "
            "compared to before the disruption."
        ),
    )

    change_in_beneficiaries_yes_temporarily: BooleanLike = Field(
        default="",
        description=(
            "Select if there was a temporary change in the type of beneficiaries (e.g., "
            "from students to families)."
        ),
    )

    change_in_beneficiaries_yes_to_this_day: BooleanLike = Field(
        default="",
        description=(
            "Select if there was a change in the type of beneficiaries that is still in "
            "place to this day."
        ),
    )

    change_in_beneficiaries_no_change: BooleanLike = Field(
        default="", description="Select if there was no change in the type of beneficiaries."
    )

    change_in_venue_of_distributing_receiving_food_yes_temporarily: BooleanLike = Field(
        default="",
        description=(
            "Select if the location where food was distributed or received changed temporarily."
        ),
    )

    change_in_venue_of_distributing_receiving_food_yes_to_this_day: BooleanLike = Field(
        default="",
        description=(
            "Select if the location where food is distributed or received changed and "
            "remains changed to this day."
        ),
    )

    change_in_venue_of_distributing_receiving_food_no_change: BooleanLike = Field(
        default="",
        description=(
            "Select if there was no change in the location of distributing or receiving food."
        ),
    )

    change_in_feeding_modality_yes_temporarily: BooleanLike = Field(
        default="",
        description=(
            "Select if the way food was provided (e.g., in-school meals vs. take-home "
            "rations) changed temporarily."
        ),
    )

    change_in_feeding_modality_yes_to_this_day: BooleanLike = Field(
        default="",
        description="Select if the way food is provided changed and remains changed to this day.",
    )

    change_in_feeding_modality_no_change: BooleanLike = Field(
        default="", description="Select if there was no change in the way food was provided."
    )

    change_in_the_sourcing_of_food_yes_temporarily: BooleanLike = Field(
        default="",
        description="Select if the sources from which food was obtained changed temporarily.",
    )

    change_in_the_sourcing_of_food_yes_to_this_day: BooleanLike = Field(
        default="",
        description=(
            "Select if the sources from which food is obtained changed and remain changed "
            "to this day."
        ),
    )

    change_in_the_sourcing_of_food_no_change: BooleanLike = Field(
        default="",
        description="Select if there was no change in the sources from which food was obtained.",
    )

    change_in_source_of_funding_yes_temporarily: BooleanLike = Field(
        default="",
        description="Select if the sources of funding for school feeding changed temporarily.",
    )

    change_in_source_of_funding_yes_to_this_day: BooleanLike = Field(
        default="",
        description=(
            "Select if the sources of funding for school feeding changed and remain changed "
            "to this day."
        ),
    )

    change_in_source_of_funding_no_change: BooleanLike = Field(
        default="",
        description="Select if there was no change in the sources of funding for school feeding.",
    )

    ceased_feeding_operations_yes_temporarily: BooleanLike = Field(
        default="",
        description="Select if school feeding operations stopped temporarily during the disruption.",
    )

    ceased_feeding_operations_yes_to_this_day: BooleanLike = Field(
        default="",
        description="Select if school feeding operations stopped and remain stopped to this day.",
    )

    ceased_feeding_operations_no: BooleanLike = Field(
        default="", description="Select if school feeding operations did not cease."
    )


class I11Changesinmodalityorpointoffooddistribution(BaseModel):
    """Specific ways in which the modality or point of food distribution changed"""

    meals_snacks_prepared_at_school_served_in_different_way: BooleanLike = Field(
        default="",
        description=(
            "Check if meals/snacks continued to be prepared at school but were served in a "
            "substantially different way than before."
        ),
    )

    meals_snacks_prepared_at_school_picked_up_and_eaten_at_home: BooleanLike = Field(
        default="",
        description=(
            "Check if meals/snacks were prepared at school but collected by students or "
            "parents to be eaten at home."
        ),
    )

    ingredients_delivered_to_students_homes: BooleanLike = Field(
        default="",
        description=(
            "Check if ingredients were delivered directly to students' homes for "
            "preparation and consumption at home."
        ),
    )

    ingredients_picked_up_at_school_to_prepare_at_home: BooleanLike = Field(
        default="",
        description=(
            "Check if ingredients were provided at school for students or parents to pick "
            "up and prepare at home."
        ),
    )

    cash_or_vouchers_electronic: BooleanLike = Field(
        default="",
        description=(
            "Check if families received electronic cash transfers or electronic vouchers to "
            "purchase food instead of school meals."
        ),
    )

    cash_or_vouchers_hard_currency_or_physical: BooleanLike = Field(
        default="",
        description=(
            "Check if families received cash in hand or physical paper vouchers/coupons to "
            "purchase food instead of school meals."
        ),
    )


class SectionISchoolFeedingOperationsAndCovid19(BaseModel):
    """
    SECTION I: SCHOOL FEEDING OPERATIONS AND COVID-19

    SECTION I: SCHOOL FEEDING OPERATIONS AND COVID-19. This section collects information on how school feeding operations changed due to disruptions from the COVID-19 pandemic in the most recently completed school year, including changes in the number of students fed, frequency and size of rations, food basket variety, funding levels and sources, targeting of beneficiaries, venues and modalities of food distribution, sourcing of food, and whether feeding operations ceased temporarily or permanently.
    """

    i1_changes_in_school_feeding_operations_due_to_covid_19: I1ChangesinschoolfeedingoperationsduetoCOVID19 = Field(
        ..., description="I1. Changes in school feeding operations due to COVID-19"
    )
    i11_changes_in_modality_or_point_of_food_distribution: I11Changesinmodalityorpointoffooddistribution = Field(
        ..., description="I1.1. Changes in modality or point of food distribution"
    )
