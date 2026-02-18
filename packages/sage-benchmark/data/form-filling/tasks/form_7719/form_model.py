from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class NominatedClub(BaseModel):
    """Information about the nominated Lions or Leo club and its service project"""

    type_of_club_this_nomination_is_for_lions_club: BooleanLike = Field(
        ..., description="Select if this nomination is for a Lions Club."
    )

    type_of_club_this_nomination_is_for_leo_club: BooleanLike = Field(
        ..., description="Select if this nomination is for a Leo Club."
    )

    club_service_chairperson_leo_club_president_name: str = Field(
        ...,
        description=(
            "Full name of the club service chairperson (Lions) or Leo club president (Leo). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Email address of the club service chairperson or Leo club president. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(
        ...,
        description=(
            "Date the nomination form is completed by the club service chairperson or Leo "
            "club president."
        ),
    )  # YYYY-MM-DD format

    club_service_chairperson_leo_club_president_signature: str = Field(
        ...,
        description=(
            "Signature of the club service chairperson or Leo club president confirming the "
            'nomination. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    lions_leo_club_name: str = Field(
        ...,
        description=(
            "Official name of the Lions or Leo club being nominated. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    lions_club_leo_number: str = Field(
        ...,
        description=(
            "Official Lions Club or Leo Club identification number. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_service_project: str = Field(
        ...,
        description=(
            "Title or name of the service project being nominated. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    consent_for_use_of_information_and_photographs: BooleanLike = Field(
        default="",
        description=(
            "Indicate consent for Lions Clubs International to use the provided information "
            "and photos for public recognition."
        ),
    )


class EndorsedBy(BaseModel):
    """Endorsement details from the immediate past club president or advisor"""

    immediate_past_president_or_advisor_name_printed: str = Field(
        ...,
        description=(
            "Printed name of the immediate past Lions club president or immediate past Leo "
            "club advisor endorsing the nomination. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    member_number: str = Field(
        ...,
        description=(
            "Membership number of the immediate past Lions club president or Leo club "
            'advisor. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    immediate_past_president_or_advisor_signature: str = Field(
        ...,
        description=(
            "Signature of the immediate past Lions club president or immediate past Leo "
            "club advisor endorsing the nomination. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    endorsement_date: str = Field(
        ...,
        description="Date the endorsement by the immediate past president or advisor is signed.",
    )  # YYYY-MM-DD format


class ServiceProjectDescription(BaseModel):
    """Narrative description and details about the service project"""

    q1_unique_outstanding_innovative_aspects: str = Field(
        ...,
        description=(
            "Describe what made the service project unique, outstanding, or innovative and "
            "how it met or surpassed global cause goals. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    q2_importance_in_community: str = Field(
        ...,
        description=(
            "Explain the significance and impact of this service project within your "
            'community. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    q3_local_partnerships: str = Field(
        default="",
        description=(
            "List and describe any local partners or organizations that contributed to the "
            'project. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    q4_lci_resources_used: str = Field(
        default="",
        description=(
            "Indicate whether LCI resources were used and describe how they supported "
            'planning or execution. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    q5_additional_comments: str = Field(
        default="",
        description=(
            "Provide any additional information or comments about the service project or "
            'nomination. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class LionsClubsInternationalKindnessMattersServiceAwardNominationForm(BaseModel):
    """
        Lions Clubs International

    KINDNESS MATTERS SERVICE AWARD NOMINATION FORM

        A Lions or Leo club that has performed outstanding service in a global cause may be nominated for the Kindness Matters Service Award. Lions or Leo clubs that wish to be nominated must be in active status and have reported their service project on MyLion® or their regional reporting system. A minimum of two of the twenty awards will be awarded to Leo clubs. Lions and Leo club nominations should be submitted separately.
    """

    nominated_club: NominatedClub = Field(..., description="Nominated Club")
    endorsed_by: EndorsedBy = Field(..., description="Endorsed By")
    service_project_description: ServiceProjectDescription = Field(
        ..., description="Service Project Description"
    )
