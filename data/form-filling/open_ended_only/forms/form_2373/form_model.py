from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class StudentData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Basic information about the student applicant"""

    first_name: str = Field(
        ...,
        description=(
            "Student's first name .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    last_name: str = Field(
        ...,
        description=(
            "Student's last name .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    e_mail: str = Field(
        ...,
        description=(
            "Student's email address .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    telephone: str = Field(
        ...,
        description=(
            "Student's telephone number .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    university: str = Field(
        ...,
        description=(
            "Name of the university .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    faculty: str = Field(
        ...,
        description=(
            "Faculty at the university .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    field_of_study: str = Field(
        ...,
        description=(
            "Student's field of study .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )


class SupervisorData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the thesis supervisor"""

    title_supervisor: str = Field(
        ...,
        description=(
            "Academic title of the supervisor (e.g., Prof., Dr.) .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    first_name_supervisor: str = Field(
        ...,
        description=(
            "Supervisor's first name .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    last_name_supervisor: str = Field(
        ...,
        description=(
            "Supervisor's last name .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    e_mail_supervisor: str = Field(
        ...,
        description=(
            "Supervisor's email address .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    faculty_supervisor: str = Field(
        ...,
        description=(
            "Supervisor's faculty .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    subject_area: str = Field(
        ...,
        description=(
            "Subject area of the thesis .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )


class ThesisInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details about the thesis and exposé"""

    title_of_the_bachelor_or_master_thesis: str = Field(
        ...,
        description=(
            "Full title of the bachelor or master thesis .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    expose_text: str = Field(
        ...,
        description=(
            "Text of the exposé (max 3,500 keystrokes, including spaces) .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )


class ThesisProposalApplicationFormSouthTyrolEconomy(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    CALL FOR PROPOSALS "BACHELOR’S AND MASTER’S THESES ON THE SOUTH TYROLEAN ECONOMY"  
APPLICATION FORM

    Application form for the "Bachelor’s and Master’s Theses on the South Tyrolean Economy" call for proposals, organized by the Chamber of Commerce, Industry, Crafts and Agriculture of Bolzano and the Institute for Economic Research (IER). Students are invited to submit their thesis exposé, addressing its relevance to the South Tyrolean economy, existing knowledge, research methods, structure, and timetable.
    """

    student_data: StudentData = Field(
        ...,
        description="Student Data"
    )
    supervisor_data: SupervisorData = Field(
        ...,
        description="Supervisor Data"
    )
    thesis_information: ThesisInformation = Field(
        ...,
        description="Thesis Information"
    )