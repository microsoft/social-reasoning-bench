from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AwardLevel(BaseModel):
    """Selected level of the Venturing Leadership Award"""

    council_level: BooleanLike = Field(
        ...,
        description="Check if the nomination is for the Council-level Venturing Leadership Award",
    )

    area_level: BooleanLike = Field(
        ..., description="Check if the nomination is for the Area-level Venturing Leadership Award"
    )

    region_level: BooleanLike = Field(
        ...,
        description="Check if the nomination is for the Region-level Venturing Leadership Award",
    )

    national_level: BooleanLike = Field(
        ...,
        description="Check if the nomination is for the National-level Venturing Leadership Award",
    )


class CandidateInformation(BaseModel):
    """Basic information about the candidate and their council/area/region"""

    region: str = Field(
        ...,
        description=(
            'Region of the candidate\'s council .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    area: str = Field(
        ...,
        description=(
            'Area of the candidate\'s council .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    council_name: str = Field(
        ...,
        description=(
            'Full name of the council .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    council_no: str = Field(
        ...,
        description=(
            'Council number .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    name: str = Field(
        ...,
        description=(
            'Full name of the candidate .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    youth: BooleanLike = Field(..., description="Check if the candidate is a youth member")

    adult: BooleanLike = Field(..., description="Check if the candidate is an adult member")

    street: str = Field(
        ...,
        description=(
            'Street address of the candidate .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip_code: str = Field(
        ...,
        description=(
            "City, state, and ZIP code of the candidate .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_no: str = Field(
        ...,
        description=(
            "Primary phone number for the candidate .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Email address of the candidate .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    crew_ship_no: str = Field(
        ...,
        description=(
            "Number of the Venturing crew or Sea Scout ship .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    tenure_in_years_as_a_venturer: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of years the candidate has been a Venturer"
    )

    current_venturing_position_of_responsibility: str = Field(
        ...,
        description=(
            "Current leadership or responsibility position held in Venturing .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    chartered_organization: str = Field(
        ...,
        description=(
            "Name of the chartered organization for the crew or ship .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    school_name_and_grade_level: str = Field(
        default="",
        description=(
            "Current school name and grade level of the candidate .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LeadershipandPositions(BaseModel):
    """Venturing positions and leadership roles on which the recommendation is based"""

    venturing_positions_recommendation_is_based_on: str = Field(
        ...,
        description=(
            "List the Venturing positions that form the basis for this recommendation .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    list_leadership_positions_held_related_to_this_award_level_and_explain_how_these_roles_relate_to_this_level_of_award: str = Field(
        ...,
        description=(
            "Describe leadership positions held that relate to this award level and explain "
            'their relevance .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class RecommendationForTheVenturingLeadershipAward(BaseModel):
    """
        Recommendation for the
    Venturing Leadership Award

        ''
    """

    award_level: AwardLevel = Field(..., description="Award Level")
    candidate_information: CandidateInformation = Field(..., description="Candidate Information")
    leadership_and_positions: LeadershipandPositions = Field(
        ..., description="Leadership and Positions"
    )
