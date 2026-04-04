from pydantic import BaseModel, ConfigDict, Field


class BrainerdCityCouncilAgendaRequest(BaseModel):
    """Brainerd City Council Agenda Request

    City staff submit this form to request that an item be placed on an upcoming Brainerd City Council meeting agenda. The city administrator/clerk and other agenda-prep staff use it to assemble the agenda packet, and council members/committees use it to understand the requested action, discuss options, and decide whether to approve, adopt, direct, hold a hearing, or otherwise act on the item.
    """

    model_config = ConfigDict(extra="forbid")

    requested_meeting_date: str = Field(
        ...,
        description='Requested meeting date (YYYY-MM-DD).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    title_of_item: str = Field(
        ...,
        description='Agenda item title. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


    submitted_by: str = Field(
        ...,
        description='Submitted by (name). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    department: str = Field(
        ...,
        description='Submitting department. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
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
