from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PatientInformation(BaseModel):
    """Basic demographic and identification details for the patient"""

    patient_name: str = Field(
        ...,
        description=(
            'Full legal name of the patient .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth_dd_mm_yyyy: str = Field(
        ..., description="Patient's date of birth in DD/MM/YYYY format"
    )  # YYYY-MM-DD format

    gender_male: BooleanLike = Field(..., description="Check if the patient's gender is male")

    gender_female: BooleanLike = Field(..., description="Check if the patient's gender is female")

    parents_name: str = Field(
        default="",
        description=(
            'Name of parent or legal guardian .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing address for the patient or family .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mrn: str = Field(
        default="",
        description=(
            "Medical Record Number for the patient, if available .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    health_card_number: str = Field(
        default="",
        description=(
            "Provincial health card number (Canada only) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    version: str = Field(
        default="",
        description=(
            "Version code on the provincial health card, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    issuing_province: str = Field(
        default="",
        description=(
            'Province that issued the health card .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class SpecimenInformation(BaseModel):
    """Details about the specimen drawn for testing"""

    specimen_drawn_date_dd_mm_yyyy: str = Field(
        ..., description="Date the specimen was drawn, in DD/MM/YYYY format"
    )  # YYYY-MM-DD format

    specimen_drawn_time_hh_mm: str = Field(
        ...,
        description=(
            "Time the specimen was drawn, in HH:MM format .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    specimen_type_peripheral_blood_in_edta_3_ml_minimum_1_ml_minimum_for_newborns: BooleanLike = (
        Field(
            ...,
            description=(
                "Check if the submitted specimen is peripheral blood in EDTA (3 mL minimum, 1 "
                "mL for newborns)"
            ),
        )
    )

    specimen_type_fibroblast_cell_culture_2xt25_confluent_flasks_at_room_temperature: BooleanLike = Field(
        ...,
        description=(
            "Check if the submitted specimen is fibroblast cell culture (2xT25 confluent "
            "flasks at room temperature)"
        ),
    )

    specimen_type_dna_1ug_at_50ng_ul_minimum: BooleanLike = Field(
        ..., description="Check if the submitted specimen is DNA (1 μg at ≥50 ng/μL minimum)"
    )

    karyotype_if_known: str = Field(
        default="",
        description=(
            "Known karyotype result, if previously performed .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IndicationsforTestingFamilyInformation(BaseModel):
    """Clinical indications for testing and family/proband details"""

    indications_for_testing_developmental_delay_or_intellectual_disability: BooleanLike = Field(
        ...,
        description=(
            "Check if the indication for testing is developmental delay or intellectual disability"
        ),
    )

    indications_for_testing_developmental_delay_or_intellectual_disability_and_additional_clinical_features_complete_clinical_description_form_page_2: BooleanLike = Field(
        ...,
        description=(
            "Check if the indication is developmental delay or intellectual disability with "
            "additional clinical features"
        ),
    )

    indications_for_testing_two_or_more_congenital_anomalies_complete_clinical_description_form_page_2: BooleanLike = Field(
        ..., description="Check if the indication is two or more congenital anomalies"
    )

    indications_for_testing_microarray_qpcr_family_follow_up: BooleanLike = Field(
        ..., description="Check if the indication is microarray/qPCR family follow-up testing"
    )

    relationship_to_proband: str = Field(
        default="",
        description=(
            "Describe the patient's relationship to the proband .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    proband_report_order_number: str = Field(
        default="",
        description=(
            "Proband's report or order number for reference .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    relevant_family_history: str = Field(
        default="",
        description=(
            "Summary of relevant family medical or genetic history .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    pedigree_at_least_3_generation_when_available_and_if_applicable: str = Field(
        default="",
        description=(
            "Space to draw or describe a three-generation pedigree, if applicable .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class ReferringPhysician(BaseModel):
    """Information about the referring physician"""

    referring_physician_name: str = Field(
        ...,
        description=(
            'Full name of the referring physician .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    referring_physician_address: str = Field(
        ...,
        description=(
            "Mailing address of the referring physician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    referring_physician_phone: str = Field(
        ...,
        description=(
            "Telephone number of the referring physician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    referring_physician_fax: str = Field(
        default="",
        description=(
            'Fax number of the referring physician .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    referring_physician_email: str = Field(
        default="",
        description=(
            "Email address of the referring physician .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    referring_physician_signature_required: str = Field(
        ...,
        description=(
            "Signature of the referring physician authorizing the test .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CopyReportTo(BaseModel):
    """Details of additional recipient(s) for the report"""

    copy_report_to_name: str = Field(
        default="",
        description=(
            "Name of additional provider or recipient to receive a copy of the report .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    copy_report_to_address: str = Field(
        default="",
        description=(
            "Mailing address for the additional report recipient .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    copy_report_to_phone: str = Field(
        default="",
        description=(
            "Telephone number for the additional report recipient .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    copy_report_to_fax: str = Field(
        default="",
        description=(
            "Fax number for the additional report recipient .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    copy_report_to_email: str = Field(
        default="",
        description=(
            "Email address for the additional report recipient .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class GenomicSnpMicroarrayReferredinRequisition(BaseModel):
    """
        GENOMIC SNP MICROARRAY
    Referred-In Requisition

        Complete in full to avoid delay in reporting result.
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    specimen_information: SpecimenInformation = Field(..., description="Specimen Information")
    indications_for_testing__family_information: IndicationsforTestingFamilyInformation = Field(
        ..., description="Indications for Testing & Family Information"
    )
    referring_physician: ReferringPhysician = Field(..., description="Referring Physician")
    copy_report_to: CopyReportTo = Field(..., description="Copy Report To")
