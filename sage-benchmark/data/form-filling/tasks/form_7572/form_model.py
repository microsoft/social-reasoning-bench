from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MemberInformation(BaseModel):
    """Basic information about the member"""

    last_name: str = Field(
        ...,
        description=(
            'Member\'s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Member\'s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    insurance_id_number: str = Field(
        ...,
        description=(
            "Member's insurance identification number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    dob: str = Field(..., description="Member's date of birth")  # YYYY-MM-DD format

    phone: str = Field(
        ...,
        description=(
            'Member\'s primary phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Member's mailing or residential address .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_admit: str = Field(
        ..., description="Member's admission date for this episode of care"
    )  # YYYY-MM-DD format

    date_span_requested: str = Field(
        ...,
        description=(
            "Requested date range for authorization (from–to) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ProviderandFacilityInformation(BaseModel):
    """PCP, requesting/attending providers, and treating facility details"""

    primary_care_physician_pcp: str = Field(
        default="",
        description=(
            "Name of the member's primary care physician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    requesting_provider: str = Field(
        ...,
        description=(
            "Name of the provider requesting authorization .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    tin_requesting_provider: str = Field(
        ...,
        description=(
            "Tax Identification Number for the requesting provider .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_requesting_provider: str = Field(
        ...,
        description=(
            "Mailing or practice address of the requesting provider .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    npi_requesting_provider: str = Field(
        ...,
        description=(
            "National Provider Identifier for the requesting provider .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    attending_provider: str = Field(
        default="",
        description=(
            "Name of the attending provider responsible for care .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tin_attending_provider: str = Field(
        default="",
        description=(
            "Tax Identification Number for the attending provider .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_attending_provider: str = Field(
        default="",
        description=(
            "Mailing or practice address of the attending provider .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    npi_attending_provider: str = Field(
        default="",
        description=(
            "National Provider Identifier for the attending provider .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    treating_facility: str = Field(
        ...,
        description=(
            "Name of the facility where treatment is being provided .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tin_treating_facility: str = Field(
        ...,
        description=(
            "Tax Identification Number for the treating facility .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_treating_facility: str = Field(
        ...,
        description=(
            'Address of the treating facility .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    npi_treating_facility: str = Field(
        ...,
        description=(
            "National Provider Identifier for the treating facility .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ServiceRequestDetails(BaseModel):
    """Requested level of care and coding information"""

    requested_level_of_care_asam_level: str = Field(
        ...,
        description=(
            "Requested level of care or ASAM level for this authorization .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    icd_10_codes: str = Field(
        ...,
        description=(
            "Relevant ICD-10 diagnosis code or codes .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    revenue_cpt_codes: str = Field(
        ...,
        description=(
            "Applicable revenue and/or CPT procedure codes .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mental_health: BooleanLike = Field(
        default="", description="Check if the request is for mental health services"
    )

    substance_use: BooleanLike = Field(
        default="", description="Check if the request is for substance use services"
    )


class AuthorizationJustification(BaseModel):
    """Explanations for expedited review and out-of-network use"""

    explanation_required_expedite: str = Field(
        default="",
        description=(
            "Explanation and supporting details for requesting an expedited review .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    explanation_required_in_network_benefits: str = Field(
        default="",
        description=(
            "Explanation why services cannot be provided by an in-network provider/facility "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class UtilizationReviewContactInformation(BaseModel):
    """Contact details for utilization review"""

    name_utilization_review_contact_information: str = Field(
        ...,
        description=(
            "Name of the utilization review contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_utilization_review_contact_information: str = Field(
        ...,
        description=(
            "Phone number for the utilization review contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    fax_utilization_review_contact_information: str = Field(
        ...,
        description=(
            "Fax number for the utilization review contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProvidenceFacilityBasedBehavioralHealthAuthorizationRequest(BaseModel):
    """
    Providence Facility Based Behavioral Health Authorization Request

    Providence Facility Based Behavioral Health Authorization Request
    """

    member_information: MemberInformation = Field(..., description="Member Information")
    provider_and_facility_information: ProviderandFacilityInformation = Field(
        ..., description="Provider and Facility Information"
    )
    service_request_details: ServiceRequestDetails = Field(
        ..., description="Service Request Details"
    )
    authorization_justification: AuthorizationJustification = Field(
        ..., description="Authorization Justification"
    )
    utilization_review_contact_information: UtilizationReviewContactInformation = Field(
        ..., description="Utilization Review Contact Information"
    )
