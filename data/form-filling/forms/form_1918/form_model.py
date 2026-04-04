from pydantic import BaseModel, ConfigDict, Field


class TheWatersVolunteerApplication(BaseModel):
    """THE WATERS VOLUNTEER APPLICATION

    Prospective volunteers submit this application to The Waters to share personal
    details, availability, and interests/skills so the volunteer coordinator and
    administrative/HR staff can screen applicants, determine eligibility, and place
    them into appropriate volunteer roles and schedules with resident services.
    """

    model_config = ConfigDict(extra="forbid")

    personal_information_date_of_birth: str = Field(
        ...,
        description='Date of birth (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    personal_information_telephone_number: str = Field(
        ...,
        description='Telephone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    personal_information_date_available_to_start_volunteering: str = Field(
        ...,
        description='Date available to start (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


    availability_other_details: str = Field(
        ...,
        description='Other availability details. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    commitment_level_hours_per: float | None = Field(
        ...,
        description="Hours per selected period",
    )
    commitment_level_per_other_details: str = Field(
        ...,
        description='Other period details. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    commitment_length_value: float | None = Field(
        ...,
        description="Length of commitment value",
    )

    personal_information_why_interested_in_volunteering: str = Field(
        ...,
        description='Why interested in volunteering. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    interest_skills_and_experience_areas_of_interest_skills_experience: str = Field(
        ...,
        description='Interests, skills, senior experience. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )