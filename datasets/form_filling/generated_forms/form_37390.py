from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProjectInformation(BaseModel):
    """Basic information about the project and its reach"""

    organization_name: str = Field(
        ...,
        description=(
            "Legal name of the organization applying for the grant .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    approximate_number_of_people_served_by_this_project: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Estimated total number of individuals who will be served by this specific project"
        ),
    )

    period_of_time_covered_by_the_project: str = Field(
        ...,
        description=(
            "Timeframe for the project (e.g., dates or duration such as 'Jan–Dec 2026' or "
            "'12 months') .If you cannot fill this, write \"N/A\". If this field should not "
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class OrganizationalInformation(BaseModel):
    """Background, scale, partnerships, and governance of the organization"""

    how_long_has_the_organization_been_in_existence: str = Field(
        ...,
        description=(
            "Length of time the organization has operated (e.g., number of years, founding "
            'year) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    how_many_people_are_served_annually_overall: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of individuals served by the organization in a typical year"
    )

    number_of_paid_staff_full_time: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of full-time paid staff employed by the organization"
    )

    number_of_paid_staff_part_time: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of part-time paid staff employed by the organization"
    )

    number_of_volunteers_involved_in_your_organization: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Total number of volunteers who are actively involved with the organization",
    )

    percentage_of_the_people_you_serve_who_use_your_services_multiple_times: str = Field(
        default="",
        description=(
            "Approximate percentage and any explanation of repeat service usage by clients "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    other_non_profit_agencies_that_your_organization_is_partnered_with: str = Field(
        default="",
        description=(
            "List of partner non-profit agencies and any relevant details about the "
            'partnerships .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    how_often_does_your_board_meet: str = Field(
        ...,
        description=(
            "Frequency of board meetings (e.g., monthly, quarterly, annually) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    members_of_the_board_of_directors: str = Field(
        ...,
        description=(
            "Names of all members of the Board of Directors, optionally including roles or "
            'affiliations .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    names_and_titles_of_the_leadership_of_your_organization: str = Field(
        ...,
        description=(
            "Names and official titles of key leadership staff (e.g., Executive Director, "
            'CFO, Program Director) .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class EngelstadFoundationGrantApplication(BaseModel):
    """
    Engelstad Foundation Grant Application

    ''
    """

    project_information: ProjectInformation = Field(..., description="Project Information")
    organizational_information: OrganizationalInformation = Field(
        ..., description="Organizational Information"
    )
