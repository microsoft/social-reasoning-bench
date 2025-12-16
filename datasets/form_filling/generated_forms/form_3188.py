from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PatientPersonalInformation(BaseModel):
    """Basic identifying and demographic details about the patient"""

    name: str = Field(
        ...,
        description=(
            'Patient\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street address .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of residence .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    postcode: str = Field(..., description="Postal code")

    national_identification_number: str = Field(
        ...,
        description=(
            'National identification or ID number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        ...,
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    e_mail_address: str = Field(
        ...,
        description=(
            'Email address .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Date of birth")  # YYYY-MM-DD format

    age: Union[float, Literal["N/A", ""]] = Field(..., description="Age in years")

    place_of_birth: str = Field(
        default="",
        description=(
            'City and country of birth .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    sex: str = Field(
        ...,
        description=(
            'Sex or gender .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    height: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Height (specify units, e.g. cm)"
    )

    weight: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Weight (specify units, e.g. kg)"
    )


class MedicalHistory(BaseModel):
    """Current health status, past illnesses, surgeries, and co-existing diseases"""

    please_briefly_describe_your_health: str = Field(
        ...,
        description=(
            "Short description of current health status and main complaints .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    please_list_your_underlying_illness_and_any_accidents_or_surgeries_year: str = Field(
        ...,
        description=(
            "List chronic illnesses and any accidents or surgeries with year .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    co_existing_diseases_eg_heart_and_kidney_diseases_cancer_other: str = Field(
        default="",
        description=(
            "Other co-existing diseases such as heart, kidney disease, cancer, etc. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    metal_body_parts_valve_pacemaker_stent_implant_prosthesis_metal_screws: str = Field(
        default="",
        description=(
            "List any metal implants or devices in the body .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class RehabilitationPlan(BaseModel):
    """Information about the timing and purpose of rehabilitation"""

    rehabilitation_will_be_performed_before_surgery: BooleanLike = Field(
        default="", description="Check if rehabilitation is planned before surgery"
    )

    rehabilitation_will_be_performed_as_a_continuation_of_rehabilitation: BooleanLike = Field(
        default="",
        description="Check if rehabilitation is a continuation of previous rehabilitation",
    )

    rehabilitation_will_be_performed_after_surgery: BooleanLike = Field(
        default="", description="Check if rehabilitation is planned after surgery"
    )

    rehabilitation_will_be_performed_others_please_list: str = Field(
        default="",
        description=(
            "If other timing, describe when rehabilitation will be performed .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class FunctionalStatusandAccommodationNeeds(BaseModel):
    """Daily living assistance and room adaptation requirements"""

    need_help_with_activities_no: BooleanLike = Field(
        default="", description="Select if you do not need help with daily activities"
    )

    need_help_with_activities_yes: str = Field(
        default="",
        description=(
            "If you need help, describe which daily activities you need help with .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    room_adapted_for_disabled_yes: BooleanLike = Field(
        default="", description="Select if you need an adapted room for the disabled"
    )

    room_adapted_for_disabled_no: BooleanLike = Field(
        default="", description="Select if you do not need an adapted room for the disabled"
    )


class ColumnaMedicaPatientFormPrequalificationFormForPhysiotherapy(BaseModel):
    """
    COLUMNA MEDICA             PATIENT FORM - PRE-QUALIFICATION FORM FOR PHYSIOTHERAPY

    Please read the patient form carefully. Providing detailed information will allow us to qualify you for treatment in Columna Medica and make the best rehabilitation programme. Please complete the form by filling the gaps or choosing one of given answers.
    """

    patient_personal_information: PatientPersonalInformation = Field(
        ..., description="Patient Personal Information"
    )
    medical_history: MedicalHistory = Field(..., description="Medical History")
    rehabilitation_plan: RehabilitationPlan = Field(..., description="Rehabilitation Plan")
    functional_status_and_accommodation_needs: FunctionalStatusandAccommodationNeeds = Field(
        ..., description="Functional Status and Accommodation Needs"
    )
