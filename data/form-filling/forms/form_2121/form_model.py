from pydantic import BaseModel, ConfigDict, Field


class WestDistrictChurchRepairsApplication(BaseModel):
    """APPLICATION FOR WEST DISTRICT CHURCH REPAIRS

    A local church congregation submits this application to request West District
    assistance or funding for needed building repairs. District leaders review
    the scope of work, any professional evaluations/estimates, the church’s
    operating budget and financial capacity, attendance trends, apportionment
    payment history, and the congregation’s willingness to contribute funds or
    volunteer support, then decide whether and how the District will undertake
    or support the repair project.
    """

    model_config = ConfigDict(extra="forbid")

    application_date: str = Field(
        ...,
        description='Application date (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    contact_person_phone: str = Field(
        ...,
        description='Contact person phone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    work_description: str = Field(
        ...,
        description='Work needed description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    professional_evaluation_or_estimate_details: str = Field(
        ...,
        description='Evaluation/estimate details provided. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    operating_budget_current_year: float | None = Field(
        ...,
        description="Operating budget current year",
    )
    why_cannot_undertake_alone: str = Field(
        ...,
        description='Why congregation cannot do alone. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    funds_and_fundraising_description: str = Field(
        ...,
        description='Funds and fundraising description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )