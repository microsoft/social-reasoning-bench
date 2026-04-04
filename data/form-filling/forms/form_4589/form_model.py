from pydantic import BaseModel, ConfigDict, Field


class ReiSelfAssessment(BaseModel):
    """REI Self-Assessment

    County/agency staff (often former leaders or longstanding employees) complete this intake form to document their
    background and involvement in past racial equity, inclusion, and anti-racism initiatives. REI evaluators,
    consultants, or internal project staff review the responses to place current REI efforts in historical context,
    identify knowledgeable interview participants, and locate other people connected to prior initiatives.
    """

    model_config = ConfigDict(extra="forbid")



    background_a2b_agency_role_at_that_time: str = Field(
        ...,
        description='Agency role at that time.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    background_a2b_project_role_at_that_time: str = Field(
        ...,
        description='Project role at that time.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    background_a2d_contact_info_for_other_people: str = Field(
        ...,
        description='How to contact other person/people.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )