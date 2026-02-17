from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RequestInformation(BaseModel):
    """Information about the request for an independent review and the requesting party"""

    todays_date_month: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month of today's date as a number (1–12)"
    )

    todays_date_day: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day of today's date"
    )

    todays_date_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year of today's date (four digits)"
    )

    name_of_party_requesting_independent_review: str = Field(
        ...,
        description=(
            "Full name of the person requesting the independent review .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    self: BooleanLike = Field(
        default="",
        description="Check if the person requesting the review is the patient or injured employee",
    )

    person_acting_on_behalf_of_patient_or_injured_employee: BooleanLike = Field(
        default="",
        description="Check if a non-provider is acting on behalf of the patient or injured employee",
    )

    provider_acting_on_behalf_of_patient_or_injured_employee: BooleanLike = Field(
        default="",
        description=(
            "Check if a health care provider is acting on behalf of the patient or injured employee"
        ),
    )

    provider_that_received_the_denial: BooleanLike = Field(
        default="",
        description="Check if the requesting party is the provider that received the denial",
    )

    sub_claimant_workers_compensation_only: BooleanLike = Field(
        default="",
        description="Check if the requesting party is a sub claimant in a workers’ compensation case",
    )


class ReasonforRequestforReviewbyanIRO(BaseModel):
    """Reason and circumstances for requesting an independent review"""

    is_the_condition_life_threatening_yes: BooleanLike = Field(
        default="", description="Select if the condition is life-threatening"
    )

    is_the_condition_life_threatening_no: BooleanLike = Field(
        default="", description="Select if the condition is not life-threatening"
    )

    is_the_review_ordered_by_a_court_yes: BooleanLike = Field(
        default="", description="Select if the review has been ordered by a court"
    )

    is_the_review_ordered_by_a_court_no: BooleanLike = Field(
        default="", description="Select if the review has not been ordered by a court"
    )

    denial_of_prescription_drugs_or_intravenous_infusions_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if the denial concerns prescription drugs or IV infusions you are "
            "already receiving"
        ),
    )

    denial_of_prescription_drugs_or_intravenous_infusions_no: BooleanLike = Field(
        default="",
        description=(
            "Select if the denial does not concern prescription drugs or IV infusions you "
            "are already receiving"
        ),
    )

    denial_of_exception_request_to_step_therapy_yes: BooleanLike = Field(
        default="",
        description=(
            "Select if this is a denial of an exception request to a prescription drug step "
            "therapy protocol"
        ),
    )

    denial_of_exception_request_to_step_therapy_no: BooleanLike = Field(
        default="",
        description=(
            "Select if this is not a denial of an exception request to a prescription drug "
            "step therapy protocol"
        ),
    )


class DeniedServices(BaseModel):
    """Description of the health care services that are being denied"""

    describe_denied_health_care_services: str = Field(
        ...,
        description=(
            "Describe the denied health care services and include dates if services have "
            'already been performed .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class PatientInjuredEmployeeInformation(BaseModel):
    """Identification and contact information for the patient or injured employee"""

    health_plan_or_claim_identification_number: str = Field(
        ...,
        description=(
            "Health plan ID number or workers’ compensation claim number .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date_of_birth_month: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month of the patient’s date of birth"
    )

    date_of_birth_day: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day of the patient’s date of birth"
    )

    date_of_birth_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year of the patient’s date of birth (four digits)"
    )

    sex: Literal["Male", "Female", "Other", "Unknown", "N/A", ""] = Field(
        ..., description="Sex of the patient or injured employee"
    )

    first_name: str = Field(
        ...,
        description=(
            "Patient’s or injured employee’s first name .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    middle_name: str = Field(
        default="",
        description=(
            "Patient’s or injured employee’s middle name .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            "Patient’s or injured employee’s last name .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    suffix: str = Field(
        default="",
        description=(
            "Name suffix, if any (e.g., Jr., Sr., III) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    street: str = Field(
        ...,
        description=(
            "Street address of the patient or injured employee .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            "City of the patient’s or injured employee’s address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of the patient’s or injured employee’s address")

    zip_code: str = Field(
        ..., description="ZIP code of the patient’s or injured employee’s address"
    )

    phone: str = Field(
        ...,
        description=(
            'Primary phone number with area code .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            "Fax number with area code, if available .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            "Email address of the patient or injured employee .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class RequestFormRequestForAReviewByAnIndependentReviewOrganization(BaseModel):
    """
        REQUEST FORM

    REQUEST FOR A REVIEW BY AN INDEPENDENT REVIEW ORGANIZATION

        ''
    """

    request_information: RequestInformation = Field(..., description="Request Information")
    reason_for_request_for_review_by_an_iro: ReasonforRequestforReviewbyanIRO = Field(
        ..., description="Reason for Request for Review by an IRO"
    )
    denied_services: DeniedServices = Field(..., description="Denied Services")
    patientinjured_employee_information: PatientInjuredEmployeeInformation = Field(
        ..., description="Patient/Injured Employee Information"
    )
