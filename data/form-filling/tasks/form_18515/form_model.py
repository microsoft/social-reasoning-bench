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
    """Basic contact information for the applicant"""

    name: str = Field(
        ...,
        description=(
            'Applicant\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            'Applicant\'s email address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class InterestinCommittee(BaseModel):
    """Applicant’s motivation for serving on the Advisory Committee"""

    why_are_you_interested_in_serving_on_the_pennsylvania_prek_counts_head_start_supplemental_assistance_program_advisory_committee: str = Field(
        ...,
        description=(
            "Explain your reasons for wanting to serve on the Advisory Committee .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class RelevantExperienceandAttributes(BaseModel):
    """Attributes, experiences, and backgrounds relevant to serving on the Advisory Committee"""

    pa_prek_counts_program_content_knowledge_and_or_experience: BooleanLike = Field(
        default="",
        description=(
            "Indicate if you have content knowledge and/or experience with the PA PreK "
            "Counts Program"
        ),
    )

    head_start_head_start_supplemental_assistance_program_content_knowledge_and_or_experience: BooleanLike = Field(
        default="",
        description=(
            "Indicate if you have content knowledge and/or experience with Head Start or "
            "the Head Start Supplemental Assistance Program"
        ),
    )

    content_knowledge_and_or_experience: BooleanLike = Field(
        default="",
        description="Indicate if you have other relevant content knowledge and/or experience",
    )

    family_member_experience_with_pa_pkc_program_services_in_pennsylvania_child_currently_or_formerly_enrolled_in_the_program: BooleanLike = Field(
        default="",
        description=(
            "Check if you have family member experience with PA PKC Program services in "
            "Pennsylvania"
        ),
    )

    family_member_experience_with_hs_hssap_program_services_in_pennsylvania_child_currently_or_formerly_enrolled_in_the_program: BooleanLike = Field(
        default="",
        description=(
            "Check if you have family member experience with HS/HSSAP Program services in "
            "Pennsylvania"
        ),
    )

    practical_experiences_in_center_setting: BooleanLike = Field(
        default="",
        description="Indicate if you have practical experience in a center-based setting",
    )

    practical_experiences_in_family_child_care_setting: BooleanLike = Field(
        default="",
        description="Indicate if you have practical experience in a family child care setting",
    )

    practical_experiences_in_group_home_setting: BooleanLike = Field(
        default="", description="Indicate if you have practical experience in a group home setting"
    )

    practical_experiences_in_school_district_setting: BooleanLike = Field(
        default="",
        description="Indicate if you have practical experience in a school district setting",
    )

    practical_experiences_in_pde_private_academic_school_setting: BooleanLike = Field(
        default="",
        description=(
            "Indicate if you have practical experience in a PDE Private Academic School setting"
        ),
    )

    practical_experiences_in_an_intermediate_unit_setting: BooleanLike = Field(
        default="",
        description="Indicate if you have practical experience in an Intermediate Unit setting",
    )

    practical_experiences_in_other_setting_that_is_not_listed_please_describe: str = Field(
        default="",
        description=(
            "Describe any practical experience in other settings not listed above .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    early_childhood_education_academic_and_or_research_experience: BooleanLike = Field(
        default="",
        description=(
            "Indicate if you have academic and/or research experience in early childhood education"
        ),
    )

    mentoring_technical_assistance_or_professional_development_experience: BooleanLike = Field(
        default="",
        description=(
            "Indicate if you have mentoring, technical assistance, or professional "
            "development experience"
        ),
    )

    non_profit_or_other_statewide_committee_experience_please_describe: str = Field(
        default="",
        description=(
            "Describe any non-profit or other statewide committee experience .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    political_advocacy_experience: BooleanLike = Field(
        default="", description="Indicate if you have political or advocacy experience"
    )

    parent_family_leadership_training: BooleanLike = Field(
        default="",
        description="Indicate if you have participated in parent or family leadership training",
    )

    other_please_describe: str = Field(
        default="",
        description=(
            "Describe any other relevant experience or attributes not listed above .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PaPaOfficeOfChildDevEarlyLearningPkchssapAdvisoryApp(BaseModel):
    """
        PA pennsylvania
    OFFICE OF CHILD DEVELOPMENT
    AND EARLY LEARNING

    Pennsylvania PKC/HSSAP Advisory Committee Application

        ''
    """

    applicant_information: ApplicantInformation = Field(..., description="Applicant Information")
    interest_in_committee: InterestinCommittee = Field(..., description="Interest in Committee")
    relevant_experience_and_attributes: RelevantExperienceandAttributes = Field(
        ..., description="Relevant Experience and Attributes"
    )
