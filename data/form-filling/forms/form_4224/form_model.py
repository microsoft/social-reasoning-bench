from typing import Literal, Optional, List, Union
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

    physical_address_line_1: str = Field(
        ...,
        description=(
            "First line of the applicant's physical (street) address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    physical_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the applicant's physical (street) address, if needed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mailing_address_line_1: str = Field(
        default="",
        description=(
            "First line of the applicant's mailing address, if different from physical "
            'address .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    mailing_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the applicant's mailing address, if needed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phones_line_1: str = Field(
        ...,
        description=(
            'Primary phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    phones_line_2: str = Field(
        default="",
        description=(
            'Additional phone number, if any .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    emails_line_1: str = Field(
        ...,
        description=(
            'Primary email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    emails_line_2: str = Field(
        default="",
        description=(
            'Additional email address, if any .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class HowDoYouIdentifyYourself(BaseModel):
    """Information about the applicant’s relationship to developmental disability"""

    i_have_a_developmental_disability: BooleanLike = Field(
        default="", description="Check if the applicant personally has a developmental disability"
    )

    i_am_a_parent_of_a_person_with_a_developmental_disability: BooleanLike = Field(
        default="",
        description="Check if the applicant is a parent of a person with a developmental disability",
    )

    i_am_a_sibling_of_a_person_with_a_developmental_disability: BooleanLike = Field(
        default="",
        description="Check if the applicant is a sibling of a person with a developmental disability",
    )

    i_am_a_child_of_a_person_with_a_developmental_disability: BooleanLike = Field(
        default="",
        description="Check if the applicant is a child of a person with a developmental disability",
    )

    other_relationship_to_a_person_with_a_developmental_disability: str = Field(
        default="",
        description=(
            "Describe any other relationship to a person with a developmental disability "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    description_of_my_his_her_disability_line_1: str = Field(
        default="",
        description=(
            "First line of description of the disability .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    description_of_my_his_her_disability_line_2: str = Field(
        default="",
        description=(
            "Second line of description of the disability .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class BackgroundCheckandMemberApplicationAgreement(BaseModel):
    """Authorization and certification related to background check and application"""

    signature: str = Field(
        ...,
        description=(
            "Applicant's signature authorizing background check and certifying the "
            'information .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the application is signed")  # YYYY-MM-DD format


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
