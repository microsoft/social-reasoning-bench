from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class StudentContactInformation(BaseModel):
    """Basic contact details for the student applicant"""

    student_contact_information: str = Field(
        default="",
        description=(
            "General section heading for student contact details .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name: str = Field(
        ...,
        description=(
            'Student\'s full legal name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street address or mailing address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of residence .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of residence")

    zip: str = Field(..., description="ZIP or postal code")

    e_mail: str = Field(
        ...,
        description=(
            'Student\'s email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            "Primary telephone number with area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ShortAnswerQuestions(BaseModel):
    """Applicant’s interests, financial need, and education plans"""

    what_are_your_interests: str = Field(
        ...,
        description=(
            "Describe your personal, academic, and extracurricular interests .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    please_explain_your_financial_need_or_a_scholarship_to_further_your_educational_goals: str = (
        Field(
            ...,
            description=(
                "Explain your financial need and how this scholarship will support your "
                'educational goals .If you cannot fill this, write "N/A". If this field '
                "should not be filled by you (for example, it belongs to another person or "
                'office), leave it blank (empty string "").'
            ),
        )
    )

    what_are_your_plans_for_furthering_your_education: str = Field(
        ...,
        description=(
            "Describe your future educational plans and goals .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class NormanPublicSchoolFoundationScholarshipApplication(BaseModel):
    """
        Norman Public School Foundation
    Scholarship Application

        ''
    """

    student_contact_information: StudentContactInformation = Field(
        ..., description="Student Contact Information"
    )
    short_answer_questions: ShortAnswerQuestions = Field(..., description="Short Answer Questions")
