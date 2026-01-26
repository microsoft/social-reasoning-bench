from typing import List, Literal, Optional, Union

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
            "List all jurisdictions where you are qualified, including SRA number and "
            "practising certificate status if qualified in the UK. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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
            "Indicate whether you currently hold a licence to practise law in any jurisdiction."
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
            "Provide your current annual salary, including currency and any fixed bonuses "
            'if relevant. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    what_is_your_salary_expectation: str = Field(
        ...,
        description=(
            "Indicate your expected annual salary for this role, including currency. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    what_is_your_current_or_most_recent_job_title: str = Field(
        ...,
        description=(
            "Provide your current or most recent professional job title. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    please_give_details_of_your_notice_period_availability: str = Field(
        ...,
        description=(
            "Explain your current notice period and when you would be available to start. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    have_you_previously_applied_to_work_for_or_been_employed_by_volterra_fietta: BooleanLike = (
        Field(
            ...,
            description=(
                "Indicate whether you have ever applied to or been employed by Volterra Fietta "
                "before."
            ),
        )
    )

    if_you_answered_yes_to_q10_above_please_give_details: str = Field(
        default="",
        description=(
            "If you have previously applied to or worked for Volterra Fietta, provide "
            "details including dates, role and outcome. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    do_you_know_anyone_or_have_professional_connections_with_vf: str = Field(
        default="",
        description=(
            "List any personal or professional connections you have with Volterra Fietta or "
            'its staff. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )
