from pydantic import BaseModel, ConfigDict, Field


class AnnualPreparticipationPhysicalExam(BaseModel):
    """2021-22 ANNUAL PREPARTICIPATION PHYSICAL EXAMINATION

    Purpose: This form is used to collect medical history and COVID-19 related information about a student prior to their participation in interscholastic sports, ensuring they are medically cleared for athletic activities.
    Recipient: The form is intended for review by physicians conducting the physical examination, as well as school athletic staff or administrators responsible for verifying student eligibility for sports participation.
    """

    model_config = ConfigDict(extra="forbid")


    patient_history_explain_yes: str = Field(..., description='Explain "Yes" answers for patient history. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')

    covid_explain_yes: str = Field(..., description='Explain "Yes" answers for COVID-19 section. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')