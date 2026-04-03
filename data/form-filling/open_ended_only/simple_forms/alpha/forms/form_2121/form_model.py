from pydantic import BaseModel, ConfigDict, Field


class WestDistrictChurchRepairsApp(BaseModel):
    """APPLICATION FOR WEST DISTRICT CHURCH REPAIRS

    Purpose: Application for churches in the West District to request financial and/or logistical assistance for building repairs, including evaluation of need and the church's capacity to contribute.
    Recipient: West District administrative committee or leadership team responsible for allocating church repair resources and evaluating requests from local congregations.
    """

    model_config = ConfigDict(extra="forbid")

    contact_person_phone: str = Field(..., description='Contact phone. If you cannot fill this, write "N/A".')
    professional_evaluation: str = Field(..., description='Details of professional evaluation or cost estimate. If you cannot fill this, write "N/A".')
    funds_for_project: str = Field(..., description='Funds available and fundraising plans. If you cannot fill this, write "N/A".')
    avg_attendance_last_year: float | None = Field(..., description="Average attendance last year")
    district_apportionment_paid_pct: float | None = Field(..., description="District apportionment percentage paid")