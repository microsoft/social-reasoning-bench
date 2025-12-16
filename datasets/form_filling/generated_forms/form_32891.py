from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PartIGeneralContactInformationApplicantContactInformation(BaseModel):
    """Contact details for the person applying on behalf of the team"""

    first_and_last_name: str = Field(
        ...,
        description=(
            'Applicant\'s full first and last name .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(
        ..., description="Applicant's date of birth (must be at least 18 years old)"
    )  # YYYY-MM-DD format

    mailing_address: str = Field(
        ...,
        description=(
            "Street mailing address for the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City for the mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for the mailing address")

    zip: str = Field(..., description="ZIP or postal code for the mailing address")

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Email address for the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    us_lacrosse_membership_id_if_applicablenot_required: str = Field(
        default="",
        description=(
            "US Lacrosse membership ID number, if the applicant has one .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    relationship_to_organization_ie_program_administrator: str = Field(
        ...,
        description=(
            "Applicant's role or relationship to the team/organization .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PartIGeneralContactInformationTeamOrganizationGeneralInformation(BaseModel):
    """General information about the team or organization"""

    team_organization_name: str = Field(
        ...,
        description=(
            "Official name of the team or organization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    website_if_applicablenot_required: str = Field(
        default="",
        description=(
            "Team or organization website URL, if one exists .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    type_of_program: str = Field(
        ...,
        description=(
            "Description of the program type (e.g., school, community, club) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    gender_of_participants: str = Field(
        ...,
        description=(
            "Primary gender of the team participants (e.g., boys, girls, co-ed) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    level_of_participants: str = Field(
        ...,
        description=(
            "Competitive or age level of participants (e.g., youth, high school, beginner) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    current_number_of_participants: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total current number of players/participants in the program"
    )

    equipment_grant_package_if_awarded: str = Field(
        ...,
        description=(
            "Requested or assigned equipment grant package description .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PartIIHistoryDevelopment(BaseModel):
    """Background and history of the team"""

    why_and_in_what_year_was_the_team_established: str = Field(
        ...,
        description=(
            "Narrative explanation of the reasons for starting the team and the year it was "
            'founded .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class PartIGeneralContactInformation(BaseModel):
    """
    PART I: GENERAL CONTACT INFORMATION

    Please provide contact information for the person applying to the First Stick program on behalf of the team as well as general information about the team itself. Reminder: Applicant must be at least 18 years old.
    The US Lacrosse First Stick Program is the ESSENTIAL grassroots initiative for new and developing lacrosse teams across the country. Its purpose is to create two-year partnerships between USL and First Stick teams with the goal of creating self-sustaining programs that operate by US Lacrosse national standards and best practices.
    """

    part_i_general_contact_information___applicant_contact_information: PartIGeneralContactInformationApplicantContactInformation = Field(
        ..., description="Part I: General Contact Information - Applicant Contact Information"
    )
    part_i_general_contact_information___teamorganization_general_information: PartIGeneralContactInformationTeamOrganizationGeneralInformation = Field(
        ...,
        description="Part I: General Contact Information - Team/Organization General Information",
    )
    part_ii_history__development: PartIIHistoryDevelopment = Field(
        ..., description="Part II: History & Development"
    )
