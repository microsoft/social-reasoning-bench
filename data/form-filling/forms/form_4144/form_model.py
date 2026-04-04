from pydantic import BaseModel, ConfigDict, Field


class AAWorldServicesDirectorResumeSheet(BaseModel):
    """A.A. World Services Director Resume Sheet

    Individuals seeking consideration for a Director position with A.A. World Services submit this resume sheet to
    summarize sobriety date, education, A.A. service experience, occupational background, relevant skills, and any
    current or past contractual relationships with A.A. entities. Trustees/directors, nominating or selection
    committees, and administrative staff review it to evaluate qualifications, fit, and potential conflicts of
    interest when deciding whom to advance in the selection process.
    """

    model_config = ConfigDict(extra="forbid")

    contact_primary_phone: str = Field(
        ...,
        description='Primary phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    contact_address: str = Field(
        ...,
        description='Mailing address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    education: str = Field(
        ...,
        description='Education history. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    aa_experience_current_and_past: str = Field(
        ...,
        description='Current and past A.A. experience. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    occupational_background: str = Field(
        ...,
        description='Occupational background. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    additional_abilities_skills_background_life_experiences: str = Field(
        ...,
        description='Additional abilities/skills/life experiences. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    relationships_contractual_with_aa_entities: str = Field(
        ...,
        description='Contractual relationships with A.A. entities. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )