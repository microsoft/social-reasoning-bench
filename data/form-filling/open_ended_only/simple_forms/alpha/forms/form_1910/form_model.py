from pydantic import BaseModel, ConfigDict, Field


class VolunteerApplicationCarewest(BaseModel):
    """Volunteer Application

    Purpose: Volunteer application to collect personal details, motivations, preferences, and background checks for individuals interested in volunteering with Carewest.
    Recipient: Carewest's volunteer recruitment staff or HR personnel, who will review applications to assess suitability and match applicants with appropriate volunteer opportunities.
    """

    model_config = ConfigDict(extra="forbid")

    personal_information_primary_phone: str = Field(..., description='Primary phone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    personal_information_alternate_phone: str = Field(..., description='Alternate phone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    personal_information_vulnerable_sector_check_date: str = Field(..., description='Date of vulnerable sector criminal records check (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')

    motivation_other_details: str = Field(..., description='Details for other motivation. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')
    motivation_hobbies_interests: str = Field(..., description='Hobbies and interests. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')




    volunteering_preferences_time_commitment: str = Field(..., description='Available time commitment per shift (e.g. hours/week). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')