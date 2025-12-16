from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CollegesAttended(BaseModel):
    """List of colleges attended with years attended"""

    college_a_name: str = Field(
        default="",
        description=(
            "Name of the first college you have attended (row A) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_a_year_began: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year you began attending the first listed college (row A)"
    )

    college_a_year_ended: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year you ended attendance at the first listed college (row A)"
    )

    college_b_name: str = Field(
        default="",
        description=(
            "Name of the second college you have attended (row B) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_b_year_began: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year you began attending the second listed college (row B)"
    )

    college_b_year_ended: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year you ended attendance at the second listed college (row B)"
    )

    college_c_name: str = Field(
        default="",
        description=(
            "Name of the third college you have attended (row C) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_c_year_began: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year you began attending the third listed college (row C)"
    )

    college_c_year_ended: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year you ended attendance at the third listed college (row C)"
    )


class CommunityService(BaseModel):
    """Community service activities and dates"""

    community_service_a_description: str = Field(
        default="",
        description=(
            "Description of the first community service activity (row A) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    community_service_a_year_began: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year you began the first listed community service activity (row A)"
    )

    community_service_a_year_ended: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year you ended the first listed community service activity (row A)"
    )

    community_service_b_description: str = Field(
        default="",
        description=(
            "Description of the second community service activity (row B) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    community_service_b_year_began: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Year you began the second listed community service activity (row B)",
    )

    community_service_b_year_ended: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Year you ended the second listed community service activity (row B)",
    )

    community_service_c_description: str = Field(
        default="",
        description=(
            "Description of the third community service activity (row C) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    community_service_c_year_began: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year you began the third listed community service activity (row C)"
    )

    community_service_c_year_ended: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Year you ended the third listed community service activity (row C)"
    )


class CareerGoalsandBackground(BaseModel):
    """Brief explanation of career goals and biographical information"""

    career_goals_and_biographical_information: str = Field(
        default="",
        description=(
            "Brief explanation of your career goals and background (approximately 250 "
            'words) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class HeinleinSocietyScholarshipProgramApplication(BaseModel):
    """
    Heinlein Society Scholarship Program Application

    ''
    """

    colleges_attended: CollegesAttended = Field(..., description="Colleges Attended")
    community_service: CommunityService = Field(..., description="Community Service")
    career_goals_and_background: CareerGoalsandBackground = Field(
        ..., description="Career Goals and Background"
    )
