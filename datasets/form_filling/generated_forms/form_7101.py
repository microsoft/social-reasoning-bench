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
    """Basic details about the meeting and agenda item"""

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


class AgendaPlacement(BaseModel):
    """Where this item appears on the agenda"""

    information_only: BooleanLike = Field(
        default="", description="Check if this agenda item is for information only"
    )

    consent_agenda: BooleanLike = Field(
        default="", description="Check if this item should be placed on the consent agenda"
    )

    p_f_committee: BooleanLike = Field(
        default="", description="Check if this item is to be referred to the P&F Committee"
    )

    spw_committee: BooleanLike = Field(
        default="", description="Check if this item is to be referred to the SPW Committee"
    )

    main_agenda: BooleanLike = Field(
        default="", description="Check if this item should appear on the main agenda"
    )


class ActionRequested(BaseModel):
    """Type of action or direction requested from the council"""

    action_requested: str = Field(
        default="",
        description=(
            "Describe the specific action requested from the Council .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    direction_requested: BooleanLike = Field(
        default="", description="Check if direction from the Council is requested"
    )

    approve_deny_motion: BooleanLike = Field(
        default="", description="Check if the requested action is to approve or deny a motion"
    )

    discussion_item: BooleanLike = Field(
        default="", description="Check if this item is for discussion only"
    )

    adopt_resolution: BooleanLike = Field(
        default="",
        description="Check if the requested action is to adopt a resolution (attach draft)",
    )

    hold_public_hearing: BooleanLike = Field(
        default="",
        description=(
            "Check if a public hearing is to be held (provide copy of published hearing notice)"
        ),
    )

    ordinance_1st_reading: BooleanLike = Field(
        default="", description="Check if this item is for the first reading of an ordinance"
    )


class SubmissionDetails(BaseModel):
    """Who is submitting and presenting the item"""

    submitted_by: str = Field(
        ...,
        description=(
            "Name of the person submitting this agenda request .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    department: str = Field(
        ...,
        description=(
            "Department associated with this request .If you cannot fill this, write "
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
            "Estimated amount of meeting time needed for this item .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IssueDescription(BaseModel):
    """Narrative description of the issue and recommended action"""

    summary_of_issue: str = Field(
        ...,
        description=(
            "Brief summary and background of the issue .If you cannot fill this, write "
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
            "State the recommended Council action or motion text .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FinancialImpact(BaseModel):
    """Cost, budgeting, and financial explanation for the request"""

    financial_impact: str = Field(
        default="",
        description=(
            "Overall description of the financial impact of this request .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    is_there_a_cost_associated_with_this_request: Literal["Yes", "No", "N/A", ""] = Field(
        ..., description="Indicate whether there is any cost associated with this request"
    )

    yes_cost_associated_with_this_request: BooleanLike = Field(
        default="", description="Checked if there is a cost associated with this request"
    )

    no_cost_associated_with_this_request: BooleanLike = Field(
        default="", description="Checked if there is no cost associated with this request"
    )

    what_is_the_total_cost_with_tax_and_shipping: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total cost of the request, including tax and shipping"
    )

    is_this_budgeted: Literal["Yes", "No", "N/A", ""] = Field(
        default="", description="Indicate whether this cost is included in the current budget"
    )

    yes_budgeted: BooleanLike = Field(default="", description="Checked if the cost is budgeted")

    no_budgeted: BooleanLike = Field(default="", description="Checked if the cost is not budgeted")

    please_explain: str = Field(
        default="",
        description=(
            "Explain budget status, funding source, or other financial details .If you "
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

    meeting__item_information: MeetingItemInformation = Field(
        ..., description="Meeting & Item Information"
    )
    agenda_placement: AgendaPlacement = Field(..., description="Agenda Placement")
    action_requested: ActionRequested = Field(..., description="Action Requested")
    submission_details: SubmissionDetails = Field(..., description="Submission Details")
    issue_description: IssueDescription = Field(..., description="Issue Description")
    financial_impact: FinancialImpact = Field(..., description="Financial Impact")
