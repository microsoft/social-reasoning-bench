from pydantic import BaseModel, ConfigDict, Field


class RequiredInformationNeighborhoodRegistrationForm(BaseModel):
    """REQUIRED INFORMATION Neighborhood Registration Form"""

    model_config = ConfigDict(extra="forbid")

    telephone_number: str = Field(
        ..., description='Telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    optional_newsletter: str = Field(
        ..., description='Newsletter or other publication. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    optional_meetings_info: str = Field(
        ..., description='Regularly scheduled meetings (date, time, location). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    optional_comments: str = Field(
        ..., description='Comments, questions, or suggested topics for neighborhood planning workshops. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )