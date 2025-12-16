from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class SampleNoRow(BaseModel):
    """Single row in Sample No"""

    sample_no: str = Field(default="", description="Sample_No")
    sample_description_or_techmet_part_number: str = Field(
        default="", description="Sample_Description_Or_Techmet_Part_Number"
    )
    grade: str = Field(default="", description="Grade")
    qty_pcs: str = Field(default="", description="Qty_Pcs")


class SampleNotesAndCommentsRow(BaseModel):
    """Single row in Sample Notes and Comments"""

    sample_no: str = Field(default="", description="Sample_No")
    sample_notes_and_comments: str = Field(default="", description="Sample_Notes_And_Comments")


class CanSamplesBeDestroyedRow(BaseModel):
    """Single row in Can Samples Be Destroyed?"""

    sample_no: str = Field(default="", description="Sample_No")
    can_samples_be_destroyed: str = Field(default="", description="Can_Samples_Be_Destroyed")
    do_parts_need_to_be_returned: str = Field(
        default="", description="Do_Parts_Need_To_Be_Returned"
    )
    return_address_if_yes: str = Field(default="", description="Return_Address_If_Yes")


class RequestorInformation(BaseModel):
    """Information about the company and person requesting testing"""

    company: str = Field(
        ...,
        description=(
            "Name of the company submitting the samples .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    requestor_name: str = Field(
        ...,
        description=(
            "Full name of the person requesting the testing .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_information_and_return_address: str = Field(
        ...,
        description=(
            "Phone, email, and full mailing address for returning results or parts .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    techmet_sales_representative_if_different_than_requestor_name: str = Field(
        default="",
        description=(
            "Name of the TechMet sales representative, if not the same as the requestor .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SampleInformation(BaseModel):
    """Details about each submitted sample"""

    sample_no: List[SampleNoRow] = Field(
        ...,
        description="Table listing each sample number with its description, grade, and quantity",
    )  # List of table rows

    sample_description_or_techmet_part_number: str = Field(
        ...,
        description=(
            "Description of the sample or the corresponding TechMet part number .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    grade: str = Field(
        default="",
        description=(
            "Material grade or specification for the sample, if known .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    qty_pcs: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Quantity or number of pieces for each sample"
    )


class NotesComments(BaseModel):
    """Additional notes and comments for each sample"""

    sample_notes_and_comments: List[SampleNotesAndCommentsRow] = Field(
        default="", description="Table to record detailed notes and comments for each sample"
    )  # List of table rows


class TestingQuestions(BaseModel):
    """Testing-related instructions and return requirements for each sample"""

    can_samples_be_destroyed: List[CanSamplesBeDestroyedRow] = Field(
        ...,
        description=(
            "Table indicating for each sample whether it may be destroyed during testing "
            "and whether parts need to be returned"
        ),
    )  # List of table rows

    do_parts_need_to_be_returned: BooleanLike = Field(
        default="", description="Indicate if tested parts must be returned to the requestor"
    )

    if_yes_please_provide_return_address: str = Field(
        default="",
        description=(
            "Return shipping address if parts need to be returned .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class TechmetTestingLabSampleSubmissionForm(BaseModel):
    """
    TechMet Testing Lab Sample Submission Form

    Include completed form with sample(s) and send to: Rich Deptola/Brian Powell Jr, 730 21st St Dr SE, Hickory, NC 28602. Clearly describe what needs to be done and include all relevant information for each sample submitted for testing. Please note that if not sending a complete rod or insert the sample needs to weigh at least 5 grams.
    """

    requestor_information: RequestorInformation = Field(..., description="Requestor Information")
    sample_information: SampleInformation = Field(..., description="Sample Information")
    notescomments: NotesComments = Field(..., description="Notes/Comments")
    testing_questions: TestingQuestions = Field(..., description="Testing Questions")
