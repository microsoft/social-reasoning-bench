from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FacultyInformation(BaseModel):
    """Basic information about the faculty member and their teaching assignment"""

    faculty_members_name: str = Field(
        ...,
        description=(
            "Full name of the faculty member being appointed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    status_rank_title: str = Field(
        ...,
        description=(
            "Faculty appointment status, academic rank, and title .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    department_college: str = Field(
        ...,
        description=(
            "Name of the department and/or college of the appointment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    teaching_discipline: str = Field(
        ...,
        description=(
            "Primary teaching discipline or subject area .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    course_assignments_or_level_of_instruction: str = Field(
        ...,
        description=(
            "List course assignments or level of instruction; attach the syllabus for each "
            'course listed .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class Qualifications(BaseModel):
    """Documentation of academic and professional qualifications"""

    undergraduate_and_graduate_degrees_list_degrees: str = Field(
        default="",
        description=(
            "List all relevant undergraduate and graduate degrees .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    related_work_experience: BooleanLike = Field(
        default="", description="Indicate whether the faculty member has related work experience"
    )

    professional_licensure_and_certifications: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the faculty member holds relevant professional licensure or "
            "certifications"
        ),
    )

    honors_and_awards: BooleanLike = Field(
        default="", description="Indicate whether the faculty member has relevant honors or awards"
    )

    continuous_documented_excellence_in_teaching: BooleanLike = Field(
        default="",
        description="Indicate whether there is continuous documented excellence in teaching",
    )

    additional_demonstrated_competencies_and_achievements: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether there are additional demonstrated competencies and achievements"
        ),
    )

    detailed_description_of_qualifications: str = Field(
        ...,
        description=(
            "Provide a detailed description of qualifications; attach copies of licenses, "
            "certificates, and other supporting documents .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Approvals(BaseModel):
    """Signatures and dates for departmental, dean, and SACSCOC approvals"""

    department_head_director_signature: str = Field(
        ...,
        description=(
            "Signature of the department head or director approving the appointment .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    department_head_director_signature_date: str = Field(
        ..., description="Date the department head or director signed the form"
    )  # YYYY-MM-DD format

    deans_signature: str = Field(
        ...,
        description=(
            "Signature of the dean approving the appointment .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    deans_signature_date: str = Field(
        ..., description="Date the dean signed the form"
    )  # YYYY-MM-DD format

    sacscoc_liaison_signature: str = Field(
        ...,
        description=(
            "Signature of the SACSCOC Liaison indicating final review .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    sacscoc_liaison_signature_date: str = Field(
        ..., description="Date the SACSCOC Liaison signed the form"
    )  # YYYY-MM-DD format


class FacultyAppointmentQualifications(BaseModel):
    """DOCUMENTATION OF QUALIFICATIONS FOR A FULL-TIME OR PART-TIME FACULTY APPOINTMENT"""

    faculty_information: FacultyInformation = Field(..., description="Faculty Information")
    qualifications: Qualifications = Field(..., description="Qualifications")
    approvals: Approvals = Field(..., description="Approvals")
