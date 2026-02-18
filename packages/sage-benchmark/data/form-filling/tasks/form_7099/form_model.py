from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AgendaItemDetails(BaseModel):
    """Basic information about the requested agenda item and where it belongs on the agenda"""

    requested_meeting_date: str = Field(
        ..., description="Date of the City Council meeting being requested"
    )  # YYYY-MM-DD format

    title_of_item: str = Field(
        ...,
        description=(
            "Short descriptive title of the agenda item .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    information_only: BooleanLike = Field(
        default="", description="Check if this agenda item is for information only"
    )

    consent_agenda: BooleanLike = Field(
        default="", description="Check if this item should appear on the consent agenda"
    )

    p_f_committee: BooleanLike = Field(
        default="", description="Check if this item is for the P&F Committee"
    )

    spw_committee: BooleanLike = Field(
        default="", description="Check if this item is for the SPW Committee"
    )

    main_agenda: BooleanLike = Field(
        default="", description="Check if this item should appear on the main agenda"
    )


class RequestedAction(BaseModel):
    """Type of action being requested from the council"""

    action_requested: str = Field(
        default="",
        description=(
            "Brief description of the action requested from the Council .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    approve_deny_motion: BooleanLike = Field(
        default="", description="Check if the requested action is to approve or deny a motion"
    )

    adopt_resolution_attach_draft: BooleanLike = Field(
        default="",
        description="Check if the requested action is to adopt a resolution and attach the draft",
    )

    direction_requested: BooleanLike = Field(
        default="", description="Check if guidance or direction from the Council is requested"
    )

    discussion_item: BooleanLike = Field(
        default="", description="Check if this is for discussion only with no formal action"
    )

    hold_public_hearing: BooleanLike = Field(
        default="",
        description=(
            "Check if a public hearing is to be held; provide copy of published hearing notice"
        ),
    )

    ordinance_1st_reading: BooleanLike = Field(
        default="", description="Check if this item is for the first reading of an ordinance"
    )


class SubmissionPresenterInformation(BaseModel):
    """Who is submitting the request and who will present it"""

    submitted_by: str = Field(
        ...,
        description=(
            "Name of the person submitting the agenda request .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    department: str = Field(
        ...,
        description=(
            "Department responsible for the agenda item .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    presenter_name_title: str = Field(
        default="",
        description=(
            "Name and title of the person who will present this item .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    estimated_time_needed: str = Field(
        default="",
        description=(
            "Approximate amount of meeting time needed for this item .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IssueDetails(BaseModel):
    """Description of the issue, alternatives, and recommended action"""

    summary_of_issue: str = Field(
        ...,
        description=(
            "Concise summary of the issue to be considered .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    alternatives_options_effects_on_others_comments: str = Field(
        default="",
        description=(
            "Describe alternatives, options, and potential effects on others; include any "
            'comments .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    recommended_action_motion: str = Field(
        ...,
        description=(
            "Specific recommended action or motion language for the Council .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class FinancialImpact(BaseModel):
    """Cost and budget information related to the request"""

    financial_impact: str = Field(
        default="",
        description=(
            "Narrative description of the financial impact of this request .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    is_there_a_cost_associated_with_this_request_yes: BooleanLike = Field(
        default="", description="Select if there is a cost associated with this request"
    )

    is_there_a_cost_associated_with_this_request_no: BooleanLike = Field(
        default="", description="Select if there is no cost associated with this request"
    )

    what_is_the_total_cost_with_tax_and_shipping: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total dollar amount of the cost including tax and shipping"
    )

    is_this_budgeted_yes: BooleanLike = Field(
        default="", description="Select if the cost is already included in the approved budget"
    )

    is_this_budgeted_no: BooleanLike = Field(
        default="", description="Select if the cost is not included in the approved budget"
    )

    please_explain: str = Field(
        default="",
        description=(
            "Explanation of budget status or additional financial details .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class BrainerdCityCouncilAgendaRequest(BaseModel):
    """
        Brainerd City Council
    Agenda Request

        ''
    """

    agenda_item_details: AgendaItemDetails = Field(..., description="Agenda Item Details")
    requested_action: RequestedAction = Field(..., description="Requested Action")
    submission__presenter_information: SubmissionPresenterInformation = Field(
        ..., description="Submission & Presenter Information"
    )
    issue_details: IssueDetails = Field(..., description="Issue Details")
    financial_impact: FinancialImpact = Field(..., description="Financial Impact")
