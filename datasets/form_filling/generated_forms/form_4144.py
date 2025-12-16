from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PersonalInformation(BaseModel):
    """Basic contact and background details of the applicant"""

    name: str = Field(
        ...,
        description=(
            'Full legal name of the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    primary_phone: str = Field(
        ...,
        description=(
            "Primary telephone number where you can be reached .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing address, including street, city, state, and ZIP code .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Primary email address .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date_of_sobriety: str = Field(
        ..., description="Date you achieved continuous sobriety"
    )  # YYYY-MM-DD format

    education: str = Field(
        default="",
        description=(
            "Educational background, including degrees, certifications, and institutions "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class ExperienceandQualifications(BaseModel):
    """A.A. experience, work history, and relevant skills/background"""

    current_and_past_aa_experience: str = Field(
        ...,
        description=(
            "Describe your current and past service and participation in A.A. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    occupational_background: str = Field(
        ...,
        description=(
            "Summary of your work history and professional background .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_abilities_skills_background_and_life_experiences_that_may_benefit_the_aa_world_services_board: str = Field(
        default="",
        description=(
            "Any additional skills, abilities, background, or life experiences that may "
            'benefit the A.A. World Services Board .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ContractualRelationships(BaseModel):
    """Disclosure of any current or past contractual relationships with A.A. entities"""

    current_or_past_contractual_relationships_with_aa_world_services_inc_aa_grapevine_inc_or_aa_general_service_board_inc: str = Field(
        default="",
        description=(
            "Describe any current or past contractual relationships with A.A. World "
            "Services, Inc., AA Grapevine, Inc., or A.A. General Service Board, Inc. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Certification(BaseModel):
    """Applicant’s signature and date of application"""

    signature_of_applicant: str = Field(
        ...,
        description=(
            "Signature of the applicant certifying the information provided .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date: str = Field(..., description="Date the form is signed")  # YYYY-MM-DD format


class AaWorldServicesDirectorResumeSheet(BaseModel):
    """
    A.A. WORLD SERVICES DIRECTOR RESUME SHEET

    ''
    """

    personal_information: PersonalInformation = Field(..., description="Personal Information")
    experience_and_qualifications: ExperienceandQualifications = Field(
        ..., description="Experience and Qualifications"
    )
    contractual_relationships: ContractualRelationships = Field(
        ..., description="Contractual Relationships"
    )
    certification: Certification = Field(..., description="Certification")
