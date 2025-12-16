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
    """Member demographics and coverage details"""

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

    address: str = Field(
        ...,
        description=(
            'Member\'s mailing address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_service: str = Field(
        ..., description="Date the service is scheduled or was provided"
    )  # YYYY-MM-DD format

    date_span_requested: str = Field(
        default="",
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
    """Details for the provider requesting authorization"""

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


class ServicingProviderInformation(BaseModel):
    """Details for the provider rendering services"""

    servicing_provider: str = Field(
        default="",
        description=(
            "Name of the provider who will render the service .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tin_servicing_provider: str = Field(
        default="",
        description=(
            "Tax Identification Number of the servicing provider .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_servicing_provider: str = Field(
        default="",
        description=(
            "Mailing address of the servicing provider .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    npi_servicing_provider: str = Field(
        default="",
        description=(
            "National Provider Identifier of the servicing provider .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ServicingFacilityInformation(BaseModel):
    """Details for the facility where services will be provided"""

    servicing_facility: str = Field(
        default="",
        description=(
            "Name of the facility where services will be provided .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    tin_servicing_facility: str = Field(
        default="",
        description=(
            "Tax Identification Number of the servicing facility .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_servicing_facility: str = Field(
        default="",
        description=(
            "Mailing address of the servicing facility .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    npi_servicing_facility: str = Field(
        default="",
        description=(
            "National Provider Identifier of the servicing facility .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RequestedServices(BaseModel):
    """Requested item/service and related codes and visit details"""

    requested_item_service: str = Field(
        ...,
        description=(
            "Description of the item or service for which authorization is requested .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
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

    cpt_codes: str = Field(
        ...,
        description=(
            "CPT procedure code or codes related to this request .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    office_visits_number_of_visits: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of office visits being requested"
    )

    surgery: BooleanLike = Field(
        default="", description="Check if surgical services are being requested"
    )

    diagnostic: BooleanLike = Field(
        default="", description="Check if diagnostic services are being requested"
    )

    facility_auth_only: BooleanLike = Field(
        default="", description="Check if authorization is requested for facility only"
    )

    dme: BooleanLike = Field(
        default="", description="Check if durable medical equipment (DME) is being requested"
    )

    other_requested_services: str = Field(
        default="",
        description=(
            "Describe any other type of requested service not listed .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    elective_inpatient_admit: BooleanLike = Field(
        default="", description="Check if the request is for an elective inpatient admission"
    )

    elective_outpatient_surgery: BooleanLike = Field(
        default="", description="Check if the request is for elective outpatient surgery"
    )

    office_surgery: BooleanLike = Field(
        default="", description="Check if the request is for surgery performed in an office setting"
    )

    outpatient_diagnostics: BooleanLike = Field(
        default="", description="Check if the request is for outpatient diagnostic services"
    )

    asc: BooleanLike = Field(
        default="",
        description="Check if the request is for services at an ambulatory surgery center (ASC)",
    )


class ExpeditedReview(BaseModel):
    """Information required to justify expedited review"""

    explanation_required_expedite: str = Field(
        default="",
        description=(
            "Explanation and supporting details for requesting expedited review .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class InNetworkBenefits(BaseModel):
    """Information about patient status and in-network justification"""

    new_patient: BooleanLike = Field(
        default="", description="Check if the member is a new patient to this provider"
    )

    established_patient: BooleanLike = Field(
        default="", description="Check if the member is an established patient with this provider"
    )

    date_last_seen: str = Field(
        default="", description="Date the member was last seen by this provider"
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


class ContactInformation(BaseModel):
    """Required contact details for this request"""

    name_contact_information: str = Field(
        ...,
        description=(
            "Name of the contact person for this authorization request .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_contact_information: str = Field(
        ...,
        description=(
            'Phone number for the contact person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    fax_contact_information: str = Field(
        ...,
        description=(
            "Fax number for the contact person or office .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ProvidenceMedicareAdvantagePriorAuthRequest(BaseModel):
    """
    PROVIDENCE Health Plan Prior Authorization Request PROVIDENCE Medicare Advantage Plans

    ''
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
    requested_services: RequestedServices = Field(..., description="Requested Services")
    expedited_review: ExpeditedReview = Field(..., description="Expedited Review")
    in_network_benefits: InNetworkBenefits = Field(..., description="In-Network Benefits")
    contact_information: ContactInformation = Field(..., description="Contact Information")
