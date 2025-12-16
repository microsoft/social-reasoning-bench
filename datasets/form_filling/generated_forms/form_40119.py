from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PartyInformation(BaseModel):
    """Contact information for the party submitting the request"""

    name: str = Field(
        ...,
        description=(
            "Full name of the party submitting this request .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    address: str = Field(
        ...,
        description=(
            'Street address of the party .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code of the party’s address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    telephone_no: str = Field(
        ...,
        description=(
            'Primary telephone number for contact .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    fax_no_optional: str = Field(
        default="",
        description=(
            'Fax number, if available .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    email_address_optional: str = Field(
        default="",
        description=(
            "Email address for contact, if available .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class CaseInformation(BaseModel):
    """Court and case caption information"""

    plaintiff_petitioner: str = Field(
        ...,
        description=(
            "Name of the plaintiff or petitioner in this case .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    defendant_respondent: str = Field(
        ...,
        description=(
            "Name of the defendant or respondent in this case .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    case_number: str = Field(
        ...,
        description=(
            'Court-assigned case number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )


class RequesttoAmendNameAfterJudgment(BaseModel):
    """Details of the requested name amendment and supporting facts"""

    date_judgment_entered_on: str = Field(
        ..., description="Date the judgment was originally entered"
    )  # YYYY-MM-DD format

    incorrect_names: str = Field(
        ...,
        description=(
            "Name or names as they incorrectly appear on the judgment .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    correct_legal_name_and_actually_used_names: str = Field(
        ...,
        description=(
            "Correct legal name and name actually used that should appear on the judgment "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    plaintiff: BooleanLike = Field(
        ..., description="Check if the requesting party is the plaintiff in this action"
    )

    defendant: BooleanLike = Field(
        ..., description="Check if the requesting party is the defendant in this action"
    )

    facts_supporting_this_request: str = Field(
        ...,
        description=(
            "Explain the facts and reasons supporting the request to amend the name, and "
            'reference any attached documentation .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    date_declaration: str = Field(
        ..., description="Date the party signs this declaration"
    )  # YYYY-MM-DD format

    signature_of_party: str = Field(
        ...,
        description=(
            "Signature of the party making the request .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ClerksCertificateofMailing(BaseModel):
    """Information completed by the clerk regarding mailing of the request"""

    place_request_was_mailed_at: str = Field(
        ...,
        description=(
            "City in California where the clerk mailed the request .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_request_was_mailed_on: str = Field(
        ..., description="Date the clerk mailed the request"
    )  # YYYY-MM-DD format

    mailing_address_column_1: str = Field(
        default="",
        description=(
            "Mailing address block for first recipient .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_column_2: str = Field(
        default="",
        description=(
            "Mailing address block for second recipient .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_column_3: str = Field(
        default="",
        description=(
            "Mailing address block for third recipient .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    mailing_address_column_4: str = Field(
        default="",
        description=(
            "Mailing address block for fourth recipient .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    see_attached_sheet_for_additional_parties: BooleanLike = Field(
        default="",
        description=(
            "Check if additional parties and mailing addresses are listed on an attached sheet"
        ),
    )

    date_clerks_certificate: str = Field(
        ..., description="Date the clerk completes the certificate of mailing"
    )  # YYYY-MM-DD format

    deputy: str = Field(
        ...,
        description=(
            "Signature or printed name of the deputy clerk .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class RequestToAmendNameAfterJudgment(BaseModel):
    """
    REQUEST TO AMEND NAME AFTER JUDGMENT

    ''
    """

    party_information: PartyInformation = Field(..., description="Party Information")
    case_information: CaseInformation = Field(..., description="Case Information")
    request_to_amend_name_after_judgment: RequesttoAmendNameAfterJudgment = Field(
        ..., description="Request to Amend Name After Judgment"
    )
    clerks_certificate_of_mailing: ClerksCertificateofMailing = Field(
        ..., description="Clerk’s Certificate of Mailing"
    )
