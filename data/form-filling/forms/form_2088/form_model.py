from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class LocationSNoOfWorkersJobTasksAndDescriptionsTableRow(BaseModel):
    """Single row in Location(s)"""

    location_s: str = Field(default="", description="Location_S")
    no_of_workers: str = Field(default="", description="No_Of_Workers")
    job_tasks_and_descriptions: str = Field(default="", description="Job_Tasks_And_Descriptions")


class EmployeeExposureQuestions(BaseModel):
    """Questions about whether employees are exposed to people with suspected or confirmed COVID-19 and whether they perform aerosol-generating procedures (AGPs)."""

    do_employees_provide_direct_care_to_or_are_they_otherwise_exposed_to_people_with_suspected_or_confirmed_covid_19: BooleanLike = Field(
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
            "Check if employees perform cardiopulmonary resuscitation (CPR) as an "
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
            "high-speed handpieces, air/water syringes, air polishing, or air abrasion."
        ),
    )

    yes: BooleanLike = Field(
        default="", description="Column to indicate a YES response to the exposure question."
    )

    no: BooleanLike = Field(
        default="", description="Column to indicate a NO response to the exposure question."
    )

    follow_up_notes: str = Field(
        default="",
        description=(
            "Space to record follow-up actions or notes related to the exposure question. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class ExposureJobTaskDetails(BaseModel):
    """Details about locations, number of workers, and job tasks where employees have potential exposure."""

    location_s_no_of_workers_job_tasks_and_descriptions_table: List[
        LocationSNoOfWorkersJobTasksAndDescriptionsTableRow
    ] = Field(
        ...,
        description=(
            "Table to list each location, the number of workers, and the job tasks and "
            "descriptions where employees may be exposed."
        ),
    )  # List of table rows

    no_of_workers: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of workers at the specified location performing the listed tasks.",
    )

    job_tasks_and_descriptions: str = Field(
        default="",
        description=(
            "Describe the job tasks performed at the location that may involve exposure. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class NonExposureAreas(BaseModel):
    """Well-defined workplace areas where there is no reasonable expectation of presence of persons with suspected or confirmed COVID-19."""

    are_there_any_well_defined_areas_of_your_workplace_in_which_there_is_no_reasonable_expectation_that_any_person_with_suspected_or_confirmed_covid_19_will_be_present_if_yes_list_here: str = Field(
        default="",
        description=(
            "Prompt asking whether there are well-defined areas with no reasonable "
            "expectation of COVID-19 presence; list such areas below if applicable. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    well_defined_area_1: str = Field(
        default="",
        description=(
            "Name or description of a well-defined area with no reasonable expectation of "
            'COVID-19 presence (first entry). .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    well_defined_area_2: str = Field(
        default="",
        description=(
            "Name or description of a well-defined area with no reasonable expectation of "
            'COVID-19 presence (second entry). .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    well_defined_area_3: str = Field(
        default="",
        description=(
            "Name or description of a well-defined area with no reasonable expectation of "
            'COVID-19 presence (third entry). .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    well_defined_area_4: str = Field(
        default="",
        description=(
            "Name or description of a well-defined area with no reasonable expectation of "
            'COVID-19 presence (fourth entry). .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class EmployeeCovidExposureJobTaskInventory(BaseModel):
    """
        Job Task Inventory for Employees with Potential for Exposure to a Person
    with Suspected or Confirmed COVID-19

        Use this Job Task Inventory and input from employees to identify any job tasks where employees have potential for exposure to a person with suspected or confirmed COVID-19.
    """

    employee_exposure_questions: EmployeeExposureQuestions = Field(
        ..., description="Employee Exposure Questions"
    )
    exposure_job_task_details: ExposureJobTaskDetails = Field(
        ..., description="Exposure Job Task Details"
    )
    non_exposure_areas: NonExposureAreas = Field(..., description="Non-Exposure Areas")
