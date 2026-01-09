from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RequestInformation(BaseModel):
    """Requester details and basic information about the exclusion zone request"""

    requested_by: str = Field(
        ...,
        description=(
            "Name of the person submitting the request .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this request is submitted")  # YYYY-MM-DD format

    division: str = Field(
        ...,
        description=(
            "Division within the university making the request .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    department: str = Field(
        ...,
        description=(
            "Department within the division making the request .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    request_type_establish: BooleanLike = Field(
        default="",
        description="Check if the request is to establish a new campus carry exclusion zone",
    )

    request_type_eliminate: BooleanLike = Field(
        default="",
        description="Check if the request is to eliminate an existing campus carry exclusion zone",
    )

    request_type_modify: BooleanLike = Field(
        default="",
        description="Check if the request is to modify an existing campus carry exclusion zone",
    )

    request_term_permanent: BooleanLike = Field(
        default="", description="Check if the exclusion zone is requested as permanent"
    )

    request_term_temporary: BooleanLike = Field(
        default="", description="Check if the exclusion zone is requested as temporary"
    )

    request_term_temporary_date_and_time_needed: str = Field(
        default="",
        description=(
            "Specify the date and time period for the temporary exclusion zone .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    exact_zone_to_be_established_modified_or_eliminated: str = Field(
        ...,
        description=(
            "Describe the precise area or location of the exclusion zone to be established, "
            'modified, or eliminated .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    rationale_for_the_request: str = Field(
        ...,
        description=(
            "Explain the justification for the requested exclusion zone, referring to MAPP "
            '07.01.05 criteria .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    plan_for_where_signs_are_to_be_placed: str = Field(
        ...,
        description=(
            "Describe where campus carry exclusion zone signs should be placed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class CampusSafetyCommitteeRecommendation(BaseModel):
    """Review and recommendation by the Campus Safety Committee"""

    campus_safety_committee_recommendation_approve: BooleanLike = Field(
        default="", description="Indicate if the Campus Safety Committee recommends approval"
    )

    campus_safety_committee_recommendation_disapprove: BooleanLike = Field(
        default="", description="Indicate if the Campus Safety Committee recommends disapproval"
    )

    campus_safety_committee_recommendation_date: str = Field(
        default="", description="Date of the Campus Safety Committee recommendation"
    )  # YYYY-MM-DD format

    campus_safety_committee_recommendation_comments: str = Field(
        default="",
        description=(
            "Additional comments from the Campus Safety Committee .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CampusCarryExclusionZoneApplication(BaseModel):
    """
        UNIVERSITY of HOUSTON

    Application to Establish, Modify or Eliminate a Campus Carry Exclusion Zone

        ''
    """

    request_information: RequestInformation = Field(..., description="Request Information")
    campus_safety_committee_recommendation: CampusSafetyCommitteeRecommendation = Field(
        ..., description="Campus Safety Committee Recommendation"
    )
