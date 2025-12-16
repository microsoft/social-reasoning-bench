from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ADepartmentandHRKnowledge(BaseModel):
    """Pre-hiring review, concerns about inequities, future planning, and relationship building"""

    review_departments_equitable_workforce_plan: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether you have reviewed your department’s Equitable Workforce Plan "
            "before hiring."
        ),
    )

    review_industry_wide_demographics: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether you have reviewed industry-wide demographic data relevant to "
            "this position."
        ),
    )

    review_department_demographics: BooleanLike = Field(
        default="",
        description="Indicate whether you have reviewed demographic data for your department.",
    )

    review_unit_demographics: BooleanLike = Field(
        default="",
        description="Indicate whether you have reviewed demographic data for your specific unit.",
    )

    concerns_regarding_inequities_in_position: str = Field(
        default="",
        description=(
            "Describe any concerns about racial, gender, disability, or other inequities "
            'related to this position. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    how_vacancy_will_influence_future_needs: str = Field(
        default="",
        description=(
            "Explain how this vacancy will affect your agency’s future needs. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    future_job_needs_to_keep_in_mind: str = Field(
        default="",
        description=(
            "Describe any future job needs you should consider while planning for this "
            'position. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    relationship_building_with_cr_hr_and_community_leaders: str = Field(
        default="",
        description=(
            "Describe existing or planned relationship-building efforts with Civil Rights, "
            "Human Resources, and leaders from diverse communities. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class BPositionDescriptionUpdating(BaseModel):
    """Updating the position description and reviewing educational requirements"""

    date_position_description_last_updated: str = Field(
        default="", description="Enter the most recent date the position description was updated."
    )  # YYYY-MM-DD format

    ever_updated_using_equitable_hiring_tool: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether the position description has ever been updated using this "
            "Equitable Hiring tool."
        ),
    )

    date_updated_using_equitable_hiring_tool: str = Field(
        default="",
        description=(
            "If applicable, provide the date the position description was updated using "
            "this Equitable Hiring tool."
        ),
    )  # YYYY-MM-DD format

    basic_skills_for_success_in_position: str = Field(
        default="",
        description=(
            "List the core skills required for success in this position before reviewing "
            'the existing position description. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    any_minimum_education_requirements: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether there are any minimum education requirements based on the "
            "listed skills."
        ),
    )

    description_of_minimum_education_requirements: str = Field(
        default="",
        description=(
            "Describe the specific minimum education requirements, if any. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    groups_disproportionally_impacted_by_requirements: str = Field(
        default="",
        description=(
            "Identify any groups that may be disproportionately impacted by the stated "
            'education requirements. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    mitigation_of_impact_of_requirements: str = Field(
        default="",
        description=(
            "Describe the steps you will take to mitigate any disproportionate impact of "
            'the education requirements. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class EquitableHiringTool(BaseModel):
    """
    Equitable Hiring Tool

    This information can be found in your department’s equitable workforce plan. If you need further assistance understanding this data, first contact your agency’s Civil Rights Coordinator, then your assigned HR Analyst and/or the Affirmative Action Specialist.
    """

    a_department_and_hr_knowledge: ADepartmentandHRKnowledge = Field(
        ..., description="A. Department and HR Knowledge"
    )
    b_position_description_updating: BPositionDescriptionUpdating = Field(
        ..., description="B. Position Description Updating"
    )
