from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ChurchInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Basic information about the church and contact details"""

    name_of_church: str = Field(
        ...,
        description=(
            "Full name of the church applying for repairs .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    date: str = Field(
        ...,
        description="Date of application submission"
    )  # YYYY-MM-DD format

    physical_adress: str = Field(
        ...,
        description=(
            "Physical address of the church .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    name_of_contact_person: str = Field(
        ...,
        description=(
            "Name of the main contact person for this application .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    phone: str = Field(
        ...,
        description=(
            "Phone number of the contact person .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    e_mail: str = Field(
        ...,
        description=(
            "Email address of the contact person .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class ProjectDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the repair project and its needs"""

    describe_what_work_needs_to_be_done: str = Field(
        ...,
        description=(
            "Description of the repairs or work needed at the church .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    has_the_church_had_any_professional_evaluation_of_the_needed_work_or_a_professional_cost_estimate_done: BooleanLike = Field(
        ...,
        description="Indicate if a professional evaluation or cost estimate has been done"
    )


class FinancialInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Budget, funding, and financial support for the project"""

    what_is_the_churchs_operating_budget_for_the_current_calendar_year: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Operating budget amount for the current year"
    )

    briefly_tell_why_the_congregation_cannot_undertake_this_project_by_itself: str = Field(
        ...,
        description=(
            "Explanation of why the congregation cannot do the project alone .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )

    does_the_congregation_have_any_funds_to_devote_to_this_project: BooleanLike = Field(
        ...,
        description="Indicate if the congregation has funds for the project"
    )

    have_future_fundraising_activities_been_planned: BooleanLike = Field(
        ...,
        description="Indicate if future fundraising activities are planned"
    )


class CongregationalSupport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Congregation's ability to assist and provide support"""

    would_the_church_assist_if_this_project_were_undertaken_by_the_west_district_by_providing_volunteer_laborers_and_meals_for_the_work_teams: BooleanLike = Field(
        ...,
        description="Indicate if the church would provide volunteers and meals for work teams"
    )


class AttendanceandApportionments(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Attendance statistics and apportionment payments"""

    what_has_been_the_average_sunday_worship_attendance_for_the_current_calendar_year: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Average Sunday worship attendance for the current year"
    )

    what_was_the_average_attendance_last_year: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Average attendance last year"
    )

    in_the_year_before_that: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Average attendance in the year before last"
    )

    conference_percentage_paid: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Percentage of Conference apportionments paid last year"
    )

    district_percentage_paid: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Percentage of District apportionments paid last year"
    )


class Signatures(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Signatures of responsible church officials"""

    name_of_pastor: str = Field(
        ...,
        description=(
            "Name of the pastor .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    signature_pastor: str = Field(
        ...,
        description=(
            "Pastor's signature .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    name_of_trustees_chair: str = Field(
        ...,
        description=(
            "Name of the Trustees chair .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    signature_trustees_chair: str = Field(
        ...,
        description=(
            "Signature of Trustees chair .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )


class ApplicationForWestDistrictChurchRepairs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    APPLICATION FOR WEST DISTRICT CHURCH REPAIRS

    ''
    """

    church_information: ChurchInformation = Field(
        ...,
        description="Church Information"
    )
    project_details: ProjectDetails = Field(
        ...,
        description="Project Details"
    )
    financial_information: FinancialInformation = Field(
        ...,
        description="Financial Information"
    )
    congregational_support: CongregationalSupport = Field(
        ...,
        description="Congregational Support"
    )
    attendance_and_apportionments: AttendanceandApportionments = Field(
        ...,
        description="Attendance and Apportionments"
    )
    signatures: Signatures = Field(
        ...,
        description="Signatures"
    )