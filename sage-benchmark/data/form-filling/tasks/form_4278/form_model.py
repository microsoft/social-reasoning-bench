from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PermitHeader(BaseModel):
    """General identifiers for the development permit"""

    land_use_district: str = Field(
        ...,
        description=(
            "Land use district/zoning designation for the subject property .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    tax_roll: str = Field(
        ...,
        description=(
            "Municipal tax roll number for the property .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    development_permit: str = Field(
        default="",
        description=(
            "Assigned development permit number (if known) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ContactInformation(BaseModel):
    """Applicant, contractor, and landowner contact details"""

    applicant: str = Field(
        ...,
        description=(
            'Full legal name of the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    applicant_address: str = Field(
        ...,
        description=(
            'Street address of the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    applicant_city: str = Field(
        ...,
        description=(
            'City of the applicant\'s address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    applicant_prov: str = Field(
        ...,
        description=(
            'Province of the applicant\'s address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    applicant_p_c: str = Field(
        ...,
        description=(
            "Postal code of the applicant's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_email: str = Field(
        ...,
        description=(
            'Email address for the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    applicant_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contractor: str = Field(
        default="",
        description=(
            "Name of the contractor (company or individual) responsible for the work .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    contractor_address: str = Field(
        default="",
        description=(
            'Street address of the contractor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contractor_city: str = Field(
        default="",
        description=(
            'City of the contractor\'s address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contractor_prov: str = Field(
        default="",
        description=(
            'Province of the contractor\'s address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contractor_p_c: str = Field(
        default="",
        description=(
            "Postal code of the contractor's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contractor_email: str = Field(
        default="",
        description=(
            'Email address for the contractor .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contractor_phone: str = Field(
        default="",
        description=(
            "Primary phone number for the contractor .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    landowners: str = Field(
        ...,
        description=(
            "Name(s) of the registered landowner(s) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    landowner_address: str = Field(
        ...,
        description=(
            'Street address of the landowner .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    landowner_city: str = Field(
        ...,
        description=(
            'City of the landowner\'s address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    landowner_prov: str = Field(
        ...,
        description=(
            'Province of the landowner\'s address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    landowner_p_c: str = Field(
        ...,
        description=(
            "Postal code of the landowner's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    landowner_email: str = Field(
        ...,
        description=(
            'Email address for the landowner .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    landowner_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the landowner .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectAddressLegalDescription(BaseModel):
    """Location and legal land description of the project"""

    municipal_address: str = Field(
        ...,
        description=(
            "Municipal (civic) address of the project site .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    subdivision: str = Field(
        default="",
        description=(
            "Name of the subdivision where the property is located .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    plan: str = Field(
        ...,
        description=(
            'Legal plan number for the property .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    block: str = Field(
        default="",
        description=(
            "Legal block designation for the property, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    lot: str = Field(
        ...,
        description=(
            "Legal lot designation for the property .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    quarter_section_nw: BooleanLike = Field(
        default="", description="Check if the property is in the northwest quarter section"
    )

    quarter_section_ne: BooleanLike = Field(
        default="", description="Check if the property is in the northeast quarter section"
    )

    quarter_section_sw: BooleanLike = Field(
        default="", description="Check if the property is in the southwest quarter section"
    )

    quarter_section_se: BooleanLike = Field(
        default="", description="Check if the property is in the southeast quarter section"
    )

    section: str = Field(
        ...,
        description=(
            "Legal land description - section number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    township: str = Field(
        ...,
        description=(
            "Legal land description - township number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    range: str = Field(
        ...,
        description=(
            'Legal land description - range number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    meridian_w4: BooleanLike = Field(
        default="", description="Check if the property is west of the 4th meridian"
    )

    meridian_w5: BooleanLike = Field(
        default="", description="Check if the property is west of the 5th meridian"
    )


class ProjectDetails(BaseModel):
    """Details about the proposed development"""

    current_land_use: str = Field(
        ...,
        description=(
            'Existing use of the land or building .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    proposed_land_use: str = Field(
        ...,
        description=(
            "Intended future use of the land or building .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    start_date: str = Field(
        ..., description="Planned start date of construction or development"
    )  # YYYY-MM-DD format

    est_completion_date: str = Field(
        ..., description="Estimated completion date of the project"
    )  # YYYY-MM-DD format

    est_construction_value: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Estimated total construction value in dollars"
    )

    description_of_work_and_proposed_use: str = Field(
        ...,
        description=(
            "Detailed description of the proposed construction, alterations, and use .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class Authorization(BaseModel):
    """Authorizations, acknowledgements, and applicant declaration"""

    authorize_email_correspondence_initial: BooleanLike = Field(
        ...,
        description=(
            "Applicant's initials confirming consent to receive official correspondence by email"
        ),
    )

    acknowledge_no_construction_before_building_permit_initial: BooleanLike = Field(
        ...,
        description=(
            "Applicant's initials acknowledging that construction cannot proceed until the "
            "building permit is issued"
        ),
    )

    owner_representative_authorization_initial: BooleanLike = Field(
        ...,
        description=(
            "Applicant's initials confirming ownership/representation and authorizing "
            "municipal access for review and inspections"
        ),
    )

    applicant_agrees_to_protect_public_utilities_initial: BooleanLike = Field(
        ...,
        description=(
            "Applicant's initials agreeing to protect public utilities, prevent damage, and "
            "control litter during construction"
        ),
    )

    date: str = Field(
        ..., description="Date the application and authorization were signed"
    )  # YYYY-MM-DD format

    name: str = Field(
        ...,
        description=(
            "Printed name of the person signing the application .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of the applicant or authorized representative .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class TownOfStonyPlainDevelopmentPermitApplicationForm(BaseModel):
    """
        TOWN OF STONY PLAIN

    DEVELOPMENT PERMIT APPLICATION FORM

        This personal information is being collected for the Town of Stony Plain under the authority of Section 33c of the Freedom of Information and Protection of Privacy (FOIP) Act and will be used to collect information regarding a planning and development application. Personal information provided will be protected in accordance with Part 2 of the Act. If you have any questions regarding the collection, use and disclosure of personal information, please contact the FOIP Coordinator at 780-963-2151.
    """

    permit_header: PermitHeader = Field(..., description="Permit Header")
    contact_information: ContactInformation = Field(..., description="Contact Information")
    project_address__legal_description: ProjectAddressLegalDescription = Field(
        ..., description="Project Address & Legal Description"
    )
    project_details: ProjectDetails = Field(..., description="Project Details")
    authorization: Authorization = Field(..., description="Authorization")
