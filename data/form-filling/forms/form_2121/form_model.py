from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ChurchInformation(BaseModel):
    """Basic information about the church and contact person"""

    name_of_church: str = Field(
        ...,
        description=(
            'Full legal name of the church .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this application is completed")  # YYYY-MM-DD format

    physical_adress: str = Field(
        ...,
        description=(
            "Street address where the church building is located .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_contact_person: str = Field(
        ...,
        description=(
            "Primary contact person for this application .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Phone number for the contact person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            "Email address for the contact person or church .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectDescriptionandEvaluation(BaseModel):
    """Details about the repair project and any professional evaluations"""

    describe_what_work_needs_to_be_done: str = Field(
        ...,
        description=(
            "Detailed description of the repair or project work requested .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    has_the_church_had_any_professional_evaluation_of_the_needed_work_or_a_professional_cost_estimate_done: BooleanLike = Field(
        default="",
        description="Indicate whether a professional evaluation or cost estimate has been obtained",
    )

    what_was_communicated_attach_copies_of_bids_or_estimates: str = Field(
        default="",
        description=(
            "Summary of the findings, recommendations, or costs from any professional "
            'evaluations or estimates .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class FinancialInformationandFundraising(BaseModel):
    """Budget, financial capacity, and fundraising plans for the project"""

    what_is_the_churchs_operating_budget_for_the_current_calendar_year: Union[
        float, Literal["N/A", ""]
    ] = Field(..., description="Total operating budget amount for the current calendar year")

    briefly_tell_why_the_congregation_cannot_undertake_this_project_by_itself: str = Field(
        ...,
        description=(
            "Explanation of financial or other limitations preventing the congregation from "
            'doing the project alone .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    does_the_congregation_have_any_funds_to_devote_to_this_project: BooleanLike = Field(
        default="",
        description="Indicate whether the congregation has any funds available for this project",
    )

    have_future_fundraising_activities_been_planned: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether any future fundraising activities are planned to support this project"
        ),
    )

    if_so_describe: str = Field(
        default="",
        description=(
            "Description of available funds and/or planned fundraising activities .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class CongregationalSupportandParticipation(BaseModel):
    """Information about volunteer support and participation from the congregation"""

    would_the_church_assist_if_this_project_were_undertaken_by_the_west_district_by_providing_volunteer_laborers_and_meals_for_the_work_teams: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the church can provide volunteer labor and meals for work teams"
        ),
    )


class AttendanceandApportionments(BaseModel):
    """Attendance history and apportionment payment percentages"""

    what_has_been_the_average_sunday_worship_attendance_for_the_current_calendar_year: Union[
        float, Literal["N/A", ""]
    ] = Field(
        ...,
        description=(
            "Average number of people attending Sunday worship during the current calendar year"
        ),
    )

    what_was_the_average_attendance_last_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Average Sunday worship attendance for the previous calendar year"
    )

    in_the_year_before_that: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Average Sunday worship attendance for two years ago"
    )

    conference_percentage_paid: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Percentage of Conference apportionments paid by the congregation in the past "
            "calendar year"
        ),
    )

    district_percentage_paid: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Percentage of district apportionments paid by the congregation in the past "
            "calendar year"
        ),
    )


class Authorization(BaseModel):
    """Signatures and names of responsible leaders"""

    name_of_pastor: str = Field(
        ...,
        description=(
            'Full name of the pastor .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    signature_pastor: str = Field(
        ...,
        description=(
            "Pastor's signature authorizing this application .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_trustees_chair: str = Field(
        ...,
        description=(
            "Full name of the chair of the Board of Trustees .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_trustees_chair: str = Field(
        ...,
        description=(
            "Signature of the Trustees chair authorizing this application .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ApplicationForWestDistrictChurchRepairs(BaseModel):
    """APPLICATION FOR WEST DISTRICT CHURCH REPAIRS"""

    church_information: ChurchInformation = Field(..., description="Church Information")
    project_description_and_evaluation: ProjectDescriptionandEvaluation = Field(
        ..., description="Project Description and Evaluation"
    )
    financial_information_and_fundraising: FinancialInformationandFundraising = Field(
        ..., description="Financial Information and Fundraising"
    )
    congregational_support_and_participation: CongregationalSupportandParticipation = Field(
        ..., description="Congregational Support and Participation"
    )
    attendance_and_apportionments: AttendanceandApportionments = Field(
        ..., description="Attendance and Apportionments"
    )
    authorization: Authorization = Field(..., description="Authorization")
