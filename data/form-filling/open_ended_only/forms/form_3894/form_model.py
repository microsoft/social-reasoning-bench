from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class FilingInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the agencies and addresses involved in the filing."""

    county_of: str = Field(
        ...,
        description=(
            "Name of the county where the project is located .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    county_clerk_address: str = Field(
        ...,
        description=(
            "Address of the County Clerk .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    public_agency: str = Field(
        ...,
        description=(
            "Name of the public agency submitting the notice .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    public_agency_address: str = Field(
        ...,
        description=(
            "Address of the public agency .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )


class ProjectInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details about the project and its location."""

    project_title: str = Field(
        ...,
        description=(
            "Title of the project .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    project_applicant: str = Field(
        ...,
        description=(
            "Name of the project applicant .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
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

    description_of_nature_purpose_and_beneficiaries_of_project: str = Field(
        ...,
        description=(
            "Describe the nature, purpose, and beneficiaries of the project .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )


class ApprovalandImplementation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about project approval and responsible parties."""

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


class ExemptionStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details regarding the exemption status and reasons."""

    exempt_status_ministerial: BooleanLike = Field(
        ...,
        description="Check if the project is exempt under Ministerial status"
    )

    exempt_status_declared_emergency: BooleanLike = Field(
        ...,
        description="Check if the project is exempt under Declared Emergency status"
    )

    exempt_status_emergency_project: BooleanLike = Field(
        ...,
        description="Check if the project is exempt under Emergency Project status"
    )

    exempt_status_categorical_exemption_state_type_and_section_number: str = Field(
        ...,
        description=(
            "State the type and section number for categorical exemption .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )

    exempt_status_statutory_exemptions_state_code_number: str = Field(
        ...,
        description=(
            "State the code number for statutory exemption .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    reasons_why_project_is_exempt: str = Field(
        ...,
        description=(
            "Provide reasons why the project is exempt .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )


class LeadAgencyContact(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Contact information for the lead agency."""

    lead_agency_contact_person: str = Field(
        ...,
        description=(
            "Name of the contact person at the lead agency .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    area_code_telephone_extension: str = Field(
        ...,
        description=(
            "Phone number including area code and extension .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )


class ApplicantCertification(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Certification and signature fields for the applicant or lead agency."""

    has_notice_of_exemption_been_filed_by_public_agency_approving_the_project_yes: BooleanLike = Field(
        ...,
        description="Indicate Yes if the notice has been filed"
    )

    has_notice_of_exemption_been_filed_by_public_agency_approving_the_project_no: BooleanLike = Field(
        ...,
        description="Indicate No if the notice has not been filed"
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
        description="Date of signing"
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


class FilingReceipt(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Date received for filing at OPR."""

    date_received_for_filing_at_opr: str = Field(
        ...,
        description="Date received for filing at Office of Planning and Research"
    )  # YYYY-MM-DD format


class NoticeOfExemptionAppendixE(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    Notice of Exemption
Appendix E

    ''
    """

    filing_information: FilingInformation = Field(
        ...,
        description="Filing Information"
    )
    project_information: ProjectInformation = Field(
        ...,
        description="Project Information"
    )
    approval_and_implementation: ApprovalandImplementation = Field(
        ...,
        description="Approval and Implementation"
    )
    exemption_status: ExemptionStatus = Field(
        ...,
        description="Exemption Status"
    )
    lead_agency_contact: LeadAgencyContact = Field(
        ...,
        description="Lead Agency Contact"
    )
    applicant_certification: ApplicantCertification = Field(
        ...,
        description="Applicant Certification"
    )
    filing_receipt: FilingReceipt = Field(
        ...,
        description="Filing Receipt"
    )