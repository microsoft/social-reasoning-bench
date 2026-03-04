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
        default="", description="Check if the complaint is specifically about a barking dog"
    )

    general_nuisance_complaint: BooleanLike = Field(
        default="", description="Check if the complaint is about a general animal nuisance"
    )


class ComplainantRequired(BaseModel):
    """Primary complainant information"""

    complainant_name: str = Field(
        ...,
        description=(
            'Primary complainant\'s full name .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    complainant_date: str = Field(
        ..., description="Date the primary complainant completed the form"
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
            'Primary complainant\'s phone number .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    complainant_email: str = Field(
        default="",
        description=(
            'Primary complainant\'s email address .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalComplainant1Optional(BaseModel):
    """First additional complainant information"""

    additional_complainant_1_name: str = Field(
        default="",
        description=(
            "First additional complainant's full name .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_1_date: str = Field(
        default="", description="Date the first additional complainant completed the form"
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
            "Phone number of the first additional complainant .If you cannot fill this, "
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


class AdditionalComplainant2Optional(BaseModel):
    """Second additional complainant information"""

    additional_complainant_2_name: str = Field(
        default="",
        description=(
            "Second additional complainant's full name .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_2_date: str = Field(
        default="", description="Date the second additional complainant completed the form"
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
            "Phone number of the second additional complainant .If you cannot fill this, "
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

    other_notes: str = Field(
        default="",
        description=(
            "Additional information or comments about the incident .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class OwnerofAnimalsRequired(BaseModel):
    """Owner contact information"""

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
            'City of the animal owner\'s address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    owner_zip: str = Field(..., description="ZIP code of the animal owner's address")


class DescriptionofAnimals(BaseModel):
    """Details identifying the animal(s) involved"""

    animal_breed: str = Field(
        default="",
        description=(
            'Breed of the animal .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
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

    animal_sex: Literal["Male", "Female", "Unknown", "N/A", ""] = Field(
        default="", description="Sex of the animal"
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
    """For internal office processing and tracking"""

    office_use_date_received: str = Field(
        default="", description="Date the office received the complaint (office use only)"
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
    """
    ANIMAL NUISANCE COMPLAINT FORM

    ''
    """

    complaint_type: ComplaintType = Field(..., description="Complaint Type")
    complainant_required: ComplainantRequired = Field(..., description="Complainant (Required)")
    additional_complainant_1_optional: AdditionalComplainant1Optional = Field(
        ..., description="Additional Complainant 1 (Optional)"
    )
    additional_complainant_2_optional: AdditionalComplainant2Optional = Field(
        ..., description="Additional Complainant 2 (Optional)"
    )
    incident_details: IncidentDetails = Field(..., description="Incident Details")
    owner_of_animals_required: OwnerofAnimalsRequired = Field(
        ..., description="Owner of Animal(s) (Required)"
    )
    description_of_animals: DescriptionofAnimals = Field(
        ..., description="Description of Animal(s)"
    )
    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
