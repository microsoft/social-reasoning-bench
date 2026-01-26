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


class AgendaPlacementActionType(BaseModel):
    """Where the item appears on the agenda and what type of action is requested"""

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

    action_requested: str = Field(
        default="",
        description=(
            "Brief description of the specific action requested from the Council .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    direction_requested: BooleanLike = Field(
        default="", description="Check if direction from the Council is requested"
    )

    approve_deny: BooleanLike = Field(
        default="", description="Check if the requested action is to approve or deny something"
    )

    discussion_item: BooleanLike = Field(
        default="", description="Check if this is intended as a discussion item"
    )

    motion: str = Field(
        default="",
        description=(
            "Text of the proposed motion, if applicable .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    hold_public_hearing: BooleanLike = Field(
        default="",
        description=(
            "Check if a public hearing is to be held; attach copy of published hearing notice"
        ),
    )

    adopt: BooleanLike = Field(
        default="", description="Check if the requested action is to adopt the attached item"
    )

    resolution: BooleanLike = Field(
        default="", description="Check if the action involves adopting a resolution (attach draft)"
    )

    ordinance_1st_reading: BooleanLike = Field(
        default="", description="Check if this is an ordinance for first reading"
    )


class SubmitterPresentationDetails(BaseModel):
    """Who is submitting and presenting the item and timing"""

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
            "Estimated amount of meeting time needed for this item .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IssueDescription(BaseModel):
    """Narrative description of the issue, options, and recommended action"""

    summary_of_issue: str = Field(
        ...,
        description=(
            "Brief summary describing the issue or request .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    alternatives_options_effects_comments: str = Field(
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
            "Recommended Council action or exact motion language .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FinancialImpact(BaseModel):
    """Cost, budgeting, and financial explanation related to the request"""

    financial_impact: str = Field(
        default="",
        description=(
            "Narrative description of the financial impact of this request .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    is_there_a_cost_associated_with_this_request: BooleanLike = Field(
        ..., description="Indicate whether there is any cost associated with this request"
    )

    yes_cost_associated: BooleanLike = Field(
        default="", description="Check if there is a cost associated with this request"
    )

    no_cost_associated: BooleanLike = Field(
        default="", description="Check if there is no cost associated with this request"
    )

    what_is_the_total_cost_with_tax_and_shipping: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total dollar amount of the cost, including tax and shipping"
    )

    is_this_budgeted: BooleanLike = Field(
        ..., description="Indicate whether this cost is included in the current budget"
    )

    yes_budgeted: BooleanLike = Field(
        default="", description="Check if the cost is already budgeted"
    )

    no_budgeted: BooleanLike = Field(
        default="", description="Check if the cost is not currently budgeted"
    )

    please_explain: str = Field(
        default="",
        description=(
            "Explanation or details, especially if the item is not budgeted .If you cannot "
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

    meeting__item_details: MeetingItemDetails = Field(..., description="Meeting & Item Details")
    agenda_placement__action_type: AgendaPlacementActionType = Field(
        ..., description="Agenda Placement & Action Type"
    )
    submitter__presentation_details: SubmitterPresentationDetails = Field(
        ..., description="Submitter & Presentation Details"
    )
    issue_description: IssueDescription = Field(..., description="Issue Description")
    financial_impact: FinancialImpact = Field(..., description="Financial Impact")
