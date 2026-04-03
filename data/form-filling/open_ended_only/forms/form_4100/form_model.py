from typing import Literal, Optional, List, Union
from pydantic import BaseModel, ConfigDict, Field


NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ContactInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Your contact details and a contact person in case you cannot be reached"""

    my_primary_telephone_number: str = Field(
        ...,
        description=(
            "Your main telephone number where you can be reached .If you cannot fill this, "
            "write \"N/A\". If this field should not be filled by you (for example, it "
            "belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    my_secondary_telephone_number: str = Field(
        ...,
        description=(
            "An alternate telephone number where you can be reached .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    my_date_of_birth: str = Field(
        ...,
        description="Your date of birth"
    )  # YYYY-MM-DD format

    my_email_address: str = Field(
        ...,
        description=(
            "Your email address (required if you have one) .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    contact_persons_name: str = Field(
        ...,
        description=(
            "Name of a person who does not live with you but can be contacted if needed .If "
            "you cannot fill this, write \"N/A\". If this field should not be filled by you "
            "(for example, it belongs to another person or office), leave it blank (empty "
            "string \"\")."
        )
    )

    contact_persons_telephone_number: str = Field(
        ...,
        description=(
            "Telephone number of your contact person .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    contact_persons_address: str = Field(
        ...,
        description=(
            "Address of your contact person .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    contact_persons_email_address: str = Field(
        ...,
        description=(
            "Email address of your contact person .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    contact_persons_relationship_to_me: str = Field(
        ...,
        description=(
            "Relationship of the contact person to you .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )


class SpecialNeeds(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Requests for interpretation, accommodations, privacy, or other needs"""

    interpretation_if_so_what_language: str = Field(
        ...,
        description=(
            "Specify if you need interpretation and the language required .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )

    accommodations_for_a_disability: str = Field(
        ...,
        description=(
            "Describe any accommodations you need for a disability .If you cannot fill "
            "this, write \"N/A\". If this field should not be filled by you (for example, "
            "it belongs to another person or office), leave it blank (empty string \"\")."
        )
    )

    privacy_keep_my_contact_information_confidential_as_i_am_a_victim_of_domestic_violence: BooleanLike = Field(
        ...,
        description=(
            "Check if you want your contact information kept confidential due to domestic "
            "violence"
        )
    )

    other_special_needs: str = Field(
        ...,
        description=(
            "Describe any other special needs .If you cannot fill this, write \"N/A\". If "
            "this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )


class SettlementConciliation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """What you want to happen as a result of this complaint"""

    settlement_conciliation_what_you_want_to_happen_as_a_result_of_this_complaint: str = Field(
        ...,
        description=(
            "Explain what you want to happen as a result of this complaint .If you cannot "
            "fill this, write \"N/A\". If this field should not be filled by you (for "
            "example, it belongs to another person or office), leave it blank (empty string "
            "\"\")."
        )
    )


class Witnesses(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """Information about people who witnessed the discrimination"""

    witness_1_name: str = Field(
        ...,
        description=(
            "Name of the first witness .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    witness_1_title: str = Field(
        ...,
        description=(
            "Title of the first witness .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    witness_1_telephone_number: str = Field(
        ...,
        description=(
            "Telephone number of the first witness .If you cannot fill this, write \"N/A\". "
            "If this field should not be filled by you (for example, it belongs to another "
            "person or office), leave it blank (empty string \"\")."
        )
    )

    witness_1_relationship_to_me: str = Field(
        ...,
        description=(
            "Relationship of the first witness to you .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    witness_1_what_did_this_person_witness: str = Field(
        ...,
        description=(
            "Describe what the first witness saw or heard .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    witness_2_name: str = Field(
        ...,
        description=(
            "Name of the second witness .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    witness_2_title: str = Field(
        ...,
        description=(
            "Title of the second witness .If you cannot fill this, write \"N/A\". If this "
            "field should not be filled by you (for example, it belongs to another person "
            "or office), leave it blank (empty string \"\")."
        )
    )

    witness_2_telephone_number: str = Field(
        ...,
        description=(
            "Telephone number of the second witness .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    witness_2_relationship_to_me: str = Field(
        ...,
        description=(
            "Relationship of the second witness to you .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )

    witness_2_what_did_this_person_witness: str = Field(
        ...,
        description=(
            "Describe what the second witness saw or heard .If you cannot fill this, write "
            "\"N/A\". If this field should not be filled by you (for example, it belongs to "
            "another person or office), leave it blank (empty string \"\")."
        )
    )


class AdditionalInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    """
    Additional Information

    This page is for the Division’s records and will not be sent to the company or person(s) whom you are filing against. The Division uses email, whenever possible, to communicate with the parties to complaints. This avoids delays and lost mail, and increases the efficiency of Division case processing. Therefore, you are required to provide an email address, if you have one, and to keep us advised of any change of your email address. The Division will not use your email address for any non-case related matters.
    """

    contact_information: ContactInformation = Field(
        ...,
        description="Contact Information"
    )
    special_needs: SpecialNeeds = Field(
        ...,
        description="Special Needs"
    )
    settlement__conciliation: SettlementConciliation = Field(
        ...,
        description="Settlement / Conciliation"
    )
    witnesses: Witnesses = Field(
        ...,
        description="Witnesses"
    )