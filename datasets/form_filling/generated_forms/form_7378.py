from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PreviousDisciplinaryActionsTableRow(BaseModel):
    """Single row in Form of Discipline"""

    form_of_discipline: str = Field(default="", description="Form_Of_Discipline")
    date_of_discipline: str = Field(default="", description="Date_Of_Discipline")
    reasons_for_discipline: str = Field(default="", description="Reasons_For_Discipline")


class DateOfDisciplineRow(BaseModel):
    """Single row in Date of Discipline"""

    form_of_discipline: str = Field(default="", description="Form_Of_Discipline")
    date_of_discipline: str = Field(default="", description="Date_Of_Discipline")
    reasons_for_discipline: str = Field(default="", description="Reasons_For_Discipline")


class ReasonsForDisciplineRow(BaseModel):
    """Single row in Reason(s) for Discipline"""

    form_of_discipline: str = Field(default="", description="Form_Of_Discipline")
    date_of_discipline: str = Field(default="", description="Date_Of_Discipline")
    reasons_for_discipline: str = Field(default="", description="Reasons_For_Discipline")


class EmployeeandDepartmentInformation(BaseModel):
    """Basic information about the employee and department"""

    date: str = Field(
        ..., description="Date this discipline notice and request for approval form is completed"
    )  # YYYY-MM-DD format

    department: str = Field(
        ...,
        description=(
            "Name of the department submitting this discipline notice .If you cannot fill "
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
        ..., description="Check if termination is the recommended form of discipline"
    )

    suspension_more_than_10_days: BooleanLike = Field(
        ...,
        description="Check if suspension of more than 10 days is the recommended form of discipline",
    )

    number_of_days: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of days of suspension, if suspension is recommended"
    )


class PreviousDisciplinaryActions(BaseModel):
    """Record of prior discipline for the employee"""

    previous_disciplinary_actions_table: List[PreviousDisciplinaryActionsTableRow] = Field(
        default="",
        description=(
            "Table to record each prior disciplinary action, including form, date, and reason"
        ),
    )  # List of table rows

    date_of_discipline: List[DateOfDisciplineRow] = Field(
        default="",
        description="See the previous disciplinary actions table for dates of each prior discipline",
    )  # List of table rows

    reasons_for_discipline: List[ReasonsForDisciplineRow] = Field(
        default="",
        description=(
            "See the previous disciplinary actions table for reasons for each prior discipline"
        ),
    )  # List of table rows


class BasisforRecommendedAction(BaseModel):
    """Narrative explanation and justification for the recommended discipline"""

    basis_for_recommended_disciplinary_action: str = Field(
        ...,
        description=(
            "Detailed narrative explaining the basis or bases for the recommended "
            'disciplinary action .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class CookCountyHRDisciplineNoticeApprovalForm(BaseModel):
    """
        COOK COUNTY BUREAU OF HUMAN RESOURCES
    DISCIPLINE NOTICE AND REQUEST FOR APPROVAL FORM

        ''
    """

    employee_and_department_information: EmployeeandDepartmentInformation = Field(
        ..., description="Employee and Department Information"
    )
    recommended_discipline: RecommendedDiscipline = Field(..., description="Recommended Discipline")
    previous_disciplinary_actions: PreviousDisciplinaryActions = Field(
        ..., description="Previous Disciplinary Actions"
    )
    basis_for_recommended_action: BasisforRecommendedAction = Field(
        ..., description="Basis for Recommended Action"
    )
