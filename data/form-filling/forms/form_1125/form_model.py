from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class SubmittingAgencies(BaseModel):
    """Agencies and address information for where the notice is sent"""

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
    """Core details about the project and its location"""

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


class ApprovingandImplementingAgencies(BaseModel):
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

    ministerial_sec_21080_b1_15268: BooleanLike = Field(
        default="",
        description=(
            "Check if the project is exempt as a ministerial project under Sec. 21080(b)(1); 15268"
        ),
    )

    declared_emergency_sec_21080_b3_15269_a: BooleanLike = Field(
        default="",
        description=(
            "Check if the project is exempt as a declared emergency under Sec. 21080(b)(3); "
            "15269(a)"
        ),
    )

    emergency_project_sec_21080_b4_15269_b_c: BooleanLike = Field(
        default="",
        description=(
            "Check if the project is exempt as an emergency project under Sec. 21080(b)(4); "
            "15269(b)(c)"
        ),
    )

    categorical_exemption_state_type_and_section_number: str = Field(
        default="",
        description=(
            "If a categorical exemption applies, specify the exemption type and section "
            'number .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    statutory_exemptions_state_code_number: str = Field(
        default="",
        description=(
            "If a statutory exemption applies, specify the code number .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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
    """Lead agency and primary contact information"""

    lead_agency: str = Field(
        ...,
        description=(
            'Name of the lead agency .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
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

    contact_person: str = Field(
        ...,
        description=(
            "Name of the primary contact person for this notice .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class FilingInformation(BaseModel):
    """Information related to filing and signature of the notice"""

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

    date: str = Field(..., description="Date the notice is signed")  # YYYY-MM-DD format

    title: str = Field(
        ...,
        description=(
            'Official title of the signatory .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    signed_by_lead_agency: BooleanLike = Field(
        default="", description="Check if the notice is signed by the lead agency"
    )

    signed_by_applicant: BooleanLike = Field(
        default="", description="Check if the notice is signed by the applicant"
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

    submitting_agencies: SubmittingAgencies = Field(..., description="Submitting Agencies")
    project_information: ProjectInformation = Field(..., description="Project Information")
    approving_and_implementing_agencies: ApprovingandImplementingAgencies = Field(
        ..., description="Approving and Implementing Agencies"
    )
    exempt_status: ExemptStatus = Field(..., description="Exempt Status")
    exemption_justification: ExemptionJustification = Field(
        ..., description="Exemption Justification"
    )
    lead_agency_contact: LeadAgencyContact = Field(..., description="Lead Agency Contact")
    filing_information: FilingInformation = Field(..., description="Filing Information")
