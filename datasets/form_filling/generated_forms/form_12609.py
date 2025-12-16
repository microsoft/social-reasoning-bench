from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ProposedProjectInformation(BaseModel):
    """Basic information and description of the proposed project"""

    proposed_project: str = Field(
        ...,
        description=(
            'Name or title of the proposed project .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    description_of_proposed_project: str = Field(
        ...,
        description=(
            "Brief description of the proposed project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location: str = Field(
        ...,
        description=(
            'Location of the proposed project .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ProjectTeam(BaseModel):
    """Applicant and project team contact details"""

    applicant_name: str = Field(
        ...,
        description=(
            'Full name of the primary applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    applicant_address: str = Field(
        ...,
        description=(
            'Mailing address of the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    telephone_number: str = Field(
        ...,
        description=(
            "Primary contact telephone number for the applicant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            "Primary email address for the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    please_list_the_members_of_your_team_expected_to_accompany_you: str = Field(
        default="",
        description=(
            "Names and roles of team members expected to attend the meeting .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ProjectBackgroundQuestions(BaseModel):
    """Yes/No questions about project status and prior work with the Town"""

    do_you_have_a_concept_plan_yes: BooleanLike = Field(
        default="", description="Select yes if you currently have a concept plan for the project"
    )

    do_you_have_a_concept_plan_no: BooleanLike = Field(
        default="",
        description="Select no if you do not currently have a concept plan for the project",
    )

    is_the_property_currently_owned_by_your_party_yes: BooleanLike = Field(
        default="", description="Select yes if your party currently owns the property"
    )

    is_the_property_currently_owned_by_your_party_no: BooleanLike = Field(
        default="", description="Select no if your party does not currently own the property"
    )

    have_you_worked_with_town_of_little_elm_before_yes: BooleanLike = Field(
        default="",
        description="Select yes if you have previously worked with the Town of Little Elm",
    )

    have_you_worked_with_town_of_little_elm_before_no: BooleanLike = Field(
        default="",
        description="Select no if you have not previously worked with the Town of Little Elm",
    )


class TownOfLittleElmProjectassessment(BaseModel):
    """
    Town of Little Elm Project-Assessment

    Please fill out this Project-Assessment submit it to Development Services to better facilitate the Pre-Application Meeting. **Please complete this page to the best of your ability.**
    """

    proposed_project_information: ProposedProjectInformation = Field(
        ..., description="Proposed Project Information"
    )
    project_team: ProjectTeam = Field(..., description="Project Team")
    project_background_questions: ProjectBackgroundQuestions = Field(
        ..., description="Project Background Questions"
    )
