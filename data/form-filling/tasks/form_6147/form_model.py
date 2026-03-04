from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Section1ExistingPermit(BaseModel):
    """Permit number for renewals"""

    permit_number: str = Field(
        default="",
        description=(
            "Existing permit number if renewing a commercial permit .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Section2IndividualInformation(BaseModel):
    """Applicant’s personal and contact information"""

    county: str = Field(
        ...,
        description=(
            "County of residence for the individual permit holder .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    individual_name: str = Field(
        ...,
        description=(
            "Full legal name of the individual to whom the permit will be issued .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    doing_business_as_if_applicable_provide_fictitious_business_name_registered_with_mo_secretary_of_state: str = Field(
        default="",
        description=(
            "Fictitious business name registered with the Missouri Secretary of State, if "
            'applicable .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing street address of the individual .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City for the mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for the mailing address")

    zip_code: str = Field(..., description="ZIP Code for the mailing address")

    if_po_box_provide_physical_address: str = Field(
        default="",
        description=(
            "Physical street address if mailing address is a PO Box .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone: str = Field(
        ...,
        description=(
            'Primary contact telephone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            'Email address for contact .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class PermitandTagSelection(BaseModel):
    """Permit type, tag quantities, and payment total"""

    wildlife_hobby_permit_code_530: BooleanLike = Field(
        ..., description="Check to apply for a Wildlife Hobby Permit (Code 530)"
    )

    pheasant_leg_bands_per_100_number_requested: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of sets of 100 pheasant leg bands requested"
    )

    pheasant_leg_bands_per_100_tag_total: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total cost for pheasant leg bands requested"
    )

    quail_leg_bands_per_100_number_requested: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of sets of 100 quail leg bands requested"
    )

    quail_leg_bands_per_100_tag_total: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total cost for quail leg bands requested"
    )

    total_amount_due: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total amount due for permit and all tags requested"
    )


class LocationInformation(BaseModel):
    """Location where wildlife is held if different from main address"""

    location_county: str = Field(
        default="",
        description=(
            "County where wildlife is held if different from mailing address .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    section: str = Field(
        default="",
        description=(
            "Land survey section for the wildlife location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    township: str = Field(
        default="",
        description=(
            "Land survey township for the wildlife location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    range: str = Field(
        default="",
        description=(
            "Land survey range for the wildlife location .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_address_if_applicable: str = Field(
        default="",
        description=(
            "Street address of the wildlife location, if it has one .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    area_acreage: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total acreage of the area where wildlife is held"
    )


class StreetAddressContactDetails(BaseModel):
    """Physical street address and directions if different from mailing address"""

    name_street_address_contact: str = Field(
        default="",
        description=(
            "Name of the person at the physical street address for contact .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address_street_address_contact: str = Field(
        default="",
        description=(
            "Physical street address if different from mailing address .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_street_address_contact: str = Field(
        default="",
        description=(
            'City for the physical street address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    state_street_address_contact: str = Field(
        default="", description="State for the physical street address"
    )

    zip_code_street_address_contact: str = Field(
        default="", description="ZIP Code for the physical street address"
    )

    directions: str = Field(
        default="",
        description=(
            "Driving directions to your location, especially if in a rural area .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SpeciesCoveredbyPermit(BaseModel):
    """Species to be authorized under this permit"""

    species_list_species_to_be_covered_by_permit: str = Field(
        ...,
        description=(
            "List all wildlife species to be covered by this permit .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ConservationAgentUseOnly(BaseModel):
    """For conservation agent approval/denial and signature"""

    approved: BooleanLike = Field(
        default="", description="Indicates the conservation agent has approved the application"
    )

    disapproved: BooleanLike = Field(
        default="", description="Indicates the conservation agent has disapproved the application"
    )

    conservation_agent_signature: str = Field(
        default="",
        description=(
            "Signature of the conservation agent reviewing the application .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    conservation_agent_date: str = Field(
        default="", description="Date the conservation agent signed the form"
    )  # YYYY-MM-DD format


class ApplicantCertification(BaseModel):
    """Applicant signature and date acknowledging permit rules"""

    applicant_signature: str = Field(
        ...,
        description=(
            "Signature of the applicant accepting all permit rules .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_date: str = Field(
        ..., description="Date the applicant signed the form"
    )  # YYYY-MM-DD format


class ApplicationForWildlifeHobbyPermitcode530(BaseModel):
    """
    Application for Wildlife Hobby Permit (CODE 530)

    Application for Wildlife Hobby Permit (CODE 530)
    """

    section_1___existing_permit: Section1ExistingPermit = Field(
        ..., description="Section 1 – Existing Permit"
    )
    section_2___individual_information: Section2IndividualInformation = Field(
        ..., description="Section 2 – Individual Information"
    )
    permit_and_tag_selection: PermitandTagSelection = Field(
        ..., description="Permit and Tag Selection"
    )
    location_information: LocationInformation = Field(..., description="Location Information")
    street_address__contact_details: StreetAddressContactDetails = Field(
        ..., description="Street Address / Contact Details"
    )
    species_covered_by_permit: SpeciesCoveredbyPermit = Field(
        ..., description="Species Covered by Permit"
    )
    conservation_agent_use_only: ConservationAgentUseOnly = Field(
        ..., description="Conservation Agent Use Only"
    )
    applicant_certification: ApplicantCertification = Field(
        ..., description="Applicant Certification"
    )
