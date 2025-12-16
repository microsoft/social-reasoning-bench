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
            "Short descriptive title for the agenda item. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AgendaPlacementActionType(BaseModel):
    """Agenda category, committee routing, and type of council action requested"""

    information_only: BooleanLike = Field(
        default="",
        description="Check if this agenda item is for information only, with no action requested.",
    )

    action_requested: str = Field(
        default="",
        description=(
            "Describe the specific action being requested from the City Council. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    approve_deny_motion: BooleanLike = Field(
        default="", description="Check if the requested action is to approve or deny a motion."
    )

    direction_requested: BooleanLike = Field(
        default="",
        description="Check if you are requesting general direction or guidance from the Council.",
    )

    consent_agenda: BooleanLike = Field(
        default="", description="Check if this item is intended for the consent agenda."
    )

    adopt_resolution_attach_draft: BooleanLike = Field(
        default="",
        description=(
            "Check if the requested action is to adopt a resolution and attach the draft "
            "resolution."
        ),
    )

    discussion_item: BooleanLike = Field(
        default="", description="Check if this item is for discussion only."
    )

    p_f_committee: BooleanLike = Field(
        default="", description="Check if this item should go to the P&F Committee."
    )

    hold_public_hearing: BooleanLike = Field(
        default="",
        description=(
            "Check if a public hearing is to be held for this item. Provide a copy of the "
            "published hearing notice."
        ),
    )

    ordinance_1st_reading: BooleanLike = Field(
        default="", description="Check if this item is for the first reading of an ordinance."
    )

    spw_committee: BooleanLike = Field(
        default="", description="Check if this item should go to the SPW Committee."
    )

    main_agenda: BooleanLike = Field(
        default="", description="Check if this item should appear on the main agenda."
    )


class StaffPresentationDetails(BaseModel):
    """Submitting staff member and presentation logistics"""

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


class IssueDescriptionRecommendation(BaseModel):
    """Narrative description of the issue, options, and recommended council action"""

    summary_of_issue: str = Field(
        ...,
        description=(
            "Briefly summarize the issue or topic for the agenda item. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    alternatives_options_effects_on_others_comments: str = Field(
        default="",
        description=(
            "Describe alternatives, options considered, and any effects on others or "
            'additional comments. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    recommended_action_motion: str = Field(
        ...,
        description=(
            "State the recommended Council action or motion language. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FinancialImpact(BaseModel):
    """Cost, budgeting, and financial explanation related to the request"""

    is_there_a_cost_associated_with_this_request: BooleanLike = Field(
        ..., description="Indicate whether there is any cost associated with this request."
    )

    yes_cost_associated_with_this_request: BooleanLike = Field(
        default="", description="Check if there is a cost associated with this request."
    )

    no_cost_associated_with_this_request: BooleanLike = Field(
        default="", description="Check if there is no cost associated with this request."
    )

    what_is_the_total_cost_with_tax_and_shipping: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total dollar amount of the cost, including tax and shipping."
    )

    is_this_budgeted: BooleanLike = Field(
        ..., description="Indicate whether this cost is already included in the approved budget."
    )

    yes_budgeted: BooleanLike = Field(default="", description="Check if the cost is budgeted.")

    no_budgeted: BooleanLike = Field(default="", description="Check if the cost is not budgeted.")

    please_explain: str = Field(
        default="",
        description=(
            "Provide additional explanation regarding the financial impact or budgeting. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class BrainerdCityCouncilAgendaRequest(BaseModel):
    """Brainerd City Council
    Agenda Request"""

    meeting__item_information: MeetingItemInformation = Field(
        ..., description="Meeting & Item Information"
    )
    agenda_placement__action_type: AgendaPlacementActionType = Field(
        ..., description="Agenda Placement & Action Type"
    )
    staff__presentation_details: StaffPresentationDetails = Field(
        ..., description="Staff & Presentation Details"
    )
    issue_description__recommendation: IssueDescriptionRecommendation = Field(
        ..., description="Issue Description & Recommendation"
    )
    financial_impact: FinancialImpact = Field(..., description="Financial Impact")
