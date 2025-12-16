from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Basic contact and residency/employment details for the applicant"""

    name: str = Field(
        ...,
        description=(
            'Applicant\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    lexington_home_address: str = Field(
        default="",
        description=(
            "Home street address in Lexington, if applicant is a Lexington resident .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    employer: str = Field(
        default="",
        description=(
            "Employer name if applicant is a non-resident who works in Lexington .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    non_resident_mailing_address: str = Field(
        default="",
        description=(
            "Mailing address for applicants who are not Lexington residents .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    best_phone: str = Field(
        ...,
        description=(
            "Primary phone number where the applicant can best be reached .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    biographic_material: str = Field(
        ...,
        description=(
            "40-word biographical note written in the third person .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    personal_photo_file_name: str = Field(
        ...,
        description=(
            "File name of the high-resolution JPEG personal photo being submitted .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ProseSubmission(BaseModel):
    """Details about the prose submission"""

    prose_submission_title: str = Field(
        ...,
        description=(
            "Title of the prose submission (1 piece) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    prose_submission_file_name: str = Field(
        ...,
        description=(
            "File name of the prose submission document (WORD or text format) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    prose_submission_category: str = Field(
        ...,
        description=(
            "Category of the prose piece (e.g., story, fiction, memoir, non-fiction, etc.) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    prose_submission_previously_published: BooleanLike = Field(
        ..., description="Indicate whether the prose submission has been published before"
    )

    prose_submission_where_and_when_published: str = Field(
        default="",
        description=(
            "If previously published, specify where and when the prose submission was "
            'published .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class PoetrySubmission(BaseModel):
    """Details about the poetry submission"""

    poetry_submission_title: str = Field(
        default="",
        description=(
            "Title of the poetry submission (one of up to three pieces) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    poetry_submission_file_name: str = Field(
        default="",
        description=(
            "File name of the poetry submission document .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    poetry_submission_previously_published: BooleanLike = Field(
        default="", description="Indicate whether the poetry submission has been published before"
    )

    poetry_submission_where_and_when_published: str = Field(
        default="",
        description=(
            "If previously published, specify where and when the poetry submission was "
            'published .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class Winter2022ApplicationForm(BaseModel):
    """
    Winter 2022 Application Form

    Winter 2022 Application Form
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    prose_submission: ProseSubmission = Field(..., description="Prose Submission")
    poetry_submission: PoetrySubmission = Field(..., description="Poetry Submission")
