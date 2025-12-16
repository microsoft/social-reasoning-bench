from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantRelationship(BaseModel):
    """Your relationship with the organization or event"""

    volunteer: BooleanLike = Field(
        default="",
        description="Check if your relationship with the organization or event is as a volunteer",
    )

    board_staff: BooleanLike = Field(
        default="",
        description="Check if your relationship with the organization or event is as board or staff",
    )

    paid_solicitor_fundraiser: BooleanLike = Field(
        default="",
        description=(
            "Check if your relationship with the organization or event is as a paid "
            "solicitor or fundraiser"
        ),
    )

    other_please_describe_relationship: str = Field(
        default="",
        description=(
            "If your relationship is not listed, briefly describe it .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProgramProjectOverview(BaseModel):
    """Basic information about the requested grant and program/project focus"""

    amount_of_request: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Dollar amount being requested in this grant application"
    )

    program_project_goal: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total financial goal for the program or project in dollars"
    )

    education: BooleanLike = Field(
        default="", description="Select if the program/project area of priority is Education"
    )

    arts_culture: BooleanLike = Field(
        default="", description="Select if the program/project area of priority is Arts & Culture"
    )

    human_services: BooleanLike = Field(
        default="", description="Select if the program/project area of priority is Human Services"
    )

    other_please_describe_priority: str = Field(
        default="",
        description=(
            "If the program/project area of priority is not listed, briefly describe it .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ProgramProjectDetails(BaseModel):
    """Timing, budget, beneficiaries, and evaluation of the program/project"""

    time_frame_for_completion: str = Field(
        ...,
        description=(
            "Describe the expected start and end dates or overall timeline for completing "
            'the program or project .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    budget_for_program_project: str = Field(
        ...,
        description=(
            "Provide the total budget for the program or project, including major cost "
            'categories if applicable .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    benefits_to_community_client: str = Field(
        ...,
        description=(
            "Explain how the program or project will benefit the community and/or clients "
            'served .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    more_than_50_percent_low_moderate_income: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether more than half of the program/project funds will benefit low "
            "to moderate income families or individuals"
        ),
    )

    yes_low_moderate_income: BooleanLike = Field(
        default="",
        description=(
            "Select if more than 50% of the funds will benefit low to moderate income "
            "families or individuals"
        ),
    )

    no_low_moderate_income: BooleanLike = Field(
        default="",
        description=(
            "Select if 50% or less of the funds will benefit low to moderate income "
            "families or individuals"
        ),
    )

    how_success_will_be_measured: str = Field(
        ...,
        description=(
            "Describe the evaluation methods and who will be responsible for measuring the "
            'program/project\'s success .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class GrantApplication(BaseModel):
    """
    Grant Application

    ''
    """

    applicant_relationship: ApplicantRelationship = Field(..., description="Applicant Relationship")
    programproject_overview: ProgramProjectOverview = Field(
        ..., description="Program/Project Overview"
    )
    programproject_details: ProgramProjectDetails = Field(
        ..., description="Program/Project Details"
    )
