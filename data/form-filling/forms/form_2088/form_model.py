from pydantic import BaseModel, ConfigDict, Field


class JobTaskInventoryPotentialCovidExposure(BaseModel):
    """Job Task Inventory for Employees with Potential for Exposure to a Person with Suspected or Confirmed COVID-19

    Workplace safety/health staff, supervisors, and HR/management use this inventory with employee input to identify job tasks
    and locations where workers may be exposed to people with suspected or confirmed COVID-19, including aerosol-generating
    procedures. EHS/OSHA compliance and management review the responses to assess exposure risk and decide what controls,
    work practices, PPE, staffing, and area restrictions are needed.
    """

    model_config = ConfigDict(extra="forbid")

    exposure_questions_direct_care_or_exposed_follow_up_notes: str = Field(
        ...,
        description='Direct care/exposure follow-up/notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    exposure_questions_perform_or_assist_agps_follow_up_notes: str = Field(
        ...,
        description='AGPs follow-up/notes. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )



    no_expectation_areas_list: str = Field(
        ...,
        description='List areas with no expectation of COVID-19. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )