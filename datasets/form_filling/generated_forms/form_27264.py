from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class WorkReferencesRow(BaseModel):
    """Single row in Name"""

    name: str = Field(default="", description="Name")
    position: str = Field(default="", description="Position")
    company: str = Field(default="", description="Company")
    address: str = Field(default="", description="Address")
    telephone: str = Field(default="", description="Telephone")


class WorkReferencesPositionRow(BaseModel):
    """Single row in Position"""

    name: str = Field(default="", description="Name")
    position: str = Field(default="", description="Position")
    company: str = Field(default="", description="Company")
    address: str = Field(default="", description="Address")
    telephone: str = Field(default="", description="Telephone")


class WorkReferencesCompanyRow(BaseModel):
    """Single row in Company"""

    name: str = Field(default="", description="Name")
    position: str = Field(default="", description="Position")
    company: str = Field(default="", description="Company")
    address: str = Field(default="", description="Address")
    telephone: str = Field(default="", description="Telephone")


class WorkReferencesAddressRow(BaseModel):
    """Single row in Address"""

    name: str = Field(default="", description="Name")
    position: str = Field(default="", description="Position")
    company: str = Field(default="", description="Company")
    address: str = Field(default="", description="Address")
    telephone: str = Field(default="", description="Telephone")


class WorkReferencesTelephoneRow(BaseModel):
    """Single row in Telephone"""

    name: str = Field(default="", description="Name")
    position: str = Field(default="", description="Position")
    company: str = Field(default="", description="Company")
    address: str = Field(default="", description="Address")
    telephone: str = Field(default="", description="Telephone")


class Employer1TableRow(BaseModel):
    """Single row in Employer"""

    employer: str = Field(default="", description="Employer")
    supervisor: str = Field(default="", description="Supervisor")
    employment_dates_from: str = Field(default="", description="Employment_Dates_From")
    employment_dates_to: str = Field(default="", description="Employment_Dates_To")
    pay_or_salary_start: str = Field(default="", description="Pay_Or_Salary_Start")
    pay_or_salary_final: str = Field(default="", description="Pay_Or_Salary_Final")
    job_title: str = Field(default="", description="Job_Title")


class Employer1SupervisorRow(BaseModel):
    """Single row in Supervisor"""

    employer: str = Field(default="", description="Employer")
    supervisor: str = Field(default="", description="Supervisor")
    employment_dates_from: str = Field(default="", description="Employment_Dates_From")
    employment_dates_to: str = Field(default="", description="Employment_Dates_To")
    pay_or_salary_start: str = Field(default="", description="Pay_Or_Salary_Start")
    pay_or_salary_final: str = Field(default="", description="Pay_Or_Salary_Final")
    job_title: str = Field(default="", description="Job_Title")


class EmploymentDatesFromRow(BaseModel):
    """Single row in Employment Dates From"""

    employer: str = Field(default="", description="Employer")
    supervisor: str = Field(default="", description="Supervisor")
    employment_dates_from: str = Field(default="", description="Employment_Dates_From")
    employment_dates_to: str = Field(default="", description="Employment_Dates_To")
    pay_or_salary_start: str = Field(default="", description="Pay_Or_Salary_Start")
    pay_or_salary_final: str = Field(default="", description="Pay_Or_Salary_Final")
    job_title: str = Field(default="", description="Job_Title")


class EmploymentDatesToRow(BaseModel):
    """Single row in Employment Dates To"""

    employer: str = Field(default="", description="Employer")
    supervisor: str = Field(default="", description="Supervisor")
    employment_dates_from: str = Field(default="", description="Employment_Dates_From")
    employment_dates_to: str = Field(default="", description="Employment_Dates_To")
    pay_or_salary_start: str = Field(default="", description="Pay_Or_Salary_Start")
    pay_or_salary_final: str = Field(default="", description="Pay_Or_Salary_Final")
    job_title: str = Field(default="", description="Job_Title")


class PayOrSalaryStartRow(BaseModel):
    """Single row in Pay or Salary Start"""

    employer: str = Field(default="", description="Employer")
    supervisor: str = Field(default="", description="Supervisor")
    employment_dates_from: str = Field(default="", description="Employment_Dates_From")
    employment_dates_to: str = Field(default="", description="Employment_Dates_To")
    pay_or_salary_start: str = Field(default="", description="Pay_Or_Salary_Start")
    pay_or_salary_final: str = Field(default="", description="Pay_Or_Salary_Final")
    job_title: str = Field(default="", description="Job_Title")


class PayOrSalaryFinalRow(BaseModel):
    """Single row in Pay or Salary Final"""

    employer: str = Field(default="", description="Employer")
    supervisor: str = Field(default="", description="Supervisor")
    employment_dates_from: str = Field(default="", description="Employment_Dates_From")
    employment_dates_to: str = Field(default="", description="Employment_Dates_To")
    pay_or_salary_start: str = Field(default="", description="Pay_Or_Salary_Start")
    pay_or_salary_final: str = Field(default="", description="Pay_Or_Salary_Final")
    job_title: str = Field(default="", description="Job_Title")


class JobTitle1Row(BaseModel):
    """Single row in Job Title"""

    employer: str = Field(default="", description="Employer")
    supervisor: str = Field(default="", description="Supervisor")
    employment_dates_from: str = Field(default="", description="Employment_Dates_From")
    employment_dates_to: str = Field(default="", description="Employment_Dates_To")
    pay_or_salary_start: str = Field(default="", description="Pay_Or_Salary_Start")
    pay_or_salary_final: str = Field(default="", description="Pay_Or_Salary_Final")
    job_title: str = Field(default="", description="Job_Title")


class Employer2TableRow(BaseModel):
    """Single row in Employer (2)"""

    employer: str = Field(default="", description="Employer")
    supervisor: str = Field(default="", description="Supervisor")
    employment_dates_from: str = Field(default="", description="Employment_Dates_From")
    employment_dates_to: str = Field(default="", description="Employment_Dates_To")
    pay_or_salary_start: str = Field(default="", description="Pay_Or_Salary_Start")
    pay_or_salary_final: str = Field(default="", description="Pay_Or_Salary_Final")
    job_title: str = Field(default="", description="Job_Title")


class Employer2SupervisorRow(BaseModel):
    """Single row in Supervisor (2)"""

    employer: str = Field(default="", description="Employer")
    supervisor: str = Field(default="", description="Supervisor")
    employment_dates_from: str = Field(default="", description="Employment_Dates_From")
    employment_dates_to: str = Field(default="", description="Employment_Dates_To")
    pay_or_salary_start: str = Field(default="", description="Pay_Or_Salary_Start")
    pay_or_salary_final: str = Field(default="", description="Pay_Or_Salary_Final")
    job_title: str = Field(default="", description="Job_Title")


class EmploymentDatesFrom2Row(BaseModel):
    """Single row in Employment Dates From (2)"""

    employer: str = Field(default="", description="Employer")
    supervisor: str = Field(default="", description="Supervisor")
    employment_dates_from: str = Field(default="", description="Employment_Dates_From")
    employment_dates_to: str = Field(default="", description="Employment_Dates_To")
    pay_or_salary_start: str = Field(default="", description="Pay_Or_Salary_Start")
    pay_or_salary_final: str = Field(default="", description="Pay_Or_Salary_Final")
    job_title: str = Field(default="", description="Job_Title")


class EmploymentDatesTo2Row(BaseModel):
    """Single row in Employment Dates To (2)"""

    employer: str = Field(default="", description="Employer")
    supervisor: str = Field(default="", description="Supervisor")
    employment_dates_from: str = Field(default="", description="Employment_Dates_From")
    employment_dates_to: str = Field(default="", description="Employment_Dates_To")
    pay_or_salary_start: str = Field(default="", description="Pay_Or_Salary_Start")
    pay_or_salary_final: str = Field(default="", description="Pay_Or_Salary_Final")
    job_title: str = Field(default="", description="Job_Title")


class PayOrSalaryStart2Row(BaseModel):
    """Single row in Pay or Salary Start (2)"""

    employer: str = Field(default="", description="Employer")
    supervisor: str = Field(default="", description="Supervisor")
    employment_dates_from: str = Field(default="", description="Employment_Dates_From")
    employment_dates_to: str = Field(default="", description="Employment_Dates_To")
    pay_or_salary_start: str = Field(default="", description="Pay_Or_Salary_Start")
    pay_or_salary_final: str = Field(default="", description="Pay_Or_Salary_Final")
    job_title: str = Field(default="", description="Job_Title")


class PayOrSalaryFinal2Row(BaseModel):
    """Single row in Pay or Salary Final (2)"""

    employer: str = Field(default="", description="Employer")
    supervisor: str = Field(default="", description="Supervisor")
    employment_dates_from: str = Field(default="", description="Employment_Dates_From")
    employment_dates_to: str = Field(default="", description="Employment_Dates_To")
    pay_or_salary_start: str = Field(default="", description="Pay_Or_Salary_Start")
    pay_or_salary_final: str = Field(default="", description="Pay_Or_Salary_Final")
    job_title: str = Field(default="", description="Job_Title")


class JobTitle2Row(BaseModel):
    """Single row in Job Title (2)"""

    employer: str = Field(default="", description="Employer")
    supervisor: str = Field(default="", description="Supervisor")
    employment_dates_from: str = Field(default="", description="Employment_Dates_From")
    employment_dates_to: str = Field(default="", description="Employment_Dates_To")
    pay_or_salary_start: str = Field(default="", description="Pay_Or_Salary_Start")
    pay_or_salary_final: str = Field(default="", description="Pay_Or_Salary_Final")
    job_title: str = Field(default="", description="Job_Title")


