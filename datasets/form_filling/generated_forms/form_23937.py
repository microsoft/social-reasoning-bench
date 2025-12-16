from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    """Basic personal, contact, and employment information about the applicant"""

    full_name: str = Field(
        ...,
        description=(
            'Applicant\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Applicant's date of birth")  # YYYY-MM-DD format

    printed_name: str = Field(
        ...,
        description=(
            'Applicant\'s name printed clearly .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    other_names_used_eg_maiden_name: str = Field(
        default="",
        description=(
            "Any other names used, such as maiden name or aliases .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    home_address: str = Field(
        ...,
        description=(
            "Applicant's current residential address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    home_telephone: str = Field(
        default="",
        description=(
            'Home phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    work_telephone: str = Field(
        default="",
        description=(
            'Work phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    cell_telephone: str = Field(
        default="",
        description=(
            'Mobile phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    e_mail: str = Field(
        default="",
        description=(
            'Email address .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    occupation: str = Field(
        ...,
        description=(
            "Current primary occupation or job title .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    prior_occupation_if_any: str = Field(
        default="",
        description=(
            'Previous occupation, if applicable .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    current_employer: str = Field(
        ...,
        description=(
            'Name of current employer .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class ApplicantQuestions(BaseModel):
    """Narrative questions about experience, attitudes, and background related to the criminal justice system"""

    describe_any_personal_attitudes_life_experiences_and_prior_examples_that_demonstrate_you_can_make_objective_impartial_evidence_based_decisions_about_complaints_against_the_police: str = Field(
        ...,
        description=(
            "Narrative description of experiences and attitudes showing ability to make "
            "objective, evidence-based decisions about complaints against the police .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    have_you_a_close_friend_or_a_family_member_ever_worked_or_volunteered_in_the_criminal_justice_system_if_yes_please_describe: str = Field(
        ...,
        description=(
            "Explain any work or volunteer experience in the criminal justice system by "
            "you, a close friend, or a family member .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    have_you_or_a_family_member_ever_participated_in_an_organization_that_advocates_a_position_regarding_the_police_or_the_criminal_justice_system_if_yes_please_describe: str = Field(
        ...,
        description=(
            "Describe any participation by you or a family member in organizations that "
            "advocate positions about the police or the criminal justice system .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ApplicantQuestionsForTheCitizenReviewCommittee(BaseModel):
    """
    Applicant Questions for the Citizen Review Committee

    Please answer the questions below truthfully and fully. Attach an additional sheet, if needed.
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    applicant_questions: ApplicantQuestions = Field(..., description="Applicant Questions")
