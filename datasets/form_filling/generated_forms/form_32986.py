from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MemberDistrictInformation(BaseModel):
    """Information about the Member of Congress and district"""

    member_of_congress_name: str = Field(
        ...,
        description=(
            "Full name of the Member of Congress representing the district .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    state_district: str = Field(
        ...,
        description=(
            "State and congressional district number (e.g., CA-12) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class StudentInformation(BaseModel):
    """Basic information about the student and their parent/guardian"""

    name: str = Field(
        ...,
        description=(
            "Student's full name as it should appear on certificates .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    grade: str = Field(
        ...,
        description=(
            'Student\'s current grade level .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    street_address: str = Field(
        ...,
        description=(
            'Student\'s primary street address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            "City for the student's primary address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State abbreviation for the student's primary address")

    zip: str = Field(..., description="ZIP code for the student's primary address")

    mailing_address_if_different: str = Field(
        default="",
        description=(
            "Mailing address if different from the primary street address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    student_email: str = Field(
        ...,
        description=(
            'Student\'s email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    student_phone_cell: str = Field(
        ...,
        description=(
            'Student\'s cell phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    t_shirt_size: str = Field(
        ...,
        description=(
            'Student\'s T-shirt size .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    parent_or_guardian_names: str = Field(
        ...,
        description=(
            "Full name(s) of the student's parent(s) or legal guardian(s) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    parent_phone_home: str = Field(
        default="",
        description=(
            'Parent or guardian home phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    parent_phone_work_or_cell: str = Field(
        ...,
        description=(
            "Parent or guardian work or cell phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class School(BaseModel):
    """Information about the student's school and art teacher"""

    school_name: str = Field(
        ...,
        description=(
            'Full name of the student\'s school .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    school_street_address: str = Field(
        ...,
        description=(
            "Street address of the student's school .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    school_city: str = Field(
        ...,
        description=(
            "City where the student's school is located .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    school_state: str = Field(
        ..., description="State abbreviation where the student's school is located"
    )

    school_zip: str = Field(..., description="ZIP code for the student's school address")

    art_teacher_name: str = Field(
        ...,
        description=(
            "Full name of the student's art teacher .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    art_teacher_phone: str = Field(
        default="",
        description=(
            "Phone number for the student's art teacher .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    art_teacher_email: str = Field(
        default="",
        description=(
            "Email address for the student's art teacher .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ArtCompetitionEntry(BaseModel):
    """Details about the artwork submitted to the competition"""

    title_of_entry: str = Field(
        ...,
        description=(
            'Title of the artwork being submitted .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    medium: str = Field(
        ...,
        description=(
            "Primary medium or materials used in the artwork .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    description_line_1: str = Field(
        ...,
        description=(
            "First line of the detailed description of the artwork .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    description_line_2: str = Field(
        default="",
        description=(
            "Second line of the detailed description of the artwork .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    description_line_3: str = Field(
        default="",
        description=(
            "Third line of the detailed description of the artwork .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    framed_dimensions_height_inches: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Height of the framed artwork in inches"
    )

    framed_dimensions_width_inches: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Width of the framed artwork in inches"
    )

    framed_dimensions_depth_inches: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Depth of the framed artwork in inches"
    )


class CongressionalArtCompetitionStudentInformationReleaseForm2015(BaseModel):
    """
        2015 Congressional Art Competition
    Student Information & Release Form

        PLEASE PRINT CLEARLY. THIS INFORMATION IS USED FOR CERTIFICATES AND AWARDING SCHOLARSHIPS. INCOMPLETE FORMS WILL NOT BE ACCEPTED.
    """

    memberdistrict_information: MemberDistrictInformation = Field(
        ..., description="Member/District Information"
    )
    student_information: StudentInformation = Field(..., description="Student Information")
    school: School = Field(..., description="School")
    art_competition_entry: ArtCompetitionEntry = Field(..., description="Art Competition Entry")
