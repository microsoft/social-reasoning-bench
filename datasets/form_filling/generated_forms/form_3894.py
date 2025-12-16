from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RecipientandFilingInformation(BaseModel):
    """Information about the public agency and county clerk to whom the notice is directed"""

    public_agency: str = Field(
        ...,
        description=(
            "Name of the public agency submitting the notice .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Mailing address of the public agency .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    county_of: str = Field(
        ...,
        description=(
            'Name of the county clerk’s county .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class ProjectInformation(BaseModel):
    """Basic identifying information about the project and applicant"""

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
            "Specific location description of the project (e.g., address, cross streets, "
            'parcel number) .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
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

    description_of_nature_purpose_and_beneficiaries_of_project: str = Field(
        ...,
        description=(
            "Narrative description of the project, its purpose, and who benefits .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AgencyApprovalsandResponsibleParties(BaseModel):
    """Agencies and persons responsible for approving and carrying out the project"""

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


class ExemptStatus(BaseModel):
    """Type of exemption claimed under CEQA"""

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
            "If categorical exemption applies, specify the exemption type and CEQA section "
            'number .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    statutory_exemptions_state_code_number: str = Field(
        default="",
        description=(
            "If statutory exemption applies, specify the code section number .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class ExemptionJustification(BaseModel):
    """Explanation of why the project is exempt"""

    reasons_why_project_is_exempt: str = Field(
        ...,
        description=(
            "Explanation supporting the exemption determination .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LeadAgencyContact(BaseModel):
    """Lead agency and contact information"""

    lead_agency: str = Field(
        ...,
        description=(
            "Name of the lead agency for the project .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_person: str = Field(
        ...,
        description=(
            "Primary contact person at the lead agency .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    area_code_telephone_extension: str = Field(
        ...,
        description=(
            "Contact phone number including area code and extension .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ApplicantFilingInformation(BaseModel):
    """Information completed if filed by applicant, including prior filing status"""

    notice_of_exemption_filed_yes: BooleanLike = Field(
        default="",
        description="Select if a Notice of Exemption has been filed by the approving public agency",
    )

    notice_of_exemption_filed_no: BooleanLike = Field(
        default="",
        description=(
            "Select if a Notice of Exemption has not been filed by the approving public agency"
        ),
    )


class CertificationandSignature(BaseModel):
    """Signature block and indication of who signed"""

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
            'Title or position of the signer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    signed_by_lead_agency: BooleanLike = Field(
        default="", description="Indicate if the form is signed on behalf of the lead agency"
    )

    signed_by_applicant: BooleanLike = Field(
        default="", description="Indicate if the form is signed by the applicant"
    )


class OPRFiling(BaseModel):
    """Office of Planning and Research filing date"""

    date_received_for_filing_at_opr: str = Field(
        default="", description="Date the Office of Planning and Research received the filing"
    )  # YYYY-MM-DD format


class NoticeOfExemptionAppendixE(BaseModel):
    """
        Notice of Exemption
    Appendix E

        ''
    """

    recipient_and_filing_information: RecipientandFilingInformation = Field(
        ..., description="Recipient and Filing Information"
    )
    project_information: ProjectInformation = Field(..., description="Project Information")
    agency_approvals_and_responsible_parties: AgencyApprovalsandResponsibleParties = Field(
        ..., description="Agency Approvals and Responsible Parties"
    )
    exempt_status: ExemptStatus = Field(..., description="Exempt Status")
    exemption_justification: ExemptionJustification = Field(
        ..., description="Exemption Justification"
    )
    lead_agency_contact: LeadAgencyContact = Field(..., description="Lead Agency Contact")
    applicant_filing_information: ApplicantFilingInformation = Field(
        ..., description="Applicant Filing Information"
    )
    certification_and_signature: CertificationandSignature = Field(
        ..., description="Certification and Signature"
    )
    opr_filing: OPRFiling = Field(..., description="OPR Filing")
