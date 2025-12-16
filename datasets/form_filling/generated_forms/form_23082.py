from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class WorkExperienceEmployer1(BaseModel):
    """Details for most recent or current employer"""

    employer_name: str = Field(
        ...,
        description=(
            "Name of your present or previous employer (most recent first) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    employer_address: str = Field(
        ...,
        description=(
            "Street address, city, state, and zip code of the employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    employer_type_of_business: str = Field(
        ...,
        description=(
            "Type of business or industry of the employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    employer_telephone_area_code: str = Field(
        ...,
        description=(
            "Area code for the employer’s telephone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    employer_telephone_number: str = Field(
        ...,
        description=(
            "Employer’s main telephone number (excluding area code) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    dates_employed_from_employer_1: str = Field(
        ..., description="Start date of your employment with this employer"
    )  # YYYY-MM-DD format

    dates_employed_to_employer_1: str = Field(
        ..., description="End date of your employment with this employer"
    )  # YYYY-MM-DD format

    job_title_employer_1: str = Field(
        ...,
        description=(
            'Your job title with this employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    duties_employer_1: str = Field(
        ...,
        description=(
            "Brief description of your primary duties for this employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    supervisors_name_employer_1: str = Field(
        ...,
        description=(
            "Name of your immediate supervisor at this employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    may_we_contact_yes_employer_1: BooleanLike = Field(
        ..., description="Indicate Yes if the employer may be contacted for a reference"
    )

    may_we_contact_no_employer_1: BooleanLike = Field(
        ..., description="Indicate No if the employer may not be contacted for a reference"
    )

    if_no_why_not_employer_1: str = Field(
        default="",
        description=(
            "Reason why this employer should not be contacted (if you selected No) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reason_for_leaving_employer_1: str = Field(
        ...,
        description=(
            'Primary reason you left this employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    employer_say_reason_terminated_employer_1: str = Field(
        ...,
        description=(
            "How you believe the employer would describe the reason your employment ended "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    were_you_ever_disciplined_employer_1: str = Field(
        default="",
        description=(
            "Indicate whether you were ever disciplined by this employer and explain the "
            'reason .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    notice_given_when_resigning_employer_1: str = Field(
        default="",
        description=(
            "Amount of notice you provided when resigning and explanation if no notice was "
            'given .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class WorkExperienceEmployer2(BaseModel):
    """Details for previous employer"""

    employer_name_2: str = Field(
        default="",
        description=(
            "Name of your next most recent employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    employer_address_2: str = Field(
        default="",
        description=(
            "Street address, city, state, and zip code of this employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    employer_type_of_business_2: str = Field(
        default="",
        description=(
            "Type of business or industry of this employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    employer_telephone_area_code_2: str = Field(
        default="",
        description=(
            "Area code for this employer’s telephone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    employer_telephone_number_2: str = Field(
        default="",
        description=(
            "This employer’s main telephone number (excluding area code) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    dates_employed_from_employer_2: str = Field(
        default="", description="Start date of your employment with this employer"
    )  # YYYY-MM-DD format

    dates_employed_to_employer_2: str = Field(
        default="", description="End date of your employment with this employer"
    )  # YYYY-MM-DD format

    job_title_employer_2: str = Field(
        default="",
        description=(
            'Your job title with this employer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    duties_employer_2: str = Field(
        default="",
        description=(
            "Brief description of your primary duties for this employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    supervisors_name_employer_2: str = Field(
        default="",
        description=(
            "Name of your immediate supervisor at this employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    may_we_contact_yes_employer_2: BooleanLike = Field(
        default="", description="Indicate Yes if this employer may be contacted for a reference"
    )

    may_we_contact_no_employer_2: BooleanLike = Field(
        default="", description="Indicate No if this employer may not be contacted for a reference"
    )

    if_no_why_not_employer_2: str = Field(
        default="",
        description=(
            "Reason why this employer should not be contacted (if you selected No) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reason_for_leaving_employer_2: str = Field(
        default="",
        description=(
            'Primary reason you left this employer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    employer_say_reason_terminated_employer_2: str = Field(
        default="",
        description=(
            "How you believe this employer would describe the reason your employment ended "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    were_you_ever_disciplined_employer_2: str = Field(
        default="",
        description=(
            "Indicate whether you were ever disciplined by this employer and explain the "
            'reason .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    notice_given_when_resigning_employer_2: str = Field(
        default="",
        description=(
            "Amount of notice you provided when resigning and explanation if no notice was "
            'given .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class EmploymentTerminationHistory(BaseModel):
    """History of terminations, resignations, and related explanations"""

    terminated_or_asked_to_resign_yes: BooleanLike = Field(
        ...,
        description="Select Yes if you have ever been terminated or asked to resign from any job",
    )

    terminated_or_asked_to_resign_no: BooleanLike = Field(
        ...,
        description="Select No if you have never been terminated or asked to resign from any job",
    )

    terminated_or_asked_to_resign_times: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of times you have been terminated or asked to resign"
    )

    terminated_by_mutual_agreement_yes: BooleanLike = Field(
        ..., description="Select Yes if any employment has been terminated by mutual agreement"
    )

    terminated_by_mutual_agreement_no: BooleanLike = Field(
        ..., description="Select No if no employment has been terminated by mutual agreement"
    )

    terminated_by_mutual_agreement_times: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of times your employment has been terminated by mutual agreement",
    )

    choice_to_resign_rather_than_terminated_yes: BooleanLike = Field(
        ...,
        description=(
            "Select Yes if you have ever been given the choice to resign instead of being "
            "terminated"
        ),
    )

    choice_to_resign_rather_than_terminated_no: BooleanLike = Field(
        ...,
        description=(
            "Select No if you have never been given the choice to resign instead of being "
            "terminated"
        ),
    )

    choice_to_resign_rather_than_terminated_times: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of times you were given the choice to resign rather than be terminated",
    )

    termination_resignation_explanation_1: str = Field(
        default="",
        description=(
            "Explanation of the circumstances for the first relevant termination or "
            'resignation event .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    termination_resignation_explanation_2: str = Field(
        default="",
        description=(
            "Explanation of the circumstances for the second relevant termination or "
            'resignation event .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    termination_resignation_explanation_3: str = Field(
        default="",
        description=(
            "Explanation of the circumstances for the third relevant termination or "
            'resignation event .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class QualificationsandCredentials(BaseModel):
    """Qualifications, special skills, and professional credentials"""

    qualifications_and_special_skills: str = Field(
        ...,
        description=(
            "Summary of your qualifications, special skills, and relevant experience for "
            'the position .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    professional_registration_licensure_certification: str = Field(
        default="",
        description=(
            "List current relevant professional registrations, licenses, or certifications "
            "and note any that have been suspended, revoked, or terminated .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class WorkExperience(BaseModel):
    """
    WORK EXPERIENCE

    Please list the names of your present and/or previous employers in chronological order with present or most recent employer listed first. Provide information for at least the most recent ten (10) year period. Attach additional sheets if needed. If self-employed, supply firm name and business references. You may include any verifiable work performed on a volunteer basis, internships, or military service. Your failure to completely respond to each inquiry may disqualify you for consideration from employment. Do not answer “see résumé.”
    """

    work_experience___employer_1: WorkExperienceEmployer1 = Field(
        ..., description="Work Experience - Employer 1"
    )
    work_experience___employer_2: WorkExperienceEmployer2 = Field(
        ..., description="Work Experience - Employer 2"
    )
    employment_termination_history: EmploymentTerminationHistory = Field(
        ..., description="Employment Termination History"
    )
    qualifications_and_credentials: QualificationsandCredentials = Field(
        ..., description="Qualifications and Credentials"
    )
