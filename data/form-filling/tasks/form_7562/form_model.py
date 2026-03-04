from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class IndustryStandardFinancialStatement(BaseModel):
    """
    Industry Standard Financial Statement

    ''
    """

    borrower_1_name: str = Field(
        ...,
        description=(
            'Full name of borrower 1 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    borrower_2_name: str = Field(
        default="",
        description=(
            "Full name of borrower 2 (if applicable) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_mortgage_account_reference_nos: str = Field(
        ...,
        description=(
            "Mortgage account reference number(s) for borrower 1 .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_mortgage_account_reference_nos: str = Field(
        default="",
        description=(
            "Mortgage account reference number(s) for borrower 2 (if applicable) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    borrower_1_outstanding_mortgage_balance_eur: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Current outstanding mortgage balance for borrower 1 in euro"
    )

    borrower_2_outstanding_mortgage_balance_eur: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Current outstanding mortgage balance for borrower 2 in euro (if applicable)",
    )

    borrower_1_estimated_current_value_primary_residence_eur: Union[float, Literal["N/A", ""]] = (
        Field(
            ...,
            description="Estimated current market value of borrower 1's primary residence in euro",
        )
    )

    borrower_2_estimated_current_value_primary_residence_eur: Union[float, Literal["N/A", ""]] = (
        Field(
            default="",
            description=(
                "Estimated current market value of borrower 2's primary residence in euro (if "
                "applicable)"
            ),
        )
    )

    borrower_1_monthly_mortgage_repayments_due_eur: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Monthly mortgage repayment amount due for borrower 1 in euro"
    )

    borrower_2_monthly_mortgage_repayments_due_eur: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Monthly mortgage repayment amount due for borrower 2 in euro (if applicable)",
    )

    borrower_1_correspondence_address_line_1: str = Field(
        ...,
        description=(
            "First line of borrower 1's correspondence address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_correspondence_address_line_2: str = Field(
        default="",
        description=(
            "Second line of borrower 1's correspondence address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_correspondence_address_line_3: str = Field(
        default="",
        description=(
            "Third line of borrower 1's correspondence address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_correspondence_address_line_1: str = Field(
        default="",
        description=(
            "First line of borrower 2's correspondence address (if applicable) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    borrower_2_correspondence_address_line_2: str = Field(
        default="",
        description=(
            "Second line of borrower 2's correspondence address (if applicable) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    borrower_2_correspondence_address_line_3: str = Field(
        default="",
        description=(
            "Third line of borrower 2's correspondence address (if applicable) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    property_address_line_1_if_different_to_correspondence_address: str = Field(
        default="",
        description=(
            "First line of the property address if different from correspondence address "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    property_address_line_2_if_different_to_correspondence_address: str = Field(
        default="",
        description=(
            "Second line of the property address if different from correspondence address "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    property_address_line_3_if_different_to_correspondence_address: str = Field(
        default="",
        description=(
            "Third line of the property address if different from correspondence address "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    property_address_line_4_if_different_to_correspondence_address: str = Field(
        default="",
        description=(
            "Fourth line of the property address if different from correspondence address "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    borrower_1_home_telephone: str = Field(
        default="",
        description=(
            'Home telephone number for borrower 1 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_home_telephone_preferred_contact_method: BooleanLike = Field(
        default="",
        description="Tick if home telephone is the preferred contact method for borrower 1",
    )

    borrower_2_home_telephone: str = Field(
        default="",
        description=(
            'Home telephone number for borrower 2 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_home_telephone_preferred_contact_method: BooleanLike = Field(
        default="",
        description="Tick if home telephone is the preferred contact method for borrower 2",
    )

    borrower_1_mobile_telephone: str = Field(
        default="",
        description=(
            "Mobile telephone number for borrower 1 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_mobile_telephone_preferred_contact_method: BooleanLike = Field(
        default="",
        description="Tick if mobile telephone is the preferred contact method for borrower 1",
    )

    borrower_2_mobile_telephone: str = Field(
        default="",
        description=(
            "Mobile telephone number for borrower 2 .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_mobile_telephone_preferred_contact_method: BooleanLike = Field(
        default="",
        description="Tick if mobile telephone is the preferred contact method for borrower 2",
    )

    borrower_1_work_telephone: str = Field(
        default="",
        description=(
            'Work telephone number for borrower 1 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_work_telephone_preferred_contact_method: BooleanLike = Field(
        default="",
        description="Tick if work telephone is the preferred contact method for borrower 1",
    )

    borrower_2_work_telephone: str = Field(
        default="",
        description=(
            'Work telephone number for borrower 2 .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_work_telephone_preferred_contact_method: BooleanLike = Field(
        default="",
        description="Tick if work telephone is the preferred contact method for borrower 2",
    )

    borrower_1_email_address: str = Field(
        default="",
        description=(
            'Email address for borrower 1 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_email_address_preferred_contact_method: BooleanLike = Field(
        default="", description="Tick if email is the preferred contact method for borrower 1"
    )

    borrower_2_email_address: str = Field(
        default="",
        description=(
            'Email address for borrower 2 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_email_address_preferred_contact_method: BooleanLike = Field(
        default="", description="Tick if email is the preferred contact method for borrower 2"
    )

    borrower_1_marital_status: str = Field(
        default="",
        description=(
            'Marital status of borrower 1 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_marital_status: str = Field(
        default="",
        description=(
            'Marital status of borrower 2 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_date_of_birth_day: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day of birth for borrower 1 (DD)"
    )

    borrower_1_date_of_birth_month: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month of birth for borrower 1 (MM)"
    )

    borrower_1_date_of_birth_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year of birth for borrower 1 (YYYY)"
    )

    borrower_2_date_of_birth_day: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Day of birth for borrower 2 (DD)"
    )

    borrower_2_date_of_birth_month: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Month of birth for borrower 2 (MM)"
    )

    borrower_2_date_of_birth_year: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year of birth for borrower 2 (YYYY)"
    )

    borrower_1_number_of_dependent_children: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of dependent children for borrower 1"
    )

    borrower_1_child_1_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age of dependent child 1 for borrower 1"
    )

    borrower_1_child_2_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age of dependent child 2 for borrower 1"
    )

    borrower_1_child_3_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age of dependent child 3 for borrower 1"
    )

    borrower_1_child_4_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age of dependent child 4 for borrower 1"
    )

    borrower_1_child_5_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age of dependent child 5 for borrower 1"
    )

    borrower_1_child_6_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age of dependent child 6 for borrower 1"
    )

    borrower_2_number_of_dependent_children: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of dependent children for borrower 2"
    )

    borrower_2_child_1_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age of dependent child 1 for borrower 2"
    )

    borrower_2_child_2_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age of dependent child 2 for borrower 2"
    )

    borrower_2_child_3_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age of dependent child 3 for borrower 2"
    )

    borrower_2_child_4_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age of dependent child 4 for borrower 2"
    )

    borrower_2_child_5_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age of dependent child 5 for borrower 2"
    )

    borrower_2_child_6_age: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Age of dependent child 6 for borrower 2"
    )

    borrower_1_total_number_in_household: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of people in borrower 1's household"
    )

    borrower_2_total_number_in_household: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total number of people in borrower 2's household"
    )

    borrower_1_employed_yes: BooleanLike = Field(
        default="", description="Tick if borrower 1 is employed"
    )

    borrower_1_employed_no: BooleanLike = Field(
        default="", description="Tick if borrower 1 is not employed"
    )

    borrower_1_self_employed_details: str = Field(
        default="",
        description=(
            "Details if borrower 1 is self-employed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_2_employed_yes: BooleanLike = Field(
        default="", description="Tick if borrower 2 is employed"
    )

    borrower_2_employed_no: BooleanLike = Field(
        default="", description="Tick if borrower 2 is not employed"
    )

    borrower_2_self_employed_details: str = Field(
        default="",
        description=(
            "Details if borrower 2 is self-employed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    borrower_1_occupation_if_unemployed_give_previous_occupation: str = Field(
        default="",
        description=(
            "Current occupation for borrower 1, or previous occupation if unemployed .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    borrower_2_occupation_if_unemployed_give_previous_occupation: str = Field(
        default="",
        description=(
            "Current occupation for borrower 2, or previous occupation if unemployed .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    borrower_1_in_permanent_employment_yes: BooleanLike = Field(
        default="", description="Tick if borrower 1 is in permanent employment"
    )

    borrower_1_in_permanent_employment_no: BooleanLike = Field(
        default="", description="Tick if borrower 1 is not in permanent employment"
    )

    borrower_2_in_permanent_employment_yes: BooleanLike = Field(
        default="", description="Tick if borrower 2 is in permanent employment"
    )

    borrower_2_in_permanent_employment_no: BooleanLike = Field(
        default="", description="Tick if borrower 2 is not in permanent employment"
    )

    borrower_1_name_of_employer_length_of_service_line_1: str = Field(
        default="",
        description=(
            "First line for borrower 1's employer name and length of service .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    borrower_1_name_of_employer_length_of_service_line_2: str = Field(
        default="",
        description=(
            "Second line for borrower 1's employer name and length of service .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    borrower_1_name_of_employer_length_of_service_line_3: str = Field(
        default="",
        description=(
            "Third line for borrower 1's employer name and length of service .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    borrower_2_name_of_employer_length_of_service_line_1: str = Field(
        default="",
        description=(
            "First line for borrower 2's employer name and length of service .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    borrower_2_name_of_employer_length_of_service_line_2: str = Field(
        default="",
        description=(
            "Second line for borrower 2's employer name and length of service .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    borrower_2_name_of_employer_length_of_service_line_3: str = Field(
        default="",
        description=(
            "Third line for borrower 2's employer name and length of service .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    reasons_for_review_arrears_line_1: str = Field(
        default="",
        description=(
            "First line describing the reason(s) for review or arrears .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reasons_for_review_arrears_line_2: str = Field(
        default="",
        description=(
            "Second line describing the reason(s) for review or arrears .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reasons_for_review_arrears_line_3: str = Field(
        default="",
        description=(
            "Third line describing the reason(s) for review or arrears .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )
