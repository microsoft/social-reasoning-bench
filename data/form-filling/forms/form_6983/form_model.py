from pydantic import BaseModel, ConfigDict, Field


class RenaissanceAwardNominationForm(BaseModel):
    """Destination Imagination® The Renaissance Award Nomination Form

    Appraisers submit this nomination to recommend a Destination Imagination team or an individual
    for the Renaissance Award based on exceptional engineering, design, or performance in either
    the Team Challenge or the Instant Challenge. Tournament officials and award reviewers read the
    nomination details and cited examples to decide whether the nomination is accepted and whether
    the team/individual receives the Renaissance Award.
    """

    model_config = ConfigDict(extra="forbid")






    reason_for_nomination: str = Field(
        ...,
        description='Reason for nomination (specific examples). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )