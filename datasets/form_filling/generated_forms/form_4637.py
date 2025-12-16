from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class JobInterest(BaseModel):
    """Information about prior applications/employment, job interests, availability, referrals, and relatives employed by TDRPD"""

    employed_by_district_yes: BooleanLike = Field(
        ...,
        description=(
            "Check yes if you have ever been employed by a Division of this Recreation and "
            "Park District."
        ),
    )

    employed_by_district_no: BooleanLike = Field(
        ...,
        description=(
            "Check no if you have never been employed by a Division of this Recreation and "
            "Park District."
        ),
    )

    prior_employment_with_district_when: str = Field(
        default="",
        description=(
            "If you answered yes to prior employment with the District, indicate when you "
            'were employed. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    applied_before_tdrpd_yes: BooleanLike = Field(
        ..., description="Check yes if you have previously applied to work for TDRPD."
    )

    applied_before_tdrpd_no: BooleanLike = Field(
        ..., description="Check no if you have never applied to work for TDRPD before."
    )

    prior_application_tdrpd_when: str = Field(
        default="",
        description=(
            "If you answered yes to having applied before, indicate when you previously "
            'applied. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    types_of_work_interested_in: str = Field(
        ...,
        description=(
            "List the types of work or positions you are interested in. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    starting_wage_expected: str = Field(
        ...,
        description=(
            "Indicate the starting wage or pay rate you expect. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    availability_to_work: str = Field(
        ...,
        description=(
            "Describe when you would be available to work (start date, days, times). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    unavailable_times_to_work: str = Field(
        default="",
        description=(
            "List any days or times when you are not available to work. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_were_you_referred: str = Field(
        default="",
        description=(
            "Explain how you learned about this job or who referred you. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    referral_source_name: str = Field(
        default="",
        description=(
            "If referred by a newspaper, agency, or website, provide its name. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    relatives_or_acquaintances_employed: str = Field(
        default="",
        description=(
            "List any relatives or acquaintances employed by TDRPD, including their names "
            'and positions. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class DataandApplicantCertification(BaseModel):
    """Ability to perform essential job functions, applicant acknowledgments, and signature"""

    can_perform_essential_functions_yes: BooleanLike = Field(
        ...,
        description=(
            "Check yes if you would be able to perform the essential job functions, with or "
            "without reasonable accommodation."
        ),
    )

    can_perform_essential_functions_no: BooleanLike = Field(
        ...,
        description=(
            "Check no if you would not be able to perform the essential job functions, even "
            "with reasonable accommodation."
        ),
    )

    initial_certify_information_true: str = Field(
        ...,
        description=(
            "Applicant initials acknowledging the certification that information provided "
            'is complete and accurate. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    initial_authorize_investigation: str = Field(
        ...,
        description=(
            "Applicant initials authorizing the District to investigate references, work "
            "record, education, and related information. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    initial_understand_no_contract: str = Field(
        ...,
        description=(
            "Applicant initials acknowledging understanding that the application and any "
            "interview do not create an employment contract. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    initial_agree_to_policies: str = Field(
        ...,
        description=(
            "Applicant initials agreeing to abide by all current and future TDRPD policies. "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    initial_understand_accommodation_and_exams: str = Field(
        ...,
        description=(
            "Applicant initials acknowledging understanding of reasonable accommodation "
            "measures and possible medical or skills examinations. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    application_date: str = Field(
        ..., description="Date the application and acknowledgments are signed."
    )  # YYYY-MM-DD format

    applicants_signature: str = Field(
        ...,
        description=(
            "Applicant’s handwritten or electronic signature. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class JobInterest(BaseModel):
    """
    JOB INTEREST

    ''
    """

    job_interest: JobInterest = Field(..., description="Job Interest")
    data_and_applicant_certification: DataandApplicantCertification = Field(
        ..., description="Data and Applicant Certification"
    )