class WorkReferences(BaseModel):
    """Professional references from previous work"""

    work_references: List[WorkReferencesRow] = Field(
        default="",
        description=(
            "Work reference entries including name, position, company, address, and telephone"
        ),
    )  # List of table rows

    work_references_position: List[WorkReferencesPositionRow] = Field(
        default="",
        description=(
            "Work reference entries including name, position, company, address, and telephone"
        ),
    )  # List of table rows

    work_references_company: List[WorkReferencesCompanyRow] = Field(
        default="",
        description=(
            "Work reference entries including name, position, company, address, and telephone"
        ),
    )  # List of table rows

    work_references_address: List[WorkReferencesAddressRow] = Field(
        default="",
        description=(
            "Work reference entries including name, position, company, address, and telephone"
        ),
    )  # List of table rows

    work_references_telephone: List[WorkReferencesTelephoneRow] = Field(
        default="",
        description=(
            "Work reference entries including name, position, company, address, and telephone"
        ),
    )  # List of table rows


class EmploymentHistoryEmployer1(BaseModel):
    """Details for the most recent employer"""

    employer_1_table: List[Employer1TableRow] = Field(
        default="",
        description=(
            "First employer record including employer, supervisor, employment dates, pay or "
            "salary, and job title"
        ),
    )  # List of table rows

    employer_1_supervisor: List[Employer1SupervisorRow] = Field(
        default="",
        description=(
            "First employer record including employer, supervisor, employment dates, pay or "
            "salary, and job title"
        ),
    )  # List of table rows

    employment_dates_from: List[EmploymentDatesFromRow] = Field(
        default="", description="Start date of employment for the first employer"
    )  # List of table rows

    employment_dates_to: List[EmploymentDatesToRow] = Field(
        default="", description="End date of employment for the first employer"
    )  # List of table rows

    pay_or_salary_start: List[PayOrSalaryStartRow] = Field(
        default="", description="Starting pay or salary for the first employer"
    )  # List of table rows

    pay_or_salary_final: List[PayOrSalaryFinalRow] = Field(
        default="", description="Final pay or salary for the first employer"
    )  # List of table rows

    job_title_1: List[JobTitle1Row] = Field(
        default="", description="Job title held at the first employer"
    )  # List of table rows

    reason_for_leaving_1: str = Field(
        default="",
        description=(
            "Explanation of why you left the first employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    positions_held_advancements_or_promotions_attained_in_this_job_1: str = Field(
        default="",
        description=(
            "List positions held, advancements, or promotions attained at the first "
            'employer .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class EmploymentHistoryEmployer2(BaseModel):
    """Details for the second most recent employer"""

    employer_2_table: List[Employer2TableRow] = Field(
        default="",
        description=(
            "Second employer record including employer, supervisor, employment dates, pay "
            "or salary, and job title"
        ),
    )  # List of table rows

    employer_2_supervisor: List[Employer2SupervisorRow] = Field(
        default="",
        description=(
            "Second employer record including employer, supervisor, employment dates, pay "
            "or salary, and job title"
        ),
    )  # List of table rows

    employment_dates_from_2: List[EmploymentDatesFrom2Row] = Field(
        default="", description="Start date of employment for the second employer"
    )  # List of table rows

    employment_dates_to_2: List[EmploymentDatesTo2Row] = Field(
        default="", description="End date of employment for the second employer"
    )  # List of table rows

    pay_or_salary_start_2: List[PayOrSalaryStart2Row] = Field(
        default="", description="Starting pay or salary for the second employer"
    )  # List of table rows

    pay_or_salary_final_2: List[PayOrSalaryFinal2Row] = Field(
        default="", description="Final pay or salary for the second employer"
    )  # List of table rows

    job_title_2: List[JobTitle2Row] = Field(
        default="", description="Job title held at the second employer"
    )  # List of table rows

    reason_for_leaving_2: str = Field(
        default="",
        description=(
            "Explanation of why you left the second employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    positions_held_advancements_or_promotions_attained_in_this_job_2: str = Field(
        default="",
        description=(
            "List positions held, advancements, or promotions attained at the second "
            'employer .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class WorkReferences(BaseModel):
    """
    Work References

    Employment History (Please Include the last 3 employers, starting with the most recent positions held)
    """

    work_references: WorkReferences = Field(..., description="Work References")
    employment_history___employer_1: EmploymentHistoryEmployer1 = Field(
        ..., description="Employment History - Employer 1"
    )
    employment_history___employer_2: EmploymentHistoryEmployer2 = Field(
        ..., description="Employment History - Employer 2"
    )
