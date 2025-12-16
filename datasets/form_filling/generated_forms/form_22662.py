from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CertificationofCommercialPurpose(BaseModel):
    """Requester information and certification of commercial purpose"""

    name_of_requester: str = Field(
        ...,
        description=(
            "Full legal name of the individual making the open records request .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    information_requested_under_the_kentucky_open_records_act: str = Field(
        ...,
        description=(
            "Description of the records or information being requested under the Kentucky "
            'Open Records Act .If you cannot fill this, write "N/A". If this field should '
            "not be filled by you (for example, it belongs to another person or office), "
            'leave it blank (empty string "").'
        ),
    )

    commercial_purpose_for_which_the_information_is_to_be_used: str = Field(
        ...,
        description=(
            "Explanation of the commercial purpose for which the requested information will "
            "be used, as defined in K.R.S. 61.870(4)(a) .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    entity_benefiting_from_the_commercial_purpose: str = Field(
        ...,
        description=(
            "Name and description of the business, organization, or other entity that will "
            "benefit from the commercial use of the information .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    by: str = Field(
        ...,
        description=(
            "Signature of the requester certifying the commercial purpose .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    title: str = Field(
        default="",
        description=(
            "Title or position of the signer, if signing on behalf of an entity .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class NotaryAcknowledgment(BaseModel):
    """Notary public acknowledgment and commission details"""

    day_of_acknowledgment: Union[float, Literal["N/A", ""]] = Field(
        ...,
        description=(
            "Numeric day of the month on which the document is acknowledged before the notary"
        ),
    )

    month_of_acknowledgment: str = Field(
        ...,
        description=(
            "Month (written out) on which the document is acknowledged before the notary "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    year_of_acknowledgment: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Four-digit year in which the document is acknowledged before the notary"
    )

    my_commission_expires: str = Field(
        ..., description="Expiration date of the notary public's commission"
    )  # YYYY-MM-DD format

    notary_public_state_at_large_signature: str = Field(
        ...,
        description=(
            "Signature of the Notary Public, State-at-Large .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CertificationOfCommercialPurposeForOpenRecordsRequest(BaseModel):
    """
        CERTIFICATION OF COMMERCIAL PURPOSE
    FOR OPEN RECORDS REQUEST

        I understand that I may be required to enter into a contract with Louisville Metro Government, through any of its agencies, in order to obtain this information, which may be provided for the stated commercial purpose for a specified fee. I further understand that, in accordance with K.R.S. 61.874(5), it is unlawful to obtain a copy of any part of a public record for a commercial purpose, if I use or knowingly allow the use of the public record for a use other than that for which I submit this certification, or resell the information to a third party.
    """

    certification_of_commercial_purpose: CertificationofCommercialPurpose = Field(
        ..., description="Certification of Commercial Purpose"
    )
    notary_acknowledgment: NotaryAcknowledgment = Field(..., description="Notary Acknowledgment")
