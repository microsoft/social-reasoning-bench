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
    """Member demographics and basic information"""

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
            'Member\'s primary contact phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
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

    date_of_service: str = Field(
        ..., description="Specific date of service for this request"
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
            "Tax Identification Number for the requesting provider .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_requesting_provider: str = Field(
        ...,
        description=(
            "Mailing address for the requesting provider .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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


class ServicingProviderInformation(BaseModel):
    """Details for the servicing provider"""

    servicing_provider: str = Field(
        ...,
        description=(
            "Name of the provider who will be delivering the ABA services .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    tin_servicing_provider: str = Field(
        ...,
        description=(
            "Tax Identification Number for the servicing provider .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_servicing_provider: str = Field(
        ...,
        description=(
            "Mailing address for the servicing provider .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    npi_servicing_provider: str = Field(
        ...,
        description=(
            "National Provider Identifier for the servicing provider .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ServicingFacilityInformation(BaseModel):
    """Details for the servicing facility"""

    servicing_facility: str = Field(
        default="",
        description=(
            "Name of the facility where services will be rendered, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    tin_servicing_facility: str = Field(
        default="",
        description=(
            "Tax Identification Number for the servicing facility .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_servicing_facility: str = Field(
        default="",
        description=(
            "Mailing address for the servicing facility .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    npi_servicing_facility: str = Field(
        default="",
        description=(
            "National Provider Identifier for the servicing facility .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RequestedServicesandCodes(BaseModel):
    """Requested ABA services and associated diagnosis/procedure codes"""

    requested_item_service: str = Field(
        ...,
        description=(
            "Description of the ABA service(s) or item(s) being requested .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    icd_10_codes: str = Field(
        ...,
        description=(
            "ICD-10 diagnosis code(s) related to this request .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    cpt_codes: str = Field(
        ...,
        description=(
            "CPT procedure code(s) for the requested services .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ExpeditedReviewandInNetworkBenefits(BaseModel):
    """Information related to expedited review and in-network benefit exceptions"""

    explanation_required_expedite: str = Field(
        default="",
        description=(
            "Clinical explanation supporting the need for expedited review .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    new_patient: BooleanLike = Field(
        default="", description="Check if the member is a new patient to this provider"
    )

    established_patient: BooleanLike = Field(
        default="", description="Check if the member is an established patient with this provider"
    )

    date_last_seen: str = Field(
        default="", description="Most recent date the member was seen by this provider"
    )  # YYYY-MM-DD format

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

    name_utilization_review_contact: str = Field(
        ...,
        description=(
            "Name of the utilization review contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_utilization_review_contact: str = Field(
        ...,
        description=(
            "Phone number for the utilization review contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    fax_utilization_review_contact: str = Field(
        ...,
        description=(
            "Fax number for the utilization review contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProvidenceHealthPlanAbaPriorAuthorizationRequest(BaseModel):
    """
        PROVIDENCE Health Plan

    ABA Prior Authorization Request

        Note: This form may only be used to request ABA services.
    """

    member_information: MemberInformation = Field(..., description="Member Information")
    requesting_provider_information: RequestingProviderInformation = Field(
        ..., description="Requesting Provider Information"
    )
    servicing_provider_information: ServicingProviderInformation = Field(
        ..., description="Servicing Provider Information"
    )
    servicing_facility_information: ServicingFacilityInformation = Field(
        ..., description="Servicing Facility Information"
    )
    requested_services_and_codes: RequestedServicesandCodes = Field(
        ..., description="Requested Services and Codes"
    )
    expedited_review_and_in_network_benefits: ExpeditedReviewandInNetworkBenefits = Field(
        ..., description="Expedited Review and In-Network Benefits"
    )
    utilization_review_contact_information: UtilizationReviewContactInformation = Field(
        ..., description="Utilization Review Contact Information"
    )
