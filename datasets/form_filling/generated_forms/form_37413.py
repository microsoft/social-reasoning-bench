from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CandidatesContributions(BaseModel):
    """Details about the candidate’s scientific work and recognition"""

    candidates_significant_lifetime_contributions_to_science: str = Field(
        ...,
        description=(
            "Summarize the candidate’s most significant lifetime contributions to science "
            'in 2–4 sentences. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    place_where_the_work_above_was_completed: str = Field(
        ...,
        description=(
            "Institution(s), organization(s), or location(s) where the described work was "
            'carried out. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    additional_information_about_the_candidates_work: str = Field(
        default="",
        description=(
            "Any further details, context, or explanation of the candidate’s scientific "
            'work. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    other_honours_bestowed_on_the_candidate: str = Field(
        default="",
        description=(
            "List other awards, honours, or recognitions the candidate has received. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PersonsKnowledgeableAbouttheCandidate(BaseModel):
    """Contact information for individuals qualified to comment on the candidate’s contributions to science"""

    name_person_1_column_1: str = Field(
        ...,
        description=(
            "Full name of the first knowledgeable person (left column, first row). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    name_person_1_column_2: str = Field(
        ...,
        description=(
            "Full name of the second knowledgeable person (right column, first row). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    email_person_1_column_1: str = Field(
        ...,
        description=(
            "Email address of the first knowledgeable person (left column, first row). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    email_person_1_column_2: str = Field(
        ...,
        description=(
            "Email address of the second knowledgeable person (right column, first row). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    phone_person_1_column_1: str = Field(
        ...,
        description=(
            "Phone number of the first knowledgeable person (left column, first row). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    phone_person_1_column_2: str = Field(
        ...,
        description=(
            "Phone number of the second knowledgeable person (right column, first row). .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    name_person_2_column_1: str = Field(
        default="",
        description=(
            "Full name of an additional knowledgeable person (left column, second block). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    name_person_2_column_2: str = Field(
        default="",
        description=(
            "Full name of an additional knowledgeable person (right column, second block). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    email_person_2_column_1: str = Field(
        default="",
        description=(
            "Email address of an additional knowledgeable person (left column, second "
            'block). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    email_person_2_column_2: str = Field(
        default="",
        description=(
            "Email address of an additional knowledgeable person (right column, second "
            'block). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    phone_person_2_column_1: str = Field(
        default="",
        description=(
            "Phone number of an additional knowledgeable person (left column, second "
            'block). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    phone_person_2_column_2: str = Field(
        default="",
        description=(
            "Phone number of an additional knowledgeable person (right column, second "
            'block). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class NovaScotianInstituteOfSciencensisHallOfFameNominationForm(BaseModel):
    """
        Nova Scotian Institute of Science (NSIS)
    HALL OF FAME | Nomination Form

        ''
    """

    candidates_contributions: CandidatesContributions = Field(
        ..., description="Candidate’s Contributions"
    )
    persons_knowledgeable_about_the_candidate: PersonsKnowledgeableAbouttheCandidate = Field(
        ..., description="Persons Knowledgeable About the Candidate"
    )
