from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EducationInformation(BaseModel):
    """Details of formal education history"""

    high_school_school: str = Field(
        default="",
        description=(
            'Name of the high school attended .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    high_school_location: str = Field(
        default="",
        description=(
            'City and state of the high school .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    high_school_years_completed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years of high school completed"
    )

    high_school_diploma_or_degree: str = Field(
        default="",
        description=(
            "Type of diploma or degree received from high school, if any .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    high_school_major_minor: str = Field(
        default="",
        description=(
            "Major and minor areas of study in high school, if applicable .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    trade_bus_or_correspondence_school: str = Field(
        default="",
        description=(
            "Name of the trade, business, or correspondence school attended .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    trade_bus_or_correspondence_location: str = Field(
        default="",
        description=(
            "City and state of the trade, business, or correspondence school .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    trade_bus_or_correspondence_years_completed: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Number of years completed at the trade, business, or correspondence school",
    )

    trade_bus_or_correspondence_diploma_or_degree: str = Field(
        default="",
        description=(
            "Diploma, degree, or certificate received from the trade, business, or "
            'correspondence school, if any .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    trade_bus_or_correspondence_major_minor: str = Field(
        default="",
        description=(
            "Major and minor fields of study at the trade, business, or correspondence "
            'school .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    college_school: str = Field(
        default="",
        description=(
            'Name of the college attended .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    college_location: str = Field(
        default="",
        description=(
            'City and state of the college .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    college_years_completed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years of college completed"
    )

    college_diploma_or_degree: str = Field(
        default="",
        description=(
            "Degree or diploma received from college, if any .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    college_major_minor: str = Field(
        default="",
        description=(
            "Major and minor fields of study in college .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    graduate_school_school: str = Field(
        default="",
        description=(
            'Name of the graduate school attended .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    graduate_school_location: str = Field(
        default="",
        description=(
            'City and state of the graduate school .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    graduate_school_years_completed: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years of graduate school completed"
    )

    graduate_school_diploma_or_degree: str = Field(
        default="",
        description=(
            "Graduate degree or diploma received, if any .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    graduate_school_major_minor: str = Field(
        default="",
        description=(
            "Major and minor fields of study in graduate school .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RelatedExperienceTraining(BaseModel):
    """Experience, skills, and specialized training relevant to the position"""

    experiences_skills_qualifications_related_to_working_here: str = Field(
        default="",
        description=(
            "Describe experiences, skills, or qualifications that specifically relate to "
            'working at this organization .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    other_specialized_or_professional_training: str = Field(
        default="",
        description=(
            "Describe any specialized or professional training, including courses through "
            "employment, and indicate if a degree or certificate was received .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class References(BaseModel):
    """Professional or personal references (not relatives or former employers)"""

    reference_1_name: str = Field(
        default="",
        description=(
            "Full name of first reference (not a relative or former employer) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reference_1_title: str = Field(
        default="",
        description=(
            "Professional title or position of first reference .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_1_relationship_to_you: str = Field(
        default="",
        description=(
            'How the first reference knows you .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_1_telephone: str = Field(
        default="",
        description=(
            "Telephone number for the first reference .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reference_1_email_address: str = Field(
        default="",
        description=(
            'Email address for the first reference .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_1_years_known: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years you have known the first reference"
    )

    reference_2_name: str = Field(
        default="",
        description=(
            "Full name of second reference (not a relative or former employer) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reference_2_title: str = Field(
        default="",
        description=(
            "Professional title or position of second reference .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_relationship_to_you: str = Field(
        default="",
        description=(
            'How the second reference knows you .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_telephone: str = Field(
        default="",
        description=(
            "Telephone number for the second reference .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_email_address: str = Field(
        default="",
        description=(
            "Email address for the second reference .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reference_2_years_known: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years you have known the second reference"
    )

    reference_3_name: str = Field(
        default="",
        description=(
            "Full name of third reference (not a relative or former employer) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reference_3_title: str = Field(
        default="",
        description=(
            "Professional title or position of third reference .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reference_3_relationship_to_you: str = Field(
        default="",
        description=(
            'How the third reference knows you .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_3_telephone: str = Field(
        default="",
        description=(
            "Telephone number for the third reference .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    reference_3_email_address: str = Field(
        default="",
        description=(
            'Email address for the third reference .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    reference_3_years_known: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of years you have known the third reference"
    )


class ApplicantStatement(BaseModel):
    """Applicant certification and acknowledgment"""

    signature_of_applicant: str = Field(
        ...,
        description=(
            "Applicant’s signature indicating they have read and accept the Applicant "
            'Statement .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Date the applicant signed the application"
    )  # YYYY-MM-DD format


class EducationInformation(BaseModel):
    """EDUCATION INFORMATION"""

    education_information: EducationInformation = Field(..., description="Education Information")
    related_experience__training: RelatedExperienceTraining = Field(
        ..., description="Related Experience & Training"
    )
    references: References = Field(..., description="References")
    applicant_statement: ApplicantStatement = Field(..., description="Applicant Statement")
