from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class SubmittingFromAgencyInformation(BaseModel):
    """Information about the public agency submitting the notice and county clerk address"""

    from_public_agency: str = Field(
        ...,
        description=(
            "Name of the public agency submitting the notice .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    from_public_agency_address_line_1: str = Field(
        ...,
        description=(
            "Mailing address of the public agency, first line .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    from_public_agency_address_line_2: str = Field(
        default="",
        description=(
            "Mailing address of the public agency, second line (if needed) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    county_of: str = Field(
        ...,
        description=(
            "Name of the county where the clerk is located .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    county_clerk_additional_address_line: str = Field(
        default="",
        description=(
            "Additional address information for the County Clerk, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ProjectInformation(BaseModel):
    """Basic identifying information about the project and its location"""

    project_title: str = Field(
        ...,
        description=(
            'Official title or name of the project .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    project_applicant: str = Field(
        ...,
        description=(
            'Name of the project applicant .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    project_location_specific: str = Field(
        ...,
        description=(
            "Specific location or description of where the project is located .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    project_location_city: str = Field(
        ...,
        description=(
            'City where the project is located .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    project_location_county: str = Field(
        ...,
        description=(
            'County where the project is located .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ProjectDescriptionandResponsibleAgencies(BaseModel):
    """Narrative description of the project and the agencies involved"""

    description_nature_purpose_beneficiaries_line_1: str = Field(
        ...,
        description=(
            "First line of the description of the project's nature, purpose, and "
            'beneficiaries .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    description_nature_purpose_beneficiaries_line_2: str = Field(
        default="",
        description=(
            "Second line of the description of the project's nature, purpose, and "
            'beneficiaries (if needed) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    name_public_agency_approving_project: str = Field(
        ...,
        description=(
            "Name of the public agency that approved the project .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_person_agency_carrying_out_project: str = Field(
        ...,
        description=(
            "Name of the person or agency responsible for carrying out the project .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ExemptStatus(BaseModel):
    """Type of exemption claimed under CEQA"""

    ministerial_sec_21080b1_15268: BooleanLike = Field(
        default="",
        description=(
            "Check if the project is exempt as a ministerial project under Sec. 21080(b)(1); 15268"
        ),
    )

    declared_emergency_sec_21080b3_15269a: BooleanLike = Field(
        default="",
        description=(
            "Check if the project is exempt as a declared emergency under Sec. 21080(b)(3); "
            "15269(a)"
        ),
    )

    emergency_project_sec_21080b4_15269bc: BooleanLike = Field(
        default="",
        description=(
            "Check if the project is exempt as an emergency project under Sec. 21080(b)(4); "
            "15269(b)(c)"
        ),
    )

    categorical_exemption_type_section_number: str = Field(
        default="",
        description=(
            "If a categorical exemption applies, specify the exemption type and section "
            'number .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    statutory_exemptions_code_number: str = Field(
        default="",
        description=(
            "If a statutory exemption applies, specify the code number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ExemptionJustification(BaseModel):
    """Explanation of why the project is exempt"""

    reasons_project_exempt_line_1: str = Field(
        ...,
        description=(
            "First line explaining the reasons the project is exempt .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reasons_project_exempt_line_2: str = Field(
        default="",
        description=(
            "Second line explaining the reasons the project is exempt (if needed) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class LeadAgencyContact(BaseModel):
    """Contact information for the lead agency"""

    lead_agency_contact_person: str = Field(
        ...,
        description=(
            "Name of the lead agency contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    area_code_telephone_extension: str = Field(
        ...,
        description=(
            "Telephone number including area code and extension for the contact person .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class FilingandSignature(BaseModel):
    """Filing status, signatures, and dates"""

    notice_exemption_filed_yes: BooleanLike = Field(
        default="",
        description="Select if a Notice of Exemption has been filed by the approving public agency",
    )

    notice_exemption_filed_no: BooleanLike = Field(
        default="",
        description=(
            "Select if a Notice of Exemption has not been filed by the approving public agency"
        ),
    )

    date: str = Field(..., description="Date the notice is signed")  # YYYY-MM-DD format

    title: str = Field(
        ...,
        description=(
            "Official title of the person signing the notice .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signed_by_lead_agency: BooleanLike = Field(
        default="", description="Indicate if the notice is signed by the lead agency"
    )

    signed_by_applicant: BooleanLike = Field(
        default="", description="Indicate if the notice is signed by the applicant"
    )

    date_received_for_filing_at_opr: str = Field(
        default="",
        description="Date the notice was received for filing at the Office of Planning and Research",
    )  # YYYY-MM-DD format


class NoticeOfExemptionAppendixE(BaseModel):
    """
        Notice of Exemption
    Appendix E

        ''
    """

    submitting__from_agency_information: SubmittingFromAgencyInformation = Field(
        ..., description="Submitting / From Agency Information"
    )
    project_information: ProjectInformation = Field(..., description="Project Information")
    project_description_and_responsible_agencies: ProjectDescriptionandResponsibleAgencies = Field(
        ..., description="Project Description and Responsible Agencies"
    )
    exempt_status: ExemptStatus = Field(..., description="Exempt Status")
    exemption_justification: ExemptionJustification = Field(
        ..., description="Exemption Justification"
    )
    lead_agency_contact: LeadAgencyContact = Field(..., description="Lead Agency Contact")
    filing_and_signature: FilingandSignature = Field(..., description="Filing and Signature")
