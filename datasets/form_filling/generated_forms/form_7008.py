from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MeetingItemInformation(BaseModel):
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


class AgendaPlacementActionType(BaseModel):
    """Where the item appears on the agenda and what type of action is requested"""

    information_only: BooleanLike = Field(
        default="", description="Check if this agenda item is for information only"
    )

    consent_agenda: BooleanLike = Field(
        default="", description="Check if this item should be placed on the consent agenda"
    )

    pf_committee: BooleanLike = Field(
        default="", description="Check if this item is for the P&F Committee"
    )

    spw_committee: BooleanLike = Field(
        default="", description="Check if this item is for the SPW Committee"
    )

    main_agenda: BooleanLike = Field(
        default="", description="Check if this item should appear on the main agenda"
    )

    action_requested_direction_requested: BooleanLike = Field(
        default="", description="Check if direction from the Council is requested"
    )

    action_requested_approve_deny_motion: BooleanLike = Field(
        default="", description="Check if an approve/deny motion is requested"
    )

    action_requested_discussion_item: BooleanLike = Field(
        default="", description="Check if this item is for discussion only"
    )

    action_requested_adopt_resolution_attach_draft: BooleanLike = Field(
        default="",
        description="Check if adoption of a resolution is requested and attach the draft",
    )

    action_requested_hold_public_hearing: BooleanLike = Field(
        default="",
        description=(
            "Check if a public hearing is requested; provide copy of published hearing notice"
        ),
    )

    action_requested_ordinance_1st_reading: BooleanLike = Field(
        default="", description="Check if this is for the first reading of an ordinance"
    )


class SubmissionPresentationDetails(BaseModel):
    """Who is submitting and presenting the item"""

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
            "Approximate time needed on the agenda for this item .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IssueDescription(BaseModel):
    """Narrative description of the issue, options, and recommended action"""

    summary_of_issue: str = Field(
        ...,
        description=(
            "Brief summary of the issue to be considered .If you cannot fill this, write "
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
            "Proposed action or motion language for the Council .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FinancialImpact(BaseModel):
    """Cost, budgeting, and financial explanation for the request"""

    is_there_a_cost_associated_with_this_request_yes: BooleanLike = Field(
        default="", description="Select if there is a cost associated with this request"
    )

    is_there_a_cost_associated_with_this_request_no: BooleanLike = Field(
        default="", description="Select if there is no cost associated with this request"
    )

    what_is_the_total_cost_with_tax_and_shipping: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total cost of the request, including tax and shipping"
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
            "Explanation of cost and/or budget status .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class BrainerdCityCouncilAgendaRequest(BaseModel):
    """
        Brainerd City Council
    Agenda Request

        ''
    """

    meeting__item_information: MeetingItemInformation = Field(
        ..., description="Meeting & Item Information"
    )
    agenda_placement__action_type: AgendaPlacementActionType = Field(
        ..., description="Agenda Placement & Action Type"
    )
    submission__presentation_details: SubmissionPresentationDetails = Field(
        ..., description="Submission & Presentation Details"
    )
    issue_description: IssueDescription = Field(..., description="Issue Description")
    financial_impact: FinancialImpact = Field(..., description="Financial Impact")
