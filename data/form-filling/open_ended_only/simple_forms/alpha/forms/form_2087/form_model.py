from pydantic import BaseModel, ConfigDict, Field


class FixedWorkLocationJobTaskInventory(BaseModel):
    """Fixed Work Location and Job Task Inventory for Employees Outside of Direct Patient Care Areas Who Cannot Maintain Physical Distancing

    Purpose: To document and assess fixed work locations and job tasks outside of direct patient care areas where employees cannot maintain at least 6 feet of physical distancing, in order to identify potential COVID-19 exposure risks and determine necessary protective measures.
    Recipient: Workplace safety officers, infection prevention teams, or human resources personnel responsible for COVID-19 safety compliance and workplace risk assessment.
    """

    model_config = ConfigDict(extra="forbid")
