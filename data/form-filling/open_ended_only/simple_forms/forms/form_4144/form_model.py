from pydantic import BaseModel, ConfigDict, Field


class AAWorldServicesDirectorResumeSheet(BaseModel):
    """A.A. WORLD SERVICES DIRECTOR RESUME SHEET"""

    model_config = ConfigDict(extra="forbid")

    address: str = Field(..., description='Mailing address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    education: str = Field(..., description='Education background. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    aa_experience: str = Field(..., description='Current and past A.A. experience. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    occupational_background: str = Field(..., description='Occupational background. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    additional_abilities: str = Field(..., description='Additional abilities, skills, background, and life experiences. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    contractual_relationships: str = Field(..., description='Current or past contractual relationships with A.A. World Services, Inc., AA Grapevine, Inc., or A.A. General Service Board, Inc. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')