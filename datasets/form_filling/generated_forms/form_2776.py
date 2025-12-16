from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ClaimInformation(BaseModel):
    """Basic claim and animal identification details"""

    claim_number: str = Field(
        ...,
        description=(
            "Insurance claim number associated with this necropsy report .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    owner: str = Field(
        ...,
        description=(
            'Full name of the animal\'s owner .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_of_animal: str = Field(
        ...,
        description=(
            "Registered or common name of the animal .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    age_sex: str = Field(
        ...,
        description=(
            "Age and sex of the animal (e.g., 7 years, mare) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    color_of_animal: str = Field(
        default="",
        description=(
            "Color or primary markings of the animal .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    tattoo_or_brand: str = Field(
        default="",
        description=(
            "Tattoo, brand, or other permanent identification marks .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class NecropsyDetails(BaseModel):
    """Information about the necropsy procedure and findings"""

    date_and_time_of_necropsy: str = Field(
        ...,
        description=(
            "Date and time when the necropsy was performed .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    names_of_all_participating_veterinarians: str = Field(
        ...,
        description=(
            "Names of all veterinarians who participated in the necropsy .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    history_and_symptoms: str = Field(
        ...,
        description=(
            "Clinical history and symptoms observed prior to death or euthanasia .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    findings: str = Field(
        ...,
        description=(
            "Necropsy findings; use additional space or back of form if needed .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    cause_of_death: str = Field(
        ...,
        description=(
            "Cause of death; if euthanized, describe the problem requiring euthanasia .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    tissues_taken_yes: BooleanLike = Field(
        ...,
        description=(
            "Indicate YES if tissues were taken for histopathology, toxicology, or other tests"
        ),
    )

    tissues_taken_no: BooleanLike = Field(
        ..., description="Indicate NO if no tissues were taken for additional testing"
    )

    tissues_explanation: str = Field(
        default="",
        description=(
            "Explanation or details regarding tissues taken or tests performed, if "
            'applicable .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    photographs_taken_yes: BooleanLike = Field(
        default="",
        description="Indicate YES if photographs were taken during or related to the necropsy",
    )

    photographs_taken_no: BooleanLike = Field(
        default="", description="Indicate NO if no photographs were taken"
    )


class VeterinarianCertification(BaseModel):
    """Certifying veterinarian’s credentials and signature"""

    veterinarian_degree: str = Field(
        ...,
        description=(
            "Professional veterinary degree (e.g., DVM, VMD) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature: str = Field(
        ...,
        description=(
            "Signature of the attending or reporting veterinarian .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the necropsy report is signed")  # YYYY-MM-DD format

    address_line_1: str = Field(
        ...,
        description=(
            "First line of the veterinarian's mailing address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address_line_2: str = Field(
        default="",
        description=(
            "Second line of the veterinarian's mailing address (if needed) .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class NecropsyReport(BaseModel):
    """
    NECROPSY REPORT

    ''
    """

    claim_information: ClaimInformation = Field(..., description="Claim Information")
    necropsy_details: NecropsyDetails = Field(..., description="Necropsy Details")
    veterinarian_certification: VeterinarianCertification = Field(
        ..., description="Veterinarian Certification"
    )
