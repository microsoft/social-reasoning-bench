from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FormOfDisciplineTableRow(BaseModel):
    """Single row in Form of Discipline"""

    form_of_discipline: str = Field(default="", description="Form_Of_Discipline")
    date_of_discipline: str = Field(default="", description="Date_Of_Discipline")
    reasons_for_discipline: str = Field(default="", description="Reasons_For_Discipline")


class EmployeeInformation(BaseModel):
    """Basic information about the employee and supervisor"""

    date: str = Field(
        ..., description="Date this discipline notice and request for approval form is completed"
    )  # YYYY-MM-DD format

    department: str = Field(
        ...,
        description=(
            "Name of the department submitting the discipline notice .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_employee: str = Field(
        ...,
        description=(
            "Full name of the employee who is the subject of the discipline .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    title: str = Field(
        ...,
        description=(
            'Job title of the employee .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    position_id: str = Field(
        ...,
        description=(
            "Position identification number associated with the employee’s job .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    immediate_supervisor: str = Field(
        ...,
        description=(
            "Name of the employee’s immediate supervisor .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class RecommendedDiscipline(BaseModel):
    """Details of the discipline being recommended"""

    termination: BooleanLike = Field(
        ..., description="Indicate whether termination is the recommended form of discipline"
    )

    suspension_more_than_10_days: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether suspension of more than 10 days is the recommended form of discipline"
        ),
    )

    number_of_days: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of days of suspension, if suspension is recommended"
    )

    basis_for_recommended_disciplinary_action: str = Field(
        ...,
        description=(
            "Detailed narrative explaining the basis or bases for the recommended "
            'disciplinary action .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class PreviousDisciplinaryActions(BaseModel):
    """Record of prior discipline for the employee"""

    form_of_discipline_table: List[FormOfDisciplineTableRow] = Field(
        default_factory=list,
        description="Table listing prior forms of discipline, dates, and reasons",
    )  # List of table rows

    date_of_discipline: str = Field(
        default="",
        description=(
            "Date of each prior disciplinary action (captured as a column in the table of "
            'previous disciplinary actions) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reasons_for_discipline: str = Field(
        default="",
        description=(
            "Reason or reasons for each prior disciplinary action (captured as a column in "
            "the table of previous disciplinary actions) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CookCountyHRDisciplineNoticeApprovalForm(BaseModel):
    """COOK COUNTY BUREAU OF HUMAN RESOURCES
    DISCIPLINE NOTICE AND REQUEST FOR APPROVAL FORM"""

    employee_information: EmployeeInformation = Field(..., description="Employee Information")
    recommended_discipline: RecommendedDiscipline = Field(..., description="Recommended Discipline")
    previous_disciplinary_actions: PreviousDisciplinaryActions = Field(
        ..., description="Previous Disciplinary Actions"
    )
