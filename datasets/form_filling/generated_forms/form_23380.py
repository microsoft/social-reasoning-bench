from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EmploymentInformation(BaseModel):
    """Present or most recent employment details"""

    present_or_last_employer: str = Field(
        ...,
        description=(
            "Name of your present or most recent employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    position_or_occupation: str = Field(
        ...,
        description=(
            "Your job title or primary occupation with this employer .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    employer_address: str = Field(
        ...,
        description=(
            "Street address of your present or last employer .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    how_many_years: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Number of years you have worked for this employer"
    )

    city_state_zip_code: str = Field(
        ...,
        description=(
            "City, state, and ZIP code of your employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class EducationandTraining(BaseModel):
    """Educational background and training"""

    institution_name_city_and_state: str = Field(
        default="",
        description=(
            "Name of the educational institution and its city and state .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    major_degree_or_area_of_study: str = Field(
        default="",
        description=(
            "Your major, degree earned, or primary area of study .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class QualificationsandInterests(BaseModel):
    """Experience, qualifications, and interest in serving"""

    board_service_experience: str = Field(
        ...,
        description=(
            "Describe any current or prior service on boards, commissions, committees, or "
            "other public bodies, including names, dates, and major accomplishments during "
            'your tenure .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    experience_training_and_skills: str = Field(
        ...,
        description=(
            "Explain the experience, technical training, and skills that qualify you for "
            "this appointment, including relevant activities in business, labor, "
            "professional, social, or other organizations .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    interest_in_serving: str = Field(
        ...,
        description=(
            "Describe your reasons and motivation for serving on this advisory board, "
            'commission, or committee .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class AcknowledgmentandSignature(BaseModel):
    """Handbook acknowledgment and applicant certification"""

    handbook_acknowledgment: BooleanLike = Field(
        ...,
        description=(
            "Applicant acknowledgment that they have read the Advisory Bodies Handbook and "
            "are willing and able to fulfill the required duties"
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Applicant’s signature confirming the information and acknowledgment .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(..., description="Date the application is signed")  # YYYY-MM-DD format


class EmploymentInformation(BaseModel):
    """
    Employment Information

    Please use the space provided, or attach a separate document, responding to the questions below. If desired, you may attach a resume or other additional documentation for consideration.
    """

    employment_information: EmploymentInformation = Field(..., description="Employment Information")
    education_and_training: EducationandTraining = Field(..., description="Education and Training")
    qualifications_and_interests: QualificationsandInterests = Field(
        ..., description="Qualifications and Interests"
    )
    acknowledgment_and_signature: AcknowledgmentandSignature = Field(
        ..., description="Acknowledgment and Signature"
    )
