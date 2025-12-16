from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CaseInformation(BaseModel):
    """Details about the case and proceeding"""

    county: str = Field(
        ...,
        description=(
            "Name of the county where the case is filed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    case_caption: str = Field(
        ...,
        description=(
            "Full case caption as it appears on court documents .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    docket_number: str = Field(
        ...,
        description=(
            'Court docket number for this case .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    presiding_judge: str = Field(
        ...,
        description=(
            "Name of the judge who presided over the proceeding .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    dates_of_proceeding: str = Field(
        ...,
        description=(
            "Date or range of dates when the proceeding occurred .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    court_reporter_name_if_available: str = Field(
        default="",
        description=(
            'Name of the court reporter, if known .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    case_type_criminal: BooleanLike = Field(..., description="Check if the case type is Criminal")

    case_type_civil: BooleanLike = Field(..., description="Check if the case type is Civil")

    case_type_family: BooleanLike = Field(..., description="Check if the case type is Family")

    case_type_orphans_court: BooleanLike = Field(
        ..., description="Check if the case type is Orphans’ Court"
    )

    case_type_juvenile: BooleanLike = Field(..., description="Check if the case type is Juvenile")

    type_of_proceeding_suppression: BooleanLike = Field(
        ..., description="Check if the proceeding type is Suppression"
    )

    type_of_proceeding_argument: BooleanLike = Field(
        ..., description="Check if the proceeding type is Argument"
    )

    type_of_proceeding_trial: BooleanLike = Field(
        ..., description="Check if the proceeding type is Trial"
    )

    type_of_proceeding_plea: BooleanLike = Field(
        ..., description="Check if the proceeding type is Plea"
    )

    type_of_proceeding_sentence: BooleanLike = Field(
        ..., description="Check if the proceeding type is Sentence"
    )

    type_of_proceeding_other_please_specify: str = Field(
        default="",
        description=(
            "Describe the proceeding type if it is not listed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    pcra_yes: BooleanLike = Field(default="", description="Check Yes if this is a PCRA matter")

    pcra_no: BooleanLike = Field(default="", description="Check No if this is not a PCRA matter")

    is_the_transcript_associated_with_an_appeal_yes: BooleanLike = Field(
        default="", description="Check Yes if the transcript request is associated with an appeal"
    )

    is_the_transcript_associated_with_an_appeal_no: BooleanLike = Field(
        default="",
        description="Check No if the transcript request is not associated with an appeal",
    )

    childrens_fast_track_yes: BooleanLike = Field(
        default="", description="Check Yes if this is a Children’s Fast Track appeal"
    )

    childrens_fast_track_no: BooleanLike = Field(
        default="", description="Check No if this is not a Children’s Fast Track appeal"
    )


class RequestorInformation(BaseModel):
    """Information about the person making the request"""

    name_of_requestor_attorney_id_number_if_applicable: str = Field(
        ...,
        description=(
            "Name of the person requesting the transcript and attorney ID number if "
            'applicable .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    i_am_counsel_for: str = Field(
        default="",
        description=(
            "If you are counsel, indicate the party you represent .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    i_am_unrepresented: BooleanLike = Field(
        default="", description="Check if you are an unrepresented party"
    )

    i_am_not_a_party_to_this_action: BooleanLike = Field(
        default="", description="Check if you are not a party to this action"
    )

    agency_firm: str = Field(
        default="",
        description=(
            "Name of the agency or law firm, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    court_represented_yes: BooleanLike = Field(
        default="", description="Check Yes if you represent the court"
    )

    court_represented_no: BooleanLike = Field(
        default="", description="Check No if you do not represent the court"
    )

    street_address: str = Field(
        ...,
        description=(
            'Street address of the requestor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the requestor’s address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of the requestor’s address")

    zip: str = Field(..., description="ZIP code of the requestor’s address")

    email: str = Field(
        ...,
        description=(
            'Email address of the requestor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Primary phone number of the requestor .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            'Fax number of the requestor, if any .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    does_this_request_qualify_for_a_reduced_rate_pursuant_to_pa_r_j_a_4007_e_yes: BooleanLike = (
        Field(
            default="",
            description="Check Yes if the request qualifies for a reduced transcript rate",
        )
    )

    does_this_request_qualify_for_a_reduced_rate_pursuant_to_pa_r_j_a_4007_e_no: BooleanLike = (
        Field(
            default="",
            description="Check No if the request does not qualify for a reduced transcript rate",
        )
    )


class TranscriptItemsRequested(BaseModel):
    """Specific transcript portions being requested"""

    entire_proceeding: BooleanLike = Field(
        default="", description="Check to request a transcript of the entire proceeding"
    )

    jury_voir_dire: BooleanLike = Field(
        default="", description="Check to request a transcript of jury voir dire"
    )

    opening_statements: BooleanLike = Field(
        default="", description="Check to request a transcript of opening statements"
    )

    closing_arguments: BooleanLike = Field(
        default="", description="Check to request a transcript of closing arguments"
    )

    jury_instructions: BooleanLike = Field(
        default="", description="Check to request a transcript of jury instructions"
    )

    testimony_specify_each_witness: str = Field(
        default="",
        description=(
            "List each witness whose testimony transcript is requested .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    pre_post_trial_hearing_specify: str = Field(
        default="",
        description=(
            "Specify which pre- or post-trial hearing transcript is requested .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    other_specify: str = Field(
        default="",
        description=(
            "Describe any other transcript items requested .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class RequestForTranscriptOrCopy(BaseModel):
    """
    Request for Transcript or Copy

    Pursuant to Pa.R.J.A. 4007(A), this form must be completed by any person requesting a transcript for any court proceeding. Additional requirements may be found in the local rules of court for each judicial district. Local rules may be found by following the appropriate link at: http://www.pacourts.us/courts/courts-of-common-pleas/
    If the cost of the transcript presents an economic hardship, there are reduced rates available to those who qualify. See Pa.R.J.A. 4007(E). Copies of this request must be served in accordance with Pa.R.J.A. 4007(B). A deposit determined by local rule may be required.
    """

    case_information: CaseInformation = Field(..., description="Case Information")
    requestor_information: RequestorInformation = Field(..., description="Requestor Information")
    transcript_items_requested: TranscriptItemsRequested = Field(
        ..., description="Transcript Items Requested"
    )
