from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Header(BaseModel):
    """Overall statement information"""

    date: str = Field(
        ..., description="Date the personal financial statement is completed"
    )  # YYYY-MM-DD format


class Section1IndividualInformation(BaseModel):
    """Personal information about the individual applicant"""

    name: str = Field(
        ...,
        description=(
            "Individual applicant's full legal name .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Individual applicant\'s street address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for the individual's residence .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    social_security: str = Field(..., description="Individual applicant's Social Security number")

    date_of_birth: str = Field(
        ..., description="Individual applicant's date of birth"
    )  # YYYY-MM-DD format

    position_or_occupation: str = Field(
        ...,
        description=(
            "Individual applicant's current job title or occupation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    business_name: str = Field(
        default="",
        description=(
            "Name of the individual's employer or business .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    business_address: str = Field(
        default="",
        description=(
            "Street address of the individual's employer or business .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip_business: str = Field(
        default="",
        description=(
            "City, state, and ZIP code for the business address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    length_at_present_address: str = Field(
        default="",
        description=(
            "How long the individual has lived at the current address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    length_of_employment: str = Field(
        default="",
        description=(
            "How long the individual has been employed at current job .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    res_phone: str = Field(
        default="",
        description=(
            "Individual applicant's residential phone number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    bus_phone: str = Field(
        default="",
        description=(
            "Individual applicant's business phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    bankruptcy_settlement_yes: BooleanLike = Field(
        default="", description="Check if the answer to the bankruptcy/settlement question is Yes"
    )

    bankruptcy_settlement_no: BooleanLike = Field(
        default="", description="Check if the answer to the bankruptcy/settlement question is No"
    )

    defendant_legal_action_yes: BooleanLike = Field(
        default="",
        description="Check if the individual is currently a defendant in a suit or legal action",
    )

    defendant_legal_action_no: BooleanLike = Field(
        default="",
        description="Check if the individual is not a defendant in any suit or legal action",
    )

    unsatisfied_judgments_tax_liens_yes: BooleanLike = Field(
        default="",
        description="Check if the individual is subject to unsatisfied judgments or tax liens",
    )

    unsatisfied_judgments_tax_liens_no: BooleanLike = Field(
        default="",
        description="Check if the individual is not subject to unsatisfied judgments or tax liens",
    )

    irs_audit_when: str = Field(
        default="",
        description=(
            "Provide date(s) or year(s) of any IRS audits, or 'never' if none .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Section2OtherPartyInformation(BaseModel):
    """Personal information about the other party whose income/assets may be relied upon"""

    other_party_name: str = Field(
        default="",
        description=(
            'Other party\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    other_party_address: str = Field(
        default="",
        description=(
            'Other party\'s street address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    other_party_city_state_zip: str = Field(
        default="",
        description=(
            "City, state, and ZIP code for the other party's residence .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_party_social_security: str = Field(
        default="", description="Other party's Social Security number"
    )

    other_party_date_of_birth: str = Field(
        default="", description="Other party's date of birth"
    )  # YYYY-MM-DD format

    other_party_position_or_occupation: str = Field(
        default="",
        description=(
            "Other party's current job title or occupation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_party_business_name: str = Field(
        default="",
        description=(
            "Name of the other party's employer or business .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_party_business_address: str = Field(
        default="",
        description=(
            "Street address of the other party's employer or business .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_party_business_city_state_zip: str = Field(
        default="",
        description=(
            "City, state, and ZIP code for the other party's business address .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_party_length_at_present_address: str = Field(
        default="",
        description=(
            "How long the other party has lived at the current address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_party_length_of_employment: str = Field(
        default="",
        description=(
            "How long the other party has been employed at current job .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_party_res_phone: str = Field(
        default="",
        description=(
            "Other party's residential phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    other_party_bus_phone: str = Field(
        default="",
        description=(
            'Other party\'s business phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class Section3StatementofFinancialCondition(BaseModel):
    """Assets, liabilities, net worth as of a specific date"""

    statement_financial_condition_date: str = Field(
        ..., description="Effective date of the statement of financial condition"
    )  # YYYY-MM-DD format

    assets_cash_checking_savings_cds_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual share of cash, checking, savings, and CDs"
    )

    assets_cash_checking_savings_cds_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint share of cash, checking, savings, and CDs"
    )

    assets_us_govt_marketable_securities_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual share of U.S. government and marketable securities"
    )

    assets_us_govt_marketable_securities_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint share of U.S. government and marketable securities"
    )

    assets_non_marketable_securities_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual share of non-marketable securities"
    )

    assets_non_marketable_securities_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint share of non-marketable securities"
    )

    assets_securities_margin_accounts_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual share of securities held by broker in margin accounts"
    )

    assets_securities_margin_accounts_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint share of securities held by broker in margin accounts"
    )

    assets_restricted_control_margin_stocks_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual share of restricted, control, or margin account stocks"
    )

    assets_restricted_control_margin_stocks_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint share of restricted, control, or margin account stocks"
    )

    assets_real_estate_owned_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual share of real estate owned"
    )

    assets_real_estate_owned_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint share of real estate owned"
    )

    assets_accounts_loans_notes_receivable_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual share of accounts, loans, and notes receivable"
    )

    assets_accounts_loans_notes_receivable_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint share of accounts, loans, and notes receivable"
    )

    assets_automobiles_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual share of automobile value"
    )

    assets_automobiles_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint share of automobile value"
    )

    assets_cash_surrender_value_life_insurance_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual share of cash surrender value of life insurance"
    )

    assets_cash_surrender_value_life_insurance_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint share of cash surrender value of life insurance"
    )

    assets_vested_interest_deferred_comp_profit_sharing_individual: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Individual vested interest in deferred compensation or profit-sharing plans",
    )

    assets_vested_interest_deferred_comp_profit_sharing_joint: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Joint vested interest in deferred compensation or profit-sharing plans",
        )
    )

    assets_business_ventures_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual share of business ventures value"
    )

    assets_business_ventures_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint share of business ventures value"
    )

    assets_other_assets_personal_property_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual share of other assets or personal property"
    )

    assets_other_assets_personal_property_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint share of other assets or personal property"
    )

    total_assets_individual: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total individual assets"
    )

    total_assets_joint: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total joint assets"
    )

    net_worth_individual: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Individual net worth (total assets minus total liabilities)"
    )

    net_worth_joint: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Joint net worth (total assets minus total liabilities)"
    )

    total_liabilities_and_net_worth_individual: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Sum of individual total liabilities and net worth"
    )

    total_liabilities_and_net_worth_joint: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Sum of joint total liabilities and net worth"
    )

    liabilities_notes_payable_banks_others_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual notes payable to banks and others"
    )

    liabilities_notes_payable_banks_others_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint notes payable to banks and others"
    )

    liabilities_due_to_brokers_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual amounts due to brokers"
    )

    liabilities_due_to_brokers_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint amounts due to brokers"
    )

    liabilities_amounts_payable_others_secured_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual secured amounts payable to others"
    )

    liabilities_amounts_payable_others_secured_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint secured amounts payable to others"
    )

    liabilities_amounts_payable_others_unsecured_individual: Union[float, Literal["N/A", ""]] = (
        Field(default="", description="Individual unsecured amounts payable to others")
    )

    liabilities_amounts_payable_others_unsecured_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint unsecured amounts payable to others"
    )

    liabilities_accounts_bills_due_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual accounts and bills due"
    )

    liabilities_accounts_bills_due_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint accounts and bills due"
    )

    liabilities_unpaid_income_tax_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual unpaid income tax"
    )

    liabilities_unpaid_income_tax_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint unpaid income tax"
    )

    liabilities_other_unpaid_taxes_interest_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual other unpaid taxes and interest"
    )

    liabilities_other_unpaid_taxes_interest_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint other unpaid taxes and interest"
    )

    liabilities_real_estate_mortgages_payable_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual real estate mortgages payable"
    )

    liabilities_real_estate_mortgages_payable_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint real estate mortgages payable"
    )

    total_liabilities_individual: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total individual liabilities"
    )

    total_liabilities_joint: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total joint liabilities"
    )


