from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class MedicalInformation(BaseModel):
    """Youth participant details and medical history"""

    full_name: str = Field(
        ...,
        description=(
            'Youth participant\'s full legal name .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    birth_date: str = Field(..., description="Participant's date of birth")  # YYYY-MM-DD format

    male: BooleanLike = Field(default="", description="Check if the participant's sex is male")

    female: BooleanLike = Field(default="", description="Check if the participant's sex is female")

    height: str = Field(
        ...,
        description=(
            "Participant's height (include units, e.g., feet/inches) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    weight: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Participant's weight (in pounds or specified units)"
    )

    past_medical_history: str = Field(
        ...,
        description=(
            "Summary of participant's past medical conditions, surgeries, or "
            'hospitalizations .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    other_pertinent_history: str = Field(
        default="",
        description=(
            "Any additional relevant medical or personal history not listed above .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    allergies: str = Field(
        ...,
        description=(
            "List all known allergies (medications, foods, environmental, etc.) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    medications: str = Field(
        ...,
        description=(
            "List all current medications and dosages .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    primary_care_physician: str = Field(
        ...,
        description=(
            "Name of the participant's primary care physician .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_care_physicians_telephone: str = Field(
        ...,
        description=(
            "Telephone number for the primary care physician .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    health_insurance_carrier: str = Field(
        ...,
        description=(
            "Name of the participant's health insurance provider .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    preferred_hospital: str = Field(
        ...,
        description=(
            "Name of the hospital preferred for emergency treatment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class EmergencyContactInformation(BaseModel):
    """People to contact in case of emergency"""

    emergency_contact_name_1: str = Field(
        ...,
        description=(
            "Name of the primary emergency contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_phone_1: str = Field(
        ...,
        description=(
            "Phone number for the primary emergency contact .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_name_2: str = Field(
        default="",
        description=(
            "Name of a secondary emergency contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_phone_2: str = Field(
        default="",
        description=(
            "Phone number for the secondary emergency contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_name_3: str = Field(
        default="",
        description=(
            "Name of an additional emergency contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    emergency_contact_phone_3: str = Field(
        default="",
        description=(
            "Phone number for the additional emergency contact .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class YouthAcademyMedicalInfoForm(BaseModel):
    """
        WESTFIELD POLICE DEPARTMENT
    Youth Academy

    Emergency Medical Information Form

        Medical Form must be filled out in its entirety. Please Print. Dependent on the applicant's past medical history, the Town of Westfield maintains the right to request a doctor's note for participation in any and all physical activities. This must be submitted prior to the first day of the academy. Supplied information will only be used in the event of a medical emergency.
    """

    medical_information: MedicalInformation = Field(..., description="Medical Information")
    emergency_contact_information: EmergencyContactInformation = Field(
        ..., description="Emergency Contact Information"
    )
