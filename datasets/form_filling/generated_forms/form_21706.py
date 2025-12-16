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
            "Name of the public agency submitting the notice .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    from_public_agency_address_line_1: str = Field(
        ...,
        description=(
            "First line of the public agency's mailing address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    from_public_agency_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the public agency's mailing address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    from_public_agency_address_line_3: str = Field(
        default="",
        description=(
            "Third line of the public agency's mailing address, if needed .If you cannot "
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

    county_address_line_1: str = Field(
        ...,
        description=(
            "First line of the county clerk's address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    county_address_line_2: str = Field(
        default="",
        description=(
            "Second line of the county clerk's address, if needed .If you cannot fill this, "
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
            "Specific location or description of where the project is situated .If you "
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

    description_of_nature_purpose_and_beneficiaries_of_project: str = Field(
        ...,
        description=(
            "Narrative description of the project's nature, purpose, and beneficiaries .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

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
    """Type of exemption claimed and reasons"""

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

    reasons_why_project_is_exempt: str = Field(
        ...,
        description=(
            "Explanation supporting the exemption determination .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class LeadAgencyContact(BaseModel):
    """Lead agency contact person and phone"""

    contact_person: str = Field(
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


class ApplicantFilingandSignature(BaseModel):
    """Applicant filing status and signature details"""

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


class OPRFilingInformation(BaseModel):
    """Office of Planning and Research filing receipt date"""

    date_received_for_filing_at_opr: str = Field(
        default="", description="Date the Office of Planning and Research received the filing"
    )  # YYYY-MM-DD format


class NoticeOfExemptionAppendixE(BaseModel):
    """Notice of Exemption
    Appendix E"""

    filing_and_agency_information: FilingandAgencyInformation = Field(
        ..., description="Filing and Agency Information"
    )
    project_information: ProjectInformation = Field(..., description="Project Information")
    exemption_status: ExemptionStatus = Field(..., description="Exemption Status")
    lead_agency_contact: LeadAgencyContact = Field(..., description="Lead Agency Contact")
    applicant_filing_and_signature: ApplicantFilingandSignature = Field(
        ..., description="Applicant Filing and Signature"
    )
    opr_filing_information: OPRFilingInformation = Field(..., description="OPR Filing Information")
