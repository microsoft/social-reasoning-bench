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
        ...,
        description=(
            "Date of the City Council meeting you are requesting this item be placed on the agenda."
        ),
    )  # YYYY-MM-DD format

    title_of_item: str = Field(
        ...,
        description=(
            "Short descriptive title of the agenda item. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AgendaPlacementActionType(BaseModel):
    """Agenda category and type of council action requested"""

    information_only: BooleanLike = Field(
        default="",
        description="Check if this agenda item is for information only, with no action requested.",
    )

    action_requested: str = Field(
        default="",
        description=(
            "Brief description of the specific action being requested from the Council. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    direction_requested: BooleanLike = Field(
        default="",
        description=(
            "Check if you are requesting general direction or guidance rather than a formal action."
        ),
    )

    consent_agenda: BooleanLike = Field(
        default="", description="Check if this item is intended for the consent agenda."
    )

    approve_deny_motion: BooleanLike = Field(
        default="",
        description="Check if the requested action is to approve or deny a specific motion.",
    )

    discussion_item: BooleanLike = Field(
        default="", description="Check if this item is for discussion only."
    )

    p_f_committee: BooleanLike = Field(
        default="", description="Check if this item is to be routed through the P&F Committee."
    )

    adopt_resolution: BooleanLike = Field(
        default="",
        description="Check if the requested action is adoption of a resolution (attach draft).",
    )

    hold_public_hearing: BooleanLike = Field(
        default="",
        description=(
            "Check if this item requires a public hearing (provide copy of published "
            "hearing notice)."
        ),
    )

    spw_committee: BooleanLike = Field(
        default="", description="Check if this item is to be routed through the SPW Committee."
    )

    ordinance_1st_reading: BooleanLike = Field(
        default="",
        description="Check if the requested action is the first reading of an ordinance.",
    )

    main_agenda: BooleanLike = Field(
        default="", description="Check if this item should appear on the main agenda."
    )


class SubmitterPresenterInformation(BaseModel):
    """Who is submitting and presenting the item"""

    submitted_by: str = Field(
        ...,
        description=(
            "Name of the person submitting this agenda request. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    department: str = Field(
        ...,
        description=(
            "Department responsible for this agenda item. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    presenter_name_title: str = Field(
        ...,
        description=(
            "Name and title of the person who will present this item to the Council. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    estimated_time_needed: str = Field(
        default="",
        description=(
            "Approximate amount of meeting time needed for this item (e.g., in minutes). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class IssueDetails(BaseModel):
    """Description of the issue, options, and recommended action"""

    summary_of_issue: str = Field(
        ...,
        description=(
            "Concise summary of the issue or topic to be considered. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    alternatives_options_effects_comments: str = Field(
        default="",
        description=(
            "Describe alternatives, options, impacts on others, and any additional "
            'comments. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    recommended_action_motion: str = Field(
        ...,
        description=(
            "Exact recommended action or motion language for the Council to consider. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class FinancialImpact(BaseModel):
    """Cost, budgeting, and financial explanation"""

    financial_impact: str = Field(
        default="",
        description=(
            "Narrative description of the financial impact of this request. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    is_there_a_cost_associated_with_this_request_yes: BooleanLike = Field(
        default="", description="Check if there is a cost associated with this request."
    )

    is_there_a_cost_associated_with_this_request_no: BooleanLike = Field(
        default="", description="Check if there is no cost associated with this request."
    )

    what_is_the_total_cost_with_tax_and_shipping: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total dollar amount of the cost, including tax and shipping."
    )

    is_this_budgeted_yes: BooleanLike = Field(
        default="", description="Check if the cost is already included in the current budget."
    )

    is_this_budgeted_no: BooleanLike = Field(
        default="", description="Check if the cost is not included in the current budget."
    )

    please_explain: str = Field(
        default="",
        description=(
            "Explanation of the budgeting status or financial details, especially if not "
            'budgeted. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
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
    submitter__presenter_information: SubmitterPresenterInformation = Field(
        ..., description="Submitter & Presenter Information"
    )
    issue_details: IssueDetails = Field(..., description="Issue Details")
    financial_impact: FinancialImpact = Field(..., description="Financial Impact")
