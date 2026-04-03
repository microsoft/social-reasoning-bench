from pydantic import BaseModel, ConfigDict, Field


class TheWatersVolunteerApplication(BaseModel):
    """THE WATERS VOLUNTEER APPLICATION

    Purpose: Volunteer application form to collect personal information, availability, interests, and experience from individuals interested in volunteering at The Waters.
    Recipient: Volunteer coordinators or staff members at The Waters responsible for screening, selecting, and scheduling volunteers.
    """

    model_config = ConfigDict(extra="forbid")

    personal_info_street_address: str = Field(..., description='Street address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    personal_info_telephone_number: str = Field(..., description='Telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    commitment_hours_per: float | None = Field(..., description='Number of hours per period')
    interest_why_volunteer: str = Field(..., description='Reason for volunteering. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    interest_areas_skills_experience: str = Field(..., description='Areas of interest, skills, and experience with seniors. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')