from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class StudentInformation(BaseModel):
    """Basic identifying information about the student"""

    student: str = Field(
        ...,
        description=(
            'Full name of the student .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(..., description="Student's date of birth")  # YYYY-MM-DD format

    diagnosis: str = Field(
        ...,
        description=(
            "Primary diabetes-related diagnosis for the student .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    school: str = Field(
        ...,
        description=(
            "Name of the school the student attends .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class DiabetesManagementComponents(BaseModel):
    """Verification that the physician’s Diabetes Management Plan includes required components"""

    blood_sugar_testing_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the physician's Diabetes Management Plan includes blood sugar "
            "testing instructions (Yes selected)"
        ),
    )

    blood_sugar_testing_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the physician's Diabetes Management Plan does not include blood "
            "sugar testing instructions (No selected)"
        ),
    )

    action_for_hypoglycemia_yes: BooleanLike = Field(
        ...,
        description="Indicate if the plan includes specific actions for hypoglycemia (Yes selected)",
    )

    action_for_hypoglycemia_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the plan does not include specific actions for hypoglycemia (No selected)"
        ),
    )

    action_for_hyperglycemia_yes: BooleanLike = Field(
        ...,
        description="Indicate if the plan includes specific actions for hyperglycemia (Yes selected)",
    )

    action_for_hyperglycemia_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the plan does not include specific actions for hyperglycemia (No selected)"
        ),
    )

    ketone_testing_yes: BooleanLike = Field(
        ..., description="Indicate if the plan includes ketone testing instructions (Yes selected)"
    )

    ketone_testing_no: BooleanLike = Field(
        ...,
        description="Indicate if the plan does not include ketone testing instructions (No selected)",
    )

    medication_regimen_including_glucagon_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the plan includes a medication regimen, including glucagon (Yes selected)"
        ),
    )

    medication_regimen_including_glucagon_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate if the plan does not include a medication regimen, including glucagon "
            "(No selected)"
        ),
    )

    meal_plan_yes: BooleanLike = Field(
        ..., description="Indicate if the plan includes a meal plan (Yes selected)"
    )

    meal_plan_no: BooleanLike = Field(
        ..., description="Indicate if the plan does not include a meal plan (No selected)"
    )


class StudentSelfManagementAssessment(BaseModel):
    """Assessment of the student’s ability to self-manage diabetes care"""

    self_manage_yes: BooleanLike = Field(
        ...,
        description="Select if the student is assessed as able to self-manage their diabetes care",
    )

    self_manage_no: BooleanLike = Field(
        ...,
        description=(
            "Select if the student is assessed as not able to self-manage their diabetes care"
        ),
    )

    self_manage_requires_assistance: BooleanLike = Field(
        ..., description="Select if the student can participate in care but requires assistance"
    )

    self_manage_dependent_upon_trained_staff: BooleanLike = Field(
        ...,
        description="Select if the student is fully dependent on trained staff for diabetes care",
    )


class AdditionalInformation(BaseModel):
    """Other diabetes-related planning details (pump failure, field trips, schedule changes, etc.)"""

    additional_information: str = Field(
        default="",
        description=(
            "Any additional details such as pump failure actions, field trip or schedule "
            "plans, snacks in classroom, or crisis plan .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class DiabeticStudentEmergencyActionPlan(BaseModel):
    """
        Health Services Department
    Individual Healthcare Plan/Emergency Action Plan for Diabetic Student

        Nursing portion of IHP, including assessment and history, must be completed for student on the Electronic Health record. Attach Diabetes Management Plan from Physician to this form. The plan must be updated at the beginning of each school year or whenever there is a change.
    """

    student_information: StudentInformation = Field(..., description="Student Information")
    diabetes_management_components: DiabetesManagementComponents = Field(
        ..., description="Diabetes Management Components"
    )
    student_self_management_assessment: StudentSelfManagementAssessment = Field(
        ..., description="Student Self-Management Assessment"
    )
    additional_information: AdditionalInformation = Field(..., description="Additional Information")
