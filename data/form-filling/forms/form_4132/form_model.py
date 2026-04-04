from pydantic import BaseModel, ConfigDict, Field


class SerenityFirstPreventionSupportYouthCoalitionRegistrationForm(BaseModel):
    """Registration Form for Serenity First Prevention and Support Youth Coalition

    Youth ages 13–18 (with a parent/guardian) submit this registration to enroll in the
    Serenity First Prevention and Support Youth Coalition’s free monthly activities/meetings.
    Coalition coordinators/staff (e.g., Jill Fabian and Diane Morrow) review it to contact the
    participant and guardian, plan transportation needs, and prepare for allergies, medical
    considerations, and dietary restrictions for safe participation.
    """

    model_config = ConfigDict(extra="forbid")

    participant_phone: str = Field(
        ...,
        description='Participant phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    participant_date_of_birth: str = Field(
        ...,
        description='Participant date of birth (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    participant_tshirt_size: str = Field(
        ...,
        description='T-shirt size (S/M/L/XL/XXL). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    parent_guardian_phone: str = Field(
        ...,
        description='Parent/guardian phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    emergency_contact_phone: str = Field(
        ...,
        description='Emergency contact phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    medical_information_dietary_restrictions: str = Field(
        ...,
        description='Medical info & dietary restrictions. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )