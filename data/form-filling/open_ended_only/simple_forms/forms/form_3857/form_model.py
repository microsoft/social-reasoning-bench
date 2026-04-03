from pydantic import BaseModel, ConfigDict, Field


class AnnualPreparticipationPhysicalExaminationForm(BaseModel):
    """2021-22 ANNUAL PREPARTICIPATION PHYSICAL EXAMINATION"""

    model_config = ConfigDict(extra="forbid")

    date_of_birth: str = Field(
        ..., description='Date of birth (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )

    patient_history_explain_yes_answers: str = Field(
        ..., description='Explanation for "Yes" answers. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )

    covid_explain_yes_answers: str = Field(
        ..., description='Explanation for "Yes" answers (COVID-19 section). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )