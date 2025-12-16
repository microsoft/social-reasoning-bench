from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class BusinessOwnersSectionHeader(BaseModel):
    """Top-of-form agency and policy identifiers"""

    agency_customer_id: str = Field(
        ...,
        description=(
            'Agency\'s internal customer identifier .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    agency_name: str = Field(
        ...,
        description=(
            'Name of the insurance agency .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    carrier: str = Field(
        ...,
        description=(
            'Name of the insurance carrier .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_mm_dd_yyyy: str = Field(
        ..., description="Date this section is completed (MM/DD/YYYY)"
    )  # YYYY-MM-DD format

    naic_code: str = Field(
        default="",
        description=(
            'NAIC code of the carrier .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    policy_number: str = Field(
        ...,
        description=(
            "Policy number for this business owners policy .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    effective_date: str = Field(..., description="Policy effective date")  # YYYY-MM-DD format

    first_named_insured: str = Field(
        ...,
        description=(
            'First named insured on the policy .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    policy_type_standard: BooleanLike = Field(
        ..., description="Check if the policy type is Standard"
    )

    policy_type_special: BooleanLike = Field(..., description="Check if the policy type is Special")


class Premium(BaseModel):
    """Premium amounts for liability and property"""

    liability_premium: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Liability premium amount"
    )

    property_premium: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Property premium amount"
    )

    minimum_premium: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Minimum premium amount, if applicable"
    )

    total_estimated_premium: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total estimated premium for the policy"
    )


class BlanketSummary(BaseModel):
    """Blanket coverage numbers, amounts, and types"""

    blkt_1_number: str = Field(
        default="",
        description=(
            'First blanket number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    amount_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount for first blanket entry"
    )

    type_1: str = Field(
        default="",
        description=(
            'Type for first blanket entry .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    blkt_2_number: str = Field(
        default="",
        description=(
            'Second blanket number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    amount_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Amount for second blanket entry"
    )

    type_2: str = Field(
        default="",
        description=(
            'Type for second blanket entry .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class GeneralInformation(BaseModel):
    """General underwriting questions 1–9"""

    q1_hazardous_material_operations: BooleanLike = Field(
        ..., description="Indicate if any operations involve hazardous materials"
    )

    q2_athletic_teams_sponsored: BooleanLike = Field(
        ..., description="Indicate if athletic teams are sponsored"
    )

    type_of_sport_1: str = Field(
        default="",
        description=(
            'Type of first sponsored sport .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    contact_sport_yn_1: BooleanLike = Field(
        default="", description="Indicate if the first sport is a contact sport"
    )

    age_group_13_18_1: BooleanLike = Field(
        default="", description="Check if first sport participants are ages 13-18"
    )

    age_group_12_under_1: BooleanLike = Field(
        default="", description="Check if first sport participants are age 12 and under"
    )

    age_group_over_18_1: BooleanLike = Field(
        default="", description="Check if first sport participants are over 18"
    )

    type_of_sport_2: str = Field(
        default="",
        description=(
            'Type of second sponsored sport .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_sport_yn_2: BooleanLike = Field(
        default="", description="Indicate if the second sport is a contact sport"
    )

    age_group_13_18_2: BooleanLike = Field(
        default="", description="Check if second sport participants are ages 13-18"
    )

    age_group_12_under_2: BooleanLike = Field(
        default="", description="Check if second sport participants are age 12 and under"
    )

    age_group_over_18_2: BooleanLike = Field(
        default="", description="Check if second sport participants are over 18"
    )

    extent_of_sponsorship: str = Field(
        default="",
        description=(
            "Describe the extent of sponsorship for athletic teams .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    q3_certificates_of_insurance_obtained: BooleanLike = Field(
        ...,
        description=(
            "Indicate if certificates of insurance are obtained and verified from "
            "subcontractors, manufacturers, and/or suppliers"
        ),
    )

    q3_if_no_explain: str = Field(
        default="",
        description=(
            "Explanation if certificates of insurance are not obtained and verified .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    q4_lease_employees: BooleanLike = Field(
        ..., description="Indicate if employees are leased to or from other employers"
    )

    lease_to: BooleanLike = Field(
        default="", description="Indicate if employees are leased to other employers"
    )

    lease_to_workers_comp_coverage: BooleanLike = Field(
        default="",
        description="For leased-to employees, indicate if workers compensation coverage is carried",
    )

    lease_from: BooleanLike = Field(
        default="", description="Indicate if employees are leased from other employers"
    )

    lease_from_workers_comp_coverage: BooleanLike = Field(
        default="",
        description="For leased-from employees, indicate if workers compensation coverage is carried",
    )

    q5_other_business_owned_or_operated: BooleanLike = Field(
        ..., description="Indicate if any other businesses are owned or operated"
    )

    other_business_1_street_city_state_zip: str = Field(
        default="",
        description=(
            "Street, city, state, and ZIP for first other business .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_business_1_type_of_business_or_loc: str = Field(
        default="",
        description=(
            "Type of business or location description for first other business .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_business_1_building_interest_own: BooleanLike = Field(
        default="", description="Check if first other business building interest is OWN"
    )

    other_business_1_building_interest_lease: BooleanLike = Field(
        default="", description="Check if first other business building interest is LEASE"
    )

    other_business_1_building_interest_rent: BooleanLike = Field(
        default="", description="Check if first other business building interest is RENT"
    )

    other_business_1_building_interest_office: BooleanLike = Field(
        default="", description="Check if first other business occupancy is OFFICE"
    )

    other_business_1_building_interest_service: BooleanLike = Field(
        default="", description="Check if first other business occupancy is SERVICE"
    )

    other_business_1_building_interest_retail: BooleanLike = Field(
        default="", description="Check if first other business occupancy is RETAIL"
    )

    other_business_1_building_interest_wholesale: BooleanLike = Field(
        default="", description="Check if first other business occupancy is WHOLESALE"
    )

    other_business_1_operations: str = Field(
        default="",
        description=(
            "Description of operations for first other business .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_business_2_street_city_state_zip: str = Field(
        default="",
        description=(
            "Street, city, state, and ZIP for second other business .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_business_2_type_of_business_or_loc: str = Field(
        default="",
        description=(
            "Type of business or location description for second other business .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_business_2_building_interest_own: BooleanLike = Field(
        default="", description="Check if second other business building interest is OWN"
    )

    other_business_2_building_interest_lease: BooleanLike = Field(
        default="", description="Check if second other business building interest is LEASE"
    )

    other_business_2_building_interest_rent: BooleanLike = Field(
        default="", description="Check if second other business building interest is RENT"
    )

    other_business_2_building_interest_office: BooleanLike = Field(
        default="", description="Check if second other business occupancy is OFFICE"
    )

    other_business_2_building_interest_service: BooleanLike = Field(
        default="", description="Check if second other business occupancy is SERVICE"
    )

    other_business_2_building_interest_retail: BooleanLike = Field(
        default="", description="Check if second other business occupancy is RETAIL"
    )

    other_business_2_building_interest_wholesale: BooleanLike = Field(
        default="", description="Check if second other business occupancy is WHOLESALE"
    )

    other_business_2_operations: str = Field(
        default="",
        description=(
            "Description of operations for second other business .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    q6_manufacture_relabel_repackage_others_products: BooleanLike = Field(
        ...,
        description=(
            "Indicate if involved in manufacture, relabeling, or repackaging of others' products"
        ),
    )

    q7_mixing_others_products: BooleanLike = Field(
        ..., description="Indicate if involved in mixing of others' products"
    )

    q8_rent_or_loan_equipment: BooleanLike = Field(
        ..., description="Indicate if equipment is rented or loaned to others"
    )

    equipment_1_equipment: str = Field(
        default="",
        description=(
            "Description of first item of equipment rented or loaned .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    equipment_1_type_small_tools: BooleanLike = Field(
        default="", description="Check if first equipment item is classified as SMALL TOOLS"
    )

    equipment_1_type_large_equipment: BooleanLike = Field(
        default="", description="Check if first equipment item is classified as LARGE EQUIPMENT"
    )

    equipment_1_instruction_given: BooleanLike = Field(
        default="", description="For first equipment item, indicate if instructions were given"
    )

    equipment_2_equipment: str = Field(
        default="",
        description=(
            "Description of second item of equipment rented or loaned .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    equipment_2_type_small_tools: BooleanLike = Field(
        default="", description="Check if second equipment item is classified as SMALL TOOLS"
    )

    equipment_2_type_large_equipment: BooleanLike = Field(
        default="", description="Check if second equipment item is classified as LARGE EQUIPMENT"
    )

    equipment_2_instruction_given: BooleanLike = Field(
        default="", description="For second equipment item, indicate if instructions were given"
    )

    q9_hours_after_9pm_or_24_hour: BooleanLike = Field(
        ..., description="Indicate if operations run after 9:00 P.M. and/or 24 hours"
    )

    start_time: str = Field(
        default="",
        description=(
            'Normal start time of operations .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    end_time: str = Field(
        default="",
        description=(
            'Normal end time of operations .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    twenty_four_hour_operations: BooleanLike = Field(
        default="", description="Check if operations run 24 hours"
    )


class Remarks(BaseModel):
    """Additional remarks and explanations"""

    remarks_line_1: str = Field(
        default="",
        description=(
            'Additional remarks, first line .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    remarks_line_2: str = Field(
        default="",
        description=(
            'Additional remarks, second line .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    remarks_line_3: str = Field(
        default="",
        description=(
            'Additional remarks, third line .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class BusinessOwnersSection(BaseModel):
    """BUSINESS OWNERS SECTION"""

    business_owners_section_header: BusinessOwnersSectionHeader = Field(
        ..., description="Business Owners Section Header"
    )
    premium: Premium = Field(..., description="Premium")
    blanket_summary: BlanketSummary = Field(..., description="Blanket Summary")
    general_information: GeneralInformation = Field(..., description="General Information")
    remarks: Remarks = Field(..., description="Remarks")
