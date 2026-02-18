from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EmployeesOffWorkTableEmployeeNameRow(BaseModel):
    """Single row in EMPLOYEE NAME"""

    employee_name: str = Field(default="", description="Employee_Name")
    occupation: str = Field(default="", description="Occupation")
    date_of_disability: str = Field(default="", description="Date_Of_Disability")
    nature_of_disability: str = Field(default="", description="Nature_Of_Disability")
    prognosis: str = Field(default="", description="Prognosis")
    life_waiver_approved: str = Field(default="", description="Life_Waiver_Approved")


class EmployeesOffWorkTableOccupationRow(BaseModel):
    """Single row in OCCUPATION"""

    employee_name: str = Field(default="", description="Employee_Name")
    occupation: str = Field(default="", description="Occupation")
    date_of_disability: str = Field(default="", description="Date_Of_Disability")
    nature_of_disability: str = Field(default="", description="Nature_Of_Disability")
    prognosis: str = Field(default="", description="Prognosis")
    life_waiver_approved: str = Field(default="", description="Life_Waiver_Approved")


class EmployeesOffWorkTableDateOfDisabilityRow(BaseModel):
    """Single row in DATE OF DISABILITY"""

    employee_name: str = Field(default="", description="Employee_Name")
    occupation: str = Field(default="", description="Occupation")
    date_of_disability: str = Field(default="", description="Date_Of_Disability")
    nature_of_disability: str = Field(default="", description="Nature_Of_Disability")
    prognosis: str = Field(default="", description="Prognosis")
    life_waiver_approved: str = Field(default="", description="Life_Waiver_Approved")


class EmployeesOffWorkTableNatureOfDisabilityRow(BaseModel):
    """Single row in NATURE OF DISABILITY"""

    employee_name: str = Field(default="", description="Employee_Name")
    occupation: str = Field(default="", description="Occupation")
    date_of_disability: str = Field(default="", description="Date_Of_Disability")
    nature_of_disability: str = Field(default="", description="Nature_Of_Disability")
    prognosis: str = Field(default="", description="Prognosis")
    life_waiver_approved: str = Field(default="", description="Life_Waiver_Approved")


class EmployeesOffWorkTablePrognosisRow(BaseModel):
    """Single row in PROGNOSIS"""

    employee_name: str = Field(default="", description="Employee_Name")
    occupation: str = Field(default="", description="Occupation")
    date_of_disability: str = Field(default="", description="Date_Of_Disability")
    nature_of_disability: str = Field(default="", description="Nature_Of_Disability")
    prognosis: str = Field(default="", description="Prognosis")
    life_waiver_approved: str = Field(default="", description="Life_Waiver_Approved")


class EmployeesOffWorkTableLifeWaiverApprovedRow(BaseModel):
    """Single row in LIFE WAIVER APPROVED?"""

    employee_name: str = Field(default="", description="Employee_Name")
    occupation: str = Field(default="", description="Occupation")
    date_of_disability: str = Field(default="", description="Date_Of_Disability")
    nature_of_disability: str = Field(default="", description="Nature_Of_Disability")
    prognosis: str = Field(default="", description="Prognosis")
    life_waiver_approved: str = Field(default="", description="Life_Waiver_Approved")


class ClientInformation(BaseModel):
    """Basic information about the client and their business"""

    nature_of_business: str = Field(
        ...,
        description=(
            "Describe the client's nature of business with specific details. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    number_of_years_in_business: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of years the business has been operating."
    )


class EmployeeWorkforceDetails(BaseModel):
    """Details about employees, family relationships, WSIB coverage, and premium contributions"""

    seasonal_or_contract_employees_yes: BooleanLike = Field(
        ..., description="Indicate yes if the client has any seasonal or contract employees."
    )

    seasonal_or_contract_employees_no: BooleanLike = Field(
        ...,
        description="Indicate no if the client does not have any seasonal or contract employees.",
    )

    seasonal_or_contract_employees_details: str = Field(
        default="",
        description=(
            "If there are seasonal or contract employees, provide details (e.g., roles, "
            'duration, number). .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    fifty_percent_family_employees_yes: BooleanLike = Field(
        ..., description="Indicate yes if at least half of the employees are from the same family."
    )

    fifty_percent_family_employees_no: BooleanLike = Field(
        ..., description="Indicate no if less than half of the employees are from the same family."
    )

    family_relationship_and_household: str = Field(
        default="",
        description=(
            "If 50% or more of employees are from the same family, describe the "
            "relationships and whether they live in the same household. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    wsib_covered_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate yes if all employees and owners are covered by Workers Compensation (WSIB)."
        ),
    )

    wsib_covered_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate no if any employees or owners are not covered by Workers Compensation (WSIB)."
        ),
    )

    employer_pays_percent: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Percentage of the premium paid by the employer (minimum 50%)."
    )

    employee_pays_percent: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Percentage of the premium paid by the employees."
    )


class EmployeesCurrentlyOffWork(BaseModel):
    """Information about employees who are currently off work"""

    employees_off_work_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate yes if any employees are currently off work other than for normal vacation."
        ),
    )

    employees_off_work_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate no if no employees are currently off work other than for normal vacation."
        ),
    )

    employees_off_work_table_employee_name: List[EmployeesOffWorkTableEmployeeNameRow] = Field(
        default="",
        description=(
            "Table to list employees currently off work and details of their disability status."
        ),
    )  # List of table rows

    employees_off_work_table_occupation: List[EmployeesOffWorkTableOccupationRow] = Field(
        default="",
        description=(
            "Duplicate reference to the off-work employees table (see EMPLOYEE NAME field "
            "for columns)."
        ),
    )  # List of table rows

    employees_off_work_table_date_of_disability: List[EmployeesOffWorkTableDateOfDisabilityRow] = (
        Field(
            default="",
            description=(
                "Duplicate reference to the off-work employees table (see EMPLOYEE NAME field "
                "for columns)."
            ),
        )
    )  # List of table rows

    employees_off_work_table_nature_of_disability: List[
        EmployeesOffWorkTableNatureOfDisabilityRow
    ] = Field(
        default="",
        description=(
            "Duplicate reference to the off-work employees table (see EMPLOYEE NAME field "
            "for columns)."
        ),
    )  # List of table rows

    employees_off_work_table_prognosis: List[EmployeesOffWorkTablePrognosisRow] = Field(
        default="",
        description=(
            "Duplicate reference to the off-work employees table (see EMPLOYEE NAME field "
            "for columns)."
        ),
    )  # List of table rows

    employees_off_work_table_life_waiver_approved: List[
        EmployeesOffWorkTableLifeWaiverApprovedRow
    ] = Field(
        default="",
        description=(
            "Duplicate reference to the off-work employees table (see EMPLOYEE NAME field "
            "for columns)."
        ),
    )  # List of table rows


class CurrentCoverageQuotationDetails(BaseModel):
    """Current insurance, plan comparison, and experience/rate information"""

    currently_insured_yes: BooleanLike = Field(
        ..., description="Indicate yes if the client is currently insured with another carrier."
    )

    currently_insured_no: BooleanLike = Field(
        ..., description="Indicate no if the client is not currently insured with another carrier."
    )

    current_carrier: str = Field(
        default="",
        description=(
            "Name of the current insurance carrier, if any. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    number_of_years_with_carrier: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description=(
            "Number of years the client has been with the current carrier (maximum 2 "
            "insurers in the past 5 years)."
        ),
    )

    renewal_date: str = Field(
        default="", description="Renewal date of the current insurance policy."
    )  # YYYY-MM-DD format

    benefits_same_as_current_yes: BooleanLike = Field(
        ..., description="Indicate yes if the quoted benefits match the current plan."
    )

    benefits_same_as_current_no: BooleanLike = Field(
        ..., description="Indicate no if the quoted benefits differ from the current plan."
    )

    benefits_difference_explanation: str = Field(
        default="",
        description=(
            "If benefits differ from the current plan, explain the reasons for the changes. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    experience_and_rates_provided_yes: BooleanLike = Field(
        ..., description="Indicate yes if experience and rate information has been provided."
    )

    experience_and_rates_provided_no: BooleanLike = Field(
        ..., description="Indicate no if experience and rate information has not been provided."
    )


class RequestForQuotation(BaseModel):
    """
    REQUEST FOR QUOTATION

    Please provide any information about your client. Any important details will assist in the underwriting process.
    """

    client_information: ClientInformation = Field(..., description="Client Information")
    employee__workforce_details: EmployeeWorkforceDetails = Field(
        ..., description="Employee & Workforce Details"
    )
    employees_currently_off_work: EmployeesCurrentlyOffWork = Field(
        ..., description="Employees Currently Off Work"
    )
    current_coverage__quotation_details: CurrentCoverageQuotationDetails = Field(
        ..., description="Current Coverage & Quotation Details"
    )
