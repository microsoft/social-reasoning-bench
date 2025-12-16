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
    """Information about the request for independent review and the requesting party"""

    todays_date_month: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month of today's date as a number"
    )

    todays_date_day: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day of today's date as a number"
    )

    todays_date_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year of today's date as a four-digit number"
    )

    name_of_party_requesting_independent_review: str = Field(
        ...,
        description=(
            "Full name of the person requesting the independent review .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    relationship_self: BooleanLike = Field(
        default="", description="Check if the requester is the patient or injured employee"
    )

    relationship_person_acting_on_behalf: BooleanLike = Field(
        default="",
        description="Check if the requester is acting on behalf of the patient or injured employee",
    )

    relationship_provider_acting_on_behalf: BooleanLike = Field(
        default="",
        description=(
            "Check if the requester is a provider acting on behalf of the patient or "
            "injured employee"
        ),
    )

    relationship_provider_received_denial: BooleanLike = Field(
        default="", description="Check if the requester is the provider that received the denial"
    )

    relationship_sub_claimant: BooleanLike = Field(
        default="",
        description="Check if the requester is a sub claimant in a workers’ compensation case",
    )


class ReasonforRequestforReviewbyanIRO(BaseModel):
    """Reason and context for the independent review request"""

    condition_life_threatening_yes: BooleanLike = Field(
        default="", description="Select Yes if the condition is life-threatening"
    )

    condition_life_threatening_no: BooleanLike = Field(
        default="", description="Select No if the condition is not life-threatening"
    )

    review_ordered_by_court_yes: BooleanLike = Field(
        default="", description="Select Yes if the review was ordered by a court"
    )

    review_ordered_by_court_no: BooleanLike = Field(
        default="", description="Select No if the review was not ordered by a court"
    )

    denial_prescription_drugs_current_benefits_yes: BooleanLike = Field(
        default="",
        description=(
            "Select Yes if the denial is for prescription drugs or IV infusions you are "
            "already receiving"
        ),
    )

    denial_prescription_drugs_current_benefits_no: BooleanLike = Field(
        default="",
        description=(
            "Select No if the denial is not for prescription drugs or IV infusions you are "
            "already receiving"
        ),
    )

    denial_exception_step_therapy_yes: BooleanLike = Field(
        default="",
        description=(
            "Select Yes if this is a denial of an exception request to a prescription drug "
            "step therapy protocol"
        ),
    )

    denial_exception_step_therapy_no: BooleanLike = Field(
        default="",
        description=(
            "Select No if this is not a denial of an exception request to a prescription "
            "drug step therapy protocol"
        ),
    )


class DeniedServices(BaseModel):
    """Description of the denied health care services"""

    denied_services_line_1: str = Field(
        ...,
        description=(
            "First line describing the denied health care services, including dates if "
            'already performed .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    denied_services_line_2: str = Field(
        default="",
        description=(
            "Additional description of the denied health care services .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    denied_services_line_3: str = Field(
        default="",
        description=(
            "Additional description of the denied health care services .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    denied_services_line_4: str = Field(
        default="",
        description=(
            "Additional description of the denied health care services .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PatientInjuredEmployeeInformation(BaseModel):
    """Identification and contact information for the patient or injured employee"""

    health_plan_or_claim_identification_number: str = Field(
        ...,
        description=(
            "Health plan ID or workers’ compensation claim number identifying the patient "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    date_of_birth_month: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Month of the patient’s date of birth as a number"
    )

    date_of_birth_day: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Day of the patient’s date of birth as a number"
    )

    date_of_birth_year: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Year of the patient’s date of birth as a four-digit number"
    )

    sex: str = Field(
        ...,
        description=(
            'Sex of the patient (e.g., M or F) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    first_name: str = Field(
        ...,
        description=(
            'Patient’s first name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    middle_name: str = Field(
        default="",
        description=(
            'Patient’s middle name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    last_name: str = Field(
        ...,
        description=(
            'Patient’s last name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
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
            'Street address of the patient .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the patient’s address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State abbreviation for the patient’s address")

    zip_code: str = Field(..., description="ZIP code for the patient’s address")

    phone_area_code: str = Field(
        ...,
        description=(
            "Area code of the patient’s phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        ...,
        description=(
            "Patient’s phone number (remaining digits after area code) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    fax_area_code: str = Field(
        default="",
        description=(
            'Area code of the fax number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    fax_number: str = Field(
        default="",
        description=(
            "Fax number (remaining digits after area code) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            "Email address of the patient or requester .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
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
