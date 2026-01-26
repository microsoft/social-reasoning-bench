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
    """Existing permit information for renewals"""

    permit_number: str = Field(
        default="",
        description=(
            "Existing permit number if renewing a commercial permit .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Section2IndividualInformation(BaseModel):
    """Individual applicant and contact details"""

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
            "Mailing street address of the individual permit holder .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            "City for the individual’s mailing address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State abbreviation for the individual’s mailing address")

    zip_code: str = Field(..., description="ZIP Code for the individual’s mailing address")

    telephone: str = Field(
        ...,
        description=(
            "Primary telephone number for the applicant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            'Email address for the applicant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class PermitandTagSelection(BaseModel):
    """Permit type, tag quantities, and payment total"""

    wildlife_hobby_permit_code_530: BooleanLike = Field(
        ..., description="Check to apply for the Wildlife Hobby Permit (Code 530)"
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
        ..., description="Total amount due for permit and any tags requested"
    )


class WildlifeLocationInformation(BaseModel):
    """Location details if wildlife is held at a different site"""

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
            "Land survey section where wildlife is held .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    township: str = Field(
        default="",
        description=(
            "Land survey township where wildlife is held .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    range: str = Field(
        default="",
        description=(
            "Land survey range where wildlife is held .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    location_address_if_applicable: str = Field(
        default="",
        description=(
            "Street address of the wildlife holding location, if it has an address .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    area_acreage: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Total acreage of the area where wildlife is held"
    )


class StreetAddressContactLocation(BaseModel):
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
        default="", description="State abbreviation for the physical street address"
    )

    zip_code_street_address_contact: str = Field(
        default="", description="ZIP Code for the physical street address"
    )

    directions: str = Field(
        default="",
        description=(
            "Driving directions to the physical location, especially for rural areas .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SpeciesCovered(BaseModel):
    """Species to be covered by the permit"""

    species_to_be_covered_by_permit: str = Field(
        ...,
        description=(
            "List of wildlife species to be covered under this permit .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ConservationAgentUseOnly(BaseModel):
    """For conservation agent approval and signature"""

    approved: BooleanLike = Field(
        default="", description="Indicates conservation agent approval of the application"
    )

    disapproved: BooleanLike = Field(
        default="", description="Indicates conservation agent disapproval of the application"
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
        default="", description="Date the conservation agent signed the approval or disapproval"
    )  # YYYY-MM-DD format


class ApplicantCertification(BaseModel):
    """Applicant signature and date"""

    applicant_signature: str = Field(
        ...,
        description=(
            "Signature of the applicant accepting permit rules .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    applicant_date: str = Field(
        ..., description="Date the applicant signed the application"
    )  # YYYY-MM-DD format


class ApplicationForWildlifeHobbyPermitcode530(BaseModel):
    """
    Application for Wildlife Hobby Permit (CODE 530)

    All required (*) fields must be completed or application will be returned to applicant for completion.
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
    wildlife_location_information: WildlifeLocationInformation = Field(
        ..., description="Wildlife Location Information"
    )
    street_address__contact_location: StreetAddressContactLocation = Field(
        ..., description="Street Address / Contact Location"
    )
    species_covered: SpeciesCovered = Field(..., description="Species Covered")
    conservation_agent_use_only: ConservationAgentUseOnly = Field(
        ..., description="Conservation Agent Use Only"
    )
    applicant_certification: ApplicantCertification = Field(
        ..., description="Applicant Certification"
    )
