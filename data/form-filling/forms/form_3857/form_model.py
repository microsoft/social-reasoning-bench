from pydantic import BaseModel, ConfigDict, Field


class AiaAnnualPreparticipationPhysicalExamination(BaseModel):
    """2021-22 Annual Preparticipation Physical Examination

    A licensed healthcare provider completes this annual preparticipation exam and medical history screening for a student athlete, with input from the parent/guardian as needed, to identify medical risks (including COVID-19-related issues) and determine whether the student is medically cleared to participate in AIA sports/activities. School/AIA athletics staff review the completed form to confirm eligibility and any needed restrictions or follow-up before participation is allowed.
    """

    model_config = ConfigDict(extra="forbid")

    date_of_birth: str = Field(
        ...,
        description='Date of birth (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    patient_history_yes_explanations: str = Field(
        ...,
        description='Explain "Yes" answers (patient history). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    covid_yes_explanations: str = Field(
        ...,
        description='Explain "Yes" answers (COVID-19). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )