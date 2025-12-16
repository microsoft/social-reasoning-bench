from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class StudentInformation(BaseModel):
    """Basic information about the student"""

    student_name: str = Field(
        ...,
        description=(
            "Student's full legal name, printed clearly .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    id_number: str = Field(
        default="",
        description=(
            "Student's school identification number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Student's date of birth")  # YYYY-MM-DD format

    home_phone: str = Field(
        ...,
        description=(
            'Primary home telephone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    school: str = Field(
        ...,
        description=(
            "Name of the school the student attends .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Student\'s home street address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    school_year: str = Field(
        ...,
        description=(
            "Applicable school year (e.g., 2025-2026) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    grade: str = Field(
        ...,
        description=(
            'Student\'s current grade level .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the student\'s residence .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zip: str = Field(..., description="ZIP code for the student's home address")


class ParentGuardianEmergencyContacts(BaseModel):
    """Residential parent/guardian and additional emergency contacts"""

    mothers_name: str = Field(
        ...,
        description=(
            'Residential mother\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mothers_daytime_phone: str = Field(
        ...,
        description=(
            'Mother\'s daytime contact phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    mothers_cell: str = Field(
        default="",
        description=(
            'Mother\'s cell phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    fathers_name: str = Field(
        ...,
        description=(
            'Residential father\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    fathers_daytime_phone: str = Field(
        ...,
        description=(
            'Father\'s daytime contact phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    fathers_cell: str = Field(
        default="",
        description=(
            'Father\'s cell phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_1_name: str = Field(
        ...,
        description=(
            'First emergency contact\'s full name .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_1_daytime_phone: str = Field(
        ...,
        description=(
            "First emergency contact's daytime phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_1_cell: str = Field(
        default="",
        description=(
            "First emergency contact's cell phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_2_name: str = Field(
        default="",
        description=(
            'Second emergency contact\'s full name .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_2_daytime_phone: str = Field(
        default="",
        description=(
            "Second emergency contact's daytime phone number .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_2_cell: str = Field(
        default="",
        description=(
            "Second emergency contact's cell phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_3_name: str = Field(
        default="",
        description=(
            'Third emergency contact\'s full name .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_3_daytime_phone: str = Field(
        default="",
        description=(
            "Third emergency contact's daytime phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_3_cell: str = Field(
        default="",
        description=(
            "Third emergency contact's cell phone number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class StudentHealthSection(BaseModel):
    """Student medical conditions, allergies, and medications"""

    no_medical_conditions: BooleanLike = Field(
        default="", description="Check if the student has no known medical conditions"
    )

    no_allergies: BooleanLike = Field(
        default="", description="Check if the student has no known allergies"
    )

    medication_allergy: str = Field(
        default="",
        description=(
            'List any medication allergies .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    allergic_to: str = Field(
        default="",
        description=(
            "Describe substances the student is allergic to .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    requires_treatment_with_epi_pen_antihistamine: BooleanLike = Field(
        default="",
        description="Check if student requires epi-pen or antihistamine treatment for allergies",
    )

    no_medication_required_for_allergy_treatment: BooleanLike = Field(
        default="", description="Check if no medication is required for allergy treatment"
    )

    asthma: BooleanLike = Field(default="", description="Check if the student has asthma")

    requires_inhaler_nebulizer_at_school: BooleanLike = Field(
        default="", description="Check if student requires inhaler or nebulizer use at school"
    )

    no_inhaler_nebulizer_required_at_school: BooleanLike = Field(
        default="", description="Check if no inhaler or nebulizer is required at school"
    )

    diabetes: BooleanLike = Field(default="", description="Check if the student has diabetes")

    requires_insulin: BooleanLike = Field(
        default="", description="Check if the student requires insulin for diabetes management"
    )

    requires_oral_diabetes_medications: BooleanLike = Field(
        default="", description="Check if the student requires oral diabetes medications"
    )

    seizure_disorder: BooleanLike = Field(
        default="", description="Check if the student has a seizure disorder"
    )

    type_of_seizure_disorder: str = Field(
        default="",
        description=(
            'Specify the type of seizure disorder .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    requires_emergency_rescue_medication: BooleanLike = Field(
        default="", description="Check if emergency rescue medication is required for seizures"
    )

    no_emergency_rescue_medication_required: BooleanLike = Field(
        default="", description="Check if no emergency rescue medication is required for seizures"
    )

    heart_blood_problems: str = Field(
        default="",
        description=(
            "Describe any heart or blood-related medical problems .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_specify: str = Field(
        default="",
        description=(
            "Describe any other medical conditions not listed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    medications_taken_at_home: str = Field(
        default="",
        description=(
            "List medications the student takes at home .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medications_to_be_given_at_school: str = Field(
        default="",
        description=(
            "List medications that need to be administered at school .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PartIToGrantConsent(BaseModel):
    """Medical providers and consent to emergency treatment"""

    doctor: str = Field(
        default="",
        description=(
            'Primary care physician\'s name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    doctor_phone: str = Field(
        default="",
        description=(
            'Primary care physician\'s phone number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    dentist: str = Field(
        default="",
        description=(
            'Dentist\'s name .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    dentist_phone: str = Field(
        default="",
        description=(
            'Dentist\'s phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    medical_specialist: str = Field(
        default="",
        description=(
            "Name of any medical specialist involved in the student's care .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    medical_specialist_phone: str = Field(
        default="",
        description=(
            'Medical specialist\'s phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    local_hospital_emergency_room_phone: str = Field(
        default="",
        description=(
            "Phone number of preferred local hospital or emergency room .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_parent_guardian_part_i: str = Field(
        default="",
        description=(
            "Parent or guardian signature granting consent (Part I) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_part_i: str = Field(
        default="", description="Date Part I consent is signed"
    )  # YYYY-MM-DD format


class PartIIRefusaltoConsent(BaseModel):
    """Refusal of consent and requested actions in an emergency"""

    action_to_be_taken_by_school_authorities_line_1: str = Field(
        default="",
        description=(
            "First line of instructions for school authorities if consent is refused .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    action_to_be_taken_by_school_authorities_line_2: str = Field(
        default="",
        description=(
            "Second line of instructions for school authorities if consent is refused .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    action_to_be_taken_by_school_authorities_line_3: str = Field(
        default="",
        description=(
            "Third line of instructions for school authorities if consent is refused .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    signature_of_parent_guardian_part_ii: str = Field(
        default="",
        description=(
            "Parent or guardian signature refusing consent (Part II) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_part_ii: str = Field(
        default="", description="Date Part II refusal is signed"
    )  # YYYY-MM-DD format


class CentervilleCitySchoolsEmergencyMedicalAuthorizationForm(BaseModel):
    """
        Centerville City Schools
    EMERGENCY MEDICAL AUTHORIZATION FORM

        Purpose: To enable parents and guardians to authorize the provision of emergency treatment for children who become ill or injured while under school authority, when parents or guardians cannot be reached. This information will be shared, as necessary, with teachers, bus drivers, administrative staff, health personnel including student nurses, and other school personnel.
    """

    student_information: StudentInformation = Field(..., description="Student Information")
    parentguardian__emergency_contacts: ParentGuardianEmergencyContacts = Field(
        ..., description="Parent/Guardian & Emergency Contacts"
    )
    student_health_section: StudentHealthSection = Field(..., description="Student Health Section")
    part_i_to_grant_consent: PartIToGrantConsent = Field(
        ..., description="Part I: To Grant Consent"
    )
    part_ii_refusal_to_consent: PartIIRefusaltoConsent = Field(
        ..., description="Part II: Refusal to Consent"
    )
