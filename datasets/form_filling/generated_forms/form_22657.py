from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ScholarshipSelection(BaseModel):
    """Scholarship(s) the applicant wants to be considered for and related member information"""

    college_student_chapter_scholarship_4000_must_be_current_member_in_a_nywea_student_chapter: BooleanLike = Field(
        default="",
        description=(
            "Check this box if you want to be considered for the College Student Chapter "
            "Scholarship and you are a current member in a NYWEA student chapter."
        ),
    )

    child_of_member_scholarship_4000_must_include_parents_name_nywea_membership_number: BooleanLike = Field(
        default="",
        description=(
            "Check this box if you want to be considered for the Child of Member "
            "Scholarship and will provide your parent’s name and NYWEA membership number."
        ),
    )

    parent_name_nywea_member_number: str = Field(
        default="",
        description=(
            "Parent’s full name and NYWEA membership number, required if applying for the "
            'Child of Member Scholarship. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class ApplicantInformation(BaseModel):
    """Basic personal and contact information for the applicant"""

    first_name: str = Field(
        ...,
        description=(
            'Applicant’s legal first name. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Applicant’s legal last name. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address_line_1: str = Field(
        ...,
        description=(
            'Street address, first line. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address_line_2: str = Field(
        default="",
        description=(
            "Street address, second line (apartment, suite, etc.), if applicable. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            "City of the applicant’s mailing address. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for the mailing address (e.g., NY).")

    zip_code: str = Field(..., description="5-digit ZIP code (plus 4 if applicable).")

    county: str = Field(
        default="",
        description=(
            "County of residence corresponding to the mailing address. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            'Primary contact phone number. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class NyweaScholarshipApplicationForCollegeStudents2021(BaseModel):
    """
    2021 NYWEA Scholarship Application for College Students

    Scholarship Application Tips:
    ● The state level scholarship application deadline is FEBRUARY 26, 2021 at 5 PM Eastern Time
    ● Visit our Scholarships page on the NYWEA website for full descriptions of all state-level NYWEA scholarships. Visit the Chapters pages for more information on regional scholarships.
    ● If you have questions, please email Scholarship Program Administrator Madison Quinn at madison@nywea.org.
    Application & Supporting Document Checklist
    The following documents must be emailed directly to madison@nywea.org OR mailed to: NY Water Environment Association, ATTN: Madison Quinn, 525 Plum Street, Suite 102, Syracuse, NY 13204:
      1. Completed application form - you must answer the two essay questions & initial the last page.
      2. High school transcript
      3. College transcript
      4. Two letters of recommendation: At least one of the two recommendations MUST be from a Science or Math Teacher. No recommendations can be from relatives. Only two letters will be reviewed by the committee.
    """

    scholarship_selection: ScholarshipSelection = Field(..., description="Scholarship Selection")
    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
