from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class Insured(BaseModel):
    """Details of the insured person or entity"""

    name_and_occupation: str = Field(
        ...,
        description=(
            "Full name of the insured and their occupation .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Postal address of the insured .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    tel_no: str = Field(
        ...,
        description=(
            'Telephone number of the insured .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class DescriptionofLoss(BaseModel):
    """Details about when, where, and how the loss or damage occurred"""

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
            "Location where the loss or damage took place .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    state_exactly_how_the_loss_damage_occurred: str = Field(
        ...,
        description=(
            "Detailed description of how the loss or damage occurred .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class Witnesses(BaseModel):
    """Information about witnesses to the incident"""

    name_address_tel_no_of_witnesses: str = Field(
        default="",
        description=(
            "Names, addresses, and telephone numbers of any witnesses .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    name_witness_1: str = Field(
        default="",
        description=(
            'Full name of first witness .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address_witness_1: str = Field(
        default="",
        description=(
            'Postal address of first witness .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    tel_no_witness_1: str = Field(
        default="",
        description=(
            'Telephone number of first witness .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    name_witness_2: str = Field(
        default="",
        description=(
            'Full name of second witness .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    address_witness_2: str = Field(
        default="",
        description=(
            'Postal address of second witness .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    tel_no_witness_2: str = Field(
        default="",
        description=(
            'Telephone number of second witness .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )


class Police(BaseModel):
    """Police station and case reference details"""

    name_of_police_station_and_case_reference_number: str = Field(
        default="",
        description=(
            "Name of the police station and the related case reference number, if reported "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class PropertyDamage(BaseModel):
    """Details of damage to property"""

    name_and_address_of_owner: str = Field(
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
            "Description of the damage sustained by the property .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class PersonalInjuries(BaseModel):
    """Details of any personal injuries"""

    name_and_age_of_injured_person: str = Field(
        default="",
        description=(
            "Full name and age of the injured person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address_of_injured_person: str = Field(
        default="",
        description=(
            'Postal address of the injured person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    details_of_injuries: str = Field(
        default="",
        description=(
            "Full description of the injuries sustained .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class Relationship(BaseModel):
    """Relationship of injured or affected person to the insured"""

    relationship_details: str = Field(
        default="",
        description=(
            "Details of the relationship if the injured person is your employee, tenant, or "
            'related to you .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )


class Claim(BaseModel):
    """Details of any claim made against the insured"""

    claim_details_against_you: str = Field(
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

    date: str = Field(..., description="Date the declaration is signed")  # YYYY-MM-DD format


class PublicLiabilityClaimForm(BaseModel):
    """
    PUBLIC LIABILITY CLAIM FORM

    ''
    """

    insured: Insured = Field(..., description="Insured")
    description_of_loss: DescriptionofLoss = Field(..., description="Description of Loss")
    witnesses: Witnesses = Field(..., description="Witnesses")
    police: Police = Field(..., description="Police")
    property_damage: PropertyDamage = Field(..., description="Property Damage")
    personal_injuries: PersonalInjuries = Field(..., description="Personal Injuries")
    relationship: Relationship = Field(..., description="Relationship")
    claim: Claim = Field(..., description="Claim")
    declaration: Declaration = Field(..., description="Declaration")
