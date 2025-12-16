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
    """Basic information about the student"""

    students_last_name: str = Field(
        ...,
        description=(
            'Student\'s legal last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    first: str = Field(
        ...,
        description=(
            'Student\'s legal first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    middle: str = Field(
        default="",
        description=(
            'Student\'s middle name (if any) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Student's date of birth")  # YYYY-MM-DD format

    place_of_birth_city: str = Field(
        ...,
        description=(
            'City where the student was born .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    place_of_birth_state: str = Field(
        ..., description="State or province where the student was born"
    )

    place_of_birth_country: str = Field(
        ...,
        description=(
            'Country where the student was born .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class SectionALanguageBackground(BaseModel):
    """Information about the student's language use and educational background"""

    primary_languages_spoken_in_home: str = Field(
        ...,
        description=(
            "List the main language or languages spoken in the home .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    language_child_uses_most_frequently: str = Field(
        ...,
        description=(
            'Language your child speaks most often .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    language_child_learned_first: str = Field(
        ...,
        description=(
            "First language your child learned to speak .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    language_used_most_with_child: str = Field(
        ...,
        description=(
            "Language you most often use when speaking with your child .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    is_english_main_language_child_speaks: BooleanLike = Field(
        ..., description="Indicate whether English is your child's primary spoken language"
    )

    how_long_attended_school_in_us: str = Field(
        ...,
        description=(
            "Length of time (e.g., years and/or months) your child has attended school in "
            'the U.S. .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    last_year_of_schooling_outside_us: str = Field(
        default="",
        description=(
            "Most recent school year your child completed outside the U.S. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    years_of_education_in_another_country: Union[float, Literal["N/A", ""]] = Field(
        default="",
        description="Total number of years your child attended school in another country",
    )

    languages_of_instruction: str = Field(
        ...,
        description=(
            "List the language or languages used to teach your child in school .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    additional_information_english_language_experiences: str = Field(
        default="",
        description=(
            "Any extra details about your child's experiences with English .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class SectionBCommunicationPreferences(BaseModel):
    """Preferred languages for school communication"""

    language_for_written_information: str = Field(
        ...,
        description=(
            "Preferred language for letters, emails, and other written communication from "
            'the school .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    language_for_oral_information: str = Field(
        ...,
        description=(
            "Preferred language for phone calls, meetings, and other spoken communication "
            'from the school .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class ParentGuardianCertification(BaseModel):
    """Parent/guardian name, signature, and date"""

    printed_name_parent_guardian: str = Field(
        ...,
        description=(
            "Parent or guardian's printed full name .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    signature_parent_guardian: str = Field(
        ...,
        description=(
            "Signature of the parent or guardian completing this form .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the form is signed")  # YYYY-MM-DD format


class AttachmentDCentervilleCitySchoolsHomeLanguageSurvey(BaseModel):
    """
        Attachment D

    CENTERVILLE CITY SCHOOLS

    Home Language Survey

        Parents: We ask the questions below to make sure your child receives the education services he or she needs. The answers to the questions in Section A will tell your child's school staff if they need to check your child's proficiency in English. This makes sure your child has every opportunity to succeed in school. The answers to Section B will help school staff communicate with you in the language you prefer.
    """

    student_information: StudentInformation = Field(..., description="Student Information")
    section_a___language_background: SectionALanguageBackground = Field(
        ..., description="Section A - Language Background"
    )
    section_b___communication_preferences: SectionBCommunicationPreferences = Field(
        ..., description="Section B - Communication Preferences"
    )
    parentguardian_certification: ParentGuardianCertification = Field(
        ..., description="Parent/Guardian Certification"
    )
