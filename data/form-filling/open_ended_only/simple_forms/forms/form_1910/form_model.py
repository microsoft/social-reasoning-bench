from pydantic import BaseModel, ConfigDict, Field


class VolunteerApplication(BaseModel):
    """Volunteer Application"""

    model_config = ConfigDict(extra="forbid")

    personal_information_primary_phone: str = Field(
        ..., description='Primary phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    personal_information_alternate_phone: str = Field(
        ..., description='Alternate phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    personal_information_why_volunteer_other_details: str = Field(
        ..., description='Other reason details. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    personal_information_hobbies_interests: str = Field(
        ..., description='Hobbies and interests. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )

    volunteering_preferences_other_details: str = Field(
        ..., description='Other area details. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )

    volunteering_preferences_time_commitment_per_shift: str = Field(
        ..., description='Time commitment per shift (hours/week). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )