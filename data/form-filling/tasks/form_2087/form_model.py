from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FixedWorkLocationRow(BaseModel):
    """Single row in Fixed Work Location"""

    fixed_work_location: str = Field(default="", description="Fixed_Work_Location")
    no_of_workers: str = Field(default="", description="No_Of_Workers")
    job_tasks_and_descriptions: str = Field(default="", description="Job_Tasks_And_Descriptions")


class NoOfWorkersRow(BaseModel):
    """Single row in No. of Workers"""

    fixed_work_location: str = Field(default="", description="Fixed_Work_Location")
    no_of_workers: str = Field(default="", description="No_Of_Workers")
    job_tasks_and_descriptions: str = Field(default="", description="Job_Tasks_And_Descriptions")


class JobTasksAndDescriptionsRow(BaseModel):
    """Single row in Job Tasks and Descriptions"""

    fixed_work_location: str = Field(default="", description="Fixed_Work_Location")
    no_of_workers: str = Field(default="", description="No_Of_Workers")
    job_tasks_and_descriptions: str = Field(default="", description="Job_Tasks_And_Descriptions")


class FixedWorkLocationTaskInventoryForNonPatientCareEmployees(BaseModel):
    """
        Fixed Work Location and Job Task Inventory for Employees Outside of
    Direct Patient Care Areas Who Cannot Maintain Physical Distancing

        Use this Fixed Work Location and Job Task Inventory and input from employees to identify any fixed work locations outside of direct patient care areas where employees cannot maintain at least 6 feet of physical distancing from all other people when indoors. Direct patient care means hands-on, face-to-face contact with patients for the purpose of diagnosis, treatment, and monitoring.
        Note: The ETS exempts fully vaccinated workers from physical distancing and barrier requirements when in well-defined areas of the workplace where there is no reasonable expectation that any person with suspected or confirmed COVID-19 will be present.
        Fixed work locations are workstations where an employee is assigned to work for significant periods of time. Protective measures can often be implemented at fixed workstations to minimize potential exposure to COVID-19.
    """

    fixed_work_location: List[FixedWorkLocationRow] = Field(
        ...,
        description=(
            "Table to list each fixed work location outside of direct patient care areas "
            "where employees cannot maintain 6 feet of physical distance, along with number "
            "of workers and job task descriptions."
        ),
    )  # List of table rows

    no_of_workers: List[NoOfWorkersRow] = Field(
        ...,
        description="Number of workers assigned to each fixed work location listed in the table.",
    )  # List of table rows

    job_tasks_and_descriptions: List[JobTasksAndDescriptionsRow] = Field(
        ...,
        description=(
            "Descriptions of job tasks at each fixed work location where employees cannot "
            "maintain 6 feet of physical distance from others."
        ),
    )  # List of table rows
