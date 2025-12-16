from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class NameandContactInformation(BaseModel):
    """Basic personal and contact details for the applicant"""

    first_last_name: str = Field(
        ...,
        description=(
            'Applicant\'s full first and last name .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    birthday: str = Field(..., description="Applicant's date of birth")  # YYYY-MM-DD format

    town: str = Field(
        ...,
        description=(
            'Town where the applicant lives .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    physical_address: str = Field(
        ...,
        description=(
            'Applicant\'s physical (street) address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        default="",
        description=(
            "Applicant's mailing address, if different from physical address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    phones: str = Field(
        ...,
        description=(
            "Primary phone number(s) for contacting the applicant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    emails: str = Field(
        ...,
        description=(
            "Email address(es) for contacting the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class HowDoYouIdentifyYourself(BaseModel):
    """Information about the applicant’s relationship to developmental disability"""

    has_developmental_disability: BooleanLike = Field(
        default="", description="Check if the applicant personally has a developmental disability"
    )

    is_parent_of_person_with_developmental_disability: BooleanLike = Field(
        default="",
        description="Check if the applicant is a parent of a person with a developmental disability",
    )

    is_sibling_of_person_with_developmental_disability: BooleanLike = Field(
        default="",
        description="Check if the applicant is a sibling of a person with a developmental disability",
    )

    is_child_of_person_with_developmental_disability: BooleanLike = Field(
        default="",
        description="Check if the applicant is a child of a person with a developmental disability",
    )

    other_relationship: str = Field(
        default="",
        description=(
            "Describe another way the applicant is connected to a person with a "
            'developmental disability .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    disability_description: str = Field(
        ...,
        description=(
            "Brief description of the applicant's or family member's disability .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class BackgroundCheckandMemberApplicationAgreement(BaseModel):
    """Authorization and certification for background check and application"""

    signature: str = Field(
        ...,
        description=(
            "Applicant's signature authorizing background check and certifying the "
            'information .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    signature_date: str = Field(
        ..., description="Date the applicant signed the application agreement"
    )  # YYYY-MM-DD format


class VermontDevelopmentalDisabilitiesCouncilCitizenMembersApplication(BaseModel):
    """
        VERMONT DEVELOPMENTAL DISABILITIES COUNCIL
    Citizen Members Application

        Need more space to respond? You may use the back of this application or attach extra paper.
        Applications are reviewed by VTDDC members. You may be asked for more information and invited to an interview. Members vote on finalists to recommend to the Governor, who appoints members. Finalists may need to complete an additional form as part of the Governor’s appointment process.
    """

    name_and_contact_information: NameandContactInformation = Field(
        ..., description="Name and Contact Information"
    )
    how_do_you_identify_yourself: HowDoYouIdentifyYourself = Field(
        ..., description="How Do You Identify Yourself?"
    )
    background_check_and_member_application_agreement: BackgroundCheckandMemberApplicationAgreement = Field(
        ..., description="Background Check and Member Application Agreement"
    )
