from pydantic import BaseModel, ConfigDict, Field


class TeamCoachingSupervisionTrainingProgrammeApplicationForm(BaseModel):
    """Team Coaching Supervision Training Programme Application Form

    Applicants submit this form to apply for Renewal Associates’ Team Coaching Supervision Training Programme. Programme administrators use it to contact the applicant and arrange invoicing, and training/supervision faculty review the applicant’s coaching and supervision background to assess suitability for enrolment.
    """

    model_config = ConfigDict(extra="forbid")

    contact_telephone: str = Field(
        ...,
        description='Telephone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    background_training_qualifications_certifications: str = Field(
        ...,
        description='Training quals/certs incl date/duration/level. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    experience_years_practicing_as_coach: float | None = Field(
        ...,
        description="Years practicing as a coach",
    )
    experience_years_practicing_as_team_coach: float | None = Field(
        ...,
        description="Years practicing as a team coach",
    )
    experience_years_practicing_as_coach_supervisor: float | None = Field(
        ...,
        description="Years practicing as a coach supervisor",
    )
    experience_other_role_description: str = Field(
        ...,
        description='Other role description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )