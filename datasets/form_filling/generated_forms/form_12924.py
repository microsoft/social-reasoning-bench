from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EducationalHistory(BaseModel):
    """Post-secondary and high school education details"""

    post_secondary_school_1: str = Field(
        default="",
        description=(
            "Name of the first post-secondary school attended .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    post_secondary_degree_1: str = Field(
        default="",
        description=(
            "Degree earned or pursued at the first post-secondary school .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    post_secondary_dates_1: str = Field(
        default="",
        description=(
            "Dates of attendance or completion for the first post-secondary school .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    post_secondary_school_2: str = Field(
        default="",
        description=(
            "Name of the second post-secondary school attended .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    post_secondary_degree_2: str = Field(
        default="",
        description=(
            "Degree earned or pursued at the second post-secondary school .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    post_secondary_dates_2: str = Field(
        default="",
        description=(
            "Dates of attendance or completion for the second post-secondary school .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    high_school: str = Field(
        default="",
        description=(
            'Name of the high school attended .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    high_school_graduation_date: str = Field(
        default="", description="High school graduation date"
    )  # YYYY-MM-DD format


class ClassCommitment(BaseModel):
    """Time commitment and prior application history"""

    time_commitment_prepared: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you and your employer are prepared to make the required time "
            "commitment"
        ),
    )

    applied_before: BooleanLike = Field(
        default="", description="Indicate whether you have previously applied to Tempe Leadership"
    )

    applied_before_when: str = Field(
        default="",
        description=(
            "If you have applied before, specify when (year or program cycle) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class CommunityInvolvement(BaseModel):
    """Key community and related activities"""

    community_involvement_activity_1: str = Field(
        default="",
        description=(
            "Describe your most important community, civic, professional, political, "
            "business, religious, social, athletic, or other activity, including your role, "
            "responsibilities, projects, and measures of success .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    community_involvement_activity_2: str = Field(
        default="",
        description=(
            "Describe your second most important community, civic, professional, political, "
            "business, religious, social, athletic, or other activity, including your role, "
            "responsibilities, projects, and measures of success .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    community_involvement_activity_3: str = Field(
        default="",
        description=(
            "Describe your third most important community, civic, professional, political, "
            "business, religious, social, athletic, or other activity, including your role, "
            "responsibilities, projects, and measures of success .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class EducationalHistory(BaseModel):
    """
    EDUCATIONAL HISTORY

    Tempe Leadership recognizes that involvement comes in many forms. We are interested in selecting individuals who have a commitment of time, energy and enthusiasm for their community. Please list, in order of importance to you, three community, Civic, professional, political, business, religious, social, athletic, or other activities in which you have participated. Include your contribution to each, including positions held, major responsibilities, projects under taken and YOUR measures for success.
    """

    educational_history: EducationalHistory = Field(..., description="Educational History")
    class_commitment: ClassCommitment = Field(..., description="Class Commitment")
    community_involvement: CommunityInvolvement = Field(..., description="Community Involvement")
