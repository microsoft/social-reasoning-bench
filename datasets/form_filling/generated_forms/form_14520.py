from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class SchoolandTeacherInformation(BaseModel):
    """Details about the school and nominating teacher"""

    name_of_school: str = Field(
        ...,
        description=(
            "Full name of the school the student attends .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Date this nomination form is completed"
    )  # YYYY-MM-DD format

    nominating_teacher: str = Field(
        ...,
        description=(
            "Full name of the teacher making the nomination .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    position: str = Field(
        ...,
        description=(
            "Teacher’s role or job title at the school .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Email address of the nominating teacher .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Contact phone number for the nominating teacher .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of the nominating teacher confirming this nomination .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class StudentInformation(BaseModel):
    """Basic details about the nominated student"""

    name_of_student: str = Field(
        ...,
        description=(
            'Full name of the nominated student .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    year_level_of_student: str = Field(
        ...,
        description=(
            "Current school year level of the student (e.g. Year 7, Year 8) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    age_of_student: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Age of the student in years"
    )


class GiftedandTalentedCharacteristics(BaseModel):
    """Teacher’s identification of the student’s characteristics"""

    high_ability_in_language_verbal_and_or_written_with_a_strong_memory_for_words: BooleanLike = (
        Field(
            default="",
            description=(
                "Tick to indicate the student shows high verbal and/or written language ability "
                "and strong memory for words"
            ),
        )
    )

    more_mature_in_their_thinking: BooleanLike = Field(
        default="",
        description="Tick to indicate the student demonstrates more mature thinking than peers",
    )

    talents_well_above_average_e_g_in_music_art_sport_mathematics_chess: BooleanLike = Field(
        default="",
        description=(
            "Tick to indicate the student has talents significantly above average in areas "
            "such as music, art, sport, mathematics or chess"
        ),
    )

    sets_very_high_standards_and_very_much_the_perfectionist: BooleanLike = Field(
        default="",
        description=(
            "Tick to indicate the student sets very high standards and shows perfectionist "
            "tendencies"
        ),
    )

    fears_failure_and_prefers_not_to_take_risks: BooleanLike = Field(
        default="",
        description="Tick to indicate the student tends to fear failure and avoid taking risks",
    )

    high_social_skills_leadership_organisation_humour_empathy_justice_negotiates_well_may_be_bossy: BooleanLike = Field(
        default="",
        description=(
            "Tick to indicate the student shows high social skills such as leadership, "
            "organisation, humour, empathy, sense of justice and negotiation"
        ),
    )

    wonders_about_ideas_and_the_future: BooleanLike = Field(
        default="",
        description="Tick to indicate the student often thinks or asks about ideas and the future",
    )

    trouble_with_spelling_refuses_to_write_much_may_seem_to_have_low_reading_skills: BooleanLike = (
        Field(
            default="",
            description=(
                "Tick to indicate the student has difficulty with spelling, avoids writing or "
                "appears to have low reading skills"
            ),
        )
    )

    argues_with_teachers_and_peers_has_trouble_sitting_still_and_listening_or_doodles_on_things: BooleanLike = Field(
        default="",
        description=(
            "Tick to indicate the student frequently argues, is restless, or doodles "
            "instead of listening"
        ),
    )

    may_be_good_at_working_with_computers: BooleanLike = Field(
        default="",
        description=(
            "Tick to indicate the student shows particular skill or interest in working "
            "with computers"
        ),
    )

    cant_seem_to_learn_tables_or_number_facts_or_rote_learning_but_can_solve_problems_quickly: BooleanLike = Field(
        default="",
        description=(
            "Tick to indicate the student struggles with rote learning but solves problems quickly"
        ),
    )

    daydreams_and_may_sometimes_be_perceived_as_lazy: BooleanLike = Field(
        default="",
        description="Tick to indicate the student often daydreams and may be seen as lazy",
    )

    more_interested_in_their_own_thoughts: BooleanLike = Field(
        default="",
        description=(
            "Tick to indicate the student appears more absorbed in their own thoughts than "
            "surroundings"
        ),
    )

    fits_one_or_more_of_the_profiles_of_the_gifted_and_talented_as_developed_by_neihart_and_betts: BooleanLike = Field(
        default="",
        description=(
            "Tick to indicate the student matches one or more Neihart and Betts Gifted and "
            "Talented profiles"
        ),
    )


class StudentInterestinHistory(BaseModel):
    """Teacher’s description of the student’s interest in History"""

    students_interest_in_history: str = Field(
        ...,
        description=(
            "Brief description of the student’s interest in History .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class NominationFormHistoryEnrichmentHolidayProgram(BaseModel):
    """
        TEACHER’S NOMINATION FORM – Levels 7 - 10
    HISTORY ENRICHMENT SCHOOL HOLIDAY PROGRAM

        This program is best suited for students who are independent, creative thinkers and students who are fast learners, think or perform above the level of their peers in some way (though they may not be the most successful academically) and demonstrate high potential. This program will also suit students who are recognised as Gifted and Talented, high achievers and/or those who could benefit from accelerated learning.
    """

    school_and_teacher_information: SchoolandTeacherInformation = Field(
        ..., description="School and Teacher Information"
    )
    student_information: StudentInformation = Field(..., description="Student Information")
    gifted_and_talented_characteristics: GiftedandTalentedCharacteristics = Field(
        ..., description="Gifted and Talented Characteristics"
    )
    student_interest_in_history: StudentInterestinHistory = Field(
        ..., description="Student Interest in History"
    )
