from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PermitInformation(BaseModel):
    """Permit number and type of work requested"""

    permit_application_number: str = Field(
        ...,
        description=(
            "Unique identifier assigned to this permit application .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    approach_new_driveway_street: BooleanLike = Field(
        default="", description="Check if the permit is for a new driveway or street approach"
    )

    approach_repair_approach: BooleanLike = Field(
        default="", description="Check if the permit is to repair an existing approach"
    )

    approach_relocate_approach: BooleanLike = Field(
        default="", description="Check if the permit is to relocate an existing approach"
    )

    approach_curb: BooleanLike = Field(
        default="", description="Check if the permit involves curb work for the approach"
    )

    approach_other: str = Field(
        default="",
        description=(
            "Describe any other type of approach work not listed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    encroachment_construct_new_street: BooleanLike = Field(
        default="", description="Check if the encroachment is to construct a new street"
    )

    encroachment_repair_existing_street: BooleanLike = Field(
        default="", description="Check if the encroachment is to repair an existing street"
    )

    encroachment_relocate_street: BooleanLike = Field(
        default="", description="Check if the encroachment is to relocate a street"
    )

    encroachment_public_access_easement: BooleanLike = Field(
        default="", description="Check if the encroachment involves a public access easement"
    )

    encroachment_fence_sign: BooleanLike = Field(
        default="", description="Check if the encroachment involves a fence or sign"
    )

    encroachment_berm: BooleanLike = Field(
        default="", description="Check if the encroachment involves a berm"
    )

    encroachment_utility_line: BooleanLike = Field(
        default="", description="Check if the encroachment involves a utility line"
    )

    encroachment_grading_graveling_or_snow_plowing: BooleanLike = Field(
        default="",
        description="Check if the encroachment involves grading, graveling, or snow plowing",
    )

    encroachment_other: str = Field(
        default="",
        description=(
            "Describe any other type of encroachment not listed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ApplicantorPermittee(BaseModel):
    """Applicant, owner, and contractor contact information"""

    property_owner: str = Field(
        ...,
        description=(
            'Name of the property owner .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    contractor: str = Field(
        default="",
        description=(
            "Name of the contractor responsible for the work .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    company_name: str = Field(
        default="",
        description=(
            'Name of the contractor\'s company .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contractor_phone_number: str = Field(
        default="",
        description=(
            'Phone number for the contractor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    current_use_of_property: str = Field(
        default="",
        description=(
            "Describe how the property is currently being used .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contractor_mailing_address: str = Field(
        default="",
        description=(
            'Mailing address for the contractor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city_state: str = Field(
        default="",
        description=(
            "City and state for the contractor mailing address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    zip: str = Field(default="", description="ZIP code for the contractor mailing address")

    email_address_contractor_owner_section: str = Field(
        default="",
        description=(
            "Email address for the property owner or contractor .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_contact_for_project: str = Field(
        ...,
        description=(
            "Name of the primary contact person for this project .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_phone_number: str = Field(
        ...,
        description=(
            'Phone number for the primary contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_address_primary_contact_section: str = Field(
        ...,
        description=(
            'Email address for the primary contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class PropertyProjectInformation(BaseModel):
    """Location, description, and basic details of the project"""

    physical_location_of_project: str = Field(
        ...,
        description=(
            "Physical address or description of where the project is located .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    legal_description: str = Field(
        default="",
        description=(
            "Legal description of the property including township, section, lot, block, and "
            'subdivision .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    name_of_nearest_crossroad_or_intersection: str = Field(
        default="",
        description=(
            "Name of the nearest crossroad or intersection to the project site .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    estimated_cost_of_project: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Estimated total cost of the project in dollars"
    )

    estimate_provided_by: str = Field(
        default="",
        description=(
            "Name of the person or entity that provided the cost estimate .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    zoning_of_project_area: str = Field(
        default="",
        description=(
            "Zoning designation of the project area as shown in Blaine County GIS .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    projected_start_date: str = Field(
        default="", description="Planned start date for the project"
    )  # YYYY-MM-DD format

    project_duration: str = Field(
        default="",
        description=(
            "Estimated duration of the project (e.g., number of days or months) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    project_narrative_line_1: str = Field(
        default="",
        description=(
            "First line of the narrative describing the project and proposed construction "
            'schedule .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    project_narrative_line_2: str = Field(
        default="",
        description=(
            "Second line of the narrative describing the project and proposed construction "
            'schedule .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class ApplicationAttachments(BaseModel):
    """Required submittals to accompany the application"""

    application_fee_25: BooleanLike = Field(
        default="", description="Check to indicate the $25 application fee is included"
    )

    traffic_control_plan: BooleanLike = Field(
        default="", description="Check to indicate a traffic control plan is included"
    )

    other_application_attachments: str = Field(
        default="",
        description=(
            "Describe any other attachments included with the application .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    site_plan: BooleanLike = Field(
        default="", description="Check to indicate a site plan is included"
    )

    applicable_easements_agreements: BooleanLike = Field(
        default="", description="Check to indicate applicable easements or agreements are included"
    )

    construction_drawings: BooleanLike = Field(
        default="", description="Check to indicate construction drawings are included"
    )

    land_use_building_services_approvals: BooleanLike = Field(
        default="",
        description="Check to indicate required land use or building services approvals are included",
    )


class ApplicantCertificationDeliveryPreference(BaseModel):
    """Applicant signature and how the approved permit should be delivered"""

    receipt_of_approved_permit_paper: BooleanLike = Field(
        default="", description="Check if you wish to receive the approved permit as a paper copy"
    )

    receipt_of_approved_permit_electronic: BooleanLike = Field(
        default="", description="Check if you wish to receive the approved permit electronically"
    )

    authorized_representatives_signature: str = Field(
        ...,
        description=(
            "Signature of the authorized representative submitting the application .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    authorized_representatives_signature_date: str = Field(
        ..., description="Date the authorized representative signed the application"
    )  # YYYY-MM-DD format


class InternalUse(BaseModel):
    """County internal processing, fees, approvals, and conditions"""

    road_names: str = Field(
        default="",
        description=(
            "Name or names of the roads affected (internal use) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    roadway_classification: str = Field(
        default="",
        description=(
            "Classification of the roadway such as State, County, Public, or Private "
            '(internal use) .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    inspection_fee_required: BooleanLike = Field(
        default="", description="Check if an inspection fee is required"
    )

    inspection_fee_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of the required inspection fee"
    )

    performance_bond_required: BooleanLike = Field(
        default="", description="Check if a performance bond is required"
    )

    performance_bond_amount: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Dollar amount of the required performance bond"
    )

    fee_25_paid: BooleanLike = Field(
        default="", description="Check to indicate the $25 fee has been paid"
    )

    road_bridge_manager_approval_signature: str = Field(
        default="",
        description=(
            "Signature of the Road & Bridge Manager approving the permit .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    road_bridge_manager_approval_date: str = Field(
        default="", description="Date the Road & Bridge Manager approved the permit"
    )  # YYYY-MM-DD format

    permit_expiration_date: str = Field(
        default="", description="Date on which the permit expires"
    )  # YYYY-MM-DD format

    county_engineer_approval_signature: str = Field(
        default="",
        description=(
            "Signature of the County Engineer if approval is required .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    county_engineer_approval_date: str = Field(
        default="", description="Date the County Engineer approved the permit, if applicable"
    )  # YYYY-MM-DD format

    lubs_approval: str = Field(
        default="",
        description=(
            "Notation or initials for Land Use/Building Services approval, if applicable "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    special_conditions_line_1: str = Field(
        default="",
        description=(
            "First line for listing any special conditions attached to this permit .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    special_conditions_line_2: str = Field(
        default="",
        description=(
            "Second line for listing any special conditions attached to this permit .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class BlaineCountyRoadBridgeEncroachmentPermitApp(BaseModel):
    """
        BLAINE COUNTY
    Blaine County Road & Bridge Right-Of-Way
    Approach & Encroachment Permit Application

        ''
    """

    permit_information: PermitInformation = Field(..., description="Permit Information")
    applicant_or_permittee: ApplicantorPermittee = Field(..., description="Applicant or Permittee")
    property__project_information: PropertyProjectInformation = Field(
        ..., description="Property & Project Information"
    )
    application_attachments: ApplicationAttachments = Field(
        ..., description="Application Attachments"
    )
    applicant_certification__delivery_preference: ApplicantCertificationDeliveryPreference = Field(
        ..., description="Applicant Certification & Delivery Preference"
    )
    internal_use: InternalUse = Field(..., description="Internal Use")
