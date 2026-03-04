from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class InsuredDetails(BaseModel):
    """Information about the insured person or entity"""

    insured_name_and_occupation: str = Field(
        ...,
        description=(
            "Full name of the insured and their occupation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    insured_address: str = Field(
        ...,
        description=(
            "Postal or physical address of the insured .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    insured_tel_no: str = Field(
        ...,
        description=(
            'Telephone number of the insured .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class DescriptionofLoss(BaseModel):
    """Details about when, where and how the loss or damage occurred"""

    date_and_time_of_loss_damage: str = Field(
        ...,
        description=(
            "Date and time when the loss or damage occurred .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    place_where_loss_damage_occurred: str = Field(
        ...,
        description=(
            "Location where the loss or damage occurred .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    how_the_loss_damage_occurred: str = Field(
        ...,
        description=(
            "Detailed description of exactly how the loss or damage occurred .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )


class Witnesses(BaseModel):
    """Details of witnesses to the incident"""

    witness1_name: str = Field(
        default="",
        description=(
            'Full name of the first witness .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    witness1_address: str = Field(
        default="",
        description=(
            'Address of the first witness .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    witness1_tel_no: str = Field(
        default="",
        description=(
            'Telephone number of the first witness .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    witness2_name: str = Field(
        default="",
        description=(
            'Full name of the second witness .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    witness2_address: str = Field(
        default="",
        description=(
            'Address of the second witness .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    witness2_tel_no: str = Field(
        default="",
        description=(
            "Telephone number of the second witness .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class PoliceDetails(BaseModel):
    """Information about any police report filed"""

    police_station_and_case_reference: str = Field(
        default="",
        description=(
            "Name of the police station and the related case reference number .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PropertyDamage(BaseModel):
    """Information about damaged property"""

    owner_name_and_address: str = Field(
        default="",
        description=(
            "Name and address of the owner of the damaged property .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    description_of_damage_to_property: str = Field(
        default="",
        description=(
            "Detailed description of the damage to the property .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PersonalInjuries(BaseModel):
    """Information about any injured persons"""

    injured_person_name_and_age: str = Field(
        default="",
        description=(
            "Full name and age of the injured person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    injured_person_address: str = Field(
        default="",
        description=(
            'Address of the injured person .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    details_of_injuries: str = Field(
        default="",
        description=(
            "Full details of the injuries sustained .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Relationship(BaseModel):
    """Relationship of injured/affected persons to the insured"""

    relationship_details: str = Field(
        default="",
        description=(
            "Details of the relationship if the injured person is in your service, your "
            'tenant, or related to you .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class ClaimDetails(BaseModel):
    """Information about any claim made against the insured"""

    details_of_claim_made_against_you: str = Field(
        default="",
        description=(
            "Details of any claim made against you and reference to attached correspondence "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class Declaration(BaseModel):
    """Signature and date of declaration by the insured"""

    insureds_signature: str = Field(
        ...,
        description=(
            "Signature of the insured confirming the declaration .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date the form is signed")  # YYYY-MM-DD format


class SouthsureShorttermInsurancePublicLiabilityClaimForm(BaseModel):
    """
        Southsure
    SHORT-TERM INSURANCE


    PUBLIC LIABILITY CLAIM FORM

        ''
    """

    insured_details: InsuredDetails = Field(..., description="Insured Details")
    description_of_loss: DescriptionofLoss = Field(..., description="Description of Loss")
    witnesses: Witnesses = Field(..., description="Witnesses")
    police_details: PoliceDetails = Field(..., description="Police Details")
    property_damage: PropertyDamage = Field(..., description="Property Damage")
    personal_injuries: PersonalInjuries = Field(..., description="Personal Injuries")
    relationship: Relationship = Field(..., description="Relationship")
    claim_details: ClaimDetails = Field(..., description="Claim Details")
    declaration: Declaration = Field(..., description="Declaration")
