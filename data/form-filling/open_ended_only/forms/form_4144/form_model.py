from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicantInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Basic contact and background information about the applicant"""

    name: str = Field(
        ...,
        description=(
            "Full legal name of the applicant .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    primary_phone: str = Field(
        ...,
        description=(
            "Primary contact phone number .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    address: str = Field(
        ...,
        description=(
            "Mailing address .If you cannot fill this, write \"N/A\". If this field should "
            "not be filled by you (for example, it belongs to another person or office), "
            "leave it blank (empty string \"\")."
        )
    )

    email: str = Field(
        ...,
        description=(
            "Email address .If you cannot fill this, write \"N/A\". If this field should "
            "not be filled by you (for example, it belongs to another person or office), "
            "leave it blank (empty string \"\")."
        )
    )

    date_of_sobriety: str = Field(
        ...,
        description="Date sobriety began"
    )  # YYYY-MM-DD format

    education: str = Field(
        ...,
        description=(
            "Educational background .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )


class AAandProfessionalExperience(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Applicant's experience and background relevant to A.A. World Services"""

    current_and_past_aa_experience: str = Field(
        ...,
        description=(
            "Describe current and past experience in Alcoholics Anonymous .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )

    occupational_background: str = Field(
        ...,
        description=(
            "Describe occupational background .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    additional_abilities_skills_background_and_life_experiences: str = Field(
        ...,
        description=(
            "List any additional abilities, skills, background, or life experiences that "
            "may benefit the A.A. World Services Board .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    current_or_past_contractual_relationships_with_aa_world_services_inc_aa_grapevine_inc_or_aa_general_service_board_inc: str = Field(
        ...,
        description=(
            "Describe any current or past contractual relationships with A.A. World "
            "Services, Inc., AA Grapevine, Inc., or A.A. General Service Board, Inc. .If "
            "you cannot fill this, write \"N/A\". If this field should not be filled by you "
            "(for example, it belongs to another person or office), leave it blank (empty "
            "string \"\")."
        )
    )


class Certification(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Applicant's signature and date of application"""

    signature_of_applicant: str = Field(
        ...,
        description=(
            "Signature of the applicant .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    date: str = Field(
        ...,
        description="Date of signing"
    )  # YYYY-MM-DD format


class AaWorldServicesDirectorResumeSheet(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    A.A. WORLD SERVICES DIRECTOR RESUME SHEET

    ''
    """

    applicant_information: ApplicantInformation = Field(
        ...,
        description="Applicant Information"
    )
    aa_and_professional_experience: AAandProfessionalExperience = Field(
        ...,
        description="A.A. and Professional Experience"
    )
    certification: Certification = Field(
        ...,
        description="Certification"
    )