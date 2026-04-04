from pydantic import BaseModel, ConfigDict, Field


class SafeMinistryScreeningQuestionnaire(BaseModel):
    """Safe ministry screening questionnaire

    Staff and volunteers under 18 who are serving as volunteers or junior volunteers/helpers submit this questionnaire to provide personal, contact, and eligibility details relevant to child-safe ministry. Authorised MOBC safe ministry/screening administrators and designated leadership review and securely store the information to assess suitability, manage risk, and ensure compliance with child safety requirements.
    """

    model_config = ConfigDict(extra="forbid")

    personal_details_date_of_birth: str = Field(
        ...,
        description='Date of birth (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    personal_details_address: str = Field(
        ...,
        description='Residential address. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    personal_details_phone_number: str = Field(
        ...,
        description='Phone number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    personal_details_health_conditions: str = Field(
        ...,
        description='Health conditions to note. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    personal_details_parent_guardian_contact_number: str = Field(
        ...,
        description='Parent/guardian contact number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )