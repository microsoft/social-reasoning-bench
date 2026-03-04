from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
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
            "Primary telephone number where the applicant can be reached .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Mailing address of the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Email address of the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_sobriety: str = Field(
        ..., description="Date the applicant achieved continuous sobriety"
    )  # YYYY-MM-DD format

    education: str = Field(
        default="",
        description=(
            "Educational background, including degrees, certifications, and relevant "
            'training .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class ExperienceandQualifications(BaseModel):
    """Professional, A.A. service, and other relevant experience"""

    current_and_past_aa_experience: str = Field(
        default="",
        description=(
            "Description of current and previous A.A. service and involvement .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    occupational_background: str = Field(
        default="",
        description=(
            "Summary of work history and professional experience .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_abilities_skills_background_and_life_experiences_that_may_benefit_the_aa_world_services_board: str = Field(
        default="",
        description=(
            "Other abilities, skills, background, or life experiences that may benefit the "
            'A.A. World Services Board .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    current_or_past_contractual_relationships_with_aa_world_services_inc_aa_grapevine_inc_or_aa_general_service_board_inc: str = Field(
        default="",
        description=(
            "Details of any current or past contractual relationships with A.A. World "
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

    date: str = Field(..., description="Date the applicant signs this form")  # YYYY-MM-DD format


class AaWorldServicesDirectorResumeSheet(BaseModel):
    """
    A.A. WORLD SERVICES DIRECTOR RESUME SHEET

    ''
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    experience_and_qualifications: ExperienceandQualifications = Field(
        ..., description="Experience and Qualifications"
    )
    certification: Certification = Field(..., description="Certification")
