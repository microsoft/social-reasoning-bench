from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class SectionIAcademicsStudentPortion(BaseModel):
    """Academic program, school, addresses, honours, and scholarships/grants (to be completed by the student)"""

    name_of_post_secondary_educational_institution: str = Field(
        ...,
        description=(
            "Full name of the college, university, or other post-secondary institution you "
            'attend .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    associates_degree: BooleanLike = Field(
        ..., description="Check if you are pursuing an Associate’s degree"
    )

    undergraduate_degree: BooleanLike = Field(
        ..., description="Check if you are pursuing an Undergraduate (bachelor’s) degree"
    )

    graduate_degree: BooleanLike = Field(
        ..., description="Check if you are pursuing a Graduate degree (master’s, PhD, etc.)"
    )

    certificate_degree: BooleanLike = Field(
        ..., description="Check if you are pursuing a Certificate program"
    )

    other_degree_type: str = Field(
        default="",
        description=(
            "If your degree type is not listed, specify the type of program here .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    degree: str = Field(
        ...,
        description=(
            "Name or designation of the degree you are pursuing (e.g., BA in History, BSc, "
            'MBA) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    in_what_year_of_your_current_program_will_you_be_in_the_fall_winter_semester_of_2021_2022: str = Field(
        ...,
        description=(
            "Indicate which year of your program you will be in during the 2021/2022 "
            "fall/winter semester (e.g., 1st year, 2nd year) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    school_address: str = Field(
        ...,
        description=(
            "Street address of your post-secondary educational institution .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    city_school_address: str = Field(
        ...,
        description=(
            'City where your school is located .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    prov_school_address: str = Field(..., description="Province where your school is located")

    postal_code_school_address: str = Field(
        ..., description="Postal code for your school’s address"
    )

    your_address_at_school: str = Field(
        ...,
        description=(
            "Your personal mailing address while you are at school .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_your_address_at_school: str = Field(
        ...,
        description=(
            "City for your personal address while at school .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    prov_your_address_at_school: str = Field(
        ..., description="Province for your personal address while at school"
    )

    postal_code_your_address_at_school: str = Field(
        ..., description="Postal code for your personal address while at school"
    )

    honours_and_achievements: str = Field(
        default="",
        description=(
            "List any academic honours, awards, or notable achievements .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title_amount_scholarship_or_grant_1: str = Field(
        default="",
        description=(
            "Name and amount of the first scholarship or grant applied for or received .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_scholarship_or_grant_1: str = Field(
        default="", description="Date associated with the first scholarship or grant entry"
    )  # YYYY-MM-DD format

    received_scholarship_or_grant_1: BooleanLike = Field(
        default="", description="Indicate whether the first scholarship or grant was received"
    )

    title_amount_scholarship_or_grant_2: str = Field(
        default="",
        description=(
            "Name and amount of the second scholarship or grant applied for or received .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_scholarship_or_grant_2: str = Field(
        default="", description="Date associated with the second scholarship or grant entry"
    )  # YYYY-MM-DD format

    received_scholarship_or_grant_2: BooleanLike = Field(
        default="", description="Indicate whether the second scholarship or grant was received"
    )

    title_amount_scholarship_or_grant_3: str = Field(
        default="",
        description=(
            "Name and amount of the third scholarship or grant applied for or received .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_scholarship_or_grant_3: str = Field(
        default="", description="Date associated with the third scholarship or grant entry"
    )  # YYYY-MM-DD format

    received_scholarship_or_grant_3: BooleanLike = Field(
        default="", description="Indicate whether the third scholarship or grant was received"
    )

    title_amount_scholarship_or_grant_4: str = Field(
        default="",
        description=(
            "Name and amount of the fourth scholarship or grant applied for or received .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_scholarship_or_grant_4: str = Field(
        default="", description="Date associated with the fourth scholarship or grant entry"
    )  # YYYY-MM-DD format

    received_scholarship_or_grant_4: BooleanLike = Field(
        default="", description="Indicate whether the fourth scholarship or grant was received"
    )


class SectionIAcademicsSchoolOfficialPortion(BaseModel):
    """Academic verification to be completed by a school official (e.g., Registrar, school administrator)"""

    academic_standing: str = Field(
        ...,
        description=(
            "Overall academic standing as provided by the school official (e.g., good, "
            'excellent, probation) .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    applicants_major: str = Field(
        ...,
        description=(
            "Primary field of study (major) as recorded by the school .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    applicants_minor: str = Field(
        default="",
        description=(
            "Secondary field of study (minor), if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    applicants_grade_point_average: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Current grade point average as reported by the school official"
    )

    gpa_scale: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Maximum value of the GPA scale used (e.g., 4.0, 4.3)"
    )

    signature_school_official: str = Field(
        ...,
        description=(
            "Signature of the authorized school official completing this section .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    title_school_official: str = Field(
        ...,
        description=(
            "Job title or position of the school official (e.g., Registrar, Administrator) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    date_school_official_signature: str = Field(
        ..., description="Date the school official signed this form"
    )  # YYYY-MM-DD format


class UcbeyondScholarshipHelpingStudentsWithInflammatoryDisease(BaseModel):
    """
        UCBeyond® 2021 Scholarship Program
    HELPING STUDENTS REACH BEYOND THEIR INFLAMMATORY DISEASE
    UCBeyond
    Scholarship Program

        UCBeyond® 2021 Scholarship Program – Helping students reach beyond their inflammatory disease.
    """

    section_i_academics_student_portion: SectionIAcademicsStudentPortion = Field(
        ..., description="Section I: Academics (Student Portion)"
    )
    section_i_academics_school_official_portion: SectionIAcademicsSchoolOfficialPortion = Field(
        ..., description="Section I: Academics (School Official Portion)"
    )
