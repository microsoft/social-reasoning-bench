from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MeetingAgendaDetails(BaseModel):
    """Basic information about the meeting date, item, and agenda placement"""

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
        default="", description="Check if this item should appear on the main council agenda"
    )


class RequestedCouncilAction(BaseModel):
    """Type of action or decision requested from the council"""

    approve_deny_motion: BooleanLike = Field(
        default="", description="Check if council action requested is to approve or deny a motion"
    )

    adopt_resolution_attach_draft: BooleanLike = Field(
        default="",
        description=(
            "Check if council action requested is to adopt a resolution; attach draft resolution"
        ),
    )

    direction_requested: BooleanLike = Field(
        default="", description="Check if staff is requesting direction from the council"
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


class SubmissionPresentationDetails(BaseModel):
    """Information about the submitter and presenter"""

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
            "Approximate amount of meeting time needed for this item .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IssueDescriptionRecommendation(BaseModel):
    """Narrative description of the issue, options, and recommended action"""

    summary_of_issue: str = Field(
        ...,
        description=(
            "Brief summary or description of the issue for council consideration .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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
            "Specific recommended council action or motion wording .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FinancialImpact(BaseModel):
    """Cost and budget information related to the request"""

    is_there_a_cost_associated_with_this_request: BooleanLike = Field(
        ..., description="Indicate whether there is any cost associated with this request"
    )

    what_is_the_total_cost_with_tax_and_shipping: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total dollar amount of the cost, including tax and shipping"
    )

    is_this_budgeted: BooleanLike = Field(
        ..., description="Indicate whether this cost is already included in the approved budget"
    )

    please_explain: str = Field(
        default="",
        description=(
            "Explanation of funding source, budget status, or financial details .If you "
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

    meeting__agenda_details: MeetingAgendaDetails = Field(
        ..., description="Meeting & Agenda Details"
    )
    requested_council_action: RequestedCouncilAction = Field(
        ..., description="Requested Council Action"
    )
    submission__presentation_details: SubmissionPresentationDetails = Field(
        ..., description="Submission & Presentation Details"
    )
    issue_description__recommendation: IssueDescriptionRecommendation = Field(
        ..., description="Issue Description & Recommendation"
    )
    financial_impact: FinancialImpact = Field(..., description="Financial Impact")