class Section4AnnualIncomeExpendituresandContingentLiabilities(BaseModel):
    """Income, expenses, and contingent liabilities for the year ended"""

    annual_income_year_ended: str = Field(
        ..., description="Year-end date for the annual income and expenditures"
    )  # YYYY-MM-DD format

    salary_bonuses_commissions_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual salary, bonuses, and commissions for the year"
    )

    salary_bonuses_commissions_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint salary, bonuses, and commissions for the year"
    )

    dividends_interest_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual dividends and interest income for the year"
    )

    dividends_interest_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint dividends and interest income for the year"
    )

    real_estate_income_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual real estate income for the year"
    )

    real_estate_income_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint real estate income for the year"
    )

    other_income_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual other income for the year"
    )

    other_income_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint other income for the year"
    )

    total_income_individual: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total individual annual income"
    )

    total_income_joint: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total joint annual income"
    )

    mortgage_rental_payments_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual annual mortgage or rental payments"
    )

    mortgage_rental_payments_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint annual mortgage or rental payments"
    )

    real_estate_taxes_assessments_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual annual real estate taxes and assessments"
    )

    real_estate_taxes_assessments_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint annual real estate taxes and assessments"
    )

    taxes_federal_state_local_individual: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Individual annual federal, state, and local taxes (excluding real estate)",
    )

    taxes_federal_state_local_joint: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Joint annual federal, state, and local taxes (excluding real estate)",
    )

    insurance_payments_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual annual insurance payments"
    )

    insurance_payments_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint annual insurance payments"
    )

    other_contract_payments_individual: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Individual annual payments on other contracts (car, credit cards, etc.)",
    )

    other_contract_payments_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint annual payments on other contracts (car, credit cards, etc.)"
    )

    alimony_child_support_other_obligations_individual: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Individual annual alimony, child support, or other unrevealed obligations",
    )

    alimony_child_support_other_obligations_joint: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Joint annual alimony, child support, or other unrevealed obligations",
    )

    other_expenses_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual other annual expenses not listed elsewhere"
    )

    other_expenses_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint other annual expenses not listed elsewhere"
    )

    total_expenditures_individual: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total individual annual expenditures"
    )

    total_expenditures_joint: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total joint annual expenditures"
    )

    contingent_liabilities_any_yes: BooleanLike = Field(
        default="", description="Check if the applicant has any contingent liabilities"
    )

    contingent_liabilities_any_no: BooleanLike = Field(
        default="", description="Check if the applicant has no contingent liabilities"
    )

    contingent_liabilities_endorser_comaker_guarantor_individual: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Individual contingent liabilities as endorser, co-maker, or guarantor",
    )

    contingent_liabilities_endorser_comaker_guarantor_joint: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Joint contingent liabilities as endorser, co-maker, or guarantor",
        )
    )

    contingent_on_leases_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual contingent liabilities on leases"
    )

    contingent_on_leases_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint contingent liabilities on leases"
    )

    contingent_on_contracts_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Individual contingent liabilities on contracts"
    )

    contingent_on_contracts_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Joint contingent liabilities on contracts"
    )

    contingent_pending_legal_actions_individual: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated amount of individual contingent liabilities from pending legal actions"
        ),
    )

    contingent_pending_legal_actions_joint: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Estimated amount of joint contingent liabilities from pending legal actions",
    )

    contingent_contested_income_tax_liens_individual: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated amount of individual contingent liabilities from contested income tax liens"
        ),
    )

    contingent_contested_income_tax_liens_joint: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated amount of joint contingent liabilities from contested income tax liens"
        ),
    )

    contingent_estimated_capital_gains_tax_unrealized_appreciation_individual: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="",
        description="Estimated individual capital gains tax on unrealized asset appreciation",
    )

    contingent_estimated_capital_gains_tax_unrealized_appreciation_joint: Union[
        float, Literal["N/A", ""]
    ] = Field(
        default="", description="Estimated joint capital gains tax on unrealized asset appreciation"
    )

    contingent_other_special_debt_circumstances_individual: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description=(
                "Estimated amount of individual contingent liabilities from other special debts "
                "or circumstances"
            ),
        )
    )

    contingent_other_special_debt_circumstances_joint: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Estimated amount of joint contingent liabilities from other special debts or "
            "circumstances"
        ),
    )

    contingent_if_yes_describe: str = Field(
        default="",
        description=(
            "Description of contingent liabilities if any of the contingent questions are "
            'answered yes .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    total_contingent_liabilities_individual: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total individual contingent liabilities"
    )

    total_contingent_liabilities_joint: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total joint contingent liabilities"
    )


