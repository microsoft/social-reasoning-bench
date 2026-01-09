from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class PolicyandInsuredDetails(BaseModel):
    """Basic policy and insured information"""

    policy_number: str = Field(
        ...,
        description=(
            "AIG professional indemnity policy number .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    expiry_date: str = Field(..., description="Policy expiry date")  # YYYY-MM-DD format

    name_of_insured: str = Field(
        ...,
        description=(
            'Full legal name of the insured entity .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    postal_address: str = Field(
        ...,
        description=(
            'Postal mailing address of the insured .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    broker: str = Field(
        default="",
        description=(
            'Name of the insurance broker .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    phone: str = Field(
        ...,
        description=(
            "Primary contact phone number for the insured .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    email: str = Field(
        ...,
        description=(
            "Primary contact email address for the insured .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )


class ClaimContactDetails(BaseModel):
    """Person to contact to discuss the claim"""

    name_contact_to_discuss_the_claim: str = Field(
        ...,
        description=(
            "Name of the person we should contact to discuss the claim .If you cannot fill "
            'this, write "N/A". If this field should not be filled by you (for example, '
            'it belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    position_contact_to_discuss_the_claim: str = Field(
        ...,
        description=(
            "Job title or position of the contact person .If you cannot fill this, write "
            '"N/A". If this field should not be filled by you (for example, it belongs to '
            'another person or office), leave it blank (empty string "").'
        ),
    )

    phone_contact_to_discuss_the_claim: str = Field(
        ...,
        description=(
            'Phone number for the contact person .If you cannot fill this, write "N/A". '
            "If this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    email_fax_contact_to_discuss_the_claim: str = Field(
        default="",
        description=(
            "Email address or fax number for the contact person .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class ClaimCircumstanceDetails(BaseModel):
    """Information about the allegation, claim, and exposure"""

    allegation_or_intimation_made: BooleanLike = Field(
        ...,
        description="Indicate whether any allegation or intimation of claim has already been made",
    )

    date_allegation_made: str = Field(
        ..., description="Date on which the allegation or intimation of claim was made"
    )  # YYYY-MM-DD format

    prior_awareness_of_potential_threat: BooleanLike = Field(
        ...,
        description=(
            "Indicate whether anyone in the insured entity was aware of the potential "
            "liability or circumstance before the above date"
        ),
    )

    details_of_who_and_when: str = Field(
        ...,
        description=(
            "Provide details of who was aware and when they became aware .If you cannot "
            'fill this, write "N/A". If this field should not be filled by you (for '
            "example, it belongs to another person or office), leave it blank (empty string "
            '"").'
        ),
    )

    amount_claimed_or_intimated_nz: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Amount claimed or intimated in New Zealand dollars"
    )

    estimate_amount_at_risk_nz: Union[float, Literal["N/A", ""]] = Field(
        ..., description="Your estimate of the total amount at risk in New Zealand dollars"
    )

    proceedings_issued: BooleanLike = Field(
        ..., description="Indicate whether legal proceedings have been issued"
    )

    details_of_allegation_if_no_proceedings: str = Field(
        ...,
        description=(
            "Full details of the allegation if proceedings have not been issued, including "
            "summary of any correspondence or verbal allegations .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )

    comment_in_answer_to_allegation: str = Field(
        ...,
        description=(
            "Your detailed response or comments in answer to the allegation or circumstance "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class LegalRepresentation(BaseModel):
    """Details of any legal advice obtained"""

    taken_legal_advice: BooleanLike = Field(
        ..., description="Indicate whether legal advice has been obtained regarding this matter"
    )

    name_of_law_firm: str = Field(
        default="",
        description=(
            "Name of the law firm that provided advice, if any .If you cannot fill this, "
            'write "N/A". If this field should not be filled by you (for example, it '
            'belongs to another person or office), leave it blank (empty string "").'
        ),
    )


class AigProfessionalIndemnityNotificationOfCircumstanceClaimForm(BaseModel):
    """
        AIG

    Professional Indemnity
    Notification of Circumstance
    Claim Form

        Please attach copies of all relevant documentation. This form must be completed by a partner or director or principal of the insured. Any questions which are not fully within that person's knowledge must be investigated to obtain such knowledge.
    """

    policy_and_insured_details: PolicyandInsuredDetails = Field(
        ..., description="Policy and Insured Details"
    )
    claim_contact_details: ClaimContactDetails = Field(..., description="Claim Contact Details")
    claim__circumstance_details: ClaimCircumstanceDetails = Field(
        ..., description="Claim / Circumstance Details"
    )
    legal_representation: LegalRepresentation = Field(..., description="Legal Representation")
