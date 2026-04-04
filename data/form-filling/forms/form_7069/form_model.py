from pydantic import BaseModel, ConfigDict, Field


class BrainerdCityCouncilAgendaRequest(BaseModel):
    """Brainerd City Council Agenda Request

    City staff submit this form to request that an item be placed on a Brainerd City Council meeting agenda. Administrative staff and the City Council (and relevant committees) review the requested meeting date, agenda category, requested action, and supporting details to schedule the item, understand impacts and alternatives, and decide what action to take during the meeting.
    """

    model_config = ConfigDict(extra="forbid")

    requested_meeting_date: str = Field(
        ...,
        description='Requested meeting date (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    title_of_item: str = Field(
        ...,
        description='Agenda item title. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    agenda_category_information_only: bool | None = Field(..., description="Agenda category: information only")
    agenda_category_consent_agenda: bool | None = Field(..., description="Agenda category: consent agenda")
    agenda_category_pf_committee: bool | None = Field(..., description="Agenda category: P&F committee")
    agenda_category_spw_committee: bool | None = Field(..., description="Agenda category: SPW committee")
    agenda_category_main_agenda: bool | None = Field(..., description="Agenda category: main agenda")

    action_requested_approve_deny_motion: bool | None = Field(..., description="Action requested: approve/deny motion")
    action_requested_adopt_resolution: bool | None = Field(..., description="Action requested: adopt resolution")
    action_requested_direction_requested: bool | None = Field(..., description="Action requested: direction requested")
    action_requested_discussion_item: bool | None = Field(..., description="Action requested: discussion item")
    action_requested_hold_public_hearing: bool | None = Field(..., description="Action requested: hold public hearing")
    action_requested_ordinance_1st_reading: bool | None = Field(..., description="Action requested: ordinance 1st reading")

    submitted_by: str = Field(
        ...,
        description='Submitted by (name). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    department: str = Field(
        ...,
        description='Department. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    presenter_name_title: str = Field(
        ...,
        description='Presenter name and title. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    estimated_time_needed: str = Field(
        ...,
        description='Estimated time needed. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    summary_of_issue: str = Field(
        ...,
        description='Summary of issue. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    alternatives_options_effects_comments: str = Field(
        ...,
        description='Alternatives/options/effects/comments. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    recommended_action_motion: str = Field(
        ...,
        description='Recommended action/motion. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    financial_impact_cost_associated_yes: bool | None = Field(..., description="Cost associated: yes")
    financial_impact_cost_associated_no: bool | None = Field(..., description="Cost associated: no")
    financial_impact_total_cost_with_tax_shipping: float | None = Field(..., description="Total cost incl tax/shipping")
    financial_impact_is_budgeted_yes: bool | None = Field(..., description="Is this budgeted: yes")
    financial_impact_is_budgeted_no: bool | None = Field(..., description="Is this budgeted: no")
    financial_impact_please_explain: str = Field(
        ...,
        description='Financial impact explanation. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )