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
    """Member demographics and admission details"""

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
            "Member's Providence insurance ID number .If you cannot fill this, write "
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
            'Member\'s mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_admit: str = Field(
        ..., description="Date the member was admitted to the facility or level of care"
    )  # YYYY-MM-DD format

    date_span_requested: str = Field(
        ...,
        description=(
            "Requested date range for authorization (from–to) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_care_physician_pcp: str = Field(
        default="",
        description=(
            "Name of the member's primary care physician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class RequestingProviderInformation(BaseModel):
    """Details for the requesting provider"""

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
            "Tax Identification Number of the requesting provider .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_requesting_provider: str = Field(
        ...,
        description=(
            "Mailing address of the requesting provider .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    npi_requesting_provider: str = Field(
        ...,
        description=(
            "National Provider Identifier of the requesting provider .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AttendingProviderInformation(BaseModel):
    """Details for the attending provider"""

    attending_provider: str = Field(
        default="",
        description=(
            "Name of the attending provider responsible for the member's care .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    tin_attending_provider: str = Field(
        default="",
        description=(
            "Tax Identification Number of the attending provider .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_attending_provider: str = Field(
        default="",
        description=(
            "Mailing address of the attending provider .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    npi_attending_provider: str = Field(
        default="",
        description=(
            "National Provider Identifier of the attending provider .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class TreatingFacilityInformation(BaseModel):
    """Details for the treating facility"""

    treating_facility: str = Field(
        ...,
        description=(
            "Name of the facility where the member is receiving treatment .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    tin_treating_facility: str = Field(
        ...,
        description=(
            "Tax Identification Number of the treating facility .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_treating_facility: str = Field(
        ...,
        description=(
            "Mailing address of the treating facility .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    npi_treating_facility: str = Field(
        ...,
        description=(
            "National Provider Identifier of the treating facility .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ServiceRequestDetails(BaseModel):
    """Clinical and service-level information for the authorization request"""

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
            "ICD-10 diagnosis code or codes related to this request .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    revenue_cpt_codes: str = Field(
        ...,
        description=(
            "Relevant revenue and/or CPT procedure codes for the requested services .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mental_health: BooleanLike = Field(
        default="", description="Check if the request is for mental health services"
    )

    substance_use: BooleanLike = Field(
        default="", description="Check if the request is for substance use services"
    )

    explanation_required_expedite: str = Field(
        default="",
        description=(
            "Explanation and supporting details for requesting expedited review .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    explanation_required_in_network_benefits: str = Field(
        default="",
        description=(
            "Explanation why services cannot be provided by an in-network provider or "
            'facility .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
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


class pythonProvidenceHealthBehavioralHealthAuthRequest(BaseModel):
    """
        PROVIDENCE Health Plan

    Facility Based Behavioral Health
    Inpatient, Residential, Partial Hospitalization and IOP
    Prior Authorization Request

        Facility Based Behavioral Health Inpatient, Residential, Partial Hospitalization and IOP Prior Authorization Request. Chart Notes Required. NOTE: This form cannot be used to request ABA therapy, TMS or outpatient behavioral health services.
    """

    member_information: MemberInformation = Field(..., description="Member Information")
    requesting_provider_information: RequestingProviderInformation = Field(
        ..., description="Requesting Provider Information"
    )
    attending_provider_information: AttendingProviderInformation = Field(
        ..., description="Attending Provider Information"
    )
    treating_facility_information: TreatingFacilityInformation = Field(
        ..., description="Treating Facility Information"
    )
    service_request_details: ServiceRequestDetails = Field(
        ..., description="Service Request Details"
    )
    utilization_review_contact_information: UtilizationReviewContactInformation = Field(
        ..., description="Utilization Review Contact Information"
    )
