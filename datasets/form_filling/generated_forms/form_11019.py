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
    """Basic information about the student and school year"""

    student_name: str = Field(
        ...,
        description=(
            'Full legal name of the student .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Student’s date of birth")  # YYYY-MM-DD format

    school_of_attendance_in_the_2021_2022_school_year: str = Field(
        ...,
        description=(
            "Name of the school the student attended during the 2021-2022 school year .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    grade_level_in_the_2021_2022_school_year: str = Field(
        ...,
        description=(
            "Student’s grade level during the 2021-2022 school year .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RemoteInstructionRequest(BaseModel):
    """Parent/guardian request and reason for remote instruction"""

    student_high_risk_health_condition: BooleanLike = Field(
        default="",
        description=(
            "Check if the student has a high-risk health condition preventing in-person attendance"
        ),
    )

    household_member_high_risk_health_condition: BooleanLike = Field(
        default="",
        description=(
            "Check if someone in the student’s household has a high-risk health condition "
            "preventing the student’s in-person attendance"
        ),
    )

    signature_of_parent_guardian: str = Field(
        ...,
        description=(
            "Signature of the parent or legal guardian requesting remote instruction .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(
        ..., description="Date the parent/guardian signed the form"
    )  # YYYY-MM-DD format


class HealthcareProfessionalSection(BaseModel):
    """To be completed by a licensed healthcare professional"""

    physical_health_diagnosis: str = Field(
        default="",
        description=(
            "Description of the student’s or household member’s relevant physical health "
            'diagnosis .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    mental_emotional_health_diagnosis: str = Field(
        default="",
        description=(
            "Description of the student’s or household member’s relevant mental or "
            'emotional health diagnosis .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    other_diagnosis_information: str = Field(
        default="",
        description=(
            "Any additional diagnoses or relevant medical information .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RemoteInstructionApplication(BaseModel):
    """Remote Instruction Application"""

    student_information: StudentInformation = Field(..., description="Student Information")
    remote_instruction_request: RemoteInstructionRequest = Field(
        ..., description="Remote Instruction Request"
    )
    healthcare_professional_section: HealthcareProfessionalSection = Field(
        ..., description="Healthcare Professional Section"
    )
