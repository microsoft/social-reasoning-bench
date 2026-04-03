from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MedicalTreatmentTriage(BaseModel):
    """Determines whether this injury/illness requires this form or a First Aid report"""

    are_you_seeking_medical_treatment_yes: BooleanLike = Field(
        ..., description="Check if you are seeking medical treatment for this injury or illness."
    )

    are_you_seeking_medical_treatment_no: BooleanLike = Field(
        ...,
        description=(
            "Check if you are not seeking medical treatment and will instead complete an "
            "Employee First Aid Report."
        ),
    )


class EmployeeInformation(BaseModel):
    """Identifying and contact information about the employee"""

    name_last: str = Field(
        ...,
        description=(
            'Employee\'s last name. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    name_first: str = Field(
        ...,
        description=(
            'Employee\'s first name. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    name_middle: str = Field(
        default="",
        description=(
            'Employee\'s middle name or initial. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address: str = Field(
        ...,
        description=(
            'Employee\'s full mailing address. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Employee's date of birth.")  # YYYY-MM-DD format

    date_of_death_if_applicable: str = Field(
        default="", description="Date of death, if the injury or illness resulted in death."
    )  # YYYY-MM-DD format

    city: str = Field(
        ...,
        description=(
            "City for the employee's mailing address. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State for the employee's mailing address.")

    zip_code: str = Field(..., description="Zip code for the employee's mailing address.")

    last_4_of_ssn: str = Field(
        ..., description="Last four digits of the employee's Social Security Number."
    )

    gender_f: BooleanLike = Field(..., description="Check if the employee's gender is female.")

    gender_m: BooleanLike = Field(..., description="Check if the employee's gender is male.")

    gender_u: BooleanLike = Field(
        ..., description="Check if the employee's gender is unknown or unspecified."
    )

    telephone_no_primary: str = Field(
        ...,
        description=(
            "Primary telephone number for the employee. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_no_alternate: str = Field(
        default="",
        description=(
            "Alternate telephone number for the employee. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    marital_status_m_married: BooleanLike = Field(
        ..., description="Check if the employee is married."
    )

    marital_status_s_separated: BooleanLike = Field(
        ..., description="Check if the employee is separated."
    )

    marital_status_u_unmarried: BooleanLike = Field(
        ..., description="Check if the employee is unmarried."
    )

    marital_status_k_unknown: BooleanLike = Field(
        ..., description="Check if the employee's marital status is unknown."
    )

    number_of_dependents: Union[float, Literal["N/A", ""]] = Field(
        default="", description="Number of dependents the employee has."
    )


class InjuryIllnessandEmploymentDetails(BaseModel):
    """Details about the injury/illness event and employment context"""

    date_of_injury_illness: str = Field(
        ..., description="Date when the injury or illness occurred."
    )  # YYYY-MM-DD format

    time_of_injury_illness: str = Field(
        ...,
        description=(
            "Time when the injury or illness occurred. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    employer_borough: BooleanLike = Field(..., description="Check if the employer is the Borough.")

    employer_school_district: BooleanLike = Field(
        ..., description="Check if the employer is the School District."
    )

    department_school_location: str = Field(
        ...,
        description=(
            "Name of the department or school location where the employee works. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    describe_part_of_body_affected: str = Field(
        ...,
        description=(
            "Describe the specific part(s) of the body that were injured or affected. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    union_affiliation: str = Field(
        default="",
        description=(
            'Employee\'s union affiliation, if any. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    supervisors_name: str = Field(
        ...,
        description=(
            'Name of the employee\'s supervisor. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    describe_nature_of_injury_illness: str = Field(
        ...,
        description=(
            "Brief description of the type of injury or illness (e.g., sprain, laceration). "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    occur_on_employers_premises_yes: BooleanLike = Field(
        ..., description="Check if the injury or illness occurred on the employer's premises."
    )

    occur_on_employers_premises_no: BooleanLike = Field(
        ..., description="Check if the injury or illness did not occur on the employer's premises."
    )

    supervisors_contact_number: str = Field(
        default="",
        description=(
            'Telephone number for the supervisor. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    was_this_an_assault_yes: BooleanLike = Field(
        default="", description="Check if the incident was an assault."
    )

    was_this_an_assault_no: BooleanLike = Field(
        default="", description="Check if the incident was not an assault."
    )

    describe_how_the_injury_illness_happened_line_1: str = Field(
        ...,
        description=(
            "First line of description explaining how the injury or illness occurred. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    describe_how_the_injury_illness_happened_line_2: str = Field(
        default="",
        description=(
            "Second line of description explaining how the injury or illness occurred. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    describe_how_the_injury_illness_happened_line_3: str = Field(
        default="",
        description=(
            "Third line of description explaining how the injury or illness occurred. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    witness_name_contact_number_1: str = Field(
        default="",
        description=(
            "Name and contact number for the first witness. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    witness_name_contact_phone_number_2: str = Field(
        default="",
        description=(
            "Name and contact phone number for the second witness. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class MedicalTreatmentandProvider(BaseModel):
    """Initial treatment information and treating provider details"""

    initial_treatment_minor_clinic_hospital_remedies_and_diagnostic_testing: BooleanLike = Field(
        default="",
        description=(
            "Check if initial treatment was minor clinic/hospital remedies and diagnostic testing."
        ),
    )

    initial_treatment_emergency_evaluation_diagnostic_testing_and_medical_procedures: BooleanLike = Field(
        default="",
        description=(
            "Check if initial treatment was emergency evaluation, diagnostic testing, and "
            "medical procedures."
        ),
    )

    initial_treatment_hospitalization_greater_than_24_hours: BooleanLike = Field(
        default="",
        description="Check if initial treatment included hospitalization greater than 24 hours.",
    )

    initial_treatment_future_major_medical_lost_time_anticipated: BooleanLike = Field(
        default="",
        description="Check if future major medical treatment or lost time is anticipated.",
    )

    physician_name: str = Field(
        default="",
        description=(
            'Name of the treating physician. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    medical_facility_name: str = Field(
        default="",
        description=(
            "Name of the medical facility where treatment is provided. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class EmployeeAuthorizationandSignature(BaseModel):
    """Authorization to release medical records and signature information"""

    employee_signature_digital_signature_print: str = Field(
        ...,
        description=(
            "Employee's signature, digital signature, or printed name authorizing release "
            'of medical records. .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date_signed_employee_authorization: str = Field(
        ..., description="Date the employee signed the medical records authorization."
    )  # YYYY-MM-DD format

    if_employee_unavailable_explain_circumstances: str = Field(
        default="",
        description=(
            "Explanation of why the employee is unavailable to sign the authorization. .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date_signed_if_employee_unavailable_explanation: str = Field(
        default="", description="Date the explanation was signed if the employee was unavailable."
    )  # YYYY-MM-DD format


class FairbanksNorthStarBoroughEmployeeInjuryIllnessReport(BaseModel):
    """
        FAIRBANKS NORTH STAR BOROUGH - RISK MANAGEMENT
    EMPLOYEE REPORT OF OCCUPATIONAL
    INJURY OR ILLNESS TO EMPLOYER

        EMPLOYEE REPORT OF OCCUPATIONAL INJURY OR ILLNESS TO EMPLOYER
    """

    medical_treatment_triage: MedicalTreatmentTriage = Field(
        ..., description="Medical Treatment Triage"
    )
    employee_information: EmployeeInformation = Field(..., description="Employee Information")
    injury__illness_and_employment_details: InjuryIllnessandEmploymentDetails = Field(
        ..., description="Injury / Illness and Employment Details"
    )
    medical_treatment_and_provider: MedicalTreatmentandProvider = Field(
        ..., description="Medical Treatment and Provider"
    )
    employee_authorization_and_signature: EmployeeAuthorizationandSignature = Field(
        ..., description="Employee Authorization and Signature"
    )
