from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PersonalDetails(BaseModel):
    """Student identification and signatures"""

    last_name: str = Field(
        ...,
        description=(
            "Student's family name as registered at the university .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Student\'s given name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    student_number: str = Field(
        ...,
        description=(
            "Official Ghent University student identification number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_student: str = Field(
        ...,
        description=(
            "Handwritten or digital signature of the student .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_student_signature: str = Field(
        ..., description="Date on which the student signed the form"
    )  # YYYY-MM-DD format

    signature_phd_supervisor: str = Field(
        ...,
        description=(
            "Handwritten or digital signature of the PhD supervisor .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_phd_supervisor_signature: str = Field(
        ..., description="Date on which the PhD supervisor signed the form"
    )  # YYYY-MM-DD format


class ChangeofDoctoralDegree(BaseModel):
    """Details of the change to the intended doctoral degree and faculty approval"""

    current_doctoral_degree: str = Field(
        ...,
        description=(
            "Full title or name of the doctoral degree the student is currently pursuing "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    new_doctoral_degree: str = Field(
        ...,
        description=(
            "Full title or name of the doctoral degree to which the student wishes to "
            'switch .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    motivation: str = Field(
        ...,
        description=(
            "Explanation of the reasons for switching to another doctoral degree .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    faculty_board_meeting_date: str = Field(
        default="",
        description="Date of the Faculty Board meeting at which the change is discussed or approved",
    )  # YYYY-MM-DD format

    signature_and_stamp_of_the_faculty: str = Field(
        default="",
        description=(
            "Authorized faculty representative's signature and official faculty stamp .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_faculty_signature: str = Field(
        default="",
        description="Date on which the faculty representative signed and stamped the form",
    )  # YYYY-MM-DD format


class SwitchingToAnotherDoctoralDegreeWithinTheSameFaculty(BaseModel):
    """
    SWITCHING TO ANOTHER DOCTORAL DEGREE WITHIN THE SAME FACULTY

    Please note: this form should only be used if you want to change the doctoral degree you are pursuing (within the same faculty).
    If you want to make changes to your doctoral guidance (changing you supervisor(s), members of the doctoral advisory committee, and/or your faculty mentor), to the language of your dissertation, or to your research topic or working title, you must contact your faculty student administration (https://www.ugent.be/student/en/administration/fsa).
    If you want to switch to a doctoral degree offered by another faculty, your supervisor must start a new enrolment application in OASIS.
    """

    personal_details: PersonalDetails = Field(..., description="Personal Details")
    change_of_doctoral_degree: ChangeofDoctoralDegree = Field(
        ..., description="Change of Doctoral Degree"
    )
