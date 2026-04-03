from pydantic import BaseModel, ConfigDict, Field


class FixedWorkLocationJobTaskInventoryForm(BaseModel):
    """Fixed Work Location and Job Task Inventory for Employees Outside of Direct Patient Care Areas Who Cannot Maintain Physical Distancing"""

    model_config = ConfigDict(extra="forbid")
