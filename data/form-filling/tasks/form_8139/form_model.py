from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EmployeesOffWorkTableRow(BaseModel):
    """Single row in EMPLOYEE NAME"""

    employee_name: str = Field(default="", description="Employee_Name")
    occupation: str = Field(default="", description="Occupation")
    date_of_disability: str = Field(default="", description="Date_Of_Disability")
    nature_of_disability: str = Field(default="", description="Nature_Of_Disability")
    prognosis: str = Field(default="", description="Prognosis")
    life_waiver_approved: str = Field(default="", description="Life_Waiver_Approved")


class RequestforQuotation(BaseModel):
    """General information about the client to assist in underwriting"""

    information_about_your_client: str = Field(
        default="",
        description=(
            "General background and important details about the client to assist "
            'underwriting .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class ClientQuestions(BaseModel):
    """Detailed questions about the client's business, employees, coverage, and experience"""

    nature_of_business_please_provide_specific_details: str = Field(
        ...,
        description=(
            "Describe the client’s nature of business with specific details .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    number_of_years_in_business: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of years the business has been operating"
    )

    are_there_any_seasonal_or_contract_employees_yes: BooleanLike = Field(
        ..., description="Indicate Yes if there are any seasonal or contract employees"
    )

    are_there_any_seasonal_or_contract_employees_no: BooleanLike = Field(
        ..., description="Indicate No if there are no seasonal or contract employees"
    )

    if_yes_please_specify: str = Field(
        default="",
        description=(
            "If there are seasonal or contract employees, specify details .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    are_50_or_more_of_the_employees_from_the_same_family_yes: BooleanLike = Field(
        ..., description="Indicate Yes if at least half of the employees are from the same family"
    )

    are_50_or_more_of_the_employees_from_the_same_family_no: BooleanLike = Field(
        ..., description="Indicate No if less than half of the employees are from the same family"
    )

    relationship_and_if_they_reside_in_the_same_household: str = Field(
        default="",
        description=(
            "Describe the family relationships and whether they live in the same household "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    are_all_employees_and_owners_covered_by_workers_compensation_wsib_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate Yes if all employees and owners are covered by Workers Compensation (WSIB)"
        ),
    )

    are_all_employees_and_owners_covered_by_workers_compensation_wsib_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate No if any employees or owners are not covered by Workers Compensation (WSIB)"
        ),
    )

    employer_pays_premium_contribution_basis: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Percentage of the premium paid by the employer (minimum 50%)"
    )

    employee_pays_premium_contribution_basis: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Percentage of the premium paid by the employees"
    )

    are_there_any_employees_currently_off_work_excluding_normal_vacation_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate Yes if any employees are currently off work (excluding normal vacation)"
        ),
    )

    are_there_any_employees_currently_off_work_excluding_normal_vacation_no: BooleanLike = Field(
        ...,
        description="Indicate No if no employees are currently off work (excluding normal vacation)",
    )

    employees_off_work_table: List[EmployeesOffWorkTableRow] = Field(
        default="",
        description=(
            "Table to list employees currently off work, including occupation, disability "
            "details, prognosis, and life waiver status"
        ),
    )  # List of table rows

    occupation: str = Field(
        default="",
        description=(
            "Occupation of the employee (used as a column header in the off-work employees "
            'table) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    date_of_disability: str = Field(
        default="",
        description=(
            "Date the disability began (used as a column header in the off-work employees table)"
        ),
    )  # YYYY-MM-DD format

    nature_of_disability: str = Field(
        default="",
        description=(
            "Description of the nature of the disability (used as a column header in the "
            'off-work employees table) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    prognosis: str = Field(
        default="",
        description=(
            "Prognosis for the employee’s condition (used as a column header in the "
            'off-work employees table) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    life_waiver_approved: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether a life waiver has been approved (used as a column header in "
            "the off-work employees table)"
        ),
    )

    are_they_currently_insured_yes: BooleanLike = Field(
        ..., description="Indicate Yes if the group is currently insured"
    )

    are_they_currently_insured_no: BooleanLike = Field(
        ..., description="Indicate No if the group is not currently insured"
    )

    current_carrier: str = Field(
        default="",
        description=(
            'Name of the current insurance carrier .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    number_of_years_with_carrier: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Number of years the client has been with the current carrier (maximum 2 "
            "insurers in past 5 years)"
        ),
    )

    renewal_date: str = Field(
        default="", description="Renewal date of the current insurance plan"
    )  # YYYY-MM-DD format

    are_benefits_being_quoted_the_same_as_their_current_plan_yes: BooleanLike = Field(
        ..., description="Indicate Yes if the quoted benefits match the current plan"
    )

    are_benefits_being_quoted_the_same_as_their_current_plan_no: BooleanLike = Field(
        ..., description="Indicate No if the quoted benefits differ from the current plan"
    )

    if_not_explain_why: str = Field(
        default="",
        description=(
            "Explain why the quoted benefits differ from the current plan .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    experience_and_rates_provided_yes: BooleanLike = Field(
        ..., description="Indicate Yes if experience and rates information has been provided"
    )

    experience_and_rates_provided_no: BooleanLike = Field(
        ..., description="Indicate No if experience and rates information has not been provided"
    )


class RequestForQuotation(BaseModel):
    """
    REQUEST FOR QUOTATION

    Please provide any information about your client. Any important details will assist in the underwriting process.
    """

    request_for_quotation: RequestforQuotation = Field(..., description="Request for Quotation")
    client_questions: ClientQuestions = Field(..., description="Client Questions")
