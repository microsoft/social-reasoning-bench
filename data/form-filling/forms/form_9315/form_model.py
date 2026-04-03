from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Part1PatientAuthorization(BaseModel):
    """Patient identification and authorization details"""

    policy_no: str = Field(
        ...,
        description=(
            "Equitable Life of Canada policy number for this claim .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name: str = Field(
        ...,
        description=(
            'Full name of the patient .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(
        ..., description="Patient’s date of birth in DD / MM / YYYY format"
    )  # YYYY-MM-DD format

    address_number_street_city_province_and_postal_code: str = Field(
        ...,
        description=(
            "Patient’s full mailing address including number, street, city, province and "
            'postal code .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    phone_number_include_area_code: str = Field(
        ...,
        description=(
            "Patient’s phone number including area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    patients_signature: str = Field(
        ...,
        description=(
            "Signature of the patient authorizing release of information .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date: str = Field(
        ..., description="Date the patient signed the authorization (DD / MM / YYYY)"
    )  # YYYY-MM-DD format


class Part2AttendingPhysiciansStatement(BaseModel):
    """Clinical and visit information provided by the attending physician"""

    primary: str = Field(
        ...,
        description=(
            "Primary diagnosis related to the disability .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    secondary: str = Field(
        default="",
        description=(
            "Secondary or contributing diagnoses, if any .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_first_visit: str = Field(
        ..., description="Date of the patient’s first visit for this condition (DD / MM / YYYY)"
    )  # YYYY-MM-DD format

    date_patient_stopped_working_due_to_his_condition: str = Field(
        ...,
        description="Date the patient ceased working because of this condition (DD / MM / YYYY)",
    )  # YYYY-MM-DD format

    date_of_most_recent_visit: str = Field(
        ..., description="Date of the most recent visit related to this condition (DD / MM / YYYY)"
    )  # YYYY-MM-DD format

    frequency_of_visits_weekly: BooleanLike = Field(
        default="", description="Check if the patient is seen weekly"
    )

    frequency_of_visits_monthly: BooleanLike = Field(
        default="", description="Check if the patient is seen monthly"
    )

    frequency_of_visits_other_specify: str = Field(
        default="",
        description=(
            "If visit frequency is other than weekly or monthly, specify the pattern .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_of_hospital_in_patient_admission: str = Field(
        default="",
        description="Date the patient was admitted to hospital as an in‑patient (DD / MM / YYYY)",
    )  # YYYY-MM-DD format

    date_of_discharge: str = Field(
        default="",
        description="Date the patient was discharged from in‑patient care (DD / MM / YYYY)",
    )  # YYYY-MM-DD format

    date_of_hospital_out_patient_admission: str = Field(
        default="",
        description="Date the patient was admitted as a hospital out‑patient (DD / MM / YYYY)",
    )  # YYYY-MM-DD format

    name_of_hospital: str = Field(
        default="",
        description=(
            "Name of the hospital where the patient was treated .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    subjective_symptoms_including_severity_frequency_duration: str = Field(
        ...,
        description=(
            "Description of the patient’s subjective symptoms, including severity, "
            'frequency, and duration .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class DisabilityBenefitsAttendingPhysiciansStatementCardiac(BaseModel):
    """
    DISABILITY BENEFITS ATTENDING PHYSICIAN’S STATEMENT CARDIAC

    To allow us to make an assessment of your patient’s claim, please answer all of the questions in full.
    """

    part_1_patient_authorization: Part1PatientAuthorization = Field(
        ..., description="Part 1: Patient Authorization"
    )
    part_2_attending_physicians_statement: Part2AttendingPhysiciansStatement = Field(
        ..., description="Part 2: Attending Physician’s Statement"
    )
