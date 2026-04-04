from pydantic import BaseModel, ConfigDict, Field


class AssociateApplicationForm(BaseModel):
    """ASSOCIATE APPLICATION FORM CONFIDENTIAL

    Lawyer candidates submit this confidential associate application to Volterra Fietta as part of the recruitment
    process. The recruitment/HR team and relevant hiring partners review the applicant’s qualifications, licensing
    status, employment and compensation details, availability, and any prior applications or relationships to assess
    eligibility, potential conflicts, and overall suitability for an associate role and to make interview and hiring
    decisions.
    """

    model_config = ConfigDict(extra="forbid")

    about_you_current_or_most_recent_employer: str = Field(
        ...,
        description='Current/most recent employer. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    about_you_current_salary: float | None = Field(
        ..., description="Current salary"
    )
    about_you_salary_expectation: float | None = Field(
        ..., description="Salary expectation"
    )
    about_you_notice_period_availability_details: str = Field(
        ...,
        description='Notice period/availability details. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    about_you_previous_vf_details_if_yes: str = Field(
        ...,
        description='Details if previously applied/employed. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    about_you_uk_sra_number: str = Field(
        ...,
        description='UK SRA number (if applicable). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )