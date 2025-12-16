from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class AttorneyorPartyInformation(BaseModel):
    """Contact and representation information for the attorney or self-represented party"""

    attorney_or_party_without_an_attorney_name_state_bar_number_and_address: str = Field(
        default="",
        description=(
            "Full name, State Bar number (if applicable), and mailing address of the "
            'attorney or self-represented party .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name: str = Field(
        ...,
        description=(
            "Name of the attorney or self-represented party .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Street address of the attorney or self-represented party .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for the address above .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_no: str = Field(
        ...,
        description=(
            "Primary telephone number for the attorney or party .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    fax_no_optional: str = Field(
        default="",
        description=(
            "Fax number for the attorney or party (optional) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email_address_optional: str = Field(
        default="",
        description=(
            "Email address for the attorney or party (optional) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    attorney_for_name: str = Field(
        ...,
        description=(
            "Name of the person or entity represented by the attorney .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class CourtandCaseInformation(BaseModel):
    """Case caption and identifying information"""

    conservatorship_of: str = Field(
        ...,
        description=(
            "Name of the conservatee for whom the conservatorship is established .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    case_number: str = Field(
        ...,
        description=(
            'Court-assigned case number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class PetitionandConservatorshipDetails(BaseModel):
    """Information about the petitioner, conservatee, and conservatorship dates"""

    petitioner_name: str = Field(
        ...,
        description=(
            'Full legal name of the petitioner .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    conservatee_name: str = Field(
        ...,
        description=(
            'Full legal name of the conservatee .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    appointment_of_conservator_date: str = Field(
        ..., description="Date on which the court appointed the petitioner as conservator"
    )  # YYYY-MM-DD format

    letters_of_conservatorship_issued_date: str = Field(
        ..., description="Date the letters of conservatorship were issued to the petitioner"
    )  # YYYY-MM-DD format


class SupportingMedicalOpinions(BaseModel):
    """Information about physicians and/or clinical psychologists providing opinions"""

    physicians_psychologists_names_and_addresses: str = Field(
        ...,
        description=(
            "Names and full mailing addresses of the supporting physician(s) and/or "
            'clinical psychologist(s) .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    physician_first: BooleanLike = Field(
        default="", description="Check if the first listed professional is a physician"
    )

    clinical_psychologist_first: BooleanLike = Field(
        default="", description="Check if the first listed professional is a clinical psychologist"
    )

    physician_second: BooleanLike = Field(
        default="", description="Check if the second listed professional is a physician"
    )

    clinical_psychologist_second: BooleanLike = Field(
        default="", description="Check if the second listed professional is a clinical psychologist"
    )


class ConservatorshipTerminationInformation(BaseModel):
    """Automatic termination date if conservator is not reappointed"""

    conservatorship_automatic_termination_date: str = Field(
        ...,
        description=(
            "Date on which the conservatorship will automatically terminate if the "
            "petitioner is not reappointed"
        ),
    )  # YYYY-MM-DD format


class PetitionForReappointmentOfConservatorshipOfThePersonAndEstate(BaseModel):
    """PETITION FOR REAPPOINTMENT OF CONSERVATORSHIP OF THE PERSON AND ESTATE"""

    attorney_or_party_information: AttorneyorPartyInformation = Field(
        ..., description="Attorney or Party Information"
    )
    court_and_case_information: CourtandCaseInformation = Field(
        ..., description="Court and Case Information"
    )
    petition_and_conservatorship_details: PetitionandConservatorshipDetails = Field(
        ..., description="Petition and Conservatorship Details"
    )
    supporting_medical_opinions: SupportingMedicalOpinions = Field(
        ..., description="Supporting Medical Opinions"
    )
    conservatorship_termination_information: ConservatorshipTerminationInformation = Field(
        ..., description="Conservatorship Termination Information"
    )
