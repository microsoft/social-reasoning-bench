from typing import Literal, Optional, List, Union
from pydantic import BaseModel, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ContactInformation(BaseModel):
    """Your contact details and alternate contact person"""

    my_primary_telephone_number: str = Field(
        ...,
        description=(
            "Your main phone number where the Division should contact you .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    my_secondary_telephone_number: str = Field(
        default="",
        description=(
            "An alternate phone number where you can be reached .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    my_date_of_birth: str = Field(..., description="Your date of birth")  # YYYY-MM-DD format

    my_email_address: str = Field(
        ...,
        description=(
            "Your email address for communication about this complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    contact_persons_name: str = Field(
        ...,
        description=(
            "Full name of a person who does not live with you but can help the Division "
            'contact you .If you cannot fill this, write "N/A". If this field should not '
            "be filled by you (for example, it belongs to another person or office), leave "
            'it blank (empty string "").'
        ),
    )

    contact_persons_telephone_number: str = Field(
        ...,
        description=(
            "Telephone number for the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_persons_address: str = Field(
        default="",
        description=(
            "Mailing address for the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    contact_persons_email_address: str = Field(
        default="",
        description=(
            'Email address for the contact person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    contact_persons_relationship_to_me: str = Field(
        default="",
        description=(
            "How this contact person is related or connected to you .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SpecialNeeds(BaseModel):
    """Interpretation, disability accommodations, privacy, and other needs"""

    interpretation_if_so_what_language: str = Field(
        default="",
        description=(
            "Specify the language needed for interpretation services .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    accommodations_for_a_disability: str = Field(
        default="",
        description=(
            "Describe any disability-related accommodations you need .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    privacy_keep_my_contact_information_confidential_as_i_am_a_victim_of_domestic_violence: BooleanLike = Field(
        default="",
        description=(
            "Check if you want your contact information kept confidential due to domestic violence"
        ),
    )

    other_special_needs: str = Field(
        default="",
        description=(
            "Describe any other special needs not listed above .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class SettlementConciliation(BaseModel):
    """What you would accept to settle this complaint"""

    to_settle_this_complaint_i_would_accept: str = Field(
        ...,
        description=(
            "Explain what outcome or resolution you would accept to settle this complaint "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class Witnesses(BaseModel):
    """Information about people who witnessed the discrimination"""

    name_witness_1: str = Field(
        default="",
        description=(
            'Name of the first witness .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    title_witness_1: str = Field(
        default="",
        description=(
            "Title or role of the first witness (for example, manager, neighbor) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    telephone_number_witness_1: str = Field(
        default="",
        description=(
            "Telephone number for the first witness .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    relationship_to_me_witness_1: str = Field(
        default="",
        description=(
            "How the first witness is related or connected to you .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    what_did_this_person_witness_witness_1: str = Field(
        default="",
        description=(
            "Describe what the first witness saw or heard .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    name_witness_2: str = Field(
        default="",
        description=(
            'Name of the second witness .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    title_witness_2: str = Field(
        default="",
        description=(
            "Title or role of the second witness (for example, manager, neighbor) .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    telephone_number_witness_2: str = Field(
        default="",
        description=(
            "Telephone number for the second witness .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    relationship_to_me_witness_2: str = Field(
        default="",
        description=(
            "How the second witness is related or connected to you .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    what_did_this_person_witness_witness_2: str = Field(
        default="",
        description=(
            "Describe what the second witness saw or heard .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class AdditionalInformation(BaseModel):
    """
    Additional Information

    Additional Information, Page 1: This page is for the Division’s records and will not be sent to the company or person(s) whom you are filing against.
    """

    contact_information: ContactInformation = Field(..., description="Contact Information")
    special_needs: SpecialNeeds = Field(..., description="Special Needs")
    settlement__conciliation: SettlementConciliation = Field(
        ..., description="Settlement / Conciliation"
    )
    witnesses: Witnesses = Field(..., description="Witnesses")
