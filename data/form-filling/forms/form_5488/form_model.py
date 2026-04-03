from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AssociateApplicationForm(BaseModel):
    """
    ASSOCIATE APPLICATION FORM

    Please complete and submit this form, along with a covering letter, CV and transcripts to applications@volterrafietta.com.
    """

    are_you_a_qualified_lawyer: BooleanLike = Field(
        ..., description="Indicate whether you are currently a qualified lawyer."
    )

    in_which_jurisdictions_are_you_qualified: str = Field(
        ...,
        description=(
            "List all jurisdictions in which you are qualified to practice law. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    please_provide_your_qualifications_date: str = Field(
        ...,
        description=(
            "Provide the date or dates on which you obtained your legal qualification(s). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    are_you_licensed_to_practice_law_in_one_or_more_jurisdictions: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you currently hold a licence to practice law in any jurisdiction."
        ),
    )

    if_qualified_in_the_uk_please_provide_your_sra_number: str = Field(
        default="",
        description=(
            "If you are UK-qualified, enter your Solicitors Regulation Authority (SRA) "
            'number. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    if_qualified_in_the_uk_indicate_whether_you_hold_a_current_practising_certificate: BooleanLike = Field(
        default="",
        description=(
            "If you are UK-qualified, indicate whether you currently hold a valid "
            "practising certificate."
        ),
    )

    who_is_your_current_or_most_recent_employer: str = Field(
        ...,
        description=(
            "State the name of your current or most recent employer. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    what_is_your_current_salary: str = Field(
        ...,
        description=(
            "Provide your current annual salary, including currency and any fixed "
            'components. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    what_is_your_salary_expectation: str = Field(
        ...,
        description=(
            "State your expected annual salary for this role, including currency. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    what_is_your_current_or_most_recent_job_title: str = Field(
        ...,
        description=(
            "Provide your current or most recent official job title. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    please_give_details_of_your_notice_period_availability: str = Field(
        ...,
        description=(
            "Explain your notice period and when you would be available to start. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    have_you_previously_applied_to_work_for_or_been_employed_by_volterra_fietta: BooleanLike = Field(
        ...,
        description="Indicate whether you have ever applied to or worked for Volterra Fietta before.",
    )

    if_yes_to_q10_please_give_details: str = Field(
        default="",
        description=(
            "If you have previously applied to or worked for Volterra Fietta, provide "
            "details including dates, roles, and outcomes. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    do_you_know_anyone_or_have_professional_connections_with_vf: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether you have any personal or professional connections with "
            "Volterra Fietta or its staff."
        ),
    )
