from pydantic import BaseModel, ConfigDict, Field


class UniversalAmbulanceMedicalNecessityQuestionnaire(BaseModel):
    """Universal Ambulance Service - Medical Necessity Questionnaire/Physician Certification

    Ambulance providers use this form to document and certify that a patient's ambulance transport meets Medicare medical-necessity requirements (including rules for repetitive scheduled transports). A physician or other authorized healthcare professional completes and signs it, and the ambulance service billing/claims team submits or retains it for Medicare/CMS review and potential audit to support coverage and payment decisions for the transport.
    """

    model_config = ConfigDict(extra="forbid")

    section_i_date_of_birth: str = Field(
        ...,
        description='Date of birth (YYYY-MM-DD). If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    section_i_medicare_number: str = Field(
        ...,
        description='Medicare number. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    section_i_origin: str = Field(
        ...,
        description='Origin location/facility. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    section_i_destination: str = Field(
        ...,
        description='Destination location/facility. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    section_i_not_closest_facility_reason: str = Field(
        ...,
        description='Reason not closest appropriate facility. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    section_i_hospital_to_hospital_services_needed: str = Field(
        ...,
        description='Services needed at 2nd facility. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
    section_i_hospice_transport_related_description: str = Field(
        ...,
        description='Hospice relation description. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    section_ii_q1_medical_condition_and_contraindication: str = Field(
        ...,
        description='Medical condition and why other transport contraindicated. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    section_ii_condition_other_specify: str = Field(
        ...,
        description='Other condition specify. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )

    section_iii_incapable_reason: str = Field(
        ...,
        description='Reason patient incapable of signing. If you cannot fill this, write "N/A". If this field should not be filled by you, leave it blank (empty string "").',
    )
