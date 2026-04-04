from pydantic import BaseModel, ConfigDict, Field


class AiaAnnualPreparticipationPhysicalExamination(BaseModel):
    """2021-22 Annual Preparticipation Physical Examination

    A licensed healthcare provider completes this annual sports physical for a student-athlete to document medical history context, vital signs, physical exam findings, and the final clearance decision. The completed form is submitted to the student’s school and/or AIA athletics administration, who review it to determine eligibility to participate in AIA sports and whether any restrictions or follow-up recommendations apply.
    """

    model_config = ConfigDict(extra="forbid")


    vitals_bp_systolic: float | None = Field(..., description="BP systolic")
    vitals_bp_diastolic: float | None = Field(..., description="BP diastolic")
    vitals_bp_repeat_1_systolic: float | None = Field(..., description="BP repeat 1 systolic")






















    notes: str = Field(
        ...,
        description='Notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    clearance_restriction_details: str = Field(
        ...,
        description='Restriction details. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    clearance_not_cleared_certain_sports_list: str = Field(
        ...,
        description='Certain sports not cleared for. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    clearance_not_cleared_reason: str = Field(
        ...,
        description='Not cleared reason. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    recommendations: str = Field(
        ...,
        description='Recommendations. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
