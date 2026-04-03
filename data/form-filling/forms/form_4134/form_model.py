from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RecipientInformation(BaseModel):
    """Information about the office or county clerk to which the notice is sent"""

    office_of_planning_and_research: BooleanLike = Field(
        default="",
        description=(
            "Check if the Notice of Exemption is being sent to the Office of Planning and Research"
        ),
    )

    county_clerk: BooleanLike = Field(
        default="", description="Check if the Notice of Exemption is being sent to the County Clerk"
    )

    county_of: str = Field(
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
            "Name of the public agency submitting the Notice of Exemption .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    from_address: str = Field(
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
            "Specific location details of the project (e.g., address, coordinates, parcel "
            'number) .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
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

    description_of_project: str = Field(
        ...,
        description=(
            "Narrative description of the project, including main components and activities "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
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
    """Type of exemption claimed and supporting reasons"""

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
            "If a categorical exemption applies, specify the exemption type and CEQA "
            'section number .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    statutory_exemptions_state_code_number: str = Field(
        default="",
        description=(
            "If a statutory exemption applies, specify the applicable code number .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    reasons_why_project_is_exempt: str = Field(
        ...,
        description=(
            "Explanation of why the project qualifies for the selected exemption .If you "
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
            "Name of the lead agency contact person for this project .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    area_code_telephone_extension: str = Field(
        ...,
        description=(
            "Telephone number, including area code and extension, for the lead agency "
            'contact person .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class FilingandCertification(BaseModel):
    """Applicant filing details, certification, and signatures"""

    notice_of_exemption_filed_yes: BooleanLike = Field(
        default="",
        description=(
            "Check if a Notice of Exemption has already been filed by the approving public agency"
        ),
    )

    notice_of_exemption_filed_no: BooleanLike = Field(
        default="",
        description=(
            "Check if a Notice of Exemption has not been filed by the approving public agency"
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

    date: str = Field(
        ..., description="Date the Notice of Exemption is signed"
    )  # YYYY-MM-DD format

    title: str = Field(
        ...,
        description=(
            "Title or position of the person signing the notice .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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
        description=(
            "Date the Notice of Exemption was received for filing at the Office of Planning "
            "and Research"
        ),
    )  # YYYY-MM-DD format


class NoticeOfExemptionFormD(BaseModel):
    """
    Notice of Exemption                                                                 Form D

    ''
    """

    recipient_information: RecipientInformation = Field(..., description="Recipient Information")
    submitting_agency_information: SubmittingAgencyInformation = Field(
        ..., description="Submitting Agency Information"
    )
    project_information: ProjectInformation = Field(..., description="Project Information")
    exemption_status: ExemptionStatus = Field(..., description="Exemption Status")
    lead_agency_contact: LeadAgencyContact = Field(..., description="Lead Agency Contact")
    filing_and_certification: FilingandCertification = Field(
        ..., description="Filing and Certification"
    )
