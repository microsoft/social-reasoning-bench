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
    """Location of the requested traffic study and primary contact details"""

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
    """Residents signing in support of the neighborhood traffic study"""

    name: str = Field(
        ...,
        description=(
            "Printed name of the person signing the petition .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            "Street address of the person signing the petition .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        default="",
        description=(
            "Email address of the person signing the petition .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    signature_required: str = Field(
        ...,
        description=(
            "Signature of the person indicating support for the traffic study .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    one_name: str = Field(
        ...,
        description=(
            'Printed name for signer 1 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    one_address: str = Field(
        ...,
        description=(
            'Street address for signer 1 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    one_email: str = Field(
        default="",
        description=(
            'Email address for signer 1 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    one_signature_required: str = Field(
        ...,
        description=(
            'Signature for signer 1 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    two_name: str = Field(
        ...,
        description=(
            'Printed name for signer 2 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    two_address: str = Field(
        ...,
        description=(
            'Street address for signer 2 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    two_email: str = Field(
        default="",
        description=(
            'Email address for signer 2 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    two_signature_required: str = Field(
        ...,
        description=(
            'Signature for signer 2 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    three_name: str = Field(
        ...,
        description=(
            'Printed name for signer 3 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    three_address: str = Field(
        ...,
        description=(
            'Street address for signer 3 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    three_email: str = Field(
        default="",
        description=(
            'Email address for signer 3 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    three_signature_required: str = Field(
        ...,
        description=(
            'Signature for signer 3 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    four_name: str = Field(
        ...,
        description=(
            'Printed name for signer 4 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    four_address: str = Field(
        ...,
        description=(
            'Street address for signer 4 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    four_email: str = Field(
        default="",
        description=(
            'Email address for signer 4 .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    four_signature_required: str = Field(
        ...,
        description=(
            'Signature for signer 4 .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    five_name: str = Field(
        default="",
        description=(
            "Printed name for signer 5 (optional additional signer) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    five_address: str = Field(
        default="",
        description=(
            "Street address for signer 5 (optional additional signer) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    five_email: str = Field(
        default="",
        description=(
            "Email address for signer 5 (optional additional signer) .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    five_signature_required: str = Field(
        default="",
        description=(
            "Signature for signer 5 (form requires at least four total signatures) .If you "
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
