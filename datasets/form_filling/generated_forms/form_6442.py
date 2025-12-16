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
        ..., description="Check if this complaint is specifically about a barking dog."
    )

    general_nuisance_complaint: BooleanLike = Field(
        ...,
        description="Check if this complaint is about a general animal nuisance other than barking.",
    )


class ComplainantRequired(BaseModel):
    """Primary complainant information"""

    complainant_name: str = Field(
        ...,
        description=(
            'Full name of the primary complainant. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    complainant_date: str = Field(
        ..., description="Date the primary complainant is completing and signing this form."
    )  # YYYY-MM-DD format

    complainant_signature: str = Field(
        ...,
        description=(
            'Signature of the primary complainant. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    complainant_address: str = Field(
        ...,
        description=(
            "Mailing or street address of the primary complainant. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    complainant_zip: str = Field(..., description="ZIP code for the primary complainant's address.")

    complainant_phone: str = Field(
        ...,
        description=(
            "Primary phone number for the complainant. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    complainant_email: str = Field(
        default="",
        description=(
            "Email address for the primary complainant. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalComplainant1Optional(BaseModel):
    """First additional complainant information"""

    additional_complainant_name_1: str = Field(
        default="",
        description=(
            "Full name of the first additional complainant (optional). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_date_1: str = Field(
        default="", description="Date the first additional complainant signs the form."
    )  # YYYY-MM-DD format

    additional_complainant_signature_1: str = Field(
        default="",
        description=(
            "Signature of the first additional complainant. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_address_1: str = Field(
        default="",
        description=(
            "Mailing or street address of the first additional complainant. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    additional_complainant_zip_1: str = Field(
        default="", description="ZIP code for the first additional complainant's address."
    )

    additional_complainant_phone_1: str = Field(
        default="",
        description=(
            "Phone number for the first additional complainant. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_email_1: str = Field(
        default="",
        description=(
            "Email address for the first additional complainant. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalComplainant2Optional(BaseModel):
    """Second additional complainant information"""

    additional_complainant_name_2: str = Field(
        default="",
        description=(
            "Full name of the second additional complainant (optional). .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_date_2: str = Field(
        default="", description="Date the second additional complainant signs the form."
    )  # YYYY-MM-DD format

    additional_complainant_signature_2: str = Field(
        default="",
        description=(
            "Signature of the second additional complainant. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_address_2: str = Field(
        default="",
        description=(
            "Mailing or street address of the second additional complainant. .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    additional_complainant_zip_2: str = Field(
        default="", description="ZIP code for the second additional complainant's address."
    )

    additional_complainant_phone_2: str = Field(
        default="",
        description=(
            "Phone number for the second additional complainant. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    additional_complainant_email_2: str = Field(
        default="",
        description=(
            "Email address for the second additional complainant. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class IncidentDetailsRequired(BaseModel):
    """Date, time, location, and notes about the incident"""

    incident_date: str = Field(
        ..., description="Date on which the nuisance incident occurred."
    )  # YYYY-MM-DD format

    incident_time: str = Field(
        ...,
        description=(
            "Time of day when the nuisance incident occurred, including am/pm. .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    incident_location: str = Field(
        ...,
        description=(
            'Location where the nuisance occurred. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    other_notes_line_1: str = Field(
        default="",
        description=(
            "First line for any additional notes about the incident. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_notes_line_2: str = Field(
        default="",
        description=(
            "Second line for any additional notes about the incident. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    other_notes_line_3: str = Field(
        default="",
        description=(
            "Third line for any additional notes about the incident. .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class OwnerofAnimalsRequired(BaseModel):
    """Owner information for the animal(s) involved"""

    owner_last_name: str = Field(
        ...,
        description=(
            'Last name of the animal owner. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    owner_first_name: str = Field(
        ...,
        description=(
            'First name of the animal owner. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    owner_address: str = Field(
        ...,
        description=(
            "Street or mailing address of the animal owner. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    owner_city: str = Field(
        ...,
        description=(
            'City for the animal owner\'s address. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    owner_zip: str = Field(..., description="ZIP code for the animal owner's address.")


class DescriptionofAnimals(BaseModel):
    """Physical description and names of the animal(s)"""

    animal_breed_row_1: str = Field(
        default="",
        description=(
            'Breed of the first animal described. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    animal_color_row_1: str = Field(
        default="",
        description=(
            'Color of the first animal described. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    animal_sex_row_1: str = Field(
        default="",
        description=(
            'Sex of the first animal described. .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    animal_name_row_1: str = Field(
        default="",
        description=(
            "Name of the first animal described, if known. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    animal_breed_row_2: str = Field(
        default="",
        description=(
            'Breed of the second animal described. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    animal_color_row_2: str = Field(
        default="",
        description=(
            'Color of the second animal described. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    animal_sex_row_2: str = Field(
        default="",
        description=(
            'Sex of the second animal described. .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    animal_name_row_2: str = Field(
        default="",
        description=(
            "Name of the second animal described, if known. .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class OfficeUseOnly(BaseModel):
    """Administrative tracking information for office use only"""

    office_use_only_date_received_header_line: str = Field(
        default="",
        description="Date the complaint form was received, for office use only (header line).",
    )  # YYYY-MM-DD format

    date_received_footer_line: str = Field(
        default="",
        description="Date the complaint form was received, for office use only (footer line).",
    )  # YYYY-MM-DD format

    reference_complaint: str = Field(
        default="",
        description=(
            "Reference or related complaint identifier, if any. .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    complaint_number: str = Field(
        default="",
        description=(
            "Unique complaint number assigned by the office. .If you cannot fill this, "
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
    complainant_required: ComplainantRequired = Field(..., description="Complainant (Required)")
    additional_complainant_1_optional: AdditionalComplainant1Optional = Field(
        ..., description="Additional Complainant 1 (Optional)"
    )
    additional_complainant_2_optional: AdditionalComplainant2Optional = Field(
        ..., description="Additional Complainant 2 (Optional)"
    )
    incident_details_required: IncidentDetailsRequired = Field(
        ..., description="Incident Details (Required)"
    )
    owner_of_animals_required: OwnerofAnimalsRequired = Field(
        ..., description="Owner of Animal(s) (Required)"
    )
    description_of_animals: DescriptionofAnimals = Field(
        ..., description="Description of Animal(s)"
    )
    office_use_only: OfficeUseOnly = Field(..., description="Office Use Only")
