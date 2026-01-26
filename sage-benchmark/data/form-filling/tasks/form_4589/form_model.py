from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AgencyandRespondentInformation(BaseModel):
    """Basic information about the agency/county and the person completing the form"""

    name_of_agency_county: str = Field(
        ...,
        description=(
            'Full name of the agency or county .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_person_completing_form: str = Field(
        ...,
        description=(
            "Full name of the person completing this form .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    position_title: str = Field(
        ...,
        description=(
            "Job title or position of the person completing the form .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PriorREIAntiRacismInitiativesInvolvement(BaseModel):
    """County involvement in prior anti-racism and REI initiatives"""

    family_to_family_through_annie_e_casey: BooleanLike = Field(
        default="",
        description=(
            "Check if the county was involved in the Family to Family initiative through "
            "Annie E. Casey"
        ),
    )

    the_california_disproportionality_project_cdp: BooleanLike = Field(
        default="",
        description=(
            "Check if the county was involved in The California Disproportionality Project (CDP)"
        ),
    )

    capp: BooleanLike = Field(default="", description="Check if the county was involved in CAPP")

    an_initiative_to_address_racism_in_child_welfare_in_the_past: BooleanLike = Field(
        default="",
        description=(
            "Check if the county was involved in any past initiative to address racism in "
            "child welfare"
        ),
    )


class ABackgroundofPersonCompletingForm(BaseModel):
    """Background and experience of the person completing the form related to REI initiatives"""

    a1_how_long_have_you_been_with_the_agency: str = Field(
        ...,
        description=(
            "Length of time you have been employed with the agency (e.g., number of "
            'years/months) .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    a2_were_you_with_the_agency_when_or_if_they_participated_in_any_of_those_anti_racism_initiatives_listed_above_yes: BooleanLike = Field(
        ...,
        description=(
            "Select Yes if you were with the agency when it participated in any of the "
            "listed anti-racism initiatives"
        ),
    )

    a2_were_you_with_the_agency_when_or_if_they_participated_in_any_of_those_anti_racism_initiatives_listed_above_no: BooleanLike = Field(
        ...,
        description=(
            "Select No if you were not with the agency when it participated in any of the "
            "listed anti-racism initiatives"
        ),
    )

    a_are_you_familiar_with_any_of_those_anti_racism_initiatives_yes: BooleanLike = Field(
        ...,
        description="Select Yes if you are familiar with any of the listed anti-racism initiatives",
    )

    a_are_you_familiar_with_any_of_those_anti_racism_initiatives_no: BooleanLike = Field(
        ...,
        description=(
            "Select No if you are not familiar with any of the listed anti-racism initiatives"
        ),
    )

    agency_role: str = Field(
        default="",
        description=(
            "Describe your role in the agency at the time of the initiative(s) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    project_role: str = Field(
        default="",
        description=(
            "Describe your role on the anti-racism project(s) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    c_are_there_any_remaining_members_of_any_of_those_anti_racism_initiatives_that_i_could_talk_to_yes: BooleanLike = Field(
        default="",
        description=(
            "Select Yes if there are remaining members of those initiatives you can refer us to"
        ),
    )

    c_are_there_any_remaining_members_of_any_of_those_anti_racism_initiatives_that_i_could_talk_to_no: BooleanLike = Field(
        default="",
        description=(
            "Select No if there are no remaining members of those initiatives you can refer us to"
        ),
    )

    d_contact_information_for_other_person_people: str = Field(
        default="",
        description=(
            "Provide names and contact information (e.g., phone, email, role) for any other "
            'relevant person or people .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class ReiSelfassessment(BaseModel):
    """
    REI Self-Assessment

    The purpose of conducting interviews with former leaders and longstanding staff members is to situate current REI efforts in the context of the history of the agency’s approach to REI work.
    """

    agency_and_respondent_information: AgencyandRespondentInformation = Field(
        ..., description="Agency and Respondent Information"
    )
    prior_rei__anti_racism_initiatives_involvement: PriorREIAntiRacismInitiativesInvolvement = (
        Field(..., description="Prior REI / Anti-Racism Initiatives Involvement")
    )
    a_background_of_person_completing_form: ABackgroundofPersonCompletingForm = Field(
        ..., description="A. Background of Person Completing Form"
    )
