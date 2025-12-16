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
    """Names and birthdays of students covered by this form"""

    student_1_first_name: str = Field(
        ...,
        description=(
            'First student\'s first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    student_1_last_name: str = Field(
        ...,
        description=(
            'First student\'s last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    student_1_birthday: str = Field(
        ..., description="First student's date of birth"
    )  # YYYY-MM-DD format

    student_2_first_name: str = Field(
        default="",
        description=(
            'Second student\'s first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    student_2_last_name: str = Field(
        default="",
        description=(
            'Second student\'s last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    student_2_birthday: str = Field(
        default="", description="Second student's date of birth"
    )  # YYYY-MM-DD format

    student_3_first_name: str = Field(
        default="",
        description=(
            'Third student\'s first name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    student_3_last_name: str = Field(
        default="",
        description=(
            'Third student\'s last name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    student_3_birthday: str = Field(
        default="", description="Third student's date of birth"
    )  # YYYY-MM-DD format


class ParentLegalGuardianAuthorization(BaseModel):
    """Parent or legal guardian information and consent"""

    parent_or_legal_guardian_name: str = Field(
        ...,
        description=(
            "Full name of the parent or legal guardian completing this form .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    parent_or_legal_guardian_signature: str = Field(
        ...,
        description=(
            "Signature of the parent or legal guardian authorizing consent .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    date: str = Field(..., description="Date the form is signed")  # YYYY-MM-DD format


class ContactInformation(BaseModel):
    """Primary family contact and address details"""

    address: str = Field(
        ...,
        description=(
            "Street address of the parent or legal guardian .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City of the home address .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(..., description="State of the home address")

    zip: str = Field(..., description="ZIP code of the home address")

    fathers_name: str = Field(
        default="",
        description=(
            'Father\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    fathers_phone: str = Field(
        default="",
        description=(
            'Father\'s primary phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    mothers_name: str = Field(
        default="",
        description=(
            'Mother\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    mothers_phone: str = Field(
        default="",
        description=(
            'Mother\'s primary phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class EmergencyContactInformation(BaseModel):
    """Non-parent contacts to reach in case of emergency"""

    emergency_contact_1_name: str = Field(
        ...,
        description=(
            "Name of the first emergency contact (other than parent/guardian, if possible) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    emergency_contact_1_relationship: str = Field(
        ...,
        description=(
            "Relationship of the first emergency contact to the student .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_1_phone: str = Field(
        ...,
        description=(
            "Phone number for the first emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_2_name: str = Field(
        default="",
        description=(
            'Name of the second emergency contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_2_relationship: str = Field(
        default="",
        description=(
            "Relationship of the second emergency contact to the student .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    emergency_contact_2_phone: str = Field(
        default="",
        description=(
            "Phone number for the second emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class MedicalInformation(BaseModel):
    """Insurance, doctor, allergies, and medical conditions"""

    insurance_provider: str = Field(
        default="",
        description=(
            "Name of the student's health insurance provider .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    doctor: str = Field(
        default="",
        description=(
            "Name of the student's primary doctor or physician .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    allergies_line_1: str = Field(
        default="",
        description=(
            'Allergies information (first line) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    allergies_line_2: str = Field(
        default="",
        description=(
            "Additional allergies information (second line) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medication_medical_conditions_line_1: str = Field(
        default="",
        description=(
            "Medication or medical conditions (first line) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    medication_medical_conditions_line_2: str = Field(
        default="",
        description=(
            "Additional medication or medical conditions (second line) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    medication_medical_conditions_line_3: str = Field(
        default="",
        description=(
            "Additional medication or medical conditions (third line) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class BauerChristianReformedChurchContactMedicalForm(BaseModel):
    """
        Bauer Christian Reformed Church
    Contact & Medical Form

        As the parent or guardian of the students listed above, I give Bauer Christian Reformed Church the authority to obtain medical treatment for the students listed on this document. I further release from any liability Bauer CRC and its leaders in the event of injury while traveling to an event, during an event, or returning from an event. I also give Bauer CRC permission to use any pictures taken during the event of the students listed on this document for advertising purposes.
    """

    student_information: StudentInformation = Field(..., description="Student Information")
    parent__legal_guardian_authorization: ParentLegalGuardianAuthorization = Field(
        ..., description="Parent / Legal Guardian Authorization"
    )
    contact_information: ContactInformation = Field(..., description="Contact Information")
    emergency_contact_information: EmergencyContactInformation = Field(
        ..., description="Emergency Contact Information"
    )
    medical_information: MedicalInformation = Field(..., description="Medical Information")
