from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FilingRecipient(BaseModel):
    """Agency or office where the notice is being filed"""

    office_of_planning_and_research: BooleanLike = Field(
        default="",
        description=(
            "Check if the Notice of Exemption is being sent to the Office of Planning and Research"
        ),
    )

    county_clerk: BooleanLike = Field(
        default="", description="Check if the Notice of Exemption is being sent to the County Clerk"
    )

    county: str = Field(
        ...,
        description=(
            "Name of the county where the County Clerk is located .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SubmittingAgencyInformation(BaseModel):
    """Public agency submitting the notice and its address"""

    from_public_agency: str = Field(
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
            "Mailing address of the public agency submitting the notice .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProjectInformation(BaseModel):
    """Basic details and location of the project"""

    project_title: str = Field(
        ...,
        description=(
            'Official title or name of the project .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    project_location_specific: str = Field(
        ...,
        description=(
            "Specific location description of the project (e.g., address, parcel number, "
            'landmarks) .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
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

    description_of_project: str = Field(
        ...,
        description=(
            "Brief description of the project and its main components or activities .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ApprovingandCarryingAgencies(BaseModel):
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


class ExemptStatus(BaseModel):
    """Type of exemption claimed for the project"""

    ministerial_sec_21080_b_1_15268: BooleanLike = Field(
        default="",
        description=(
            "Check if the exemption is based on a ministerial project under Sec. 21080(b)(1); 15268"
        ),
    )

    declared_emergency_sec_21080_b_3_15269_a: BooleanLike = Field(
        default="",
        description=(
            "Check if the exemption is based on a declared emergency under Sec. "
            "21080(b)(3); 15269(a)"
        ),
    )

    emergency_project_sec_21080_b_4_15269_b_c: BooleanLike = Field(
        default="",
        description=(
            "Check if the exemption is based on an emergency project under Sec. "
            "21080(b)(4); 15269(b)(c)"
        ),
    )

    categorical_exemption_state_type_and_section_number: str = Field(
        default="",
        description=(
            "If a categorical exemption applies, specify the exemption type and CEQA "
            'section number .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    statutory_exemptions_state_code_number: str = Field(
        default="",
        description=(
            "If a statutory exemption applies, specify the relevant code number .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ExemptionJustification(BaseModel):
    """Explanation of why the project is exempt"""

    reasons_why_project_is_exempt: str = Field(
        ...,
        description=(
            "Explanation of why the project qualifies for the cited exemption(s) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class LeadAgencyContact(BaseModel):
    """Lead agency and primary contact information"""

    lead_agency: str = Field(
        ...,
        description=(
            "Name of the lead agency responsible for CEQA compliance .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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
            "Telephone number for the contact person, including area code and any extension "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class ApplicantCertification(BaseModel):
    """Applicant certification, signature, and filing status"""

    notice_of_exemption_filed_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if a Notice of Exemption has already been filed by the approving public agency"
        ),
    )

    notice_of_exemption_filed_no: BooleanLike = Field(
        default="",
        description=(
            "Select if a Notice of Exemption has not been filed by the approving public agency"
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of the authorized representative .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the form is signed")  # YYYY-MM-DD format

    title: str = Field(
        ...,
        description=(
            "Official title or position of the person signing the form .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signed_by_lead_agency: BooleanLike = Field(
        default="", description="Check if the form is signed by the lead agency"
    )

    signed_by_applicant: BooleanLike = Field(
        default="", description="Check if the form is signed by the applicant"
    )


class OPRFiling(BaseModel):
    """Office of Planning and Research filing information"""

    date_received_for_filing_at_opr: str = Field(
        default="",
        description="Date the Office of Planning and Research received the notice for filing",
    )  # YYYY-MM-DD format


class NoticeOfExemptionFormD(BaseModel):
    """Notice of Exemption
    Form D"""

    filing_recipient: FilingRecipient = Field(..., description="Filing Recipient")
    submitting_agency_information: SubmittingAgencyInformation = Field(
        ..., description="Submitting Agency Information"
    )
    project_information: ProjectInformation = Field(..., description="Project Information")
    approving_and_carrying_agencies: ApprovingandCarryingAgencies = Field(
        ..., description="Approving and Carrying Agencies"
    )
    exempt_status: ExemptStatus = Field(..., description="Exempt Status")
    exemption_justification: ExemptionJustification = Field(
        ..., description="Exemption Justification"
    )
    lead_agency_contact: LeadAgencyContact = Field(..., description="Lead Agency Contact")
    applicant_certification: ApplicantCertification = Field(
        ..., description="Applicant Certification"
    )
    opr_filing: OPRFiling = Field(..., description="OPR Filing")
