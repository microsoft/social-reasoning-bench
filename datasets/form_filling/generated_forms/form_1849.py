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
    """Identifying information about the patient"""

    patient_name: str = Field(
        ...,
        description=(
            'Full legal name of the patient .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    accession_number: str = Field(
        ...,
        description=(
            "Laboratory accession number associated with the patient's test .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Mailing address of the patient .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(..., description="Patient's date of birth")  # YYYY-MM-DD format


class PurposeofRelease(BaseModel):
    """Reason for requesting release of laboratory results"""

    purpose_of_release_line_1: str = Field(
        ...,
        description=(
            "First line describing the purpose for which the laboratory results are being "
            'released .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    purpose_of_release_line_2: str = Field(
        default="",
        description=(
            "Second line for additional details about the purpose of release .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    purpose_of_release_line_3: str = Field(
        default="",
        description=(
            "Third line for additional details about the purpose of release .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class RecipientofLaboratoryResults(BaseModel):
    """Details of the person or organization to receive the lab results"""

    name_of_person_organization_facility: str = Field(
        ...,
        description=(
            "Name of the person, organization, or facility that will receive the laboratory "
            'results .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    mail: str = Field(
        default="",
        description=(
            "Mailing address where the laboratory results should be sent .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    fax: str = Field(
        default="",
        description=(
            "Fax number where the laboratory results should be sent .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            "Email address where the laboratory results should be sent .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone_number: str = Field(
        default="",
        description=(
            "Contact phone number for the person or organization receiving the results .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    relationship_to_patient: str = Field(
        default="",
        description=(
            "Relationship of the recipient to the patient (e.g., self, spouse, physician) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class AuthorizationandSignature(BaseModel):
    """Authorization confirmation and signatures"""

    patients_signature_or_patients_representative: str = Field(
        ...,
        description=(
            "Signature of the patient or the patient's authorized representative .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    date: str = Field(..., description="Date the authorization form is signed")  # YYYY-MM-DD format

    printed_name_of_patients_representative: str = Field(
        default="",
        description=(
            "Printed full name of the patient's authorized representative, if applicable "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    relationship_of_patient: str = Field(
        default="",
        description=(
            "Relationship of the representative to the patient .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AuthorizationForReleaseOfLaboratoryResults(BaseModel):
    """
    AUTHORIZATION FOR RELEASE OF LABORATORY RESULTS

    COMPLETE AND SIGN THIS FORM TO REQUEST RELEASE OF LABORATORY RESULTS
    """

    patient_information: PatientInformation = Field(..., description="Patient Information")
    purpose_of_release: PurposeofRelease = Field(..., description="Purpose of Release")
    recipient_of_laboratory_results: RecipientofLaboratoryResults = Field(
        ..., description="Recipient of Laboratory Results"
    )
    authorization_and_signature: AuthorizationandSignature = Field(
        ..., description="Authorization and Signature"
    )
