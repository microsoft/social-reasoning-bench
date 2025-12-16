from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PropertyandZoningInformation(BaseModel):
    """Current zoning, historic district, land use, and property use details"""

    current_zoning_districts: str = Field(
        ...,
        description=(
            "List the current zoning district or districts that apply to the property. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    current_historic_districts_local_state_national: str = Field(
        ...,
        description=(
            "Indicate any local, state, or national historic districts that currently apply "
            'to the property. .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    designated_future_land_use_category: str = Field(
        ...,
        description=(
            "Provide the designated future land use category for the property from the "
            'applicable plan or map. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    current_use_of_property: str = Field(
        ...,
        description=(
            "Describe the current use of the property (e.g., single-family residential, "
            'commercial, mixed-use). .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    proposed_use_of_property: str = Field(
        ...,
        description=(
            "Describe the proposed use of the property after the project is completed. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ProjectDescriptionandDesignReview(BaseModel):
    """Description of proposed work and responses to design review criteria"""

    brief_description_of_proposed_work_and_rationale: str = Field(
        ...,
        description=(
            "Briefly describe the proposed construction, reconstruction, or exterior "
            "alteration, explain the rationale for the design review request, and note any "
            'project schedule or timeline. .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    explanation_effect_on_exterior_architectural_features: str = Field(
        ...,
        description=(
            "Explain whether and how the proposed work will detrimentally change, destroy, "
            "or adversely affect any exterior architectural features of the building or "
            'structure. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    explanation_harmonize_with_neighboring_improvements: str = Field(
        ...,
        description=(
            "Explain whether the proposed work will match and harmonize with the external "
            "appearance of adjacent neighboring buildings or improvements. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    explanation_conformance_with_historic_preservation_plan: str = Field(
        ...,
        description=(
            "Explain whether the proposed work conforms to the objectives of any applicable "
            "historic preservation plan for the district. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    explanation_conformance_with_architectural_design_guidelines: str = Field(
        ...,
        description=(
            "Explain whether the proposed work conforms to the historic architectural "
            "design guidelines, including compatibility of size, volume, proportions, "
            "rhythm, materials, detailing, colors, and expressiveness. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Exhibits(BaseModel):
    """Supporting documents and visual materials"""

    letter_to_district_alderperson: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether a letter to the District Alderperson is included as an exhibit."
        ),
    )

    additional_exhibits_if_any_list: str = Field(
        default="",
        description=(
            "List any additional exhibits included with the application. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    photographs_of_building_or_structure: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether photographs of the building or structure are included as exhibits."
        ),
    )

    renderings_or_elevations: BooleanLike = Field(
        default="",
        description="Indicate whether renderings or elevations are included as exhibits.",
    )

    site_plan_for_additions_and_new_construction: BooleanLike = Field(
        default="",
        description=(
            "Indicate whether a site plan is included (required for additions and new "
            "construction)."
        ),
    )


class CertificationandSignature(BaseModel):
    """Applicant and property owner certifications and signatures"""

    signature_of_applicant: str = Field(
        ...,
        description=(
            "Signature of the applicant certifying the accuracy and completeness of the "
            'application. .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    date_signature_of_applicant: str = Field(
        ..., description="Date the applicant signed the application."
    )  # YYYY-MM-DD format

    signature_of_property_owners: str = Field(
        ...,
        description=(
            "Signature of the property owner or owners certifying the application. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_signature_of_property_owners: str = Field(
        ..., description="Date the property owner or owners signed the application."
    )  # YYYY-MM-DD format


class DesignReviewApplication(BaseModel):
    """
    DESIGN REVIEW APPLICATION

    Briefly describe the proposed building, structure construction, reconstruction or exterior alteration. Please also provide rationale for the design review request, along with the time schedule (if any) for the project.
    """

    property_and_zoning_information: PropertyandZoningInformation = Field(
        ..., description="Property and Zoning Information"
    )
    project_description_and_design_review: ProjectDescriptionandDesignReview = Field(
        ..., description="Project Description and Design Review"
    )
    exhibits: Exhibits = Field(..., description="Exhibits")
    certification_and_signature: CertificationandSignature = Field(
        ..., description="Certification and Signature"
    )
