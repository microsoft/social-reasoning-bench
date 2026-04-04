from pydantic import BaseModel, ConfigDict, Field


class BrainerdCityCouncilAgendaRequest(BaseModel):
    """Brainerd City Council Agenda Request

    Staff submit this form to request that an item be placed on a Brainerd City Council meeting agenda. City administrative staff use it to compile the agenda packet, and the City Council and relevant committees review the request to decide how the item is categorized, what action (if any) is taken, and what supporting information and financial impacts must be considered.
    """

    model_config = ConfigDict(extra="forbid")

    requested_meeting_date: str = Field(
        ...,
        description='Requested meeting date (YYYY-MM-DD).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


    submitted_by: str = Field(
        ...,
        description='Submitted by.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    department: str = Field(
        ...,
        description='Department.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    estimated_time_needed: str = Field(
        ...,
        description='Estimated time needed.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    summary_of_issue: str = Field(
        ...,
        description='Summary of issue.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    alternatives_options_effects_comments: str = Field(
        ...,
        description='Alternatives/options/effects/comments.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    recommended_action_motion: str = Field(
        ...,
        description='Recommended action/motion.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
