from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

NA_HINT = '.If you cannot fill this, write "N/A".'
BLANK_HINT = (
    "If this field should not be filled by you (for example, it belongs to another person or office), leave it blank (empty string "
    ")."
)

# Type alias for boolean-like fields
BooleanLike = Literal["true", "false", "N/A", ""]


class CitroensIOwnTableRow(BaseModel):
    """Single row in Model"""

    model: str = Field(default="", description="Model")
    year: str = Field(default="", description="Year")
    reg_no: str = Field(default="", description="Reg_No")
    full_reg_conc_unreg: str = Field(default="", description="Full_Reg_Conc_Unreg")


class RenewingApplicantInformation(BaseModel):
    """Contact and personal details of the renewing member"""

    last_name: str = Field(
        ...,
        description=(
            'Renewing member\'s family name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    first: str = Field(
        ...,
        description=(
            'Renewing member\'s given name .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    date: str = Field(..., description="Date this renewal form is completed")  # YYYY-MM-DD format

    street_postal_address: str = Field(
        ...,
        description=(
            'Street or postal mailing address .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    city: str = Field(
        ...,
        description=(
            'City or suburb of residence .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    state: str = Field(
        ...,
        description=(
            'State or territory (e.g. WA, NSW) .If you cannot fill this, write "N/A". If '
            "this field should not be filled by you (for example, it belongs to another "
            'person or office), leave it blank (empty string "").'
        ),
    )

    pc: str = Field(..., description="Postcode")

    phone: str = Field(
        default="",
        description=(
            'Primary contact phone number .If you cannot fill this, write "N/A". If this '
            "field should not be filled by you (for example, it belongs to another person "
            'or office), leave it blank (empty string "").'
        ),
    )

    mobile_phone: str = Field(
        default="",
        description=(
            'Mobile phone number .If you cannot fill this, write "N/A". If this field '
            "should not be filled by you (for example, it belongs to another person or "
            'office), leave it blank (empty string "").'
        ),
    )

    email_address: str = Field(
        ...,
        description=(
            "Member's email address for club communication and ACE magazine if emailed .If "
            'you cannot fill this, write "N/A". If this field should not be filled by you '
            "(for example, it belongs to another person or office), leave it blank (empty "
            'string "").'
        ),
    )


class CitroënsIOwn(BaseModel):
    """Details of Citroën vehicles owned by the member"""

    citroens_i_own_table: List[CitroensIOwnTableRow] = Field(
        default="",
        description=(
            "List of Citroëns owned, including model, year, registration number and "
            "registration status"
        ),
    )  # List of table rows


class ServicesICanOffer(BaseModel):
    """Services the member can offer to the club and/or members"""

    services_i_can_offer_to_the_club_and_or_members: str = Field(
        default="",
        description=(
            "Describe any skills, services or assistance you can offer the club or its "
            'members .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )


class MembershipandPayment(BaseModel):
    """Membership options and payment reference details"""

    forty_dollars_per_year_with_ace_magazine_emailed: BooleanLike = Field(
        default="",
        description="Select if you want $40 membership with ACE magazine delivered by email",
    )

    seventy_dollars_per_year_40_00_membership_and_30_for_ace_magazine_printed_and_posted_in_australia: BooleanLike = Field(
        default="",
        description=(
            "Select if you want $70 membership including printed ACE magazine posted in Australia"
        ),
    )

    ref_your_name: str = Field(
        ...,
        description=(
            "Reference text used on your bank transfer (enter your name as it will appear) "
            '.If you cannot fill this, write "N/A". If this field should not be filled by '
            "you (for example, it belongs to another person or office), leave it blank "
            '(empty string "").'
        ),
    )


class SignatureandConfirmation(BaseModel):
    """Member’s confirmation of understanding and signature"""

    signature_of_renewing_member: str = Field(
        ...,
        description=(
            "Signature confirming understanding of 404 registration rules and membership "
            'renewal .If you cannot fill this, write "N/A". If this field should not be '
            "filled by you (for example, it belongs to another person or office), leave it "
            'blank (empty string "").'
        ),
    )

    date_signature: str = Field(
        ..., description="Date the renewing member signs this confirmation"
    )  # YYYY-MM-DD format


class AssociationOfCitroënEnthusiastsRenewalMembershipForm(BaseModel):
    """
        ASSOCIATION OF CITROËN ENTHUSIASTS
    Renewal Membership Form

        ''
    """

    renewing_applicant_information: RenewingApplicantInformation = Field(
        ..., description="Renewing Applicant Information"
    )
    citroëns_i_own: CitroënsIOwn = Field(..., description="Citroëns I Own")
    services_i_can_offer: ServicesICanOffer = Field(..., description="Services I Can Offer")
    membership_and_payment: MembershipandPayment = Field(..., description="Membership and Payment")
    signature_and_confirmation: SignatureandConfirmation = Field(
        ..., description="Signature and Confirmation"
    )
