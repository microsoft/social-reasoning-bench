from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class JointCreditAcknowledgment(BaseModel):
    """Signatures indicating intent to apply for joint credit"""

    borrower_signature_for_joint_credit: str = Field(
        default="",
        description=(
            "Borrower's signature indicating intent to apply for joint credit .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    co_borrower_signature_for_joint_credit: str = Field(
        default="",
        description=(
            "Co-Borrower's signature indicating intent to apply for joint credit .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ITypeofMortgageandTermsofLoan(BaseModel):
    """Mortgage type, case numbers, and loan terms"""

    mortgage_applied_for_va: BooleanLike = Field(
        ..., description="Check if the mortgage applied for is a VA loan"
    )

    mortgage_applied_for_conventional: BooleanLike = Field(
        ..., description="Check if the mortgage applied for is a Conventional loan"
    )

    mortgage_applied_for_usda_rural_housing_service: BooleanLike = Field(
        ..., description="Check if the mortgage applied for is a USDA/Rural Housing Service loan"
    )

    mortgage_applied_for_fha: BooleanLike = Field(
        ..., description="Check if the mortgage applied for is an FHA loan"
    )

    mortgage_applied_for_other_explain: str = Field(
        default="",
        description=(
            "Describe other type of mortgage if not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    agency_case_number: str = Field(
        default="",
        description=(
            "Agency-assigned case number for this loan .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    lender_case_number: str = Field(
        default="",
        description=(
            "Lender-assigned case or file number for this loan .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    loan_amount: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total mortgage amount requested in dollars"
    )

    interest_rate: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Proposed interest rate percentage for the loan"
    )

    number_of_months: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of months in the loan term"
    )

    amortization_type_fixed_rate: BooleanLike = Field(
        ..., description="Check if the amortization type is fixed rate"
    )

    amortization_type_other_explain: str = Field(
        default="",
        description=(
            "Describe other amortization type if not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    amortization_type_gpm: BooleanLike = Field(
        ..., description="Check if the amortization type is GPM (Graduated Payment Mortgage)"
    )

    amortization_type_arm_type: str = Field(
        default="",
        description=(
            "Specify the type of ARM (Adjustable Rate Mortgage) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IIPropertyInformationandPurposeofLoan(BaseModel):
    """Subject property details, loan purpose, occupancy, construction and refinance information, title and down payment source"""

    subject_property_address_street_city_state_zip: str = Field(
        ...,
        description=(
            "Full address of the subject property including street, city, state, and ZIP "
            'code .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    number_of_units: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of housing units in the subject property"
    )

    legal_description_of_subject_property: str = Field(
        ...,
        description=(
            "Full legal description of the subject property .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    year_built: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year the subject property was originally built"
    )

    purpose_of_loan_purchase: BooleanLike = Field(
        ..., description="Check if the loan purpose is to purchase the property"
    )

    purpose_of_loan_construction: BooleanLike = Field(
        ..., description="Check if the loan purpose is construction"
    )

    purpose_of_loan_refinance: BooleanLike = Field(
        ..., description="Check if the loan purpose is to refinance an existing loan"
    )

    purpose_of_loan_construction_permanent: BooleanLike = Field(
        ..., description="Check if the loan purpose is construction-permanent"
    )

    purpose_of_loan_other_explain: str = Field(
        default="",
        description=(
            "Describe other loan purpose if not listed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    property_will_be_primary_residence: BooleanLike = Field(
        ..., description="Check if the property will be the borrower's primary residence"
    )

    property_will_be_secondary_residence: BooleanLike = Field(
        ..., description="Check if the property will be a secondary residence"
    )

    property_will_be_investment: BooleanLike = Field(
        ..., description="Check if the property will be held as an investment"
    )

    year_lot_acquired: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Year the lot was acquired (for construction or construction-permanent loans)",
    )

    original_cost_of_lot: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Original purchase cost of the lot"
    )

    amount_existing_liens_on_lot: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total amount of existing liens on the lot"
    )

    present_value_of_lot: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current market value of the lot"
    )

    cost_of_improvements: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Cost of improvements to be made to the lot or property"
    )

    total_present_value_of_lot_and_cost_of_improvements_a_b: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Total of present value of lot plus cost of improvements (a + b)",
        )
    )

    year_acquired_refinance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year the property was acquired for refinance loans"
    )

    original_cost_refinance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Original cost of the property being refinanced"
    )

    amount_existing_liens_refinance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total amount of existing liens on the property being refinanced"
    )

    purpose_of_refinance: str = Field(
        default="",
        description=(
            'Describe the purpose of the refinance .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    describe_improvements: str = Field(
        default="",
        description=(
            "Description of improvements made or to be made .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    improvements_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount associated with the improvements"
    )

    improvements_cost: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Cost of the improvements themselves"
    )

    improvements_made: BooleanLike = Field(
        default="", description="Check if the improvements have already been made"
    )

    improvements_to_be_made: BooleanLike = Field(
        default="", description="Check if the improvements are to be made in the future"
    )

    title_will_be_held_in_what_names: str = Field(
        ...,
        description=(
            "Name or names in which the property title will be held .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    manner_in_which_title_will_be_held: str = Field(
        ...,
        description=(
            "Form of ownership in which title will be held (e.g., joint tenancy, tenants in "
            'common) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    estate_will_be_held_in_fee_simple: BooleanLike = Field(
        ..., description="Check if the estate will be held in fee simple"
    )

    estate_will_be_held_in_leasehold_expiration_date: str = Field(
        default="",
        description=(
            "Check if estate is leasehold and provide lease expiration date .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    source_of_down_payment_settlement_charges_and_or_subordinate_financing_explain: str = Field(
        ...,
        description=(
            "Explain the sources of down payment, settlement charges, and any subordinate "
            'financing .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class IIIBorrowerInformation(BaseModel):
    """Personal and address information for borrower and co-borrower"""

    borrower_name_include_jr_or_sr_if_applicable: str = Field(
        ...,
        description=(
            "Borrower's full legal name including suffix if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_social_security_number: str = Field(
        ..., description="Borrower's Social Security Number"
    )

    borrower_home_phone_incl_area_code: str = Field(
        ...,
        description=(
            "Borrower's home telephone number including area code .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_date_of_birth_mm_dd_yyyy: str = Field(
        ..., description="Borrower's date of birth"
    )  # YYYY-MM-DD format

    borrower_years_school: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of years of schooling completed by the borrower"
    )

    borrower_marital_status_married: BooleanLike = Field(
        ..., description="Check if the borrower is married"
    )

    borrower_marital_status_unmarried_include_single_divorced_widowed: BooleanLike = Field(
        ..., description="Check if the borrower is unmarried (single, divorced, or widowed)"
    )

    borrower_marital_status_separated: BooleanLike = Field(
        ..., description="Check if the borrower is separated"
    )

    borrower_dependents_not_listed_by_co_borrower_number: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of dependents not listed by the co-borrower"
    )

    borrower_dependents_not_listed_by_co_borrower_ages: str = Field(
        default="",
        description=(
            "Ages of dependents not listed by the co-borrower .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_present_address_street_city_state_zip: str = Field(
        ...,
        description=(
            "Borrower's current residence address including street, city, state, and ZIP "
            'code .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    borrower_present_address_own: BooleanLike = Field(
        ..., description="Check if the borrower owns the present residence"
    )

    borrower_present_address_rent: BooleanLike = Field(
        ..., description="Check if the borrower rents the present residence"
    )

    borrower_present_address_number_of_years: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of years the borrower has lived at the present address"
    )

    borrower_mailing_address_if_different_from_present_address: str = Field(
        default="",
        description=(
            "Borrower's mailing address if different from present address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    borrower_former_address_street_city_state_zip: str = Field(
        default="",
        description=(
            "Borrower's former address if present address is less than two years .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    borrower_former_address_own: BooleanLike = Field(
        default="", description="Check if the borrower owned the former residence"
    )

    borrower_former_address_rent: BooleanLike = Field(
        default="", description="Check if the borrower rented the former residence"
    )

    borrower_former_address_number_of_years: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years the borrower lived at the former address"
    )

    co_borrower_name_include_jr_or_sr_if_applicable: str = Field(
        default="",
        description=(
            "Co-borrower's full legal name including suffix if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    co_borrower_social_security_number: str = Field(
        default="", description="Co-borrower's Social Security Number"
    )

    co_borrower_home_phone_incl_area_code: str = Field(
        default="",
        description=(
            "Co-borrower's home telephone number including area code .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    co_borrower_date_of_birth_mm_dd_yyyy: str = Field(
        default="", description="Co-borrower's date of birth"
    )  # YYYY-MM-DD format

    co_borrower_years_school: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of years of schooling completed by the co-borrower"
    )

    co_borrower_marital_status_married: BooleanLike = Field(
        default="", description="Check if the co-borrower is married"
    )

    co_borrower_marital_status_unmarried_include_single_divorced_widowed: BooleanLike = Field(
        default="",
        description="Check if the co-borrower is unmarried (single, divorced, or widowed)",
    )

    co_borrower_marital_status_separated: BooleanLike = Field(
        default="", description="Check if the co-borrower is separated"
    )

    co_borrower_dependents_not_listed_by_borrower_number: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of dependents not listed by the borrower"
    )

    co_borrower_dependents_not_listed_by_borrower_ages: str = Field(
        default="",
        description=(
            "Ages of dependents not listed by the borrower .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    co_borrower_present_address_street_city_state_zip: str = Field(
        default="",
        description=(
            "Co-borrower's current residence address including street, city, state, and ZIP "
            'code .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    co_borrower_present_address_own: BooleanLike = Field(
        default="", description="Check if the co-borrower owns the present residence"
    )

    co_borrower_present_address_rent: BooleanLike = Field(
        default="", description="Check if the co-borrower rents the present residence"
    )

    co_borrower_present_address_number_of_years: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years the co-borrower has lived at the present address"
    )

    co_borrower_mailing_address_if_different_from_present_address: str = Field(
        default="",
        description=(
            "Co-borrower's mailing address if different from present address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    co_borrower_former_address_street_city_state_zip: str = Field(
        default="",
        description=(
            "Co-borrower's former address if present address is less than two years .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    co_borrower_former_address_own: BooleanLike = Field(
        default="", description="Check if the co-borrower owned the former residence"
    )

    co_borrower_former_address_rent: BooleanLike = Field(
        default="", description="Check if the co-borrower rented the former residence"
    )

    co_borrower_former_address_number_of_years: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years the co-borrower lived at the former address"
    )


class IVEmploymentInformation(BaseModel):
    """Current and prior employment details for borrower and co-borrower"""

    borrower_name_address_of_employer_current: str = Field(
        ...,
        description=(
            "Name and address of the borrower's current employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_self_employed_current: BooleanLike = Field(
        default="", description="Check if the borrower is self-employed at the current job"
    )

    borrower_years_on_this_job: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of years the borrower has been in the current job"
    )

    borrower_years_employed_in_this_line_of_work_profession: Union[float, Literal["N/A", ""]] = (
        Field(
            ...,
            description="Total years the borrower has worked in this line of work or profession",
        )
    )

    borrower_position_title_type_of_business_current: str = Field(
        ...,
        description=(
            "Borrower's current job title, position, and type of business .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    borrower_business_phone_incl_area_code_current: str = Field(
        ...,
        description=(
            "Borrower's current business phone number including area code .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    borrower_name_address_of_employer_prior_1: str = Field(
        default="",
        description=(
            "Name and address of the borrower's prior employer (most recent prior) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    borrower_self_employed_prior_1: BooleanLike = Field(
        default="", description="Check if the borrower was self-employed at this prior job"
    )

    borrower_dates_of_employment_from_to_prior_1: str = Field(
        default="",
        description=(
            "Employment dates (from–to) for this prior job .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_monthly_income_prior_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly income from this prior job"
    )

    borrower_position_title_type_of_business_prior_1: str = Field(
        default="",
        description=(
            "Job title, position, and type of business for this prior job .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    borrower_business_phone_incl_area_code_prior_1: str = Field(
        default="",
        description=(
            "Business phone number including area code for this prior job .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    borrower_name_address_of_employer_prior_2: str = Field(
        default="",
        description=(
            "Name and address of the borrower's second prior employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_dates_of_employment_from_to_prior_2: str = Field(
        default="",
        description=(
            "Employment dates (from–to) for this second prior job .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_monthly_income_prior_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly income from this second prior job"
    )

    borrower_position_title_type_of_business_prior_2: str = Field(
        default="",
        description=(
            "Job title, position, and type of business for this second prior job .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    borrower_business_phone_incl_area_code_prior_2: str = Field(
        default="",
        description=(
            "Business phone number including area code for this second prior job .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    co_borrower_name_address_of_employer_current: str = Field(
        default="",
        description=(
            "Name and address of the co-borrower's current employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    co_borrower_self_employed_current: BooleanLike = Field(
        default="", description="Check if the co-borrower is self-employed at the current job"
    )

    co_borrower_years_on_this_job: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years the co-borrower has been in the current job"
    )

    co_borrower_years_employed_in_this_line_of_work_profession: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Total years the co-borrower has worked in this line of work or profession",
        )
    )

    co_borrower_position_title_type_of_business_current: str = Field(
        default="",
        description=(
            "Co-borrower's current job title, position, and type of business .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    co_borrower_business_phone_incl_area_code_current: str = Field(
        default="",
        description=(
            "Co-borrower's current business phone number including area code .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    co_borrower_name_address_of_employer_prior_1: str = Field(
        default="",
        description=(
            "Name and address of the co-borrower's prior employer (most recent prior) .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    co_borrower_self_employed_prior_1: BooleanLike = Field(
        default="", description="Check if the co-borrower was self-employed at this prior job"
    )

    co_borrower_dates_of_employment_from_to_prior_1: str = Field(
        default="",
        description=(
            "Employment dates (from–to) for this prior job .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    co_borrower_monthly_income_prior_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly income from this prior job"
    )

    co_borrower_position_title_type_of_business_prior_1: str = Field(
        default="",
        description=(
            "Job title, position, and type of business for this prior job .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    co_borrower_business_phone_incl_area_code_prior_1: str = Field(
        default="",
        description=(
            "Business phone number including area code for this prior job .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    co_borrower_name_address_of_employer_prior_2: str = Field(
        default="",
        description=(
            "Name and address of the co-borrower's second prior employer .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    co_borrower_dates_of_employment_from_to_prior_2: str = Field(
        default="",
        description=(
            "Employment dates (from–to) for this second prior job .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    co_borrower_monthly_income_prior_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly income from this second prior job"
    )

    co_borrower_position_title_type_of_business_prior_2: str = Field(
        default="",
        description=(
            "Job title, position, and type of business for this second prior job .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    co_borrower_business_phone_incl_area_code_prior_2: str = Field(
        default="",
        description=(
            "Business phone number including area code for this second prior job .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class UniformResidentialLoanApplication(BaseModel):
    """
    Uniform Residential Loan Application

    This application is designed to be completed by the applicant(s) with the Lender's assistance. Applicants should complete this form as Borrower or Co-Borrower, as applicable. Co-Borrower information must also be provided (and the appropriate box checked) when the income or assets of a person other than the Borrower (including the Borrower's spouse) will be used as a basis for loan qualification or the income or assets of the Borrower's spouse or other person who has community property rights pursuant to applicable law will not be used as a basis for loan qualification, but his or her liabilities must be considered because the spouse or other person has community property rights pursuant to applicable law and Borrower resides in a community property state, the security property is located in a community property state, or the Borrower is relying on other property located in a community property state as a basis for repayment of the loan.
    """

    joint_credit_acknowledgment: JointCreditAcknowledgment = Field(
        ..., description="Joint Credit Acknowledgment"
    )
    i_type_of_mortgage_and_terms_of_loan: ITypeofMortgageandTermsofLoan = Field(
        ..., description="I. Type of Mortgage and Terms of Loan"
    )
    ii_property_information_and_purpose_of_loan: IIPropertyInformationandPurposeofLoan = Field(
        ..., description="II. Property Information and Purpose of Loan"
    )
    iii_borrower_information: IIIBorrowerInformation = Field(
        ..., description="III. Borrower Information"
    )
    iv_employment_information: IVEmploymentInformation = Field(
        ..., description="IV. Employment Information"
    )
