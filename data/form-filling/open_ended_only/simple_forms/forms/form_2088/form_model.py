from pydantic import BaseModel, ConfigDict, Field


class JobTaskInventoryForEmployeesWithPotentialForExposureToAPersonWithSuspectedOrConfirmedCovid19(BaseModel):
    """Job Task Inventory for Employees with Potential for Exposure to a Person with Suspected or Confirmed COVID-19"""

    model_config = ConfigDict(extra="forbid")

    exposure_direct_care: bool | None = Field(
        ..., description="Employee(s) provide direct care or exposure to suspected/confirmed COVID-19 person?"
    )
    exposure_direct_care_followup_notes: str = Field(
        ..., description='Follow-up / Notes for direct care exposure. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    exposure_agp: bool | None = Field(
        ..., description="Employee(s) perform or assist in AGPs on suspected/confirmed COVID-19 person?"
    )
    exposure_agp_followup_notes: str = Field(
        ..., description='Follow-up / Notes for AGP exposure. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    exposure_agp_open_suctioning: bool | None = Field(
        ..., description="Performs open suctioning of airways?"
    )
    exposure_agp_sputum_induction: bool | None = Field(
        ..., description="Performs sputum induction?"
    )
    exposure_agp_cpr: bool | None = Field(
        ..., description="Performs cardiopulmonary resuscitation?"
    )
    exposure_agp_intubation_extubation: bool | None = Field(
        ..., description="Performs endotracheal intubation and extubation?"
    )
    exposure_agp_noninvasive_ventilation: bool | None = Field(
        ..., description="Performs non-invasive ventilation (e.g., BiPAP, CPAP)?"
    )
    exposure_agp_bronchoscopy: bool | None = Field(
        ..., description="Performs bronchoscopy?"
    )
    exposure_agp_manual_ventilation: bool | None = Field(
        ..., description="Performs manual ventilation?"
    )
    exposure_agp_oscillating_bone_saws: bool | None = Field(
        ..., description="Performs medical/surgical/postmortem procedures using oscillating bone saws?"
    )
    exposure_agp_dental_procedures: bool | None = Field(
        ..., description="Performs dental procedures involving ultrasonic scalers, high-speed dental handpieces, air/water syringes, air polishing, or air abrasion?"
    )
    exposure_table: list[list[str]] = Field(
        ...,
        description='Table of exposure locations, number of workers, and job tasks and descriptions. Columns: Location(s), No. of Workers, Job Tasks and Descriptions. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    well_defined_no_exposure_areas: str = Field(
        ..., description='List of well-defined workplace areas with no reasonable expectation of exposure. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )