from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class StudentInformation(BaseModel):
    """Basic information about the student and planned college attendance"""

    students_name: str = Field(
        ...,
        description=(
            "Full legal name of the student applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing address including street, city, state, and zip code .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Primary email address for contacting the applicant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        ...,
        description=(
            "Primary phone number for contacting the applicant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    year_of_graduation_from_hardin_northern: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Four-digit year the student will graduate from Hardin Northern"
    )

    will_be_attending_a_2_or_4_year_college: str = Field(
        ...,
        description=(
            "Indicate whether you will attend a 2-year or 4-year college .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    public_or_private_college: str = Field(
        ...,
        description=(
            "Specify whether the college you plan to attend is public or private .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class FinancialInformation(BaseModel):
    """Family and student income details related to financial need"""

    family_income_for_past_year_include_your_income_and_parents_income: str = Field(
        ...,
        description=(
            "Total family income for the past year, including the applicant’s and parents’ "
            'income .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class EssayQuestions(BaseModel):
    """Short essays about goals, interests, family, and need"""

    essay_would_you_enjoy_attending_and_earning_a_four_4_year_degree_or_a_two_2_year_technical_degree_what_subjects_are_you_interested_in_what_profession_or_skills_would_you_like_to_acquire_in_your_schooling_to_make_you_more_marketable_in_todays_business_world_if_you_are_undecided_please_list_the_fields_s_of_interest_you_are_considering: str = Field(
        ...,
        description=(
            "Essay response describing preferred degree type, academic interests, and "
            "skills or professions you hope to gain .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    essay_what_are_your_career_goals_where_do_you_see_yourself_in_5_to_10_years: str = Field(
        ...,
        description=(
            "Essay response outlining your career goals and where you see yourself in 5–10 "
            'years .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    essay_tell_us_about_your_family_have_any_of_your_family_attended_or_graduated_from_college_elaborate_on_family_situation: str = Field(
        ...,
        description=(
            "Essay response describing your family background and any family college "
            'attendance or graduation .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    essay_please_tell_us_about_yourself_this_could_include_special_interests_you_may_have_hobbies_where_and_how_many_hours_you_worked_during_the_school_year_volunteering_or_community_projects_you_have_been_involved_with_a_particular_opinion_you_may_have_on_a_community_or_school_topic_why_you_are_interested_in_a_particular_career_or_any_other_information_you_would_like_to_share_with_the_committee_focus_on_your_willingness_to_learn_and_extra_circumstances_that_contribute_to_your_need: str = Field(
        ...,
        description=(
            "Comprehensive essay about your background, interests, work, volunteering, "
            "views, and circumstances related to your need and willingness to learn .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    essay_why_do_you_think_the_committee_should_give_this_scholarship_to_you: str = Field(
        ...,
        description=(
            "Essay response explaining why you believe you should receive this scholarship "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class Certification(BaseModel):
    """Applicant signature and certification"""

    signature_of_applicant: str = Field(
        ...,
        description=(
            "Applicant’s signature certifying the accuracy of the information provided .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class NormaDirmeyerBiblerScholarship(BaseModel):
    """
    Norma Dirmeyer Bibler Scholarship

    ''
    """

    student_information: StudentInformation = Field(..., description="Student Information")
    financial_information: FinancialInformation = Field(..., description="Financial Information")
    essay_questions: EssayQuestions = Field(..., description="Essay Questions")
    certification: Certification = Field(..., description="Certification")
