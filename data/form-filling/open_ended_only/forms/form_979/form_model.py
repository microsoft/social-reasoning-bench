from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class RequestorInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the party requesting the independent review"""

    todays_date_month: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Month of today's date"
    )

    todays_date_day: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Day of today's date"
    )

    todays_date_year: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Year of today's date"
    )

    name_of_party_requesting_independent_review: str = Field(
        ...,
        description=(
            "Name of the person or entity requesting the review .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    print_last_name_first_name_and_middle_initial: str = Field(
        ...,
        description=(
            "Last name, first name, and middle initial of the requester .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    relationship_to_the_patient_or_injured_employee: Literal["Self", "Person acting on behalf of patient or injured employee", "Provider acting on behalf of patient or injured employee", "Provider that received the denial", "Sub claimant (Workers’ Compensation only)", "N/A", ""] = Field(
        ...,
        description="Relationship of the requester to the patient or injured employee"
    )


class ReasonforRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Details about the reason for requesting the independent review"""

    is_the_condition_life_threatening: BooleanLike = Field(
        ...,
        description="Indicate if the condition is life-threatening"
    )

    is_the_review_ordered_by_a_court: BooleanLike = Field(
        ...,
        description="Indicate if the review was ordered by a court"
    )

    is_this_a_denial_of_prescription_drugs_or_intravenous_infusions_for_which_you_are_already_receiving_benefits: BooleanLike = Field(
        ...,
        description=(
            "Indicate if this is a denial of prescription drugs or intravenous infusions "
            "for which you are already receiving benefits"
        )
    )

    is_this_a_denial_of_an_exception_request_to_a_prescription_drug_step_therapy_protocol: BooleanLike = Field(
        ...,
        description=(
            "Indicate if this is a denial of an exception request to a prescription drug "
            "step therapy protocol"
        )
    )


class DeniedServices(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Description of the health care services that are being denied"""

    describe_the_health_care_services_that_are_being_denied: str = Field(
        ...,
        description=(
            "Description of the health care services being denied, including dates if "
            "applicable .If you cannot fill this, write \"N/A\". If this field should not "
            "be filled by you (for example, it belongs to another person or office), leave "
            "it blank (empty string \"\")."
        )
    )


class PatientInjuredEmployeeInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about the patient or injured employee"""

    health_plan_or_claim_identification_number: str = Field(
        ...,
        description=(
            "Health plan or claim identification number .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    date_of_birth_month: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Month of patient's date of birth"
    )

    date_of_birth_day: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Day of patient's date of birth"
    )

    date_of_birth_year: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description="Year of patient's date of birth"
    )

    sex: Literal["Male", "Female", "Other", "N/A", ""] = Field(
        ...,
        description="Sex of the patient"
    )

    first_name: str = Field(
        ...,
        description=(
            "Patient's first name .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    middle_name: str = Field(
        ...,
        description=(
            "Patient's middle name .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    last_name: str = Field(
        ...,
        description=(
            "Patient's last name .If you cannot fill this, write \"N/A\". If this field "
            "should not be filled by you (for example, it belongs to another person or "
            "office), leave it blank (empty string \"\")."
        )
    )

    suffix: str = Field(
        ...,
        description=(
            "Suffix for the patient's name (e.g., Jr., Sr., III) .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    street: str = Field(
        ...,
        description=(
            "Street address .If you cannot fill this, write \"N/A\". If this field should "
            "not be filled by you (for example, it belongs to another person or office), "
            "leave it blank (empty string \"\")."
        )
    )

    city: str = Field(
        ...,
        description=(
            "City .If you cannot fill this, write \"N/A\". If this field should not be "
            "filled by you (for example, it belongs to another person or office), leave it "
            "blank (empty string \"\")."
        )
    )

    state: str = Field(
        ...,
        description="State"
    )

    zip_code: str = Field(
        ...,
        description="Zip code"
    )

    phone: str = Field(
        ...,
        description=(
            "Phone number .If you cannot fill this, write \"N/A\". If this field should not "
            "be filled by you (for example, it belongs to another person or office), leave "
            "it blank (empty string \"\")."
        )
    )

    fax: str = Field(
        ...,
        description=(
            "Fax number .If you cannot fill this, write \"N/A\". If this field should not "
            "be filled by you (for example, it belongs to another person or office), leave "
            "it blank (empty string \"\")."
        )
    )

    email: str = Field(
        ...,
        description=(
            "Email address .If you cannot fill this, write \"N/A\". If this field should "
            "not be filled by you (for example, it belongs to another person or office), "
            "leave it blank (empty string \"\")."
        )
    )


class RequestFormRequestForAReviewByAnIndependentReviewOrganization(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    REQUEST FORM

REQUEST FOR A REVIEW BY AN INDEPENDENT REVIEW ORGANIZATION

    Request for a review by an Independent Review Organization (IRO) for denied health care or workers' compensation services. This form is used to provide information about the denial, the party requesting the review, and relevant patient or injured employee details. It applies to both health and workers' compensation cases and should be returned to the company that denied the request for services, not to the Texas Department of Insurance.
    """

    requestor_information: RequestorInformation = Field(
        ...,
        description="Requestor Information"
    )
    reason_for_request: ReasonforRequest = Field(
        ...,
        description="Reason for Request"
    )
    denied_services: DeniedServices = Field(
        ...,
        description="Denied Services"
    )
    patientinjured_employee_information: PatientInjuredEmployeeInformation = Field(
        ...,
        description="Patient/Injured Employee Information"
    )