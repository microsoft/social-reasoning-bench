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
    """Mortgage account references, balances, and property details for each borrower"""

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
            "Mortgage account reference number(s) for Borrower 2 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_outstanding_mortgage_balance: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Current outstanding mortgage balance for Borrower 1 in euro"
    )

    borrower_2_outstanding_mortgage_balance: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Current outstanding mortgage balance for Borrower 2 in euro"
    )

    borrower_1_estimated_current_value_of_primary_residence: Union[float, Literal["N/A", ""]] = (
        Field(
            ...,
            description="Estimated current market value of the primary residence for Borrower 1 in euro",
        )
    )

    borrower_2_estimated_current_value_of_primary_residence: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description="Estimated current market value of the primary residence for Borrower 2 in euro",
        )
    )

    borrower_1_monthly_mortgage_repayments_due: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Monthly mortgage repayment amount due for Borrower 1 in euro"
    )

    borrower_2_monthly_mortgage_repayments_due: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Monthly mortgage repayment amount due for Borrower 2 in euro"
    )

    borrower_1_correspondence_address: str = Field(
        ...,
        description=(
            "Mailing/correspondence address for Borrower 1 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_correspondence_address: str = Field(
        default="",
        description=(
            "Mailing/correspondence address for Borrower 2 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_property_address_if_different_to_correspondence_address: str = Field(
        default="",
        description=(
            "Address of the mortgaged property for Borrower 1, if different from "
            'correspondence address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    borrower_2_property_address_if_different_to_correspondence_address: str = Field(
        default="",
        description=(
            "Address of the mortgaged property for Borrower 2, if different from "
            'correspondence address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class BorrowerPersonalHouseholdInformation(BaseModel):
    """Names, personal details, and household composition for each borrower"""

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
            'Full name of Borrower 2 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
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
        default="", description="Number of dependent children for Borrower 1"
    )

    borrower_1_child_1_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of dependent child 1 for Borrower 1"
    )

    borrower_1_child_2_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of dependent child 2 for Borrower 1"
    )

    borrower_1_child_3_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of dependent child 3 for Borrower 1"
    )

    borrower_1_child_4_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of dependent child 4 for Borrower 1"
    )

    borrower_1_child_5_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of dependent child 5 for Borrower 1"
    )

    borrower_1_child_6_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of dependent child 6 for Borrower 1"
    )

    borrower_2_no_of_dependent_children: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of dependent children for Borrower 2"
    )

    borrower_2_child_1_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of dependent child 1 for Borrower 2"
    )

    borrower_2_child_2_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of dependent child 2 for Borrower 2"
    )

    borrower_2_child_3_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of dependent child 3 for Borrower 2"
    )

    borrower_2_child_4_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of dependent child 4 for Borrower 2"
    )

    borrower_2_child_5_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of dependent child 5 for Borrower 2"
    )

    borrower_2_child_6_age_yrs: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age in years of dependent child 6 for Borrower 2"
    )

    borrower_1_total_number_in_household: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of people living in Borrower 1's household"
    )

    borrower_2_total_number_in_household: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of people living in Borrower 2's household"
    )


class ContactInformationPreferredContactMethod(BaseModel):
    """Contact details and preferred contact methods for each borrower"""

    borrower_1_preferred_contact_method: Literal[
        "Home Telephone", "Mobile Telephone", "Work Telephone", "E-mail", "N/A", ""
    ] = Field(default="", description="Preferred method of contact for Borrower 1")

    borrower_2_preferred_contact_method: Literal[
        "Home Telephone", "Mobile Telephone", "Work Telephone", "E-mail", "N/A", ""
    ] = Field(default="", description="Preferred method of contact for Borrower 2")

    borrower_1_home_telephone: str = Field(
        default="",
        description=(
            'Home telephone number for Borrower 1 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_home_telephone_checkbox: BooleanLike = Field(
        default="",
        description="Indicates if home telephone is the preferred contact method for Borrower 1",
    )

    borrower_2_home_telephone: str = Field(
        default="",
        description=(
            'Home telephone number for Borrower 2 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_home_telephone_checkbox: BooleanLike = Field(
        default="",
        description="Indicates if home telephone is the preferred contact method for Borrower 2",
    )

    borrower_1_mobile_telephone: str = Field(
        default="",
        description=(
            "Mobile telephone number for Borrower 1 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_mobile_telephone_checkbox: BooleanLike = Field(
        default="",
        description="Indicates if mobile telephone is the preferred contact method for Borrower 1",
    )

    borrower_2_mobile_telephone: str = Field(
        default="",
        description=(
            "Mobile telephone number for Borrower 2 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_mobile_telephone_checkbox: BooleanLike = Field(
        default="",
        description="Indicates if mobile telephone is the preferred contact method for Borrower 2",
    )

    borrower_1_work_telephone: str = Field(
        default="",
        description=(
            'Work telephone number for Borrower 1 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_work_telephone_checkbox: BooleanLike = Field(
        default="",
        description="Indicates if work telephone is the preferred contact method for Borrower 1",
    )

    borrower_2_work_telephone: str = Field(
        default="",
        description=(
            'Work telephone number for Borrower 2 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_work_telephone_checkbox: BooleanLike = Field(
        default="",
        description="Indicates if work telephone is the preferred contact method for Borrower 2",
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


class EmploymentIncomeInformation(BaseModel):
    """Employment status, occupation, and employer details for each borrower"""

    borrower_1_employed_yes_checkbox: BooleanLike = Field(
        default="", description="Indicates that Borrower 1 is employed"
    )

    borrower_1_employed_no_checkbox: BooleanLike = Field(
        default="", description="Indicates that Borrower 1 is not employed"
    )

    borrower_2_employed_yes_checkbox: BooleanLike = Field(
        default="", description="Indicates that Borrower 2 is employed"
    )

    borrower_2_employed_no_checkbox: BooleanLike = Field(
        default="", description="Indicates that Borrower 2 is not employed"
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

    borrower_1_in_permanent_employment_yes_checkbox: BooleanLike = Field(
        default="", description="Indicates that Borrower 1 is in permanent employment"
    )

    borrower_1_in_permanent_employment_no_checkbox: BooleanLike = Field(
        default="", description="Indicates that Borrower 1 is not in permanent employment"
    )

    borrower_2_in_permanent_employment_yes_checkbox: BooleanLike = Field(
        default="", description="Indicates that Borrower 2 is in permanent employment"
    )

    borrower_2_in_permanent_employment_no_checkbox: BooleanLike = Field(
        default="", description="Indicates that Borrower 2 is not in permanent employment"
    )

    borrower_1_name_of_employer_length_of_service: str = Field(
        default="",
        description=(
            "Name of Borrower 1's employer and length of service .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_name_of_employer_length_of_service: str = Field(
        default="",
        description=(
            "Name of Borrower 2's employer and length of service .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ReasonforReviewArrears(BaseModel):
    """Explanation of why the mortgage is under review or in arrears"""

    reasons_for_review_arrears: str = Field(
        ...,
        description=(
            "Explanation of the reasons for the account review and/or arrears .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
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
    borrower_personal__household_information: BorrowerPersonalHouseholdInformation = Field(
        ..., description="Borrower Personal & Household Information"
    )
    contact_information__preferred_contact_method: ContactInformationPreferredContactMethod = Field(
        ..., description="Contact Information & Preferred Contact Method"
    )
    employment__income_information: EmploymentIncomeInformation = Field(
        ..., description="Employment & Income Information"
    )
    reason_for_reviewarrears: ReasonforReviewArrears = Field(
        ..., description="Reason for Review/Arrears"
    )
