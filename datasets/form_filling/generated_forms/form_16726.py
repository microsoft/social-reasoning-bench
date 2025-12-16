from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ExecutiveSponsorAllyProgram(BaseModel):
    """Information about the ERG’s executive sponsor and Ally program"""

    job_title_of_current_executive_sponsor: str = Field(
        ...,
        description=(
            "Job title or role of the current executive sponsor for the ERG .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    do_you_have_an_ally_program: BooleanLike = Field(
        ..., description="Indicate whether your organization has an Ally program"
    )

    yes: BooleanLike = Field(
        default="", description="Select if the answer to having an Ally program is yes"
    )

    no: BooleanLike = Field(
        default="", description="Select if the answer to having an Ally program is no"
    )

    please_provide_some_brief_details_about_your_ally_program: str = Field(
        default="",
        description=(
            "Briefly describe the structure, purpose, and activities of your Ally program "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class ERGStructureLeadership(BaseModel):
    """How the ERG is formed and led"""

    how_is_a_new_erg_started: str = Field(
        default="",
        description=(
            "Describe the process or criteria for starting a new ERG .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_are_erg_leaders_chosen: str = Field(
        default="",
        description=(
            "Explain how ERG leaders are selected or appointed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_long_do_your_leaders_serve: str = Field(
        default="",
        description=(
            "Typical term length or duration of service for ERG leaders .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    list_any_other_details_relevant_for_understanding_how_your_erg_works: str = Field(
        default="",
        description=(
            "Provide any additional context or operational details about how your ERG "
            'functions .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class ERGSizeFundingReporting(BaseModel):
    """Scale, funding, and reporting structure of the ERG"""

    number_of_employees_in_the_erg_overall_all_chapters: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Total count of employees participating in the ERG across all chapters",
    )

    your_erg_has_existed_for: str = Field(
        default="",
        description=(
            "Length of time the ERG has been in existence (e.g., number of years) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    main_source_of_funding: str = Field(
        default="",
        description=(
            "Primary source from which the ERG receives its funding .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    your_ergs_annual_budget: str = Field(
        default="",
        description=(
            "Approximate annual budget allocated to the ERG .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    your_erg_primarily_reports_to: str = Field(
        default="",
        description=(
            "Department, leader, or function to which the ERG primarily reports .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class JobTitleOfCurrentExecutiveSponsor(BaseModel):
    """
    Job title of current executive sponsor

    ''
    """

    executive_sponsor__ally_program: ExecutiveSponsorAllyProgram = Field(
        ..., description="Executive Sponsor & Ally Program"
    )
    erg_structure__leadership: ERGStructureLeadership = Field(
        ..., description="ERG Structure & Leadership"
    )
    erg_size_funding__reporting: ERGSizeFundingReporting = Field(
        ..., description="ERG Size, Funding & Reporting"
    )
