from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FormofAccesstoRecord(BaseModel):
    """Preferred form of access to the requested record, including disability-related needs and format options"""

    disability: str = Field(
        default="",
        description=(
            "Describe any disability that prevents you from reading, viewing, or listening "
            'to the record in the standard form. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    form_in_which_record_is_required: str = Field(
        default="",
        description=(
            "Specify the alternative form in which you require access to the record due to "
            'your disability. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    copy_of_record: BooleanLike = Field(
        default="", description="Select if you request a copy of the written or printed record."
    )

    inspection_of_record: BooleanLike = Field(
        default="",
        description="Select if you wish to inspect the written or printed record in person.",
    )

    view_the_images: BooleanLike = Field(
        default="",
        description=(
            "Select if you wish to view the visual images (photographs, slides, video, etc.)."
        ),
    )

    copy_of_the_images: BooleanLike = Field(
        default="", description="Select if you request a copy of the visual images."
    )

    transcription_of_the_images: BooleanLike = Field(
        default="", description="Select if you request a transcription of the visual images."
    )

    listen_to_the_soundtrack_audio_cassette: BooleanLike = Field(
        default="",
        description=(
            "Select if you wish to listen to the recorded words or information (e.g. audio "
            "cassette)."
        ),
    )

    transcription_of_soundtrack_written_or_printed_document: BooleanLike = Field(
        default="",
        description="Select if you request a written or printed transcription of the soundtrack.",
    )

    printed_copy_of_record: BooleanLike = Field(
        default="",
        description=(
            "Select if you request a printed copy of the electronic or machine-readable record."
        ),
    )

    printed_copy_of_information_derived_from_the_record: BooleanLike = Field(
        default="",
        description=(
            "Select if you request a printed copy of information derived from the "
            "electronic record."
        ),
    )

    copy_in_computer_readable_form_stiffy_or_compact_disc: BooleanLike = Field(
        default="",
        description=(
            "Select if you request a copy of the record in a computer-readable format (e.g. "
            "disk or compact disc)."
        ),
    )

    posted_copy_or_transcription_yes: BooleanLike = Field(
        default="",
        description=(
            "Select YES if you want the requested copy or transcription to be posted to you "
            "(postage payable)."
        ),
    )

    posted_copy_or_transcription_no: BooleanLike = Field(
        default="",
        description=(
            "Select NO if you do not want the requested copy or transcription to be posted to you."
        ),
    )


class ParticularsofRighttobeExercisedorProtected(BaseModel):
    """Details of the right being exercised or protected and why the record is required"""

    indicate_which_right_is_to_be_exercised_or_protected: str = Field(
        ...,
        description=(
            "State which specific right you intend to exercise or protect by requesting "
            'this record. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    explain_why_record_is_required_for_exercise_or_protection_of_right: str = Field(
        ...,
        description=(
            "Explain the reasons the requested record is necessary to exercise or protect "
            'the right you identified. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class FormCRequestForAccessToRecordOfPrivateBody(BaseModel):
    """FORM C: REQUEST FOR ACCESS TO RECORD OF PRIVATE BODY"""

    form_of_access_to_record: FormofAccesstoRecord = Field(
        ..., description="Form of Access to Record"
    )
    particulars_of_right_to_be_exercised_or_protected: ParticularsofRighttobeExercisedorProtected = Field(
        ..., description="Particulars of Right to be Exercised or Protected"
    )
