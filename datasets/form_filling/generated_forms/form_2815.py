from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class GeneralInformation(BaseModel):
    """Basic information about the student and research project"""

    name_of_the_student: str = Field(
        ...,
        description=(
            "Full name of the student submitting the entry .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email_of_the_student: str = Field(
        ...,
        description=(
            'Email address of the student .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    institution: str = Field(
        ...,
        description=(
            "Name of the institution where the student is enrolled .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    degree_m_sc: BooleanLike = Field(
        ..., description="Select if the student is enrolled in an M.Sc. program"
    )

    degree_ph_d: BooleanLike = Field(
        ..., description="Select if the student is enrolled in a Ph.D. program"
    )

    title_of_the_research_project: str = Field(
        ...,
        description=(
            "Full title of the student's research project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_the_academic_supervisor: str = Field(
        ...,
        description=(
            "Full name of the student's academic supervisor .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    category_of_the_submission_podcast: BooleanLike = Field(
        ..., description="Select if the submission category is Podcast"
    )

    category_of_the_submission_video: BooleanLike = Field(
        ..., description="Select if the submission category is Video"
    )

    category_of_the_submission_infographic: BooleanLike = Field(
        ..., description="Select if the submission category is Infographic"
    )


class Biography(BaseModel):
    """Brief biography of the student"""

    brief_biography_line_1: str = Field(
        ...,
        description=(
            "First line of the brief biography (up to 5 lines total) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    brief_biography_line_2: str = Field(
        default="",
        description=(
            'Second line of the brief biography .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    brief_biography_line_3: str = Field(
        default="",
        description=(
            'Third line of the brief biography .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    brief_biography_line_4: str = Field(
        default="",
        description=(
            'Fourth line of the brief biography .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    brief_biography_line_5: str = Field(
        default="",
        description=(
            'Fifth line of the brief biography .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class MyDairyResearchStudentCompetitionEntryForm(BaseModel):
    """
        My Dairy Research
    Student Competition

    Entry Form

        ''
    """

    general_information: GeneralInformation = Field(..., description="General Information")
    biography: Biography = Field(..., description="Biography")
