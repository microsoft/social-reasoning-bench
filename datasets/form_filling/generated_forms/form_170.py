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
    """Basic information about the student and the petition term"""

    pronouns_optional: str = Field(
        default="",
        description=(
            "Your pronouns (e.g., she/her, he/him, they/them). .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name: str = Field(
        ...,
        description=(
            'Your full legal name. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    uid: str = Field(
        ...,
        description=(
            "Your Caltech university identification number. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    class_year: str = Field(
        ...,
        description=(
            'Your expected graduation class year. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    option: str = Field(
        ...,
        description=(
            'Your academic option/major. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    advisor_name: str = Field(
        ...,
        description=(
            'Full name of your academic advisor. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    caltech_email: str = Field(
        ...,
        description=(
            'Your official Caltech email address. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    cell_phone: str = Field(
        ...,
        description=(
            'Your mobile phone number. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    on_campus_residence: str = Field(
        ...,
        description=(
            "Your on-campus residence (house, apartment, room, etc.). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    petition_is_for_term_year_term: str = Field(
        ...,
        description=(
            "Academic term for which this underload petition applies (e.g., Fall, Winter, "
            'Spring). .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    petition_is_for_term_year_year: str = Field(
        ...,
        description=(
            "Academic year for which this underload petition applies (e.g., 2025). .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PlannedCourseLoad(BaseModel):
    """Courses and units for this term and the next two terms"""

    this_term_courses_row_1: str = Field(
        default="",
        description=(
            'Course(s) for this term, first row. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    this_term_units_row_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) this term, first row."
    )

    next_term_courses_row_1: str = Field(
        default="",
        description=(
            'Course(s) for next term, first row. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    next_term_units_row_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) next term, first row."
    )

    the_next_term_courses_row_1: str = Field(
        default="",
        description=(
            "Course(s) for the following term, first row. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    the_next_term_units_row_1: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) in the following term, first row."
    )

    this_term_courses_row_2: str = Field(
        default="",
        description=(
            'Course(s) for this term, second row. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    this_term_units_row_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) this term, second row."
    )

    next_term_courses_row_2: str = Field(
        default="",
        description=(
            'Course(s) for next term, second row. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    next_term_units_row_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) next term, second row."
    )

    the_next_term_courses_row_2: str = Field(
        default="",
        description=(
            "Course(s) for the following term, second row. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    the_next_term_units_row_2: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) in the following term, second row."
    )

    this_term_courses_row_3: str = Field(
        default="",
        description=(
            'Course(s) for this term, third row. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    this_term_units_row_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) this term, third row."
    )

    next_term_courses_row_3: str = Field(
        default="",
        description=(
            'Course(s) for next term, third row. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    next_term_units_row_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) next term, third row."
    )

    the_next_term_courses_row_3: str = Field(
        default="",
        description=(
            "Course(s) for the following term, third row. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    the_next_term_units_row_3: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) in the following term, third row."
    )

    this_term_courses_row_4: str = Field(
        default="",
        description=(
            'Course(s) for this term, fourth row. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    this_term_units_row_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) this term, fourth row."
    )

    next_term_courses_row_4: str = Field(
        default="",
        description=(
            'Course(s) for next term, fourth row. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    next_term_units_row_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) next term, fourth row."
    )

    the_next_term_courses_row_4: str = Field(
        default="",
        description=(
            "Course(s) for the following term, fourth row. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    the_next_term_units_row_4: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) in the following term, fourth row."
    )

    this_term_courses_row_5: str = Field(
        default="",
        description=(
            'Course(s) for this term, fifth row. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    this_term_units_row_5: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) this term, fifth row."
    )

    next_term_courses_row_5: str = Field(
        default="",
        description=(
            'Course(s) for next term, fifth row. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    next_term_units_row_5: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) next term, fifth row."
    )

    the_next_term_courses_row_5: str = Field(
        default="",
        description=(
            "Course(s) for the following term, fifth row. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    the_next_term_units_row_5: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) in the following term, fifth row."
    )

    this_term_courses_row_6: str = Field(
        default="",
        description=(
            'Course(s) for this term, sixth row. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    this_term_units_row_6: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) this term, sixth row."
    )

    next_term_courses_row_6: str = Field(
        default="",
        description=(
            'Course(s) for next term, sixth row. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    next_term_units_row_6: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) next term, sixth row."
    )

    the_next_term_courses_row_6: str = Field(
        default="",
        description=(
            "Course(s) for the following term, sixth row. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    the_next_term_units_row_6: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) in the following term, sixth row."
    )

    this_term_courses_row_7: str = Field(
        default="",
        description=(
            'Course(s) for this term, seventh row. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    this_term_units_row_7: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) this term, seventh row."
    )

    next_term_courses_row_7: str = Field(
        default="",
        description=(
            'Course(s) for next term, seventh row. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    next_term_units_row_7: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) next term, seventh row."
    )

    the_next_term_courses_row_7: str = Field(
        default="",
        description=(
            "Course(s) for the following term, seventh row. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    the_next_term_units_row_7: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Units for the listed course(s) in the following term, seventh row."
    )

    total_units_this_term: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of units you plan to take this term."
    )

    total_units_next_term: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of units you plan to take next term."
    )

    total_units_the_next_term: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total number of units you plan to take in the following term."
    )


class UnderloadJustification(BaseModel):
    """Student explanation for requesting an underload"""

    explain_why_you_need_an_underload_for_this_term: str = Field(
        ...,
        description=(
            "Explanation of the reasons you are requesting an underload for this term. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AdvisorandDeanRecommendation(BaseModel):
    """Recommendation and decision on the petition"""

    recommend: BooleanLike = Field(
        default="", description="Advisor indication that they recommend this underload."
    )

    do_not_recommend: BooleanLike = Field(
        default="", description="Advisor indication that they do not recommend this underload."
    )

    approve: BooleanLike = Field(
        default="", description="Administrative indication that this petition is approved."
    )

    deny_this_petition: BooleanLike = Field(
        default="", description="Administrative indication that this petition is denied."
    )

    advisor_signature: str = Field(
        ...,
        description=(
            'Signature of your academic advisor. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    advisor_signature_date: str = Field(
        ..., description="Date the advisor signed this petition."
    )  # YYYY-MM-DD format

    dean_assoc_dean_signature_for_seniors_registrar: str = Field(
        ...,
        description=(
            "Signature of the Dean/Associate Dean, or Registrar for seniors. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    dean_assoc_dean_signature_date: str = Field(
        ..., description="Date the Dean/Associate Dean or Registrar signed this petition."
    )  # YYYY-MM-DD format


class AdditionalApprovals(BaseModel):
    """Signatures required for NCAA athletes and international students"""

    associate_athletic_director_signature: str = Field(
        default="",
        description=(
            "Signature of the Associate Athletic Director (required for NCAA "
            'student-athletes only). .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    associate_athletic_director_signature_date: str = Field(
        default="",
        description="Date the Associate Athletic Director signed (NCAA student-athletes only).",
    )  # YYYY-MM-DD format

    international_student_programs_signature: str = Field(
        default="",
        description=(
            "Signature from International Student Programs (required for international "
            'students only). .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    international_student_programs_signature_date: str = Field(
        default="",
        description="Date International Student Programs signed (international students only).",
    )  # YYYY-MM-DD format


class StudentAcknowledgment(BaseModel):
    """Student acknowledgment of underload and related policies"""

    i_acknowledge_required: BooleanLike = Field(
        ...,
        description=(
            "Confirmation that you have read and understand the information regarding "
            "underloads and related policies."
        ),
    )


class PetitionToRegisterForUnderload(BaseModel):
    """
    Petition to Register for Underload

    ''
    """

    student_information: StudentInformation = Field(..., description="Student Information")
    planned_course_load: PlannedCourseLoad = Field(..., description="Planned Course Load")
    underload_justification: UnderloadJustification = Field(
        ..., description="Underload Justification"
    )
    advisor_and_dean_recommendation: AdvisorandDeanRecommendation = Field(
        ..., description="Advisor and Dean Recommendation"
    )
    additional_approvals: AdditionalApprovals = Field(..., description="Additional Approvals")
    student_acknowledgment: StudentAcknowledgment = Field(..., description="Student Acknowledgment")
