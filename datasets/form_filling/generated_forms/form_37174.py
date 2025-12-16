from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FilingandAgencyInformation(BaseModel):
    """Originating public agency and county clerk information"""

    from_public_agency: str = Field(
        ...,
        description=(
            "Name of the public agency submitting this notice .If you cannot fill this, "
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
            'Name of the county clerk\'s county .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    county_address_line_1: str = Field(
        ...,
        description=(
            "County clerk office address, first line .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    county_address_line_2: str = Field(
        default="",
        description=(
            "County clerk office address, second line (if needed) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectInformation(BaseModel):
    """Basic details about the project and its location"""

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
            "Specific location description of the project (e.g., address, parcel number) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    project_location_city: str = Field(
        default="",
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

    description_of_nature_purpose_and_beneficiaries_of_project_line_1: str = Field(
        ...,
        description=(
            "First line of the description of the project's nature, purpose, and "
            'beneficiaries .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    description_of_nature_purpose_and_beneficiaries_of_project_line_2: str = Field(
        default="",
        description=(
            "Second line of the description of the project's nature, purpose, and "
            'beneficiaries (if needed) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class ApprovalandImplementation(BaseModel):
    """Agencies responsible for approving and carrying out the project"""

    name_of_public_agency_approving_project: str = Field(
        ...,
        description=(
            "Name of the public agency that approved the project .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_of_person_or_agency_carrying_out_project: str = Field(
        ...,
        description=(
            "Name of the person or agency responsible for carrying out the project .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ExemptionStatus(BaseModel):
    """Type and basis of exemption being claimed"""

    ministerial_sec_21080_b_1_15268: BooleanLike = Field(
        default="",
        description=(
            "Check if the project is exempt as a ministerial project under Sec. 21080(b)(1); 15268"
        ),
    )

    declared_emergency_sec_21080_b_3_15269_a: BooleanLike = Field(
        default="",
        description=(
            "Check if the project is exempt as a declared emergency under Sec. 21080(b)(3); "
            "15269(a)"
        ),
    )

    emergency_project_sec_21080_b_4_15269_b_c: BooleanLike = Field(
        default="",
        description=(
            "Check if the project is exempt as an emergency project under Sec. 21080(b)(4); "
            "15269(b)(c)"
        ),
    )

    categorical_exemption_state_type_and_section_number: str = Field(
        default="",
        description=(
            "If categorical exemption applies, specify the exemption type and section "
            'number .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    statutory_exemptions_state_code_number: str = Field(
        default="",
        description=(
            "If statutory exemption applies, specify the code number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    reasons_why_project_is_exempt_line_1: str = Field(
        ...,
        description=(
            "First line explaining the reasons the project qualifies for exemption .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reasons_why_project_is_exempt_line_2: str = Field(
        default="",
        description=(
            "Second line explaining the reasons the project qualifies for exemption (if "
            'needed) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class LeadAgencyContact(BaseModel):
    """Lead agency contact person and phone information"""

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
            "Telephone number including area code and extension for the lead agency contact "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class ApplicantFilingandCertification(BaseModel):
    """Applicant filing status, signature, and authorization"""

    notice_of_exemption_filed_yes: BooleanLike = Field(
        default="",
        description=(
            "Indicate YES if a Notice of Exemption has been filed by the approving public agency"
        ),
    )

    notice_of_exemption_filed_no: BooleanLike = Field(
        default="",
        description=(
            "Indicate NO if a Notice of Exemption has not been filed by the approving public agency"
        ),
    )

    signature: str = Field(
        ...,
        description=(
            'Authorized signer’s signature .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the notice is signed")  # YYYY-MM-DD format

    title: str = Field(
        ...,
        description=(
            "Title or position of the person signing .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    signed_by_lead_agency: BooleanLike = Field(
        default="", description="Check if the notice is signed on behalf of the lead agency"
    )

    signed_by_applicant: BooleanLike = Field(
        default="", description="Check if the notice is signed by the applicant"
    )


class OPRFiling(BaseModel):
    """Office of Planning and Research filing information"""

    date_received_for_filing_at_opr: str = Field(
        default="", description="Date the Office of Planning and Research received the filing"
    )  # YYYY-MM-DD format


class NoticeOfExemption(BaseModel):
    """
    Notice of Exemption

    ''
    """

    filing_and_agency_information: FilingandAgencyInformation = Field(
        ..., description="Filing and Agency Information"
    )
    project_information: ProjectInformation = Field(..., description="Project Information")
    approval_and_implementation: ApprovalandImplementation = Field(
        ..., description="Approval and Implementation"
    )
    exemption_status: ExemptionStatus = Field(..., description="Exemption Status")
    lead_agency_contact: LeadAgencyContact = Field(..., description="Lead Agency Contact")
    applicant_filing_and_certification: ApplicantFilingandCertification = Field(
        ..., description="Applicant Filing and Certification"
    )
    opr_filing: OPRFiling = Field(..., description="OPR Filing")
