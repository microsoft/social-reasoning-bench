from pydantic import BaseModel, ConfigDict, Field


class UnityNationalBankRecordOfEmployment(BaseModel):
    """UNITY National Bank Record of Employment

    Job applicants submit this employment history and authorization form as part of
    applying to Unity National Bank. HR and hiring managers review the listed prior
    employers, dates, pay history, duties, and reasons for leaving, and may use the
    signed permission to contact employers for verification and reference checks to
    support hiring decisions.
    """

    model_config = ConfigDict(extra="forbid")

    employment_history_1_monthly_last_salary: float | None = Field(
        ...,
        description="Monthly last salary (job 1)",
    )
    employment_history_1_reason_for_leaving: str = Field(
        ...,
        description='Reason for leaving (job 1).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    employment_history_1_title_job_duties: str = Field(
        ...,
        description='Title and job duties (job 1).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    employment_history_1_telephone: str = Field(
        ...,
        description='Employer telephone (job 1).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    employment_history_2_reason_for_leaving: str = Field(
        ...,
        description='Reason for leaving (job 2).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    employment_history_2_title_job_duties: str = Field(
        ...,
        description='Title and job duties (job 2).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    employment_history_3_reason_for_leaving: str = Field(
        ...,
        description='Reason for leaving (job 3).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    employment_history_3_title_job_duties: str = Field(
        ...,
        description='Title and job duties (job 3).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    employment_history_3_telephone: str = Field(
        ...,
        description='Employer telephone (job 3).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    employment_history_4_monthly_starting_salary: float | None = Field(
        ...,
        description="Monthly starting salary (job 4)",
    )
    employment_history_4_monthly_last_salary: float | None = Field(
        ...,
        description="Monthly last salary (job 4)",
    )
    employment_history_4_reason_for_leaving: str = Field(
        ...,
        description='Reason for leaving (job 4).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    employment_history_4_title_job_duties: str = Field(
        ...,
        description='Title and job duties (job 4).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    authorization_worked_under_different_name_note: str = Field(
        ...,
        description='Different name used with employers note.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    authorization_employers_do_not_contact: str = Field(
        ...,
        description='Employers you do not wish to contact.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    qualifications_skills_aptitudes: str = Field(
        ...,
        description='Skills and aptitudes for bank position.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )