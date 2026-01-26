from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MeetingAgendaPlacement(BaseModel):
    """Requested meeting date, item title, and where it appears on the agenda"""

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
        default="", description="Check if this item is for the P&F Committee agenda"
    )

    spw_committee: BooleanLike = Field(
        default="", description="Check if this item is for the SPW Committee agenda"
    )

    main_agenda: BooleanLike = Field(
        default="", description="Check if this item should appear on the main council agenda"
    )


class ActionRequested(BaseModel):
    """Type of council action or discussion requested"""

    approve_deny_motion: BooleanLike = Field(
        default="", description="Check if the requested action is to approve or deny a motion"
    )

    adopt_resolution_attach_draft: BooleanLike = Field(
        default="",
        description="Check if the requested action is to adopt a resolution and attach the draft",
    )

    direction_requested: BooleanLike = Field(
        default="", description="Check if guidance or direction from the council is requested"
    )

    discussion_item: BooleanLike = Field(
        default="", description="Check if this is intended as a discussion-only item"
    )

    hold_public_hearing: BooleanLike = Field(
        default="",
        description="Check if a public hearing is to be held for this item (attach published notice)",
    )

    ordinance_1st_reading: BooleanLike = Field(
        default="", description="Check if this item is for the first reading of an ordinance"
    )


class SubmissionDetails(BaseModel):
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


class IssueDescriptionRecommendation(BaseModel):
    """Background, alternatives, and recommended council action"""

    summary_of_issue: str = Field(
        ...,
        description=(
            "Brief summary describing the issue or request .If you cannot fill this, write "
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
            "Proposed action or motion language for the council to consider .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class FinancialImpact(BaseModel):
    """Cost, budgeting, and explanation of financial impact"""

    is_there_a_cost_associated_with_this_request: BooleanLike = Field(
        default="", description="Indicate whether there is any cost associated with this request"
    )

    what_is_the_total_cost_with_tax_and_shipping: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total dollar amount of the cost including tax and shipping"
    )

    is_this_budgeted: BooleanLike = Field(
        default="", description="Indicate whether this cost is already included in the budget"
    )

    please_explain: str = Field(
        default="",
        description=(
            "Explanation or details regarding the financial impact or budgeting .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class BrainerdCityCouncilAgendaRequest(BaseModel):
    """Brainerd City Council
    Agenda Request"""

    meeting__agenda_placement: MeetingAgendaPlacement = Field(
        ..., description="Meeting & Agenda Placement"
    )
    action_requested: ActionRequested = Field(..., description="Action Requested")
    submission_details: SubmissionDetails = Field(..., description="Submission Details")
    issue_description__recommendation: IssueDescriptionRecommendation = Field(
        ..., description="Issue Description & Recommendation"
    )
    financial_impact: FinancialImpact = Field(..., description="Financial Impact")
