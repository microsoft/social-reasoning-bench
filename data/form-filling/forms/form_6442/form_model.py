from typing import Literal, Optional, List, Union
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
        ..., description="Check if this complaint is about a general animal nuisance"
    )


class ComplainantInformation(BaseModel):
    """Primary complainant contact information"""

    complainant_name: str = Field(
        ...,
        description=(
            'Full name of the primary complainant .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    complainant_date: str = Field(
        ..., description="Date the primary complainant is completing this form"
    )  # YYYY-MM-DD format

    complainant_signature: str = Field(
        ...,
        description=(
            'Signature of the primary complainant .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    complainant_address: str = Field(
        ...,
        description=(
            "Mailing address of the primary complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    complainant_zip: str = Field(..., description="ZIP code for the primary complainant's address")

    complainant_phone: str = Field(
        ...,
        description=(
            "Phone number for the primary complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    complainant_email: str = Field(
        default="",
        description=(
            "Email address of the primary complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalComplainant1(BaseModel):
    """First additional complainant (optional)"""

    additional_complainant_1_name: str = Field(
        default="",
        description=(
            "Full name of the first additional complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_1_date: str = Field(
        default="", description="Date the first additional complainant is completing this form"
    )  # YYYY-MM-DD format

    additional_complainant_1_signature: str = Field(
        default="",
        description=(
            "Signature of the first additional complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_1_address: str = Field(
        default="",
        description=(
            "Mailing address of the first additional complainant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_1_zip: str = Field(
        default="", description="ZIP code for the first additional complainant's address"
    )

    additional_complainant_1_phone: str = Field(
        default="",
        description=(
            "Phone number for the first additional complainant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_1_email: str = Field(
        default="",
        description=(
            "Email address of the first additional complainant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalComplainant2(BaseModel):
    """Second additional complainant (optional)"""

    additional_complainant_2_name: str = Field(
        default="",
        description=(
            "Full name of the second additional complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_2_date: str = Field(
        default="", description="Date the second additional complainant is completing this form"
    )  # YYYY-MM-DD format

    additional_complainant_2_signature: str = Field(
        default="",
        description=(
            "Signature of the second additional complainant .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_2_address: str = Field(
        default="",
        description=(
            "Mailing address of the second additional complainant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_2_zip: str = Field(
        default="", description="ZIP code for the second additional complainant's address"
    )

    additional_complainant_2_phone: str = Field(
        default="",
        description=(
            "Phone number for the second additional complainant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_2_email: str = Field(
        default="",
        description=(
            "Email address of the second additional complainant .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IncidentDetails(BaseModel):
    """Date, time, location, and notes about the nuisance incident"""

    incident_date: str = Field(
        ..., description="Date when the nuisance incident occurred"
    )  # YYYY-MM-DD format

    incident_time: str = Field(
        ...,
        description=(
            "Time when the nuisance incident occurred, including am/pm .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    location_of_nuisance: str = Field(
        ...,
        description=(
            "Address or description of where the nuisance occurred .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_notes_line_1: str = Field(
        default="",
        description=(
            "Additional notes about the incident (first line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_notes_line_2: str = Field(
        default="",
        description=(
            "Additional notes about the incident (second line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_notes_line_3: str = Field(
        default="",
        description=(
            "Additional notes about the incident (third line) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class OwnerofAnimals(BaseModel):
    """Owner information for the animal(s) involved"""

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
            'Address of the animal owner .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
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

    owner_zip: str = Field(..., description="ZIP code for the animal owner's address")


class DescriptionofAnimals(BaseModel):
    """Physical description of the animal(s) involved"""

    animal_breed: str = Field(
        default="",
        description=(
            "Breed of the animal involved in the complaint .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    animal_color: str = Field(
        default="",
        description=(
            'Color or markings of the animal .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    animal_sex: str = Field(
        default="",
        description=(
            "Sex of the animal (e.g., male, female, unknown) .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    animal_name: str = Field(
        default="",
        description=(
            'Name of the animal, if known .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class OfficeUseOnly(BaseModel):
    """Administrative fields for office processing"""

    office_use_only: str = Field(
        default="",
        description=(
            "Section reserved for office staff notes and processing information .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    office_use_only_date_received: str = Field(
        default="",
        description="Date the office records as having received the complaint (office use only)",
    )  # YYYY-MM-DD format

    date_received: str = Field(
        default="", description="Date the complaint was received"
    )  # YYYY-MM-DD format

    reference_complaint: str = Field(
        default="",
        description=(
            "Reference or related complaint identifier, if any .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    complaint_number: str = Field(
        default="",
        description=(
            "Unique complaint number assigned by the office .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AnimalNuisanceComplaintForm(BaseModel):
    """ANIMAL NUISANCE COMPLAINT FORM"""

    complaint_type: ComplaintType = Field(..., description="Complaint Type")
    complainant_information: ComplainantInformation = Field(
        ..., description="Complainant Information"
    )
    additional_complainant_1: AdditionalComplainant1 = Field(
        ..., description="Additional Complainant 1"
    )
    additional_complainant_2: AdditionalComplainant2 = Field(
        ..., description="Additional Complainant 2"
    )
    incident_details: IncidentDetails = Field(..., description="Incident Details")
    owner_of_animals: OwnerofAnimals = Field(..., description="Owner of Animal(s)")
    description_of_animals: DescriptionofAnimals = Field(
        ..., description="Description of Animal(s)"
    )
    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
