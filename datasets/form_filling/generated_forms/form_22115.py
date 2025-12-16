from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CurrentEmployment(BaseModel):
    """Details of the applicant's current employment"""

    employers_name_and_full_address: str = Field(
        ...,
        description=(
            "Name of your current employer and their full postal address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    job_title: str = Field(
        ...,
        description=(
            'Your current job title .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    grade: str = Field(
        default="",
        description=(
            'Grade or band of your current post .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    amount: str = Field(
        default="",
        description=(
            "Salary amount or pay for your current role .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dates_employed_from_and_to: str = Field(
        ...,
        description=(
            "Start and end dates of your current employment (from and to) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    reason_for_leaving: str = Field(
        ...,
        description=(
            "Explain why you are leaving or wish to leave your current employment .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    notice_you_need_to_give: str = Field(
        ...,
        description=(
            "Length of notice period you are required to give your current employer .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    summary_of_current_job_description: str = Field(
        ...,
        description=(
            "Brief summary of your main duties and responsibilities in your current job .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class DisclosureofRelationship(BaseModel):
    """Disclosure of any relationship with Board, Governing Body, or staff"""

    related_to_board_governing_body_or_staff: BooleanLike = Field(
        ...,
        description="Indicate whether you are related to or a partner of any listed individuals",
    )

    yes: BooleanLike = Field(
        default="", description="Select if the answer to the relationship question is yes"
    )

    no: BooleanLike = Field(
        default="", description="Select if the answer to the relationship question is no"
    )

    if_yes_please_provide_details: str = Field(
        default="",
        description=(
            "If you answered yes, provide details of the relationship .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class HowYouHeardAbouttheVacancy(BaseModel):
    """Information on how the applicant became aware of the vacancy"""

    how_did_you_become_aware_of_this_vacancy: str = Field(
        default="",
        description=(
            "Describe how you found out about this vacancy .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    media: str = Field(
        default="",
        description=(
            "Name of the publication, website, or other media source .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        default="", description="Date you saw the vacancy advertised"
    )  # YYYY-MM-DD format

    reference: str = Field(
        default="",
        description=(
            "Any reference number or code associated with the vacancy .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CurrentEmployment(BaseModel):
    """Current Employment"""

    current_employment: CurrentEmployment = Field(..., description="Current Employment")
    disclosure_of_relationship: DisclosureofRelationship = Field(
        ..., description="Disclosure of Relationship"
    )
    how_you_heard_about_the_vacancy: HowYouHeardAbouttheVacancy = Field(
        ..., description="How You Heard About the Vacancy"
    )