class CnbStlBankPersonalFinancialStatement(BaseModel):
    """
        CNB STL BANK
    PERSONAL FINANCIAL STATEMENT

        IMPORTANT: Read these directions before completing this Statement
        If you are applying for individual credit in your own name and are relying only on your own income, or assets and not the income or assets of another person as the basis for repayment of the credit requested, or if this statement relates to your guaranty of the indebtedness of other person(s), firm(s), or corporation(s), complete only Sections 1, 3, and 4.
        If you are applying for individual credit but are relying on income from alimony, child support, or separate maintenance or on the income or assets of another person as a basis for repayment of the credit requested, complete all Sections. Provide information in Section 2 about the person whose alimony, support, or maintenance payments or income or assets you are relying on. Alimony, child support, or separate maintenance income need not be revealed if you do not wish to have it considered as a basis for repaying this obligation.
    """

    header: Header = Field(..., description="Header")
    section_1___individual_information: Section1IndividualInformation = Field(
        ..., description="Section 1 - Individual Information"
    )
    section_2___other_party_information: Section2OtherPartyInformation = Field(
        ..., description="Section 2 - Other Party Information"
    )
    section_3___statement_of_financial_condition: Section3StatementofFinancialCondition = Field(
        ..., description="Section 3 - Statement of Financial Condition"
    )
    section_4___annual_income_expenditures_and_contingent_liabilities: Section4AnnualIncomeExpendituresandContingentLiabilities = Field(
        ..., description="Section 4 - Annual Income, Expenditures, and Contingent Liabilities"
    )
