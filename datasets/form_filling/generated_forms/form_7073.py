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
    """Where the item appears on the agenda and what action is requested"""

    information_only: BooleanLike = Field(
        default="",
        description="Check if this agenda item is for information only, with no action requested.",
    )

    approve_deny_motion: BooleanLike = Field(
        default="", description="Check if the requested action is to approve or deny a motion."
    )

    direction_requested: BooleanLike = Field(
        default="",
        description="Check if you are requesting direction or guidance from the Council.",
    )

    consent_agenda: BooleanLike = Field(
        default="", description="Check if this item is intended for the consent agenda."
    )

    adopt: BooleanLike = Field(
        default="",
        description=(
            "Check if the requested action is to adopt the attached item (e.g., resolution, "
            "policy)."
        ),
    )

    discussion_item: BooleanLike = Field(
        default="", description="Check if this item is for discussion only."
    )

    p_f_committee: BooleanLike = Field(
        default="", description="Check if this item is for the P&F Committee agenda."
    )

    resolution_attach_draft: BooleanLike = Field(
        default="",
        description="Check if this item involves a resolution and attach a draft resolution.",
    )

    hold_public_hearing: BooleanLike = Field(
        default="",
        description=(
            "Check if a public hearing is to be held for this item; provide copy of "
            "published hearing notice."
        ),
    )

    spw_committee: BooleanLike = Field(
        default="", description="Check if this item is for the SPW Committee agenda."
    )

    ordinance_1st_reading: BooleanLike = Field(
        default="", description="Check if this item is for the first reading of an ordinance."
    )

    main_agenda: BooleanLike = Field(
        default="", description="Check if this item is for the main City Council agenda."
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
            "Name and title of the person who will present this item. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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
    """Description of the issue, alternatives, and recommended action"""

    summary_of_issue: str = Field(
        ...,
        description=(
            "Brief summary describing the issue or request. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    alternatives_options_effects_on_others_comments: str = Field(
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
            "Exact recommended action or motion language for the Council. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class FinancialImpact(BaseModel):
    """Cost and budget information related to the request"""

    cost_associated_yes: BooleanLike = Field(
        default="", description="Select if there is a cost associated with this request."
    )

    cost_associated_no: BooleanLike = Field(
        default="", description="Select if there is no cost associated with this request."
    )

    total_cost_with_tax_and_shipping: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total dollar amount of the cost, including tax and shipping."
    )

    is_this_budgeted_yes: BooleanLike = Field(
        default="", description="Select if this cost is already included in the approved budget."
    )

    is_this_budgeted_no: BooleanLike = Field(
        default="", description="Select if this cost is not included in the approved budget."
    )

    please_explain: str = Field(
        default="",
        description=(
            "Explanation of the financial impact and/or budget status. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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
