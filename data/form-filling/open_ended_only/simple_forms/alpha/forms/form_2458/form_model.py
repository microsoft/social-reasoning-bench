from pydantic import BaseModel, ConfigDict, Field


class UniversalAmbulanceMedicalNecessityCert(BaseModel):
    """UNIVERSAL AMBULANCE SERVICE - Medical Necessity Certification

    Purpose: Medical certification of the necessity for ambulance transport for a patient, specifically to comply with Medicare requirements and justify insurance coverage.
    Recipient: Healthcare professionals (such as physicians, nurses, or case managers) who complete the form, and administrative staff at ambulance services and Medicare/insurance reviewers who evaluate the medical necessity for ambulance transport.
    """

    model_config = ConfigDict(extra="forbid")

    general_info_date_of_birth: str = Field(
        ..., description='Patient date of birth (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    general_info_medicare_number: str = Field(
        ..., description='Patient Medicare number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    general_info_other_facility_reason: str = Field(
        ..., description='Reason for transport to other facility. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    general_info_hospital_transfer_services_needed: str = Field(
        ..., description='Services needed at 2nd facility not available at 1st. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    general_info_hospice_transport_description: str = Field(
        ..., description='Description if hospice transport related. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )

    medical_necessity_condition_description: str = Field(
        ..., description='Medical condition requiring ambulance transport. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
    medical_necessity_other_condition_specify: str = Field(
        ..., description='Other condition (specify). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").'
    )
