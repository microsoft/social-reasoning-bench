from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class SubmitterInformation(BaseModel):
    """Contact details for the person submitting the issue"""

    name: str = Field(
        ...,
        description=(
            "Full name of the person submitting the issue .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    company: str = Field(
        ...,
        description=(
            'Name of your company or organization .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Mailing or business address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    tel: str = Field(
        ...,
        description=(
            'Primary telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Email address for follow-up .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    are_you_a_current_atia_member_yes: BooleanLike = Field(
        ..., description="Indicate YES if you are currently an ATIA member"
    )

    are_you_a_current_atia_member_no: BooleanLike = Field(
        ..., description="Indicate NO if you are not currently an ATIA member"
    )

    if_not_a_current_member_please_provide_the_name_of_an_atia_member_who_is_willing_to_help_carry_this_issue_forward_on_your_behalf: str = Field(
        default="",
        description=(
            "Name of an ATIA member who will help carry this issue forward on your behalf "
            'if you are not a current member .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class IssueDetails(BaseModel):
    """Information describing the issue being submitted"""

    short_title_of_issue_topic_legislation: str = Field(
        ...,
        description=(
            "Concise title or name of the issue, topic, or legislation .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    brief_description: str = Field(
        ...,
        description=(
            'Brief summary describing the issue .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    scope_of_issue_local_to_community_or_region: BooleanLike = Field(
        ..., description="Check if the scope of the issue is local to a community or region"
    )

    scope_of_issue_statewide: BooleanLike = Field(
        ..., description="Check if the scope of the issue is statewide"
    )

    scope_of_issue_federal_or_international: BooleanLike = Field(
        ..., description="Check if the scope of the issue is federal or international"
    )

    please_list_known_supporters: str = Field(
        default="",
        description=(
            "List individuals, organizations, or entities known to support this issue .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    please_list_known_opposition: str = Field(
        default="",
        description=(
            "List individuals, organizations, or entities known to oppose this issue .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    please_describe_any_fiscal_or_legal_impact: str = Field(
        default="",
        description=(
            "Describe any financial or legal impacts related to this issue .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class RequestedATIAAction(BaseModel):
    """What action the submitter is asking ATIA to take"""

    support: BooleanLike = Field(
        ..., description="Select if you are proposing that ATIA support this issue"
    )

    opposition: BooleanLike = Field(
        ..., description="Select if you are proposing that ATIA oppose this issue"
    )

    no_action_at_this_time_informative_only: BooleanLike = Field(
        ...,
        description="Select if you are not requesting action and are providing information only",
    )


class AlaskaTravelIndustryAssociationIssueSubmissionForm(BaseModel):
    """
        ALASKA TRAVEL INDUSTRY ASSOCIATION

    Issue Submission Form

        Please fill out the attached form and return with supporting documentation to jjessen@AlaskaTIA.org. All issues will be brought forth to ATIA's Tourism Policy & Planning Committee for consideration.
    """

    submitter_information: SubmitterInformation = Field(..., description="Submitter Information")
    issue_details: IssueDetails = Field(..., description="Issue Details")
    requested_atia_action: RequestedATIAAction = Field(..., description="Requested ATIA Action")
