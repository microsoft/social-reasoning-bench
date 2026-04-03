from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PotentialExposureTableRow(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Single row in Location(s)"""

    location_s: str = Field(
        ...,
        description="Location_S"
    )
    no_of_workers: str = Field(
        ...,
        description="No_Of_Workers"
    )
    job_tasks_and_descriptions: str = Field(
        ...,
        description="Job_Tasks_And_Descriptions"
    )


class EmployeeExposureAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Questions about employee exposure to people with suspected or confirmed COVID-19, including AGP procedures."""

    direct_care_exposure_yes: BooleanLike = Field(
        ...,
        description=(
            "Check YES if employees provide direct care to or are otherwise exposed to "
            "people with suspected or confirmed COVID-19."
        )
    )

    direct_care_exposure_no: BooleanLike = Field(
        ...,
        description=(
            "Check NO if employees do not provide direct care to or are not otherwise "
            "exposed to people with suspected or confirmed COVID-19."
        )
    )

    direct_care_exposure_follow_up_notes: str = Field(
        ...,
        description=(
            "Provide any follow-up information or notes regarding employee exposure. .If "
            "you cannot fill this, write \"N/A\". If this field should not be filled by you "
            "(for example, it belongs to another person or office), leave it blank (empty "
            "string \"\")."
        )
    )

    agp_exposure_yes: BooleanLike = Field(
        ...,
        description=(
            "Check YES if employees perform or assist in performing aerosol-generating "
            "procedures (AGPs) on a person with suspected or confirmed COVID-19."
        )
    )

    agp_exposure_no: BooleanLike = Field(
        ...,
        description=(
            "Check NO if employees do not perform or assist in performing AGPs on a person "
            "with suspected or confirmed COVID-19."
        )
    )

    agp_exposure_follow_up_notes: str = Field(
        ...,
        description=(
            "Provide any follow-up information or notes regarding AGP exposure. .If you "
            "cannot fill this, write \"N/A\". If this field should not be filled by you "
            "(for example, it belongs to another person or office), leave it blank (empty "
            "string \"\")."
        )
    )


class AerosolGeneratingProceduresAGPs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """List of specific AGPs that may result in exposure."""

    open_suctioning_of_airways: BooleanLike = Field(
        ...,
        description="Check if employees perform open suctioning of airways as an AGP."
    )

    sputum_induction: BooleanLike = Field(
        ...,
        description="Check if employees perform sputum induction as an AGP."
    )

    cardiopulmonary_resuscitation: BooleanLike = Field(
        ...,
        description="Check if employees perform cardiopulmonary resuscitation as an AGP."
    )

    endotracheal_intubation_and_extubation: BooleanLike = Field(
        ...,
        description="Check if employees perform endotracheal intubation and extubation as an AGP."
    )

    non_invasive_ventilation_eg_bipap_cpap: BooleanLike = Field(
        ...,
        description=(
            "Check if employees perform non-invasive ventilation (e.g., BiPAP, CPAP) as an "
            "AGP."
        )
    )

    bronchoscopy: BooleanLike = Field(
        ...,
        description="Check if employees perform bronchoscopy as an AGP."
    )

    manual_ventilation: BooleanLike = Field(
        ...,
        description="Check if employees perform manual ventilation as an AGP."
    )

    medical_surgical_postmortem_procedures_using_oscillating_bone_saws: BooleanLike = Field(
        ...,
        description=(
            "Check if employees perform medical, surgical, or postmortem procedures using "
            "oscillating bone saws as an AGP."
        )
    )

    dental_procedures_involving_ultrasonic_scalers_high_speed_dental_handpieces_air_water_syringes_air_polishing_and_air_abrasion: BooleanLike = Field(
        ...,
        description=(
            "Check if employees perform dental procedures involving ultrasonic scalers, "
            "high-speed dental handpieces, air/water syringes, air polishing, or air "
            "abrasion as an AGP."
        )
    )


class PotentialExposureJobTasks(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Table for listing locations, number of workers, and job tasks/descriptions with potential exposure."""

    potential_exposure_table: List[PotentialExposureTableRow] = Field(
        ...,
        description=(
            "Table to record locations, number of workers, and job tasks/descriptions where "
            "employees have potential for exposure."
        )
    )  # List of table rows


class WellDefinedAreaswithNoExposure(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Areas of the workplace where there is no reasonable expectation of exposure to COVID-19."""

    well_defined_areas_no_exposure: str = Field(
        ...,
        description=(
            "List any well-defined areas of the workplace where there is no reasonable "
            "expectation of exposure to suspected or confirmed COVID-19 cases. .If you "
            "cannot fill this, write \"N/A\". If this field should not be filled by you "
            "(for example, it belongs to another person or office), leave it blank (empty "
            "string \"\")."
        )
    )


class EmployeeCovid19ExposureTaskInventory(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    Job Task Inventory for Employees with Potential for Exposure to a Person with Suspected or Confirmed COVID-19

    Use this Job Task Inventory and input from employees to identify any job tasks where employees have potential for exposure to a person with suspected or confirmed COVID-19.
    """

    employee_exposure_assessment: EmployeeExposureAssessment = Field(
        ...,
        description="Employee Exposure Assessment"
    )
    aerosol_generating_procedures_agps: AerosolGeneratingProceduresAGPs = Field(
        ...,
        description="Aerosol-Generating Procedures (AGPs)"
    )
    potential_exposure_job_tasks: PotentialExposureJobTasks = Field(
        ...,
        description="Potential Exposure Job Tasks"
    )
    well_defined_areas_with_no_exposure: WellDefinedAreaswithNoExposure = Field(
        ...,
        description="Well-Defined Areas with No Exposure"
    )