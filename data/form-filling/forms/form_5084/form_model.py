from pydantic import BaseModel, ConfigDict, Field


class EmployeeReportOfOccupationalInjuryOrIllnessToEmployer(BaseModel):
    """Employee Report of Occupational Injury or Illness to Employer

    An employee submits this report to notify the Fairbanks North Star Borough or School District that a work-related injury or illness occurred, document what happened and what care was sought, and authorize release of related medical records. Risk Management/claims staff and the employee’s supervisor review it to initiate workers’ compensation reporting, coordinate medical evaluation and benefits eligibility, and support required filings with the Alaska Division of Workers’ Compensation and the insurer/claims adjuster.
    """

    model_config = ConfigDict(extra="forbid")


    employee_date_of_birth: str = Field(
        ...,
        description='Date of birth (YYYY-MM-DD).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    employee_last4_ssn: str = Field(
        ...,
        description='Last 4 of SSN.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    employee_number_of_dependents: float | None = Field(
        ..., description="Number of dependents"
    )


    incident_part_of_body_affected: str = Field(
        ...,
        description='Part of body affected.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    incident_nature_of_injury_illness: str = Field(
        ...,
        description='Nature of injury/illness.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    incident_supervisor_contact_number: str = Field(
        ...,
        description='Supervisor contact number.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )


    incident_description_how_happened: str = Field(
        ...,
        description='How injury/illness happened.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )




    authorization_date_signed: str = Field(
        ...,
        description='Employee date signed (YYYY-MM-DD).If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    authorization_if_unavailable_explain_circumstances: str = Field(
        ...,
        description='If employee unavailable, explain.If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )