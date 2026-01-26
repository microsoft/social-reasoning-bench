from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AccountPropertyDetails(BaseModel):
    """Mortgage account references, balances, property values and repayment details"""

    borrower_1_mortgage_account_reference_nos: str = Field(
        ...,
        description=(
            "Mortgage account reference number(s) for Borrower 1 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_mortgage_account_reference_nos: str = Field(
        default="",
        description=(
            "Mortgage account reference number(s) for Borrower 2 (if applicable) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    borrower_1_outstanding_mortgage_balance_eur: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Current outstanding mortgage balance for Borrower 1 in euro"
    )

    borrower_2_outstanding_mortgage_balance_eur: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current outstanding mortgage balance for Borrower 2 in euro (if applicable)",
    )

    borrower_1_estimated_current_value_primary_residence_eur: Union[float, Literal["N/A", ""]] = (
        Field(
            ...,
            description="Estimated current market value of Borrower 1's primary residence in euro",
        )
    )

    borrower_2_estimated_current_value_primary_residence_eur: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description=(
                "Estimated current market value of Borrower 2's primary residence in euro (if "
                "applicable)"
            ),
        )
    )

    borrower_1_monthly_mortgage_repayments_due_eur: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Monthly mortgage repayment amount due for Borrower 1 in euro"
    )

    borrower_2_monthly_mortgage_repayments_due_eur: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Monthly mortgage repayment amount due for Borrower 2 in euro (if applicable)",
    )

    borrower_1_correspondence_address: str = Field(
        ...,
        description=(
            "Postal correspondence address for Borrower 1 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_correspondence_address: str = Field(
        default="",
        description=(
            "Postal correspondence address for Borrower 2 (if different/applicable) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    borrower_1_property_address_if_different_to_correspondence_address: str = Field(
        default="",
        description=(
            "Physical property address for Borrower 1 if different from correspondence "
            'address .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    borrower_2_property_address_if_different_to_correspondence_address: str = Field(
        default="",
        description=(
            "Physical property address for Borrower 2 if different from correspondence "
            'address .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class BorrowerPersonalDetails(BaseModel):
    """Names, marital status, dates of birth and household composition"""

    borrower_1_name: str = Field(
        ...,
        description=(
            'Full name of Borrower 1 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    borrower_2_name: str = Field(
        default="",
        description=(
            "Full name of Borrower 2 (if applicable) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_marital_status: str = Field(
        default="",
        description=(
            'Current marital status of Borrower 1 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_marital_status: str = Field(
        default="",
        description=(
            'Current marital status of Borrower 2 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_date_of_birth_dd_mm_yyyy: str = Field(
        ..., description="Date of birth of Borrower 1 in DD/MM/YYYY format"
    )  # YYYY-MM-DD format

    borrower_2_date_of_birth_dd_mm_yyyy: str = Field(
        default="", description="Date of birth of Borrower 2 in DD/MM/YYYY format"
    )  # YYYY-MM-DD format

    borrower_1_no_of_dependent_children: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of dependent children for Borrower 1"
    )

    borrower_2_no_of_dependent_children: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of dependent children for Borrower 2"
    )

    borrower_1_child_1_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of Borrower 1's first dependent child"
    )

    borrower_1_child_2_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of Borrower 1's second dependent child"
    )

    borrower_1_child_3_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of Borrower 1's third dependent child"
    )

    borrower_1_child_4_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of Borrower 1's fourth dependent child"
    )

    borrower_1_child_5_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of Borrower 1's fifth dependent child"
    )

    borrower_1_child_6_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of Borrower 1's sixth dependent child"
    )

    borrower_2_child_1_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of Borrower 2's first dependent child"
    )

    borrower_2_child_2_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of Borrower 2's second dependent child"
    )

    borrower_2_child_3_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of Borrower 2's third dependent child"
    )

    borrower_2_child_4_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of Borrower 2's fourth dependent child"
    )

    borrower_2_child_5_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of Borrower 2's fifth dependent child"
    )

    borrower_2_child_6_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of Borrower 2's sixth dependent child"
    )

    total_number_in_household: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of people living in the household"
    )


class ContactInformation(BaseModel):
    """Telephone numbers, email addresses and preferred contact methods"""

    preferred_contact_method_home_telephone: BooleanLike = Field(
        default="", description="Tick if home telephone is the preferred contact method"
    )

    preferred_contact_method_mobile_telephone: BooleanLike = Field(
        default="", description="Tick if mobile telephone is the preferred contact method"
    )

    preferred_contact_method_work_telephone: BooleanLike = Field(
        default="", description="Tick if work telephone is the preferred contact method"
    )

    preferred_contact_method_e_mail_address: BooleanLike = Field(
        default="", description="Tick if email is the preferred contact method"
    )

    borrower_1_home_telephone: str = Field(
        default="",
        description=(
            'Home telephone number for Borrower 1 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_home_telephone: str = Field(
        default="",
        description=(
            'Home telephone number for Borrower 2 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_mobile_telephone: str = Field(
        default="",
        description=(
            "Mobile telephone number for Borrower 1 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_mobile_telephone: str = Field(
        default="",
        description=(
            "Mobile telephone number for Borrower 2 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_work_telephone: str = Field(
        default="",
        description=(
            'Work telephone number for Borrower 1 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_work_telephone: str = Field(
        default="",
        description=(
            'Work telephone number for Borrower 2 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_e_mail_address: str = Field(
        default="",
        description=(
            'Email address for Borrower 1 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_e_mail_address: str = Field(
        default="",
        description=(
            'Email address for Borrower 2 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class EmploymentDetails(BaseModel):
    """Employment status, occupation, permanence and employer details"""

    borrower_1_employed_y_n: BooleanLike = Field(
        default="", description="Indicate whether Borrower 1 is currently employed"
    )

    borrower_2_employed_y_n: BooleanLike = Field(
        default="", description="Indicate whether Borrower 2 is currently employed"
    )

    borrower_1_self_employed_details: str = Field(
        default="",
        description=(
            "Details of Borrower 1's self-employment, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_self_employed_details: str = Field(
        default="",
        description=(
            "Details of Borrower 2's self-employment, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_occupation_if_unemployed_give_previous_occupation: str = Field(
        default="",
        description=(
            "Current occupation of Borrower 1, or previous occupation if unemployed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    borrower_2_occupation_if_unemployed_give_previous_occupation: str = Field(
        default="",
        description=(
            "Current occupation of Borrower 2, or previous occupation if unemployed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    borrower_1_in_permanent_employment_yes: BooleanLike = Field(
        default="", description="Tick if Borrower 1 is in permanent employment (Yes option)"
    )

    borrower_1_in_permanent_employment_no: BooleanLike = Field(
        default="", description="Tick if Borrower 1 is not in permanent employment (No option)"
    )

    borrower_2_in_permanent_employment_yes: BooleanLike = Field(
        default="", description="Tick if Borrower 2 is in permanent employment (Yes option)"
    )

    borrower_2_in_permanent_employment_no: BooleanLike = Field(
        default="", description="Tick if Borrower 2 is not in permanent employment (No option)"
    )

    borrower_1_name_of_employer: str = Field(
        default="",
        description=(
            'Name of Borrower 1\'s current employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_length_of_service: str = Field(
        default="",
        description=(
            "Length of time Borrower 1 has been with current employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_name_of_employer: str = Field(
        default="",
        description=(
            'Name of Borrower 2\'s current employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_length_of_service: str = Field(
        default="",
        description=(
            "Length of time Borrower 2 has been with current employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ReasonforReviewArrears(BaseModel):
    """Explanation of why the account is under review or in arrears"""

    reasons_for_review_arrears: str = Field(
        ...,
        description=(
            "Explanation of the reasons for the account review and/or mortgage arrears .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class IndustryStandardFinancialStatement(BaseModel):
    """
    Industry Standard Financial Statement

    ''
    """

    account__property_details: AccountPropertyDetails = Field(
        ..., description="Account & Property Details"
    )
    borrower_personal_details: BorrowerPersonalDetails = Field(
        ..., description="Borrower Personal Details"
    )
    contact_information: ContactInformation = Field(..., description="Contact Information")
    employment_details: EmploymentDetails = Field(..., description="Employment Details")
    reason_for_review__arrears: ReasonforReviewArrears = Field(
        ..., description="Reason for Review / Arrears"
    )
