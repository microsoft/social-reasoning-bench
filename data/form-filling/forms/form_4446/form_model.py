from pydantic import BaseModel, ConfigDict, Field


class BeginTheEpidiolexConversation(BaseModel):
    """Begin the EPIDIOLEX conversation

    A patient or caregiver fills out this worksheet to summarize current anti-seizure medications, ongoing seizure types and frequency, satisfaction with current treatment, and goals/hopes about starting EPIDIOLEX. A neurologist/epilepsy specialist and their clinical care team review it to assess treatment response and decide whether EPIDIOLEX may be appropriate and what next treatment steps to discuss.
    """

    model_config = ConfigDict(extra="forbid")

    current_seizure_medicines: str = Field(
        ...,
        description='Current seizure medicines taken. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    seizure_types_while_on_medicines: str = Field(
        ...,
        description='Seizure types occurring on medicines. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    goals_for_seizure_treatment: str = Field(
        ...,
        description='Goals for seizure treatment. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    hopes_for_epidiolex: str = Field(
        ...,
        description='Hopes for EPIDIOLEX. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    additional_notes_and_questions: str = Field(
        ...,
        description='Additional notes and questions. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )