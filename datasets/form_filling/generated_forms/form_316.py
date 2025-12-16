from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PositionsHeldRow(BaseModel):
    """Single row in Position(s) Held"""

    position_s_held: str = Field(default="", description="Position_S_Held")
    brief_description_of_duties: str = Field(default="", description="Brief_Description_Of_Duties")
    supervisor_s_name: str = Field(default="", description="Supervisor_S_Name")


class BriefDescriptionOfDutiesRow(BaseModel):
    """Single row in Brief Description of Duties"""

    position_s_held: str = Field(default="", description="Position_S_Held")
    brief_description_of_duties: str = Field(default="", description="Brief_Description_Of_Duties")
    supervisor_s_name: str = Field(default="", description="Supervisor_S_Name")


class SupervisorSNameRow(BaseModel):
    """Single row in Supervisor’s Name"""

    position_s_held: str = Field(default="", description="Position_S_Held")
    brief_description_of_duties: str = Field(default="", description="Brief_Description_Of_Duties")
    supervisor_s_name: str = Field(default="", description="Supervisor_S_Name")


class EmploymentHistory(BaseModel):
    """Details about previous employment"""

    name_of_employer: str = Field(
        ...,
        description=(
            "Full legal name of your employer for this position .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            "Primary telephone number for this employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_of_employer: str = Field(
        ...,
        description=(
            "Mailing or physical address of this employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    employed_from: str = Field(
        ..., description="Start date of your employment with this employer"
    )  # YYYY-MM-DD format

    employed_to: str = Field(
        ..., description="End date of your employment with this employer"
    )  # YYYY-MM-DD format

    positions_held: List[PositionsHeldRow] = Field(
        ..., description="List the job titles you held, with duties and supervisor for each"
    )  # List of table rows

    brief_description_of_duties: List[BriefDescriptionOfDutiesRow] = Field(
        ..., description="For each position, summarize your main responsibilities"
    )  # List of table rows

    supervisor_s_name: List[SupervisorSNameRow] = Field(
        ..., description="Name of your direct supervisor for each position listed"
    )  # List of table rows

    reason_for_leaving_if_applicable: str = Field(
        default="",
        description=(
            "Explain why you left this position, if you are no longer employed there .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    yes_have_you_ever_been_discharged_or_asked_to_resign_from_a_job: BooleanLike = Field(
        ...,
        description="Indicate whether you have ever been discharged or asked to resign from a job",
    )

    no_have_you_ever_been_discharged_or_asked_to_resign_from_a_job: BooleanLike = Field(
        ...,
        description="Indicate whether you have ever been discharged or asked to resign from a job",
    )

    if_yes_please_explain: str = Field(
        default="",
        description=(
            "If you answered yes, provide details about the circumstances .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class References(BaseModel):
    """Three references not related to the applicant"""

    reference_1_name: str = Field(
        ...,
        description=(
            "Full name of your first reference (not related to you) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_1_occupation: str = Field(
        ...,
        description=(
            "Current occupation or job title of your first reference .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_1_address: str = Field(
        ...,
        description=(
            "Mailing address for your first reference .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reference_1_years_known: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of years you have known your first reference"
    )

    reference_1_phone_number: str = Field(
        ...,
        description=(
            "Telephone number for your first reference .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_name: str = Field(
        ...,
        description=(
            "Full name of your second reference (not related to you) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_occupation: str = Field(
        ...,
        description=(
            "Current occupation or job title of your second reference .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_address: str = Field(
        ...,
        description=(
            "Mailing address for your second reference .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_years_known: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of years you have known your second reference"
    )

    reference_2_phone_number: str = Field(
        ...,
        description=(
            "Telephone number for your second reference .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reference_3_name: str = Field(
        ...,
        description=(
            "Full name of your third reference (not related to you) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_3_occupation: str = Field(
        ...,
        description=(
            "Current occupation or job title of your third reference .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_3_address: str = Field(
        ...,
        description=(
            "Mailing address for your third reference .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reference_3_years_known: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of years you have known your third reference"
    )

    reference_3_phone_number: str = Field(
        ...,
        description=(
            "Telephone number for your third reference .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Declaration(BaseModel):
    """Applicant declaration and agreement"""

    i_have_read_understand_and_agree_to_the_above_statement_initials: str = Field(
        ...,
        description=(
            "Your initials indicating you have read, understood, and agree to the "
            'declaration .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class HobsonEnterprisesLtd(BaseModel):
    """
    HOBSON ENTERPRISES LTD.

    Carefully read and initial each section then sign at the bottom.
    I certify that the answers given herein are true and complete to the best of my knowledge and that no requested information has been concealed. I authorise West Side Service Center to investigate all statements contained in this application, with the exception of contacting my present employer. If any information I have provided is untrue, or if I have concealed material information, I understand that this will constitute cause for the denial of employment or immediate dismissal.
    """

    employment_history: EmploymentHistory = Field(..., description="Employment History")
    references: References = Field(..., description="References")
    declaration: Declaration = Field(..., description="Declaration")
