from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ComplaintType(BaseModel):
    """Type of animal nuisance complaint being filed"""

    barking_dog_complaint: BooleanLike = Field(
        ..., description="Check if this complaint is specifically about a barking dog"
    )

    general_nuisance_complaint: BooleanLike = Field(
        ...,
        description="Check if this complaint is about a general animal nuisance (not just barking)",
    )


class ComplainantInformation(BaseModel):
    """Primary complainant’s required contact information and signature"""

    name: str = Field(
        ...,
        description=(
            'Complainant\'s full name .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(
        ..., description="Date the complaint is signed by the complainant"
    )  # YYYY-MM-DD format

    signature: str = Field(
        ...,
        description=(
            'Signature of the complainant .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street address of the complainant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    zip: str = Field(..., description="Zip code for the complainant's address")

    phone: str = Field(
        ...,
        description=(
            "Primary phone number for the complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            'Email address of the complainant .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalComplainant1Optional(BaseModel):
    """First additional complainant’s optional contact information and signature"""

    additional_complainant_name: str = Field(
        default="",
        description=(
            "Full name of the first additional complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_date: str = Field(
        default="", description="Date the first additional complainant signs"
    )  # YYYY-MM-DD format

    additional_complainant_signature: str = Field(
        default="",
        description=(
            "Signature of the first additional complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_address: str = Field(
        default="",
        description=(
            "Street address of the first additional complainant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_zip: str = Field(
        default="", description="Zip code for the first additional complainant's address"
    )

    additional_complainant_phone: str = Field(
        default="",
        description=(
            "Phone number for the first additional complainant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_email: str = Field(
        default="",
        description=(
            "Email address of the first additional complainant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalComplainant2Optional(BaseModel):
    """Second additional complainant’s optional contact information and signature"""

    second_additional_complainant_name: str = Field(
        default="",
        description=(
            "Full name of the second additional complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    second_additional_complainant_date: str = Field(
        default="", description="Date the second additional complainant signs"
    )  # YYYY-MM-DD format

    second_additional_complainant_signature: str = Field(
        default="",
        description=(
            "Signature of the second additional complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    second_additional_complainant_address: str = Field(
        default="",
        description=(
            "Street address of the second additional complainant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    second_additional_complainant_zip: str = Field(
        default="", description="Zip code for the second additional complainant's address"
    )

    second_additional_complainant_phone: str = Field(
        default="",
        description=(
            "Phone number for the second additional complainant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    second_additional_complainant_email: str = Field(
        default="",
        description=(
            "Email address of the second additional complainant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IncidentDetails(BaseModel):
    """Required date, time, and notes about the nuisance incident"""

    incident_date: str = Field(
        ..., description="Date on which the nuisance incident occurred"
    )  # YYYY-MM-DD format

    incident_time: str = Field(
        ...,
        description=(
            "Time at which the nuisance incident occurred, including am/pm .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    other_notes: str = Field(
        default="",
        description=(
            "Additional notes or details about the incident .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class OwnerofAnimals(BaseModel):
    """Required information about the owner of the animal(s)"""

    owner_last_name: str = Field(
        ...,
        description=(
            'Last name of the animal owner .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    owner_first_name: str = Field(
        ...,
        description=(
            'First name of the animal owner .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    owner_address: str = Field(
        ...,
        description=(
            'Street address of the animal owner .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    owner_city: str = Field(
        ...,
        description=(
            'City for the animal owner\'s address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    owner_zip: str = Field(..., description="Zip code for the animal owner's address")


class AnimalDescription(BaseModel):
    """Details describing the animal(s) involved"""

    breed: str = Field(
        default="",
        description=(
            'Breed of the animal(s) involved .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    color: str = Field(
        default="",
        description=(
            "Primary color or markings of the animal(s) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    sex: str = Field(
        default="",
        description=(
            "Sex of the animal(s), e.g., male or female .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    animal_name: str = Field(
        default="",
        description=(
            'Name of the animal(s), if known .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class OfficeUseOnly(BaseModel):
    """For internal office processing and tracking of the complaint"""

    office_use_only_date_received: str = Field(
        default="", description="For office use only: date the complaint form was received"
    )  # YYYY-MM-DD format

    date_received: str = Field(
        default="", description="For office use only: date the complaint was logged/received"
    )  # YYYY-MM-DD format

    reference_complaint: str = Field(
        default="",
        description=(
            "Reference information for a related or prior complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    complaint_number: str = Field(
        default="",
        description=(
            "Internal complaint number assigned by the office .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AnimalNuisanceComplaintForm(BaseModel):
    """
    ANIMAL NUISANCE COMPLAINT FORM

    ''
    """

    complaint_type: ComplaintType = Field(..., description="Complaint Type")
    complainant_information: ComplainantInformation = Field(
        ..., description="Complainant Information"
    )
    additional_complainant_1_optional: AdditionalComplainant1Optional = Field(
        ..., description="Additional Complainant 1 (Optional)"
    )
    additional_complainant_2_optional: AdditionalComplainant2Optional = Field(
        ..., description="Additional Complainant 2 (Optional)"
    )
    incident_details: IncidentDetails = Field(..., description="Incident Details")
    owner_of_animals: OwnerofAnimals = Field(..., description="Owner of Animal(s)")
    animal_description: AnimalDescription = Field(..., description="Animal Description")
    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
