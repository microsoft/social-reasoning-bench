from pydantic import BaseModel, ConfigDict, Field


class CarewestVolunteerApplication(BaseModel):
    """Volunteer Application (Carewest)

    Individuals submit this application to Carewest to be considered for volunteer roles. Recruitment/HR and volunteer program coordinators review the applicant’s personal details, interests, preferred volunteer areas, and availability to determine suitability, potential placement, scheduling fit, and whether required screening (such as a vulnerable sector criminal records check) can be completed before duties begin.
    """

    model_config = ConfigDict(extra="forbid")

    personal_information_primary_phone: str = Field(
        ...,
        description='Primary phone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    personal_information_alternate_phone: str = Field(
        ...,
        description='Alternate phone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    personal_information_volunteer_reason_other_details: str = Field(
        ...,
        description='Other reason details. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    personal_information_why_volunteer_at_carewest: str = Field(
        ...,
        description='Why volunteer at Carewest. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    personal_information_hobbies_and_interests: str = Field(
        ...,
        description='Hobbies and interests. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    volunteering_preferences_area_other_text: str = Field(
        ...,
        description='Other area text. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )




    volunteering_preferences_time_commitment_per_shift: str = Field(
        ...,
        description='Time commitment per shift (e.g., hours/week). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )