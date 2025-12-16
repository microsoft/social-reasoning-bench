from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ApplicationType(BaseModel):
    """Type of planning application being submitted"""

    variance: BooleanLike = Field(
        default="", description="Check if this application is for a Variance"
    )

    preliminary_plat: BooleanLike = Field(
        default="", description="Check if this application is for a Preliminary Plat"
    )

    simple_subdivision: BooleanLike = Field(
        default="", description="Check if this application is for a Simple Subdivision"
    )

    certificate_of_appropriateness: BooleanLike = Field(
        default="", description="Check if this application is for a Certificate of Appropriateness"
    )

    conditional_use_permit: BooleanLike = Field(
        default="", description="Check if this application is for a Conditional Use Permit"
    )

    major_final_plat: BooleanLike = Field(
        default="", description="Check if this application is for a Major Final Plat"
    )

    text_amendment: BooleanLike = Field(
        default="", description="Check if this application is for a Text Amendment"
    )

    advisory_design_review_public_projects: BooleanLike = Field(
        default="",
        description="Check if this application is for Advisory Design Review of Public Projects",
    )

    appeal: BooleanLike = Field(default="", description="Check if this application is an Appeal")

    minor_final_plat: BooleanLike = Field(
        default="", description="Check if this application is for a Minor Final Plat"
    )

    temporary_use_permit: BooleanLike = Field(
        default="", description="Check if this application is for a Temporary Use Permit"
    )

    certificate_of_economic_non_viability: BooleanLike = Field(
        default="",
        description="Check if this application is for a Certificate of Economic Non-Viability",
    )

    special_exception: BooleanLike = Field(
        default="", description="Check if this application is for a Special Exception"
    )

    simple_site_plan: BooleanLike = Field(
        default="", description="Check if this application is for a Simple Site Plan"
    )

    annexation: BooleanLike = Field(
        default="", description="Check if this application is for Annexation"
    )

    historic_designation: BooleanLike = Field(
        default="", description="Check if this application is for Historic Designation"
    )

    limited_setback_waiver: BooleanLike = Field(
        default="", description="Check if this application is for a Limited Setback Waiver"
    )

    minor_site_plan: BooleanLike = Field(
        default="", description="Check if this application is for a Minor Site Plan"
    )

    historic_revolving_loan: BooleanLike = Field(
        default="", description="Check if this application is for a Historic Revolving Loan"
    )

    demolition: BooleanLike = Field(
        default="", description="Check if this application is for Demolition"
    )

    rezoning_pud_id: BooleanLike = Field(
        default="", description="Check if this application is for Rezoning, PUD, or ID"
    )

    major_site_plan: BooleanLike = Field(
        default="", description="Check if this application is for a Major Site Plan"
    )

    historic_housing_grant: BooleanLike = Field(
        default="", description="Check if this application is for a Historic Housing Grant"
    )

    port_of_dubuque_chaplain_schmitt_island_design_review: BooleanLike = Field(
        default="",
        description=(
            "Check if this application is for Port of Dubuque / Chaplain Schmitt Island "
            "Design Review"
        ),
    )


class PropertyOwnerInformation(BaseModel):
    """Contact information for the property owner(s)"""

    property_owners: str = Field(
        ...,
        description=(
            'Name(s) of the property owner(s) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone_property_owner: str = Field(
        ...,
        description=(
            "Primary phone number for the property owner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_property_owner: str = Field(
        ...,
        description=(
            "Mailing street address of the property owner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_property_owner: str = Field(
        ...,
        description=(
            "City for the property owner's mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_property_owner: str = Field(
        ..., description="State for the property owner's mailing address"
    )

    zip_property_owner: str = Field(
        ..., description="ZIP code for the property owner's mailing address"
    )

    fax_property_owner: str = Field(
        default="",
        description=(
            "Fax number for the property owner, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cell_property_owner: str = Field(
        default="",
        description=(
            "Cell phone number for the property owner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_property_owner: str = Field(
        default="",
        description=(
            'Email address for the property owner .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ApplicantAgentInformation(BaseModel):
    """Contact information for the applicant or agent"""

    applicant_agent: str = Field(
        ...,
        description=(
            "Name of the applicant or authorized agent .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_applicant_agent: str = Field(
        ...,
        description=(
            "Primary phone number for the applicant or agent .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_applicant_agent: str = Field(
        ...,
        description=(
            "Mailing street address of the applicant or agent .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_applicant_agent: str = Field(
        ...,
        description=(
            "City for the applicant or agent's mailing address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    state_applicant_agent: str = Field(
        ..., description="State for the applicant or agent's mailing address"
    )

    zip_applicant_agent: str = Field(
        ..., description="ZIP code for the applicant or agent's mailing address"
    )

    fax_applicant_agent: str = Field(
        default="",
        description=(
            "Fax number for the applicant or agent, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cell_applicant_agent: str = Field(
        default="",
        description=(
            "Cell phone number for the applicant or agent .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    e_mail_applicant_agent: str = Field(
        default="",
        description=(
            "Email address for the applicant or agent .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class SiteandZoningInformation(BaseModel):
    """Location, zoning, and basic site details"""

    site_location_address: str = Field(
        ...,
        description=(
            "Street address or description of the project site location .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    neighborhood_association: str = Field(
        default="",
        description=(
            "Name of the neighborhood association, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    existing_zoning: str = Field(
        ...,
        description=(
            "Current zoning designation of the property .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    proposed_zoning: str = Field(
        default="",
        description=(
            "Requested zoning designation, if a change is proposed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    district: str = Field(
        default="",
        description=(
            "Applicable district designation, if any .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    landmark_yes: BooleanLike = Field(
        default="", description="Check if the property is designated as a landmark"
    )

    landmark_no: BooleanLike = Field(
        default="", description="Check if the property is not designated as a landmark"
    )

    legal_description_sidwell_parcel_id_or_lot_number_block_number_subdivision: str = Field(
        ...,
        description=(
            "Full legal description of the property, including Sidwell parcel ID or "
            'lot/block/subdivision information .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    total_property_lot_area_square_feet_or_acres: str = Field(
        ...,
        description=(
            "Total area of the property in square feet or acres .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectDescription(BaseModel):
    """Description of the proposal and reason it is necessary"""

    describe_proposal_and_reason_necessary: str = Field(
        ...,
        description=(
            "Description of the proposed project and why the request is necessary .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Certification(BaseModel):
    """Applicant and property owner certification and signatures"""

    property_owners_certification_signature: str = Field(
        ...,
        description=(
            "Signature of the property owner(s) certifying the information provided .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    property_owners_certification_date: str = Field(
        ..., description="Date the property owner(s) signed the certification"
    )  # YYYY-MM-DD format

    applicant_agent_certification_signature: str = Field(
        ...,
        description=(
            "Signature of the applicant or agent certifying the information provided .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    applicant_agent_certification_date: str = Field(
        ..., description="Date the applicant or agent signed the certification"
    )  # YYYY-MM-DD format


class OfficeUseOnly(BaseModel):
    """For office use only – fee and docket information"""

    fee: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Application fee amount (office use only)"
    )

    received_by: str = Field(
        default="",
        description=(
            "Name or initials of staff member who received the application (office use "
            'only) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    date_office_use: str = Field(
        default="", description="Date the application was received (office use only)"
    )  # YYYY-MM-DD format

    docket: str = Field(
        default="",
        description=(
            "Assigned docket or case number (office use only) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PlanningApplicationForm(BaseModel):
    """
    PLANNING APPLICATION FORM

    ''
    """

    application_type: ApplicationType = Field(..., description="Application Type")
    property_owner_information: PropertyOwnerInformation = Field(
        ..., description="Property Owner Information"
    )
    applicantagent_information: ApplicantAgentInformation = Field(
        ..., description="Applicant/Agent Information"
    )
    site_and_zoning_information: SiteandZoningInformation = Field(
        ..., description="Site and Zoning Information"
    )
    project_description: ProjectDescription = Field(..., description="Project Description")
    certification: Certification = Field(..., description="Certification")
    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
