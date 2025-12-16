from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProfessionalReferencesTableRow(BaseModel):
    """Single row in PROFESSIONAL REFERENCES NAME"""

    name: str = Field(default="", description="Name")
    occupation: str = Field(default="", description="Occupation")
    years_known: str = Field(default="", description="Years_Known")
    day_time_phone_number: str = Field(default="", description="Day_Time_Phone_Number")


class JobDutiesandPreviousEmployment(BaseModel):
    """Details about prior job duties, reasons for leaving, and supervisor information"""

    describe_your_job_duties: str = Field(
        ...,
        description=(
            "Describe the primary responsibilities and tasks of your job. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    reason_for_leaving: str = Field(
        ...,
        description=(
            "Explain why you left or are leaving this position. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    supervisors_name: str = Field(
        ...,
        description=(
            "Name of your supervisor for this position. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProfessionalReferences(BaseModel):
    """Professional reference contacts and related details"""

    professional_references_table: List[ProfessionalReferencesTableRow] = Field(
        default="",
        description=(
            "List professional references including name, occupation, years known, and "
            "daytime phone number."
        ),
    )  # List of table rows

    professional_references_occupation: str = Field(
        default="",
        description=(
            "Occupation or job title of the professional reference. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    professional_references_years_known: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years you have known this reference."
    )

    professional_references_day_time_phone_number: str = Field(
        default="",
        description=(
            "Daytime phone number for the professional reference. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    no_do_not_contact_my_current_employer: BooleanLike = Field(
        default="",
        description="Check if you do not want your current employer to be contacted for a reference.",
    )

    reason_do_not_contact_current_employer: str = Field(
        default="",
        description=(
            "Reason you prefer that your current employer not be contacted. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class EmploymentHistoryandPriorRustsK2Employment(BaseModel):
    """Employment history issues and prior employment with Rust’s Flying Service or K2 Aviation"""

    employment_termination_no: BooleanLike = Field(
        ...,
        description=(
            "Select if you have not been fired, dismissed, forced to resign, or resigned in "
            "lieu of termination."
        ),
    )

    employment_termination_yes: BooleanLike = Field(
        ...,
        description=(
            "Select if you have been fired, dismissed, forced to resign, or resigned in "
            "lieu of termination."
        ),
    )

    employment_termination_explanation: str = Field(
        default="",
        description=(
            "If you answered yes, provide details about the circumstances of your "
            'termination or resignation. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    prior_employment_rusts_k2_yes: BooleanLike = Field(
        ...,
        description=(
            "Select if you have previously been employed by Rust’s Flying Service or K2 Aviation."
        ),
    )

    prior_employment_rusts_k2_no: BooleanLike = Field(
        ...,
        description=(
            "Select if you have not previously been employed by Rust’s Flying Service or K2 "
            "Aviation."
        ),
    )

    prior_employment_position: str = Field(
        default="",
        description=(
            "Position or job title you held at Rust’s Flying Service or K2 Aviation. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    prior_employment_when: str = Field(
        default="",
        description=(
            "Approximate dates or time period when you were employed there. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    prior_employment_reason_for_leaving: str = Field(
        default="",
        description=(
            "Reason you left your prior employment with Rust’s Flying Service or K2 "
            'Aviation. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    prior_employment_where: str = Field(
        default="",
        description=(
            "Location or base where you worked for Rust’s Flying Service or K2 Aviation. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    supervisors_name_title_phone_number: str = Field(
        default="",
        description=(
            "Name, job title, and phone number of your supervisor at Rust’s Flying Service "
            'or K2 Aviation. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class CriminalHistory(BaseModel):
    """Disclosure of felony, misdemeanor, and traffic violation history"""

    felony_yes: BooleanLike = Field(
        ..., description="Select if you have pleaded no contest to or been convicted of a felony."
    )

    felony_no: BooleanLike = Field(
        ...,
        description="Select if you have not pleaded no contest to or been convicted of a felony.",
    )

    felony_nature_of_offense: str = Field(
        default="",
        description=(
            "Describe the nature of the felony offense. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    felony_disposition: str = Field(
        default="",
        description=(
            "Outcome or disposition of the felony case (e.g., sentence, probation). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    felony_date: str = Field(
        default="", description="Date of the felony conviction or plea."
    )  # YYYY-MM-DD format

    felony_location: str = Field(
        default="",
        description=(
            "City, county, and/or state where the felony occurred or was adjudicated. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    misdemeanor_yes: BooleanLike = Field(
        ...,
        description="Select if you have pleaded no contest to or been convicted of a misdemeanor.",
    )

    misdemeanor_no: BooleanLike = Field(
        ...,
        description=(
            "Select if you have not pleaded no contest to or been convicted of a misdemeanor."
        ),
    )

    misdemeanor_nature_of_offense: str = Field(
        default="",
        description=(
            "Describe the nature of the misdemeanor offense. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    misdemeanor_disposition: str = Field(
        default="",
        description=(
            "Outcome or disposition of the misdemeanor case (e.g., fine, probation). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    misdemeanor_date: str = Field(
        default="", description="Date of the misdemeanor conviction or plea."
    )  # YYYY-MM-DD format

    misdemeanor_location: str = Field(
        default="",
        description=(
            "City, county, and/or state where the misdemeanor occurred or was adjudicated. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    traffic_violation_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if you have pleaded no contest to or been convicted of a traffic violation."
        ),
    )

    traffic_violation_no: BooleanLike = Field(
        default="",
        description=(
            "Select if you have not pleaded no contest to or been convicted of a traffic violation."
        ),
    )


class RustsFlyingService(BaseModel):
    """
    Rust’s Flying Service

    A conviction is not an automatic bar from employment with Rust Flying Service. Failure to complete this section may result in your application being rejected. Omission of any information may result in your application being rejected or may be grounds for termination if hired.
    """

    job_duties_and_previous_employment: JobDutiesandPreviousEmployment = Field(
        ..., description="Job Duties and Previous Employment"
    )
    professional_references: ProfessionalReferences = Field(
        ..., description="Professional References"
    )
    employment_history_and_prior_rustsk2_employment: EmploymentHistoryandPriorRustsK2Employment = (
        Field(..., description="Employment History and Prior Rust’s/K2 Employment")
    )
    criminal_history: CriminalHistory = Field(..., description="Criminal History")
