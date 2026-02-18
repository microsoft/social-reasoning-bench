from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MeetingItemDetails(BaseModel):
    """Basic information about the meeting and agenda item"""

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
        default="", description="Check if this item should be placed on the consent agenda"
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


class RequestedCouncilAction(BaseModel):
    """Type of action or decision requested from the council"""

    approve_deny_motion: BooleanLike = Field(
        default="", description="Check if the requested action is to approve or deny a motion"
    )

    adopt_resolution_attach_draft: BooleanLike = Field(
        default="",
        description="Check if the requested action is to adopt a resolution and attach the draft",
    )

    direction_requested: BooleanLike = Field(
        default="", description="Check if staff is requesting direction from the Council"
    )

    discussion_item: BooleanLike = Field(
        default="", description="Check if this is for discussion only"
    )

    hold_public_hearing: BooleanLike = Field(
        default="",
        description=(
            "Check if a public hearing is to be held; attach copy of published hearing notice"
        ),
    )

    ordinance_1st_reading: BooleanLike = Field(
        default="", description="Check if this item is for the first reading of an ordinance"
    )


class SubmissionPresentation(BaseModel):
    """Who is submitting and presenting the item, and timing"""

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
            "Department responsible for this agenda item .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    presenter_name_title: str = Field(
        ...,
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
            "Brief summary or description of the issue .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    alternatives_options_effects_on_others_comments: str = Field(
        default="",
        description=(
            "Describe alternatives, options, impacts on others, and any additional comments "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    recommended_action_motion: str = Field(
        ...,
        description=(
            "Proposed action or motion language for the Council .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FinancialImpact(BaseModel):
    """Cost, budgeting, and financial explanation"""

    is_there_a_cost_associated_with_this_request_yes: BooleanLike = Field(
        default="", description="Select if there is a cost associated with this request"
    )

    is_there_a_cost_associated_with_this_request_no: BooleanLike = Field(
        default="", description="Select if there is no cost associated with this request"
    )

    what_is_the_total_cost_with_tax_and_shipping: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total dollar amount of the cost, including tax and shipping"
    )

    is_this_budgeted_yes: BooleanLike = Field(
        default="", description="Select if this cost is already included in the budget"
    )

    is_this_budgeted_no: BooleanLike = Field(
        default="", description="Select if this cost is not included in the budget"
    )

    please_explain: str = Field(
        default="",
        description=(
            "Explanation or details regarding budget status or financial impact .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class BrainerdCityCouncilAgendaRequest(BaseModel):
    """
        Brainerd City Council
    Agenda Request

        ''
    """

    meeting__item_details: MeetingItemDetails = Field(..., description="Meeting & Item Details")
    requested_council_action: RequestedCouncilAction = Field(
        ..., description="Requested Council Action"
    )
    submission__presentation: SubmissionPresentation = Field(
        ..., description="Submission & Presentation"
    )
    issue_details: IssueDetails = Field(..., description="Issue Details")
    financial_impact: FinancialImpact = Field(..., description="Financial Impact")
