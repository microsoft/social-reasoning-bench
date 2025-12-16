from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class ComplainantInformation(BaseModel):
    """Information about the member or individual submitting the complaint"""

    date: str = Field(..., description="Date the complaint form is completed")  # YYYY-MM-DD format

    from_: str = Field(
        ...,
        description=(
            "Name of the member or individual submitting the complaint .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    member_id: str = Field(
        default="",
        description=(
            "Health plan member identification number, if applicable .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    date_of_birth: str = Field(
        default="", description="Date of birth of the member or individual (mm/dd/yy)"
    )  # YYYY-MM-DD format

    address: str = Field(
        ...,
        description=(
            "Street mailing address of the member or individual .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    city_state_zip: str = Field(
        ...,
        description=(
            "City, state, and ZIP code for the mailing address .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Primary phone number where the member or individual can be reached .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class AllegedViolationDetails(BaseModel):
    """Information about who violated privacy, when, and what right was violated"""

    workforce_member_or_department_name: str = Field(
        ...,
        description=(
            "Name of the workforce member or department believed to have violated privacy "
            'rights .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    violation_date: str = Field(
        ..., description="Date on which the alleged privacy violation occurred (mm/dd/yy)"
    )  # YYYY-MM-DD format

    access_to_records_request_denied: BooleanLike = Field(
        default="",
        description="Check if the complaint involves denial of a request to access health records",
    )

    amendment_of_health_request_denied: BooleanLike = Field(
        default="",
        description="Check if the complaint involves denial of a request to amend health information",
    )

    confidential_communications_request_denied: BooleanLike = Field(
        default="",
        description=(
            "Check if the complaint involves denial of a request for confidential communications"
        ),
    )

    restriction_of_use_and_disclosures_request_denied: BooleanLike = Field(
        default="",
        description=(
            "Check if the complaint involves denial of a request to restrict use or "
            "disclosure of health information"
        ),
    )

    accounting_of_disclosures_request_denied: BooleanLike = Field(
        default="",
        description=(
            "Check if the complaint involves denial of a request for an accounting of disclosures"
        ),
    )

    breach_of_confidentiality: BooleanLike = Field(
        default="",
        description=(
            "Check if the complaint involves an improper disclosure or breach of confidentiality"
        ),
    )

    other: BooleanLike = Field(
        default="",
        description=(
            "Check if the complaint involves another type of privacy rights violation not listed"
        ),
    )

    describe_the_privacy_violation: str = Field(
        ...,
        description=(
            "Detailed description of what happened and how privacy rights were violated .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )

    what_action_if_any_do_you_believe_will_correct_the_problem: str = Field(
        default="",
        description=(
            "Describe what actions you believe would resolve or correct the problem .If you "
            'cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class SignatureandAuthorization(BaseModel):
    """Signature and relationship of the person submitting the complaint"""

    member_or_legal_representatives_signature: str = Field(
        ...,
        description=(
            "Signature of the member or their legal representative certifying the complaint "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    date_of_signature: str = Field(
        ..., description="Date the member or legal representative signed the complaint"
    )  # YYYY-MM-DD format

    member_or_legal_representatives_name: str = Field(
        ...,
        description=(
            "Printed name of the member or legal representative who signed the complaint "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )

    relationship_of_representative_to_member: str = Field(
        default="",
        description=(
            "Describe how the representative is related to the member (e.g., parent, "
            'spouse, legal guardian) .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )


class HipaaPrivacyComplaintForm(BaseModel):
    """
    HIPAA Privacy Complaint Form

    This complaint form concerns protected health information maintained by HWMG and related Business Associates subject to the HIPAA Privacy Rules.
    """

    complainant_information: ComplainantInformation = Field(
        ..., description="Complainant Information"
    )
    alleged_violation_details: AllegedViolationDetails = Field(
        ..., description="Alleged Violation Details"
    )
    signature_and_authorization: SignatureandAuthorization = Field(
        ..., description="Signature and Authorization"
    )
