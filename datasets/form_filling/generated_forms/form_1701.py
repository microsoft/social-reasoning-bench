from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class EmployerInformation(BaseModel):
    """Identifying and address information for the employer requesting the waiver"""

    employer_id_number: str = Field(
        ...,
        description=(
            'IPERS employer identification number .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    employer_name: str = Field(
        ...,
        description=(
            'Legal name of the employer .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    employer_address: str = Field(
        ...,
        description=(
            "Street mailing address of the employer .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_and_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for the employer address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class WaiverJustification(BaseModel):
    """Explanation of technological barriers and plans to comply with electronic reporting"""

    technological_barriers: str = Field(
        ...,
        description=(
            "Describe the technological issues preventing electronic wage reporting .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    steps_to_remove_barriers: str = Field(
        ...,
        description=(
            "Explain the actions you are taking to resolve the technological barriers .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    expected_compliance_date_description: str = Field(
        ...,
        description=(
            "Indicate when you expect to be able to comply with IPERS electronic reporting "
            'requirements .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )


class ContactPerson(BaseModel):
    """Contact details for the person IPERS should reach out to for additional information"""

    contact_name: str = Field(
        ...,
        description=(
            'Name of the contact person for IPERS .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_title: str = Field(
        ...,
        description=(
            "Job title of the contact person for IPERS .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_number: str = Field(
        ...,
        description=(
            "Primary telephone number for the contact person .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    fax_number: str = Field(
        default="",
        description=(
            'FAX number for the contact person .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class CertificationandSignature(BaseModel):
    """Signature of the person completing the waiver request"""

    signature: str = Field(
        ...,
        description=(
            "Signature of the person completing this waiver request .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    title_of_person_completing_this_request: str = Field(
        ...,
        description=(
            "Job title of the person completing this waiver request .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the waiver request is signed")  # YYYY-MM-DD format


class IpersElectronicWageReportingWaiver(BaseModel):
    """
        IPERS

    Electronic Wage Reporting Waiver

        This form must be submitted if you are currently unable to comply with the electronic media filing requirement and are requesting a waiver allowing you to submit your monthly wage reports via paper or other media. An approved waiver does not exempt employers from the requirement of filing their monthly wage report in a timely manner.
    """

    employer_information: EmployerInformation = Field(..., description="Employer Information")
    waiver_justification: WaiverJustification = Field(..., description="Waiver Justification")
    contact_person: ContactPerson = Field(..., description="Contact Person")
    certification_and_signature: CertificationandSignature = Field(
        ..., description="Certification and Signature"
    )
