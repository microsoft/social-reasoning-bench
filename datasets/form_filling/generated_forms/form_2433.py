from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class BasementsSwimmingPoolsGeneralQuestions(BaseModel):
    """General questions about basement and swimming pool work, including future work and use of specialist contractors"""

    have_you_ever_undertaken_any_contracts_involving_the_creation_of_a_basement: BooleanLike = (
        Field(
            ...,
            description=(
                "Indicate whether you have ever undertaken any contracts involving the creation "
                "of a basement."
            ),
        )
    )

    have_you_ever_undertaken_any_contracts_involving_the_creation_of_a_basement_yes: BooleanLike = (
        Field(
            ...,
            description=(
                "Check if the answer to having undertaken contracts involving the creation of a "
                "basement is YES."
            ),
        )
    )

    have_you_ever_undertaken_any_contracts_involving_the_creation_of_a_basement_no: BooleanLike = (
        Field(
            ...,
            description=(
                "Check if the answer to having undertaken contracts involving the creation of a "
                "basement is NO."
            ),
        )
    )

    do_you_have_any_future_basement_work_planned: BooleanLike = Field(
        ..., description="Indicate whether you have any future basement work planned."
    )

    details_of_future_basement_work_planned_line_1: str = Field(
        default="",
        description=(
            "First line of details for any future basement work planned, if applicable. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    details_of_future_basement_work_planned_line_2: str = Field(
        default="",
        description=(
            "Second line of details for any future basement work planned, if applicable. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    have_you_ever_undertaken_any_contracts_involving_swimming_pools: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you have ever undertaken any contracts involving swimming pools."
        ),
    )

    have_you_ever_undertaken_any_contracts_involving_swimming_pools_yes: BooleanLike = Field(
        ...,
        description=(
            "Check if the answer to having undertaken contracts involving swimming pools is YES."
        ),
    )

    have_you_ever_undertaken_any_contracts_involving_swimming_pools_no: BooleanLike = Field(
        ...,
        description=(
            "Check if the answer to having undertaken contracts involving swimming pools is NO."
        ),
    )

    how_many_swimming_pool_contracts_have_you_undertaken: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of swimming pool contracts you have undertaken."
    )

    are_you_currently_working_on_site_at_any_swimming_pools: BooleanLike = Field(
        ..., description="Indicate whether you are currently working on site at any swimming pools."
    )

    are_you_currently_working_on_site_at_any_swimming_pools_yes: BooleanLike = Field(
        ..., description="Check if you are currently working on site at swimming pools (YES)."
    )

    are_you_currently_working_on_site_at_any_swimming_pools_no: BooleanLike = Field(
        ..., description="Check if you are not currently working on site at swimming pools (NO)."
    )

    is_the_pool_part_of_a_larger_overall_contract: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether the pool is part of a larger overall contract (e.g. a pool "
            "within a house)."
        ),
    )

    is_the_pool_part_of_a_larger_overall_contract_yes: BooleanLike = Field(
        ..., description="Check if the pool is part of a larger overall contract (YES)."
    )

    is_the_pool_part_of_a_larger_overall_contract_no: BooleanLike = Field(
        ..., description="Check if the pool is not part of a larger overall contract (NO)."
    )

    what_service_did_you_provide_line_1: str = Field(
        default="",
        description=(
            "First line describing the service you provided in relation to the swimming "
            'pool. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    what_service_did_you_provide_line_2: str = Field(
        default="",
        description=(
            "Second line describing the service you provided in relation to the swimming "
            'pool. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    are_you_responsible_for_the_filtration_systems: BooleanLike = Field(
        ...,
        description="Indicate whether you are responsible for the swimming pool filtration systems.",
    )

    are_you_responsible_for_the_filtration_systems_yes: BooleanLike = Field(
        ..., description="Check if you are responsible for the filtration systems (YES)."
    )

    are_you_responsible_for_the_filtration_systems_no: BooleanLike = Field(
        ..., description="Check if you are not responsible for the filtration systems (NO)."
    )

    are_specialist_contractors_appointed_for_any_of_the_works: BooleanLike = Field(
        ...,
        description="Indicate whether specialist contractors are appointed for any of the works.",
    )

    are_specialist_contractors_appointed_for_any_of_the_works_yes: BooleanLike = Field(
        ..., description="Check if specialist contractors are appointed for any of the works (YES)."
    )

    are_specialist_contractors_appointed_for_any_of_the_works_no: BooleanLike = Field(
        ...,
        description="Check if specialist contractors are not appointed for any of the works (NO).",
    )

    if_yes_are_contract_terms_back_to_back_and_covered_by_third_party_pi_insurance: BooleanLike = (
        Field(
            default="",
            description=(
                "If specialist contractors are appointed, indicate whether contract terms are "
                "back-to-back and covered by third party PI insurance."
            ),
        )
    )

    if_yes_are_contract_terms_back_to_back_and_covered_by_third_party_pi_insurance_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if contract terms are back-to-back and covered by third party PI "
            "insurance (YES)."
        ),
    )

    if_yes_are_contract_terms_back_to_back_and_covered_by_third_party_pi_insurance_no: BooleanLike = Field(
        default="",
        description=(
            "Check if contract terms are not back-to-back and/or not covered by third party "
            "PI insurance (NO)."
        ),
    )

    are_the_contractors_directly_appointed_by_your_client: BooleanLike = Field(
        ..., description="Indicate whether the contractors are directly appointed by your client."
    )

    are_the_contractors_directly_appointed_by_your_client_yes: BooleanLike = Field(
        ..., description="Check if the contractors are directly appointed by your client (YES)."
    )

    are_the_contractors_directly_appointed_by_your_client_no: BooleanLike = Field(
        ..., description="Check if the contractors are not directly appointed by your client (NO)."
    )

    do_you_have_any_future_swimming_pool_work_planned: BooleanLike = Field(
        ..., description="Indicate whether you have any future swimming pool work planned."
    )

    do_you_have_any_future_swimming_pool_work_planned_yes: BooleanLike = Field(
        ..., description="Check if you have future swimming pool work planned (YES)."
    )

    do_you_have_any_future_swimming_pool_work_planned_no: BooleanLike = Field(
        ..., description="Check if you do not have future swimming pool work planned (NO)."
    )


