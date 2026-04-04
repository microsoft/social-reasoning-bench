from pydantic import BaseModel, ConfigDict, Field


class CitizenMembersApplication(BaseModel):
    """Vermont Developmental Disabilities Council Citizen Members Application

    Applicants submit this form to apply for citizen membership on the Vermont Developmental Disabilities
    Council. Council members review applications, may request more information and interviews, and vote on
    finalists to recommend to the Governor for appointment. For finalists, the Governor’s Office may review
    the application and conduct background checks as part of the appointment decision.
    """

    model_config = ConfigDict(extra="forbid")


    identity_other_description: str = Field(
        ...,
        description='Other relationship description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    identity_disability_description: str = Field(
        ...,
        description='Disability description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    agreement_date: str = Field(
        ...,
        description='Signature date (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )