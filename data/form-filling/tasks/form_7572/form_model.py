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
    """Basic information about the member and admission details"""

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

    insurance_id: str = Field(
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
            'Member\'s mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_admit: str = Field(
        ..., description="Date the member was admitted for services"
    )  # YYYY-MM-DD format

    date_span_requested: str = Field(
        ...,
        description=(
            "Range of dates for which authorization is requested .If you cannot fill this, "
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


class RequestingProvider(BaseModel):
    """Information about the requesting provider"""

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


class AttendingProvider(BaseModel):
    """Information about the attending provider"""

    attending_provider: str = Field(
        default="",
        description=(
            'Name of the attending provider .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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


class TreatingFacility(BaseModel):
    """Information about the treating facility"""

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
    """Details of the requested level of care and diagnosis/procedure codes"""

    requested_level_of_care_asam_level: str = Field(
        ...,
        description=(
            "Requested level of care or ASAM level for services .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
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
            "Revenue and/or CPT procedure code or codes for requested services .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    mental_health: BooleanLike = Field(
        ..., description="Check if the request is for mental health services"
    )

    substance_use: BooleanLike = Field(
        ..., description="Check if the request is for substance use services"
    )


class ExpeditedandInNetworkJustification(BaseModel):
    """Justification for expedited review and out-of-network use"""

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
    """Contact information for utilization review"""

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


class ProvidenceBehavioralHealthInpatientResidentialAuthRequest(BaseModel):
    """
        PROVIDENCE
    Health Plan

    Facility Based Behavioral Health
    Inpatient, Residential, Partial Hospitalization and IOP
    Prior Authorization Request

        Facility Based Behavioral Health Inpatient, Residential, Partial Hospitalization and IOP Prior Authorization Request. This form is used to request prior authorization for facility-based behavioral health services (mental health or substance use) for Providence Health Plan and Providence Medicare Advantage Plan members; chart notes are required, and it cannot be used to request ABA therapy, TMS, or outpatient behavioral health services.
    """

    member_information: MemberInformation = Field(..., description="Member Information")
    requesting_provider: RequestingProvider = Field(..., description="Requesting Provider")
    attending_provider: AttendingProvider = Field(..., description="Attending Provider")
    treating_facility: TreatingFacility = Field(..., description="Treating Facility")
    service_request_details: ServiceRequestDetails = Field(
        ..., description="Service Request Details"
    )
    expedited_and_in_network_justification: ExpeditedandInNetworkJustification = Field(
        ..., description="Expedited and In-Network Justification"
    )
    utilization_review_contact_information: UtilizationReviewContactInformation = Field(
        ..., description="Utilization Review Contact Information"
    )
