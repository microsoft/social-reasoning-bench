from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ChurchInformation(BaseModel):
    """Basic information about the church and primary contact"""

    name_of_church: str = Field(
        ...,
        description=(
            'Full legal name of the church .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this application is completed")  # YYYY-MM-DD format

    physical_address: str = Field(
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
            "Best phone number for the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            "Email address for the contact person or church office .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectDescription(BaseModel):
    """Details about the repair work requested and any professional evaluations"""

    describe_what_work_needs_to_be_done: str = Field(
        ...,
        description=(
            "Detailed description of the repair work requested .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    has_the_church_had_any_professional_evaluation_of_the_needed_work_or_a_professional_cost_estimate_done: str = Field(
        default="",
        description=(
            "Indicate whether a professional evaluation or cost estimate has been done and "
            "summarize the findings; attach bids or estimates if available .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class FinancialInformation(BaseModel):
    """Budget, funding, and fundraising related to the project"""

    what_is_the_churchs_operating_budget_for_the_current_calendar_year: Union[
        float, Literal["N/A", ""]
    ] = Field(
        ..., description="Total operating budget amount for the current calendar year in dollars"
    )

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
        description=(
            "Indicate whether the congregation currently has funds available for this project"
        ),
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


class CongregationalSupport(BaseModel):
    """Ways the congregation can assist with the project"""

    would_the_church_assist_if_this_project_were_undertaken_by_the_west_district_by_providing_volunteer_laborers_and_meals_for_the_work_teams: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the church can provide volunteer laborers and meals for work "
            "teams if the West District undertakes the project"
        ),
    )


class CongregationalStatistics(BaseModel):
    """Attendance and apportionment payment history"""

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
        ..., description="Average Sunday worship attendance for the year prior to last year"
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
    """Signatures from church leadership"""

    name_of_pastor: str = Field(
        ...,
        description=(
            'Printed name of the pastor .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    signature_of_pastor: str = Field(
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
            "Printed name of the chair of the Board of Trustees .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_trustees_chair: str = Field(
        ...,
        description=(
            "Signature of the Trustees chair supporting this application .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ApplicationForWestDistrictChurchRepairs(BaseModel):
    """
    APPLICATION FOR WEST DISTRICT CHURCH REPAIRS

    ''
    """

    church_information: ChurchInformation = Field(..., description="Church Information")
    project_description: ProjectDescription = Field(..., description="Project Description")
    financial_information: FinancialInformation = Field(..., description="Financial Information")
    congregational_support: CongregationalSupport = Field(..., description="Congregational Support")
    congregational_statistics: CongregationalStatistics = Field(
        ..., description="Congregational Statistics"
    )
    authorization: Authorization = Field(..., description="Authorization")
