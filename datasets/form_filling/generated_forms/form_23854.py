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
    """Basic information about the patient and contact details"""

    patients_name: str = Field(
        ...,
        description=(
            'Full legal name of the patient .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    patients_parent_guardian_if_filing_for_minor_child: str = Field(
        default="",
        description=(
            "Name of the parent or legal guardian if the patient is a minor .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    patients_date_of_birth: str = Field(
        ..., description="Patient’s date of birth"
    )  # YYYY-MM-DD format

    patients_gender_male: BooleanLike = Field(
        ..., description="Check if the patient’s gender is male"
    )

    patients_gender_female: BooleanLike = Field(
        ..., description="Check if the patient’s gender is female"
    )

    address: str = Field(
        ...,
        description=(
            'Mailing address of the patient .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            "Email address where you can be contacted .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    daytime_phone: str = Field(
        ...,
        description=(
            "Primary daytime phone number with area code .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    alternate_phone: str = Field(
        default="",
        description=(
            'Alternate phone number with area code .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class DemographicInformationOptional(BaseModel):
    """Optional demographic details used for statistics only"""

    primary_language_spoken_at_home: str = Field(
        default="",
        description=(
            "Primary language used in the home (for statistical purposes only) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    race_ethnicity: str = Field(
        default="",
        description=(
            "Race or ethnicity of the insured (for statistical purposes only) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class InsuranceInformation(BaseModel):
    """Information about the insurance company and coverage involved"""

    complete_name_of_insurance_company_involved: str = Field(
        ...,
        description=(
            "Full legal name of the insurance company handling the claim .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    policy_certificate_number: str = Field(
        ...,
        description=(
            "Policy or certificate number from your insurance documents .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    claim_number: str = Field(
        default="",
        description=(
            "Claim number assigned by the insurance company, if available .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    dates_of_medical_services_provided_if_applicable: str = Field(
        default="",
        description=(
            "Date or range of dates when the medical services in dispute were provided .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class TreatmentCategoryandUrgency(BaseModel):
    """Type of treatment dispute and whether there is an imminent and serious threat"""

    treatment_not_medically_necessary: BooleanLike = Field(
        ...,
        description="Check if the insurer stated the requested treatment is not medically necessary",
    )

    treatment_experimental_or_investigational: BooleanLike = Field(
        ...,
        description=(
            "Check if the insurer stated the requested treatment is experimental or investigational"
        ),
    )

    treatment_other: BooleanLike = Field(
        ...,
        description=(
            "Check if the insurer gave a different reason than medically unnecessary or "
            "experimental/investigational"
        ),
    )

    other_description_of_treatment_category: str = Field(
        default="",
        description=(
            "If 'Other' is checked, briefly describe the insurer’s stated reason .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    imminent_serious_threat_diagnosis_checkbox: BooleanLike = Field(
        default="",
        description=(
            "Check if there is an imminent and serious threat to the health of the insured "
            "or claimant"
        ),
    )

    diagnosis: str = Field(
        default="",
        description=(
            "Diagnosis related to the imminent and serious health threat, if applicable .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class DisputedServiceDetails(BaseModel):
    """Description of the disputed medical service or expense and treating physicians"""

    description_of_disputed_medical_service_or_expense: str = Field(
        ...,
        description=(
            "Brief description of the medical service or expense you want reviewed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    list_of_physicians_who_have_treated_you_for_this_condition: str = Field(
        ...,
        description=(
            "Names of physicians who have treated you for the condition related to this "
            'dispute .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class SupportingDocumentation(BaseModel):
    """Documents to attach in support of the Independent Medical Review request"""

    copy_of_insureds_insurance_identification_card_both_sides: BooleanLike = Field(
        default="",
        description=(
            "Check to indicate you are including a copy of the insured’s ID card (both sides)"
        ),
    )

    copies_of_correspondence_and_eobs: BooleanLike = Field(
        default="",
        description="Check to indicate you are including correspondence and related EOBs",
    )


class SignatureandAuthorization(BaseModel):
    """Signature authorizing release of records and requesting Independent Medical Review"""

    patient_or_parent_guardian_signature: str = Field(
        ...,
        description=(
            "Signature of the patient or parent/guardian if the patient is a minor .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    signature_date: str = Field(..., description="Date the form is signed")  # YYYY-MM-DD format


class ApplicationForIndependentMedicalReview(BaseModel):
    """
    APPLICATION FOR INDEPENDENT MEDICAL REVIEW

    If you wish to give authority to someone to assist you in filing this Independent Medical Review (IMR), please complete the Authorization for Release of Medical Records and Designation of Independent Medical Review Agent form.
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    demographic_information_optional: DemographicInformationOptional = Field(
        ..., description="Demographic Information (Optional)"
    )
    insurance_information: InsuranceInformation = Field(..., description="Insurance Information")
    treatment_category_and_urgency: TreatmentCategoryandUrgency = Field(
        ..., description="Treatment Category and Urgency"
    )
    disputed_service_details: DisputedServiceDetails = Field(
        ..., description="Disputed Service Details"
    )
    supporting_documentation: SupportingDocumentation = Field(
        ..., description="Supporting Documentation"
    )
    signature_and_authorization: SignatureandAuthorization = Field(
        ..., description="Signature and Authorization"
    )
