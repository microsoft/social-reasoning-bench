from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AgendaRequestDetails(BaseModel):
    """Basic information about the requested agenda item and meeting"""

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
    """Where the item appears on the agenda and what action is requested"""

    information_only: BooleanLike = Field(
        default="", description="Check if this agenda item is for information only"
    )

    consent_agenda: BooleanLike = Field(
        default="", description="Check if this item should be placed on the consent agenda"
    )

    p_f_committee: BooleanLike = Field(
        default="", description="Check if this item is for the P&F Committee agenda"
    )

    spw_committee: BooleanLike = Field(
        default="", description="Check if this item is for the SPW Committee agenda"
    )

    main_agenda: BooleanLike = Field(
        default="", description="Check if this item is for the main City Council agenda"
    )

    direction_requested: BooleanLike = Field(
        default="", description="Check if direction from the Council is requested"
    )

    approve_deny_motion: BooleanLike = Field(
        default="", description="Check if Council is asked to approve or deny a motion"
    )

    adopt_resolution: BooleanLike = Field(
        default="", description="Check if Council is asked to adopt a resolution (attach draft)"
    )

    discussion_item: BooleanLike = Field(
        default="", description="Check if this item is for discussion only"
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


class SubmitterPresenterInformation(BaseModel):
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
            "Approximate amount of meeting time needed for this item .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IssueDescription(BaseModel):
    """Narrative description of the issue, options, and recommended action"""

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
            "Describe alternatives, options, and impacts on others, plus any comments .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    recommended_action_motion: str = Field(
        ...,
        description=(
            "Exact recommended Council action or motion wording .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FinancialImpact(BaseModel):
    """Cost, budgeting, and financial explanation for the request"""

    is_there_a_cost_associated_with_this_request: BooleanLike = Field(
        default="", description="Indicate whether there is any cost associated with this request"
    )

    yes_cost_associated_with_this_request: BooleanLike = Field(
        default="", description="Check if there is a cost associated with this request"
    )

    no_cost_associated_with_this_request: BooleanLike = Field(
        default="", description="Check if there is no cost associated with this request"
    )

    what_is_the_total_cost_with_tax_and_shipping: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total dollar amount including tax and shipping"
    )

    is_this_budgeted: BooleanLike = Field(
        default="", description="Indicate whether this cost is included in the current budget"
    )

    yes_budgeted: BooleanLike = Field(
        default="", description="Check if the cost is already budgeted"
    )

    no_budgeted: BooleanLike = Field(default="", description="Check if the cost is not budgeted")

    please_explain: str = Field(
        default="",
        description=(
            "Explanation of cost details or budget status .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class BrainerdCityCouncilAgendaRequest(BaseModel):
    """Brainerd City Council
    Agenda Request"""

    agenda_request_details: AgendaRequestDetails = Field(..., description="Agenda Request Details")
    agenda_placement__action_type: AgendaPlacementActionType = Field(
        ..., description="Agenda Placement & Action Type"
    )
    submitter__presenter_information: SubmitterPresenterInformation = Field(
        ..., description="Submitter & Presenter Information"
    )
    issue_description: IssueDescription = Field(..., description="Issue Description")
    financial_impact: FinancialImpact = Field(..., description="Financial Impact")
