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
    """Requested meeting date, item title, agenda placement, and type of council action requested"""

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

    direction_requested: BooleanLike = Field(
        default="", description="Check if direction from the Council is requested"
    )

    approve_deny_motion: BooleanLike = Field(
        default="", description="Check if an approve/deny motion is requested"
    )

    adopt_resolution: BooleanLike = Field(
        default="", description="Check if adoption of a resolution is requested"
    )

    discussion_item: BooleanLike = Field(
        default="", description="Check if this is intended as a discussion item"
    )

    hold_public_hearing: BooleanLike = Field(
        default="", description="Check if a public hearing is to be held for this item"
    )

    ordinance_1st_reading: BooleanLike = Field(
        default="", description="Check if this item is for the first reading of an ordinance"
    )


class SubmissionPresentationDetails(BaseModel):
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
            "Estimated amount of meeting time needed for this item .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IssueDescriptionRecommendation(BaseModel):
    """Narrative description of the issue, alternatives, and recommended action"""

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
    """Cost, budgeting, and explanation of financial impact"""

    is_there_a_cost_associated_with_this_request: BooleanLike = Field(
        default="", description="Indicate whether there is any cost associated with this request"
    )

    what_is_the_total_cost_with_tax_and_shipping: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total cost of the request including tax and shipping"
    )

    is_this_budgeted: BooleanLike = Field(
        default="", description="Indicate whether this cost is already included in the budget"
    )

    please_explain: str = Field(
        default="",
        description=(
            "Explanation regarding budget status or cost details .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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
    submission__presentation_details: SubmissionPresentationDetails = Field(
        ..., description="Submission & Presentation Details"
    )
    issue_description__recommendation: IssueDescriptionRecommendation = Field(
        ..., description="Issue Description & Recommendation"
    )
    financial_impact: FinancialImpact = Field(..., description="Financial Impact")
