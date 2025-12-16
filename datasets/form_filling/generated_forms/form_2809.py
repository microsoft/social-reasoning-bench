from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantDetails(BaseModel):
    """Basic information about the applicant and their organisation (if applicable)"""

    name: str = Field(
        ...,
        description=(
            'Full name of the applicant .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    position: str = Field(
        default="",
        description=(
            "Your job title or role within the organisation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    organisation: str = Field(
        default="",
        description=(
            "Name of your organisation (leave blank if joining as an individual) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Postal address for correspondence .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    postcode: str = Field(..., description="Postcode for your address")

    tel: str = Field(
        ...,
        description=(
            'Main contact telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        ...,
        description=(
            "Primary email address for membership communications .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    website: str = Field(
        default="",
        description=(
            'Organisation or personal website URL .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class MembershipDetails(BaseModel):
    """Information about the type of membership and organisational income"""

    membership_category: str = Field(
        ...,
        description=(
            "Type of membership you are applying for .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    annual_income_bracket_under_250000: BooleanLike = Field(
        default="",
        description=(
            "Select if your annual income is under 250,000 (organisations & statutory bodies only)"
        ),
    )

    annual_income_bracket_250000_to_1m: BooleanLike = Field(
        default="",
        description=(
            "Select if your annual income is between 250,000 and 1M (organisations & "
            "statutory bodies only)"
        ),
    )

    annual_income_bracket_1m_to_2m: BooleanLike = Field(
        default="",
        description=(
            "Select if your annual income is between 1M and 2M (organisations & statutory "
            "bodies only)"
        ),
    )

    annual_income_bracket_over_2m: BooleanLike = Field(
        default="",
        description="Select if your annual income is over 2M (organisations & statutory bodies only)",
    )

    description_of_your_organisation_or_if_an_individual_your_interests_why_you_have_joined: str = (
        Field(
            default="",
            description=(
                "Brief description of your organisation or, if an individual, your interests "
                'and reasons for joining .If you cannot fill this, write "N/A". If this field '
                "should not be filled by you (for example, it belongs to another person or "
                'office), leave it blank (empty string "").'
            ),
        )
    )

    where_did_you_hear_about_children_in_scotland: str = Field(
        default="",
        description=(
            "How you found out about Children in Scotland .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CommunicationsPreferences(BaseModel):
    """Consent to receive information about other Children in Scotland activities"""

    i_would_like_to_receive_information_about_other_children_in_scotland_projects_events_and_resources: BooleanLike = Field(
        default="",
        description=(
            "Tick to consent to receive information about other Children in Scotland "
            "projects, events, and resources"
        ),
    )


class Authorisation(BaseModel):
    """Signature and date confirming the application"""

    signature: str = Field(
        ...,
        description=(
            "Signature of the applicant confirming the information and agreement .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(..., description="Date the form is signed")  # YYYY-MM-DD format


class ChildrenInScotlandMembershipApplicationForm202122(BaseModel):
    """
        Children in Scotland

    Membership Application Form 2021/22

        ''
    """

    applicant_details: ApplicantDetails = Field(..., description="Applicant Details")
    membership_details: MembershipDetails = Field(..., description="Membership Details")
    communications_preferences: CommunicationsPreferences = Field(
        ..., description="Communications Preferences"
    )
    authorisation: Authorisation = Field(..., description="Authorisation")
