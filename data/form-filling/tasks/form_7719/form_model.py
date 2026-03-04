from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class NominatedClubInformation(BaseModel):
    """Details about the nominated Lions or Leo club and the service project"""

    lions_club: BooleanLike = Field(..., description="Check if the nominated club is a Lions Club")

    leo_club: BooleanLike = Field(..., description="Check if the nominated club is a Leo Club")

    club_service_chairperson_leo_club_president_name: str = Field(
        ...,
        description=(
            "Full name of the club service chairperson (Lions) or Leo club president (Leo) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            "Email address of the club service chairperson or Leo club president .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    club_service_chairperson_leo_club_president_signature: str = Field(
        ...,
        description=(
            "Signature of the club service chairperson or Leo club president .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date: str = Field(
        ...,
        description=(
            "Date the nomination form is signed by the club service chairperson or Leo club "
            "president"
        ),
    )  # YYYY-MM-DD format

    lions_leo_club_name: str = Field(
        ...,
        description=(
            "Official name of the Lions or Leo club being nominated .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    lions_club_leo_number: str = Field(
        ...,
        description=(
            "Official Lions Club or Leo Club identification number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_service_project: str = Field(
        ...,
        description=(
            "Title or name of the service project being nominated .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    consent_for_public_recognition: BooleanLike = Field(
        default="",
        description=(
            "Check to grant permission for Lions Clubs International to use project "
            "information and photos for public recognition"
        ),
    )


class Endorsement(BaseModel):
    """Endorsement by the immediate past club president or advisor"""

    immediate_past_president_advisor_name_printed: str = Field(
        ...,
        description=(
            "Printed name of the immediate past Lions club president or immediate past Leo "
            'club advisor .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    member_number: str = Field(
        ...,
        description=(
            "Membership number of the immediate past president or advisor .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    immediate_past_president_advisor_signature: str = Field(
        ...,
        description=(
            "Signature of the immediate past Lions club president or immediate past Leo "
            'club advisor endorsing the nomination .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    endorsement_date: str = Field(
        ..., description="Date the endorsement is signed by the immediate past president or advisor"
    )  # YYYY-MM-DD format


class ServiceProjectDescription(BaseModel):
    """Narrative responses describing the service project"""

    q1_unique_outstanding_innovative: str = Field(
        ...,
        description=(
            "Describe what made the service project unique, outstanding, or innovative and "
            "how it met or exceeded global cause goals .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    q2_importance_in_community: str = Field(
        ...,
        description=(
            "Explain the significance and impact of this service project within your "
            'community .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    q3_local_partnerships: str = Field(
        default="",
        description=(
            "List and describe any local partners or organizations that contributed to the "
            'project .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    q4_lci_resources_used: str = Field(
        default="",
        description=(
            "Indicate whether LCI resources were used and specify which ones and how they "
            'were used .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    q5_additional_comments: str = Field(
        default="",
        description=(
            "Provide any additional information or comments relevant to the nomination .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class LionsClubsInternationalKindnessMattersServiceAwardNominationForm(BaseModel):
    """
        Lions Clubs International

    KINDNESS MATTERS SERVICE AWARD NOMINATION FORM

        A Lions or Leo club that has performed outstanding service in a global cause may be nominated for the Kindness Matters Service Award. Lions or Leo clubs that wish to be nominated must be in active status and have reported their service project on MyLion® or their regional reporting system. A minimum of two of the twenty awards will be awarded to Leo clubs. Lions and Leo club nominations should be submitted separately.
    """

    nominated_club_information: NominatedClubInformation = Field(
        ..., description="Nominated Club Information"
    )
    endorsement: Endorsement = Field(..., description="Endorsement")
    service_project_description: ServiceProjectDescription = Field(
        ..., description="Service Project Description"
    )
