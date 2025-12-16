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

    information_only: BooleanLike = Field(
        default="",
        description="Check if this agenda item is for information only, with no action requested.",
    )

    consent_agenda: BooleanLike = Field(
        default="", description="Check if this item should be placed on the consent agenda."
    )

    p_f_committee: BooleanLike = Field(
        default="", description="Check if this item is intended for the P&F Committee."
    )

    spw_committee: BooleanLike = Field(
        default="", description="Check if this item is intended for the SPW Committee."
    )

    main_agenda: BooleanLike = Field(
        default="", description="Check if this item should appear on the main council agenda."
    )


class RequestedCouncilAction(BaseModel):
    """Type of action or decision requested from the council"""

    approve_deny_motion: BooleanLike = Field(
        default="",
        description="Check if you are requesting the council to approve or deny a specific motion.",
    )

    adopt_resolution_attach_draft: BooleanLike = Field(
        default="",
        description=(
            "Check if you are requesting adoption of a resolution and attach a draft resolution."
        ),
    )

    direction_requested: BooleanLike = Field(
        default="",
        description="Check if you are seeking general direction or guidance from the council.",
    )

    discussion_item: BooleanLike = Field(
        default="", description="Check if this item is for discussion only, without formal action."
    )

    hold_public_hearing: BooleanLike = Field(
        default="",
        description=(
            "Check if you are requesting that a public hearing be held on this item. A copy "
            "of the published hearing notice must be provided."
        ),
    )

    ordinance_1st_reading: BooleanLike = Field(
        default="", description="Check if this request is for the first reading of an ordinance."
    )


class SubmissionPresentationDetails(BaseModel):
    """Who is submitting and presenting the item and timing"""

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
            "Department or office associated with this request. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    presenter_name_title: str = Field(
        ...,
        description=(
            "Name and title of the person who will present this item to the council. .If "
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
    """Narrative description of the issue and recommended action"""

    summary_of_issue: str = Field(
        ...,
        description=(
            "Brief summary describing the issue or topic for council consideration. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    alternatives_options_effects_on_others_comments: str = Field(
        default="",
        description=(
            "Describe possible alternatives, options, impacts on others, and any additional "
            'comments. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    recommended_action_motion: str = Field(
        ...,
        description=(
            "Specific action or motion you recommend the council take. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FinancialImpact(BaseModel):
    """Cost, budgeting, and financial explanation"""

    is_there_a_cost_associated_with_this_request_yes: BooleanLike = Field(
        default="", description="Select if there is a cost associated with this request."
    )

    is_there_a_cost_associated_with_this_request_no: BooleanLike = Field(
        default="", description="Select if there is no cost associated with this request."
    )

    what_is_the_total_cost_with_tax_and_shipping: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total dollar amount of the cost, including tax and shipping."
    )

    is_this_budgeted_yes: BooleanLike = Field(
        default="", description="Select if the cost is already included in the approved budget."
    )

    is_this_budgeted_no: BooleanLike = Field(
        default="", description="Select if the cost is not included in the approved budget."
    )

    please_explain: str = Field(
        default="",
        description=(
            "Explain budget status, funding source, or other financial details. .If you "
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
    requested_council_action: RequestedCouncilAction = Field(
        ..., description="Requested Council Action"
    )
    submission__presentation_details: SubmissionPresentationDetails = Field(
        ..., description="Submission & Presentation Details"
    )
    issue_details: IssueDetails = Field(..., description="Issue Details")
    financial_impact: FinancialImpact = Field(..., description="Financial Impact")
