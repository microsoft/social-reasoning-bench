from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AcknowledgementofReceipt(BaseModel):
    """Patient acknowledgement of receipt of Notice of Privacy Practices"""

    print_name: str = Field(
        ...,
        description=(
            "Printed full name of the patient, parent, or guardian .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Mailing address of the patient, parent, or guardian .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_of_patient_parent_or_guardian: str = Field(
        ...,
        description=(
            "Signature of the patient, parent, or legal guardian acknowledging receipt and "
            'authorization .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Date the acknowledgement form is signed"
    )  # YYYY-MM-DD format


class MeansofCommunication(BaseModel):
    """Preferred contact methods for the patient"""

    my_home_phone_number: str = Field(
        default="",
        description=(
            "Primary home telephone number for contacting you .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    my_cell_phone_number: str = Field(
        default="",
        description=(
            "Cell/mobile telephone number for contacting you .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    my_work_phone_number: str = Field(
        default="",
        description=(
            "Work telephone number for contacting you .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    my_email: str = Field(
        default="",
        description=(
            'Email address for contacting you .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    other_contact: str = Field(
        default="",
        description=(
            "Any other preferred means of communication or contact information .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AuthorizedPersonsforPHI(BaseModel):
    """Individuals authorized to discuss the patient's Protected Health Information (PHI)"""

    authorized_person_1: str = Field(
        default="",
        description=(
            "Name of the first person authorized to discuss your Protected Health "
            'Information (PHI) .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    authorized_person_1_date_added_removed: str = Field(
        default="", description="Date the first authorized person was added or removed"
    )  # YYYY-MM-DD format

    authorized_person_2: str = Field(
        default="",
        description=(
            "Name of the second person authorized to discuss your Protected Health "
            'Information (PHI) .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    authorized_person_2_date_added_removed: str = Field(
        default="", description="Date the second authorized person was added or removed"
    )  # YYYY-MM-DD format

    authorized_person_3: str = Field(
        default="",
        description=(
            "Name of the third person authorized to discuss your Protected Health "
            'Information (PHI) .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    authorized_person_3_date_added_removed: str = Field(
        default="", description="Date the third authorized person was added or removed"
    )  # YYYY-MM-DD format


class ForOfficeUseOnly(BaseModel):
    """Office documentation when written acknowledgement cannot be obtained"""

    individual_refused_to_sign: BooleanLike = Field(
        default="", description="Check if the individual refused to sign the acknowledgement"
    )

    communication_barriers_prohibited_obtaining_the_acknowledgement: BooleanLike = Field(
        default="",
        description="Check if communication barriers prevented obtaining the acknowledgement",
    )

    an_emergency_situation_prevented_us_from_obtaining_the_acknowledgement: BooleanLike = Field(
        default="",
        description="Check if an emergency situation prevented obtaining the acknowledgement",
    )

    other_office_use_only: str = Field(
        default="",
        description=(
            "If another reason applies, specify why acknowledgement could not be obtained "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    staff_person_initials: str = Field(
        default="",
        description=(
            "Initials of the staff member documenting the acknowledgement attempt .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AcknowledgementOfReceiptOfNoticeOfPrivacyPolicies(BaseModel):
    """
    Acknowledgement of Receipt of Notice of Privacy Policies

    I have received a copy of the Notice of Privacy Practices of Drs. Schramm, Symancyk, and Klampert. I hereby authorize, as indicated by my signature below, Drs. Klampert, Schramm, and Symancyk to use and to disclose my protected health information for any necessary clinical, financial, and insurance purpose, as authorized in the Patient Consent form.
    """

    acknowledgement_of_receipt: AcknowledgementofReceipt = Field(
        ..., description="Acknowledgement of Receipt"
    )
    means_of_communication: MeansofCommunication = Field(..., description="Means of Communication")
    authorized_persons_for_phi: AuthorizedPersonsforPHI = Field(
        ..., description="Authorized Persons for PHI"
    )
    for_office_use_only: ForOfficeUseOnly = Field(..., description="For Office Use Only")
