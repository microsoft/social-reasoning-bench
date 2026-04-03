from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FixedWorkLocationTableRow(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Single row in Fixed Work Location"""

    fixed_work_location: str = Field(
        ...,
        description="Fixed_Work_Location"
    )
    no_of_workers: str = Field(
        ...,
        description="No_Of_Workers"
    )
    job_tasks_and_descriptions: str = Field(
        ...,
        description="Job_Tasks_And_Descriptions"
    )


class EmployeeNonPatientCareDistancingWorkLocationJobTaskInventory(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    Fixed Work Location and Job Task Inventory for Employees Outside of Direct Patient Care Areas Who Cannot Maintain Physical Distancing

    Use this Fixed Work Location and Job Task Inventory and input from employees to identify any fixed work locations outside of direct patient care areas where employees cannot maintain at least 6 feet of physical distancing from all other people when indoors. Direct patient care means hands-on, face-to-face contact with patients for the purpose of diagnosis, treatment, and monitoring.
    Note: The ETS exempts fully vaccinated workers from physical distancing and barrier requirements when in well-defined areas of the workplace where there is no reasonable expectation that any person with suspected or confirmed COVID-19 will be present.
    Fixed work locations are workstations where an employee is assigned to work for significant periods of time. Protective measures can often be implemented at fixed workstations to minimize potential exposure to COVID-19.
    Take an inventory of all fixed work locations outside of direct patient care areas where employees cannot maintain 6 feet of physical distance from all other people. Note the number of workers at each location.
    For each fixed work location, describe the job tasks where employees cannot maintain 6 feet of physical distance from all other people.
    """

    fixed_work_location_table: List[FixedWorkLocationTableRow] = Field(
        ...,
        description=(
            "Table to record each fixed work location, number of workers, and job "
            "tasks/descriptions where employees cannot maintain 6 feet of physical "
            "distance."
        )
    )  # List of table rows
