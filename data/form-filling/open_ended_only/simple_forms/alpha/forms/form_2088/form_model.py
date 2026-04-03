from pydantic import BaseModel, ConfigDict, Field


class JobTaskInventoryCovidExposure(BaseModel):
    """Job Task Inventory for Employees with Potential for Exposure to a Person with Suspected or Confirmed COVID-19

    Purpose: Assessment tool for identifying job tasks and workplace areas where employees may be exposed to individuals with suspected or confirmed COVID-19, to inform workplace safety and infection control measures.
    Recipient: Workplace safety officers, infection control personnel, or human resources staff responsible for evaluating and managing employee health risks related to COVID-19 exposure.
    """

    model_config = ConfigDict(extra="forbid")

    no_exposure_areas: str = Field(..., description='List of well-defined workplace areas with no reasonable expectation of COVID-19 presence. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").')