from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ExposureJobTaskTableRow(BaseModel):
    """Single row in Location(s)"""

    location_s: str = Field(default="", description="Location_S")
    no_of_workers: str = Field(default="", description="No_Of_Workers")
    job_tasks_and_descriptions: str = Field(default="", description="Job_Tasks_And_Descriptions")


class EmployeeExposureScreeningQuestions(BaseModel):
    """Questions about whether employees are exposed to people with suspected or confirmed COVID-19 and related AGPs, including response columns."""

    do_employees_provide_direct_care_exposed_to_people_with_suspected_or_confirmed_covid_19: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether employees provide direct care to or are otherwise exposed to "
            "people with suspected or confirmed COVID-19."
        ),
    )

    do_employees_perform_or_assist_in_performing_agps_on_a_person_with_suspected_or_confirmed_covid_19: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether employees perform or assist in performing aerosol-generating "
            "procedures (AGPs) on a person with suspected or confirmed COVID-19."
        ),
    )

    open_suctioning_of_airways: BooleanLike = Field(
        default="",
        description=(
            "Check if employees perform open suctioning of airways as an aerosol-generating "
            "procedure."
        ),
    )

    sputum_induction: BooleanLike = Field(
        default="",
        description="Check if employees perform sputum induction as an aerosol-generating procedure.",
    )

    cardiopulmonary_resuscitation: BooleanLike = Field(
        default="",
        description=(
            "Check if employees perform cardiopulmonary resuscitation as an "
            "aerosol-generating procedure."
        ),
    )

    endotracheal_intubation_and_extubation: BooleanLike = Field(
        default="",
        description=(
            "Check if employees perform endotracheal intubation and extubation as an "
            "aerosol-generating procedure."
        ),
    )

    non_invasive_ventilation_eg_bipap_cpap: BooleanLike = Field(
        default="",
        description=(
            "Check if employees use non-invasive ventilation (e.g., BiPAP, CPAP) as an "
            "aerosol-generating procedure."
        ),
    )

    bronchoscopy: BooleanLike = Field(
        default="",
        description="Check if employees perform bronchoscopy as an aerosol-generating procedure.",
    )

    manual_ventilation: BooleanLike = Field(
        default="",
        description=(
            "Check if employees perform manual ventilation as an aerosol-generating procedure."
        ),
    )

    medical_surgical_postmortem_procedures_using_oscillating_bone_saws: BooleanLike = Field(
        default="",
        description=(
            "Check if employees perform medical, surgical, or postmortem procedures using "
            "oscillating bone saws."
        ),
    )

    dental_procedures_involving_ultrasonic_scalers_high_speed_dental_handpieces_air_water_syringes_air_polishing_and_air_abrasion: BooleanLike = Field(
        default="",
        description=(
            "Check if employees perform dental procedures involving ultrasonic scalers, "
            "high-speed dental handpieces, air/water syringes, air polishing, or air "
            "abrasion."
        ),
    )

    yes_column: BooleanLike = Field(
        default="", description="Indicates a YES response to the exposure question."
    )

    no_column: BooleanLike = Field(
        default="", description="Indicates a NO response to the exposure question."
    )

    follow_up_notes: str = Field(
        default="",
        description=(
            "Space to record follow-up actions, clarifications, or notes related to the "
            'exposure question. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class ExposureJobTaskDetails(BaseModel):
    """Table to document locations, number of workers, and job tasks where exposure may occur."""

    exposure_job_task_table: List[ExposureJobTaskTableRow] = Field(
        default="",
        description=(
            "Table to record locations, number of workers, and job tasks/descriptions where "
            "employees may be exposed."
        ),
    )  # List of table rows

    no_of_workers: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of workers at the specified location performing the described job tasks.",
    )

    job_tasks_and_descriptions: str = Field(
        default="",
        description=(
            "Describe the job tasks performed and any relevant details about potential "
            'exposure. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class AreaswithNoExpectedCOVID19Presence(BaseModel):
    """Identification of workplace areas where no person with suspected or confirmed COVID-19 is reasonably expected to be present."""

    are_there_any_well_defined_areas_with_no_reasonable_expectation_of_covid_19_presence: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether there are well-defined areas in the workplace where no person "
            "with suspected or confirmed COVID-19 is reasonably expected to be present."
        ),
    )

    well_defined_areas_no_expected_covid_19_presence_list_items: str = Field(
        default="",
        description=(
            "List each well-defined area where there is no reasonable expectation that any "
            "person with suspected or confirmed COVID-19 will be present (e.g., employee "
            'break room). .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class EmployeeCovidExposureJobTaskInventory(BaseModel):
    """
        Job Task Inventory for Employees with Potential for Exposure to a Person
    with Suspected or Confirmed COVID-19

        Use this Job Task Inventory and input from employees to identify any job tasks where employees have potential for exposure to a person with suspected or confirmed COVID-19.
    """

    employee_exposure_screening_questions: EmployeeExposureScreeningQuestions = Field(
        ..., description="Employee Exposure Screening Questions"
    )
    exposure_job_task_details: ExposureJobTaskDetails = Field(
        ..., description="Exposure Job Task Details"
    )
    areas_with_no_expected_covid_19_presence: AreaswithNoExpectedCOVID19Presence = Field(
        ..., description="Areas with No Expected COVID-19 Presence"
    )
