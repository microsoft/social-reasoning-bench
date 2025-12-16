from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class REALTORAssociationMembership(BaseModel):
    """Current and previous Association of REALTORS memberships"""

    presently_member_other_association_yes: BooleanLike = Field(
        ...,
        description="Indicate Yes if you are currently a member of any other Association of REALTORS",
    )

    presently_member_other_association_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate No if you are not currently a member of any other Association of REALTORS"
        ),
    )

    present_member_other_association_names: str = Field(
        default="",
        description=(
            "List the names of any other Associations of REALTORS where you presently hold "
            'membership .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    previously_held_membership_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate Yes if you have ever previously held membership in any other "
            "Association of REALTORS"
        ),
    )

    previously_held_membership_no: BooleanLike = Field(
        ...,
        description=(
            "Indicate No if you have never previously held membership in any other "
            "Association of REALTORS"
        ),
    )

    previous_membership_association_names: str = Field(
        default="",
        description=(
            "List the names of any Associations of REALTORS where you previously held "
            'membership .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class CommitteeInterests(BaseModel):
    """Interest in serving on NHMR committees"""

    scholarship_committee: BooleanLike = Field(
        default="",
        description="Check if you are interested in serving on the Scholarship Committee",
    )

    political_fundraising_committee: BooleanLike = Field(
        default="",
        description="Check if you are interested in serving on the Political Fundraising Committee",
    )

    legislative_political_affairs_committee: BooleanLike = Field(
        default="",
        description=(
            "Check if you are interested in serving on the Legislative/Political Affairs Committee"
        ),
    )

    orientation_committee: BooleanLike = Field(
        default="",
        description="Check if you are interested in serving on the Orientation Committee",
    )

    community_relations_committee: BooleanLike = Field(
        default="",
        description="Check if you are interested in serving on the Community Relations Committee",
    )

    awards_committee: BooleanLike = Field(
        default="", description="Check if you are interested in serving on the Awards Committee"
    )

    your_professional_network_committee: BooleanLike = Field(
        default="",
        description=(
            "Check if you are interested in serving on the Your Professional Network Committee"
        ),
    )


class SpeakingLanguageInformation(BaseModel):
    """Languages spoken and speaking engagement availability"""

    other_languages_spoken: str = Field(
        default="",
        description=(
            'List any other languages you speak .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    available_for_speaking_engagements_yes: BooleanLike = Field(
        default="", description="Indicate Yes if you are available for speaking engagements"
    )

    available_for_speaking_engagements_no: BooleanLike = Field(
        default="", description="Indicate No if you are not available for speaking engagements"
    )

    areas_of_expertise_line_1: str = Field(
        default="",
        description=(
            "First line to describe your areas of expertise for speaking engagements .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    areas_of_expertise_line_2: str = Field(
        default="",
        description=(
            "Second line to describe your areas of expertise for speaking engagements .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    areas_of_expertise_line_3: str = Field(
        default="",
        description=(
            "Third line to describe your areas of expertise for speaking engagements .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Authorization(BaseModel):
    """Signature and date of application"""

    dated: str = Field(..., description="Date the application is signed")  # YYYY-MM-DD format

    signature: str = Field(
        ...,
        description=(
            'Applicant\'s signature .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class NHMiddlesexRealtors2021AffiliateSponsorApp(BaseModel):
    """New Haven Middlesex Association of REALTORS
    2021 Affiliate/Sponsor Application"""

    realtor_association_membership: REALTORAssociationMembership = Field(
        ..., description="REALTOR Association Membership"
    )
    committee_interests: CommitteeInterests = Field(..., description="Committee Interests")
    speaking__language_information: SpeakingLanguageInformation = Field(
        ..., description="Speaking & Language Information"
    )
    authorization: Authorization = Field(..., description="Authorization")
