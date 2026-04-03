from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RecipientInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the office or clerk to whom the notice is sent"""

    office_of_planning_and_research: BooleanLike = Field(
        ...,
        description="Check if submitting to the Office of Planning and Research"
    )

    county_clerk: BooleanLike = Field(
        ...,
        description="Check if submitting to the County Clerk"
    )

    county: str = Field(
        ...,
        description=(
            "Name of the county .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )


class SubmittingAgencyInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the public agency submitting the notice"""

    public_agency: str = Field(
        ...,
        description=(
            "Name of the public agency submitting the notice .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    address: str = Field(
        ...,
        description=(
            "Address of the public agency .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )


class ProjectInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details about the project and its location"""

    project_title: str = Field(
        ...,
        description=(
            "Title of the project .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    project_location_specific: str = Field(
        ...,
        description=(
            "Specific location of the project .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    project_location_city: str = Field(
        ...,
        description=(
            "City where the project is located .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    project_location_county: str = Field(
        ...,
        description=(
            "County where the project is located .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    description_of_project: str = Field(
        ...,
        description=(
            "Brief description of the project .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class ApprovalandImplementation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Agencies and persons responsible for project approval and implementation"""

    name_of_public_agency_approving_project: str = Field(
        ...,
        description=(
            "Name of the public agency approving the project .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    name_of_person_or_agency_carrying_out_project: str = Field(
        ...,
        description=(
            "Name of the person or agency carrying out the project .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )


class ExemptStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Exemption status and relevant codes"""

    ministerial_sec_21080_b1_15268: BooleanLike = Field(
        ...,
        description="Check if the project is ministerial under the cited section"
    )

    declared_emergency_sec_21080_b3_15269_a: BooleanLike = Field(
        ...,
        description="Check if the project is a declared emergency under the cited section"
    )

    emergency_project_sec_21080_b4_15269_bc: BooleanLike = Field(
        ...,
        description="Check if the project is an emergency project under the cited section"
    )

    categorical_exemption_state_type_and_section_number: str = Field(
        ...,
        description=(
            "Type and section number for categorical exemption .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    statutory_exemption_state_code_number: str = Field(
        ...,
        description=(
            "State code number for statutory exemption .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )


class ExemptionJustification(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Reasons and explanation for the exemption"""

    reasons_why_project_is_exempt: str = Field(
        ...,
        description=(
            "Explanation of why the project is exempt .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )


class LeadAgencyContact(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Contact information for the lead agency"""

    contact_person: str = Field(
        ...,
        description=(
            "Name of the contact person for the lead agency .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    area_code_telephone_extension: str = Field(
        ...,
        description=(
            "Contact phone number with area code and extension .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )


class ApplicantCertification(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Applicant's certification and filing details"""

    notice_of_exemption_been_filed_by_the_public_agency_approving_the_project_yes: BooleanLike = Field(
        ...,
        description="Check if the notice of exemption has been filed (Yes)"
    )

    notice_of_exemption_been_filed_by_the_public_agency_approving_the_project_no: BooleanLike = Field(
        ...,
        description="Check if the notice of exemption has been filed (No)"
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of authorized person .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    date: str = Field(
        ...,
        description="Date of signature"
    )  # YYYY-MM-DD format

    title: str = Field(
        ...,
        description=(
            "Title of the person signing .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    signed_by_lead_agency: BooleanLike = Field(
        ...,
        description="Check if signed by lead agency"
    )

    signed_by_applicant: BooleanLike = Field(
        ...,
        description="Check if signed by applicant"
    )

    date_received_for_filing_at_opr: str = Field(
        ...,
        description="Date received for filing at Office of Planning and Research"
    )  # YYYY-MM-DD format


class NoticeOfExemptionFormD(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    Notice of Exemption
Form D

    ''
    """

    recipient_information: RecipientInformation = Field(
        ...,
        description="Recipient Information"
    )
    submitting_agency_information: SubmittingAgencyInformation = Field(
        ...,
        description="Submitting Agency Information"
    )
    project_information: ProjectInformation = Field(
        ...,
        description="Project Information"
    )
    approval_and_implementation: ApprovalandImplementation = Field(
        ...,
        description="Approval and Implementation"
    )
    exempt_status: ExemptStatus = Field(
        ...,
        description="Exempt Status"
    )
    exemption_justification: ExemptionJustification = Field(
        ...,
        description="Exemption Justification"
    )
    lead_agency_contact: LeadAgencyContact = Field(
        ...,
        description="Lead Agency Contact"
    )
    applicant_certification: ApplicantCertification = Field(
        ...,
        description="Applicant Certification"
    )