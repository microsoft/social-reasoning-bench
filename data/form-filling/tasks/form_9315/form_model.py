from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Part1PatientAuthorization(BaseModel):
    """Patient identification, contact details, and authorization"""

    name: str = Field(
        ...,
        description=(
            'Full name of the patient .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    policy_no: str = Field(
        ...,
        description=(
            "Insurance policy number for this claim .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_number_street_city_province_and_postal_code: str = Field(
        ...,
        description=(
            "Complete mailing address including number, street, city, province and postal "
            'code .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    phone_number_include_area_code: str = Field(
        ...,
        description=(
            "Patient’s telephone number including area code .If you cannot fill this, write "
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
        ..., description="Date the patient signed the authorization"
    )  # YYYY-MM-DD format


class Part2AttendingPhysiciansStatement(BaseModel):
    """Medical information provided by the attending physician"""

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
            "Secondary or additional diagnosis, if applicable .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_first_visit: str = Field(
        ..., description="Date the patient was first seen for this condition"
    )  # YYYY-MM-DD format

    date_patient_stopped_working_due_to_this_condition: str = Field(
        ..., description="Date the patient ceased working because of this condition"
    )  # YYYY-MM-DD format

    date_of_most_recent_visit: str = Field(
        ..., description="Most recent date the patient was seen for this condition"
    )  # YYYY-MM-DD format

    frequency_of_visits_weekly: BooleanLike = Field(
        default="", description="Check if the patient is seen weekly"
    )

    frequency_of_visits_monthly: BooleanLike = Field(
        default="", description="Check if the patient is seen monthly"
    )

    frequency_of_visits_other_specify: BooleanLike = Field(
        default="", description="Check if the visit frequency is other than weekly or monthly"
    )

    other_specify: str = Field(
        default="",
        description=(
            "If 'Other' is checked, specify the visit frequency .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_hospital_in_patient_admission: str = Field(
        default="", description="Date the patient was admitted to hospital as an in-patient"
    )  # YYYY-MM-DD format

    date_of_discharge: str = Field(
        default="", description="Date the patient was discharged from in-patient care"
    )  # YYYY-MM-DD format

    date_of_hospital_out_patient_admission: str = Field(
        default="", description="Date the patient was admitted for hospital out-patient care"
    )  # YYYY-MM-DD format

    name_of_hospital: str = Field(
        default="",
        description=(
            "Full name of the hospital where the patient was treated .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
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


class EquitableLifeDisabilityBenefitsPhysicianStatementCardiac(BaseModel):
    """
        Equitable Life of Canada®

    DISABILITY BENEFITS ATTENDING PHYSICIAN’S STATEMENT CARDIAC

        To allow us to make an assessment of your patient’s claim, please answer all of the questions in full.
    """

    part_1_patient_authorization: Part1PatientAuthorization = Field(
        ..., description="Part 1: Patient Authorization"
    )
    part_2_attending_physicians_statement: Part2AttendingPhysiciansStatement = Field(
        ..., description="Part 2: Attending Physician’s Statement"
    )