class LargestContractsContract1Details(BaseModel):
    """Details of one of the three largest contracts involving basements/swimming pools in the past 6 years (Contract 1)"""

    contract_1_who_were_you_contracted_to: str = Field(
        ...,
        description=(
            "Name of the party or organisation you were contracted to for Contract 1. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    contract_1_who_was_the_end_client_for_the_project_if_different_from_above: str = Field(
        default="",
        description=(
            "Name of the end client for Contract 1, if different from the party you were "
            'contracted to. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    contract_1_what_was_being_built_changed_or_supplied: str = Field(
        ...,
        description=(
            "Description of what was being built, changed or supplied for Contract 1 (type "
            "of building, product, business change or service). .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contract_1_what_was_the_total_cost_of_the_entire_project: Union[float, Literal["N/A", ""]] = (
        Field(
            ...,
            description=(
                "Total cost of the entire project for Contract 1; estimate if the exact amount "
                "is unknown."
            ),
        )
    )

    contract_1_what_was_your_income_from_the_contract: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Your income or fees earned from Contract 1."
    )

    contract_1_start_date: str = Field(
        ..., description="Start date of your engagement on Contract 1."
    )  # YYYY-MM-DD format

    contract_1_end_date: str = Field(
        ..., description="End date of your engagement on Contract 1."
    )  # YYYY-MM-DD format

    contract_1_what_goods_or_services_did_you_provide: str = Field(
        ...,
        description=(
            "Description of the goods or services you provided under Contract 1. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SpecialistQuestionsBasementsSwimmingPools(BaseModel):
    """
        Specialist Questions

    Basements & Swimming Pools

        ''
    """

    basements__swimming_pools___general_questions: BasementsSwimmingPoolsGeneralQuestions = Field(
        ..., description="Basements & Swimming Pools – General Questions"
    )
    largest_contracts___contract_1_details: LargestContractsContract1Details = Field(
        ..., description="Largest Contracts – Contract 1 Details"
    )
