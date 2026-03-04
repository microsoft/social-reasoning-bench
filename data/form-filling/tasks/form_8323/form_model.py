from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PetitionLocationInformation(BaseModel):
    """Location of the study area and primary contact details for the petition"""

    street_name: str = Field(
        ...,
        description=(
            "Name of the street where the traffic study is requested .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    from_cross_street_or_address: str = Field(
        ...,
        description=(
            "Starting cross street or address that defines the beginning of the study area "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    to_cross_street_or_address: str = Field(
        ...,
        description=(
            "Ending cross street or address that defines the end of the study area .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    total_number_of_affected_properties_lots: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Total count of properties or lots affected along the subject roadway"
    )

    primary_contact_name: str = Field(
        ...,
        description=(
            "Full name of the primary contact person for this petition .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    primary_contact_phone_number: str = Field(
        ...,
        description=(
            "Phone number for the primary contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_submittal_of_petition_to_cwp: str = Field(
        ..., description="Date the petition is submitted to the City of Winter Park"
    )  # YYYY-MM-DD format

    description_of_concern: str = Field(
        ...,
        description=(
            "Brief description of the traffic-related concern in the neighborhood .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PetitionSignatures(BaseModel):
    """Residents’ names, addresses, emails, and required signatures supporting the traffic study"""

    name_1: str = Field(
        ...,
        description=(
            'Printed name of the first signer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_1: str = Field(
        ...,
        description=(
            'Street address of the first signer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_1: str = Field(
        default="",
        description=(
            'Email address of the first signer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    signature_required_1: str = Field(
        ...,
        description=(
            "Signature of the first signer indicating support for the traffic study .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    name_2: str = Field(
        ...,
        description=(
            'Printed name of the second signer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_2: str = Field(
        ...,
        description=(
            'Street address of the second signer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_2: str = Field(
        default="",
        description=(
            'Email address of the second signer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    signature_required_2: str = Field(
        ...,
        description=(
            "Signature of the second signer indicating support for the traffic study .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    name_3: str = Field(
        ...,
        description=(
            'Printed name of the third signer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_3: str = Field(
        ...,
        description=(
            'Street address of the third signer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_3: str = Field(
        default="",
        description=(
            'Email address of the third signer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    signature_required_3: str = Field(
        ...,
        description=(
            "Signature of the third signer indicating support for the traffic study .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    name_4: str = Field(
        ...,
        description=(
            'Printed name of the fourth signer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    address_4: str = Field(
        ...,
        description=(
            'Street address of the fourth signer .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_4: str = Field(
        default="",
        description=(
            'Email address of the fourth signer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    signature_required_4: str = Field(
        ...,
        description=(
            "Signature of the fourth signer indicating support for the traffic study .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    name_5: str = Field(
        default="",
        description=(
            "Printed name of the fifth signer (optional additional signature) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    address_5: str = Field(
        default="",
        description=(
            'Street address of the fifth signer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_5: str = Field(
        default="",
        description=(
            'Email address of the fifth signer .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    signature_required_5: str = Field(
        default="",
        description=(
            "Signature of the fifth signer indicating support for the traffic study .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class PetitionForNeighborhoodTrafficStudy(BaseModel):
    """
    PETITION FOR NEIGHBORHOOD TRAFFIC STUDY

    The purpose of this form is to provide a means by which residents may petition the City of Winter Park (CWP) to perform field and/or office evaluations for a traffic speed study in the neighborhood. Including the Primary Contact, this petition must reflect a minimum of four (4) signatures (one (1) signature maximum per dwelling unit adjacent to subject roadway) for CWP to initiate a traffic speed study.
    """

    petition__location_information: PetitionLocationInformation = Field(
        ..., description="Petition & Location Information"
    )
    petition_signatures: PetitionSignatures = Field(..., description="Petition Signatures")
