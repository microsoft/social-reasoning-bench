from pydantic import BaseModel, ConfigDict, Field


class SerenityFirstPreventionSupportYouthCoalitionRegistrationForm(BaseModel):
    """Registration Form for Serenity First Prevention and Support Youth Coalition"""

    model_config = ConfigDict(extra="forbid")

    participant_address: str = Field(
        ..., description='Participant address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    participant_phone: str = Field(
        ..., description='Participant phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    participant_school: str = Field(
        ..., description='Participant school name. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    participant_tshirt_size: str = Field(
        ..., description='Participant T-shirt size (S, M, L, XL, XXL). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    emergency_contact_relationship: str = Field(
        ..., description='Emergency contact relationship. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    medical_info_dietary_restrictions: str = Field(
        ..., description='Medical info & dietary restrictions. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )