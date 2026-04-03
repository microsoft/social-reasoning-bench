from pydantic import BaseModel, ConfigDict, Field


class TheWatersVolunteerApplication(BaseModel):
    """THE WATERS VOLUNTEER APPLICATION"""

    model_config = ConfigDict(extra="forbid")

    personal_information_date_of_birth: str = Field(
        ..., description='Date of birth (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    personal_information_street_address: str = Field(
        ..., description='Street address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    personal_information_telephone_number: str = Field(
        ..., description='Telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    personal_information_family_member_location: str = Field(
        ..., description='Location of family member at The Waters. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    personal_information_availability_other: str = Field(
        ..., description='Other availability. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    personal_information_length_of_commitment: str = Field(
        ..., description='Length of commitment. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    personal_information_why_interested: str = Field(
        ..., description='Reason for volunteering. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    interest_skills_experience_areas_of_interest: str = Field(
        ..., description='Areas of interest, skills, and experience with seniors. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )