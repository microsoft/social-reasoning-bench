from pydantic import BaseModel, ConfigDict, Field


class FixedWorkLocationJobTaskInventory(BaseModel):
    """Fixed Work Location and Job Task Inventory for Employees Outside of Direct Patient Care Areas Who Cannot Maintain Physical Distancing

    Supervisors and workplace safety/occupational health staff use this inventory, with input from employees, to list fixed work
    locations outside direct patient care areas where workers cannot maintain at least 6 feet of indoor physical distancing, and
    to document the associated job tasks. Infection prevention/EHS/HR and compliance reviewers use it to assess COVID-19 exposure
    risk, determine where protective measures are needed, and support ETS-related decisions and inspection readiness.
    """

    model_config = ConfigDict(extra="forbid")
