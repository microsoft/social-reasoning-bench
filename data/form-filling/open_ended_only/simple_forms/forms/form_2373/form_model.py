from pydantic import BaseModel, ConfigDict, Field


class ApplicationFormBachelorsMastersThesesSouthTyroleanEconomy(BaseModel):
    """APPLICATION FORM - BACHELOR'S AND MASTER'S THESES ON THE SOUTH TYROLEAN ECONOMY"""

    model_config = ConfigDict(extra="forbid")

    student_university: str = Field(..., description='Student university. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')


    thesis_title: str = Field(..., description='Title of the bachelor or master thesis. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    expose_text: str = Field(..., description='Exposé text (max 3,500 keystrokes). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')